__all__ = ["BigVGANConfig", "BigVGAN"]

import numpy as np
from lt_tensor.torch_commons import *
from torch.nn import functional as F
from lt_tensor.config_templates import ModelConfig
from lt_tensor.torch_commons import *
from lt_tensor.model_base import Model
from math import sqrt
from lt_utils.common import *
from lt_utils.file_ops import load_json, is_file, is_dir, is_path_valid
from lt_tensor.model_zoo.residual import ConvNets
from lt_tensor.model_zoo.activations.snake import snake as activations
from huggingface_hub import PyTorchModelHubMixin, hf_hub_download
from lt_tensor.model_zoo.activations.alias_free_torch.act import (
    Activation1d as TorchActivation1d,
)


MAX_WAV_VALUE = 32767.0  # NOTE: 32768.0 -1 to prevent int16 overflow (results in popping sound in corner cases)


def get_padding(kernel_size, dilation=1):
    return int((kernel_size * dilation - dilation) / 2)


class BigVGANConfig(ModelConfig):

    def __init__(
        self,
        resblock: int = 0,
        num_gpus: int = 0,
        batch_size: int = 32,
        learning_rate: float = 0.0001,
        adam_b1: float = 0.8,
        adam_b2: float = 0.99,
        lr_decay: float = 0.999,
        seed: int = 1234,
        upsample_rates: list[int] = [8, 8, 2, 2],
        upsample_kernel_sizes: list[int] = [16, 16, 4, 4],
        upsample_initial_channel: int = 512,
        resblock_kernel_sizes: list[int] = [3, 7, 11],
        resblock_dilation_sizes: list[int] = [[1, 3, 5], [1, 3, 5], [1, 3, 5]],
        activation: str = "snakebeta",
        snake_logscale: bool = True,
        discriminator: str = "mrd",
        resolutions: list[list[int]] = [
            [1024, 120, 600],
            [2048, 240, 1200],
            [512, 50, 240],
        ],
        mpd_reshapes: list[int] = [2, 3, 5, 7, 11],
        use_spectral_norm: bool = False,
        discriminator_channel_mult: int = 1,
        segment_size: int = 8192,
        num_mels: int = 80,
        num_freq: int = 1025,
        n_fft: int = 1024,
        hop_size: int = 256,
        win_size: int = 1024,
        sampling_rate: int = 22050,
        use_cuda_kernel: bool = False,
    ):
        self.resblock = resblock
        self.num_gpus = num_gpus
        self.batch_size = batch_size
        self.learning_rate = learning_rate
        self.adam_b1 = adam_b1
        self.adam_b2 = adam_b2
        self.lr_decay = lr_decay
        self.seed = seed
        self.upsample_rates = upsample_rates
        self.upsample_kernel_sizes = upsample_kernel_sizes
        self.upsample_initial_channel = upsample_initial_channel
        self.resblock_kernel_sizes = resblock_kernel_sizes
        self.resblock_dilation_sizes = resblock_dilation_sizes
        self.activation = activation
        self.snake_logscale = snake_logscale
        self.discriminator = discriminator
        self.resolutions = resolutions
        self.mpd_reshapes = mpd_reshapes
        self.use_spectral_norm = use_spectral_norm
        self.discriminator_channel_mult = discriminator_channel_mult
        self.segment_size = segment_size
        self.num_mels = num_mels
        self.num_freq = num_freq
        self.n_fft = n_fft
        self.hop_size = hop_size
        self.win_size = win_size
        self.sampling_rate = sampling_rate
        self.use_cuda_kernel = use_cuda_kernel


class AMPBlock1(ConvNets):
    """
    AMPBlock applies Snake / SnakeBeta activation functions with trainable parameters that control periodicity, defined for each layer.
    AMPBlock1 has additional self.convs2 that contains additional Conv1d layers with a fixed dilation=1 followed by each layer in self.convs1
    Args:
        h (BigVGANConfig): Hyperparameters.
        channels (int): Number of convolution channels.
        kernel_size (int): Size of the convolution kernel. Default is 3.
        dilation (tuple): Dilation rates for the convolutions. Each dilation layer has two convolutions. Default is (1, 3, 5).
        activation (str): Activation function type. Should be either 'snake' or 'snakebeta'. Default is None.
    """

    def __init__(
        self,
        h: BigVGANConfig,
        channels: int,
        kernel_size: int = 3,
        dilation: tuple = (1, 3, 5),
        activation: str = None,
    ):
        super().__init__()

        self.h = h

        self.convs1 = nn.ModuleList(
            [
                weight_norm(
                    nn.Conv1d(
                        channels,
                        channels,
                        kernel_size,
                        stride=1,
                        dilation=d,
                        padding=get_padding(kernel_size, d),
                    )
                )
                for d in dilation
            ]
        )
        self.convs1.apply(self.init_weights)

        self.convs2 = nn.ModuleList(
            [
                weight_norm(
                    nn.Conv1d(
                        channels,
                        channels,
                        kernel_size,
                        stride=1,
                        dilation=1,
                        padding=get_padding(kernel_size, 1),
                    )
                )
                for _ in range(len(dilation))
            ]
        )
        self.convs2.apply(self.init_weights)

        self.num_layers = len(self.convs1) + len(
            self.convs2
        )  # Total number of conv layers

        # Select which Activation1d, lazy-load cuda version to ensure backward compatibility
        if self.h.use_cuda_kernel:
            from .cuda import (
                Activation1d as CudaActivation1d,
            )

            Activation1d = CudaActivation1d
        else:
            Activation1d = TorchActivation1d

        # Activation functions
        if activation == "snake":
            self.activations = nn.ModuleList(
                [
                    Activation1d(
                        activation=activations.Snake(
                            channels, alpha_logscale=h.snake_logscale
                        )
                    )
                    for _ in range(self.num_layers)
                ]
            )
        elif activation == "snakebeta":
            self.activations = nn.ModuleList(
                [
                    Activation1d(
                        activation=activations.SnakeBeta(
                            channels, alpha_logscale=h.snake_logscale
                        )
                    )
                    for _ in range(self.num_layers)
                ]
            )
        else:
            raise NotImplementedError(
                "activation incorrectly specified. check the config file and look for 'activation'."
            )

    def forward(self, x):
        acts1, acts2 = self.activations[::2], self.activations[1::2]
        for c1, c2, a1, a2 in zip(self.convs1, self.convs2, acts1, acts2):
            xt = a1(x)
            xt = c1(xt)
            xt = a2(xt)
            xt = c2(xt)
            x = xt + x

        return x

    def remove_weight_norm(self):
        for l in self.convs1:
            remove_weight_norm(l)
        for l in self.convs2:
            remove_weight_norm(l)


class AMPBlock2(ConvNets):
    """
    AMPBlock applies Snake / SnakeBeta activation functions with trainable parameters that control periodicity, defined for each layer.
    Unlike AMPBlock1, AMPBlock2 does not contain extra Conv1d layers with fixed dilation=1
    Args:
        h (AttrDict): Hyperparameters.
        channels (int): Number of convolution channels.
        kernel_size (int): Size of the convolution kernel. Default is 3.
        dilation (tuple): Dilation rates for the convolutions. Each dilation layer has two convolutions. Default is (1, 3, 5).
        activation (str): Activation function type. Should be either 'snake' or 'snakebeta'. Default is None.
    """

    def __init__(
        self,
        h: BigVGANConfig,
        channels: int,
        kernel_size: int = 3,
        dilation: tuple = (1, 3, 5),
        activation: str = None,
    ):
        super().__init__()

        self.h = h

        self.convs = nn.ModuleList(
            [
                weight_norm(
                    nn.Conv1d(
                        channels,
                        channels,
                        kernel_size,
                        stride=1,
                        dilation=d,
                        padding=get_padding(kernel_size, d),
                    )
                )
                for d in dilation
            ]
        )
        self.convs.apply(self.init_weights)

        self.num_layers = len(self.convs)  # Total number of conv layers

        # Select which Activation1d, lazy-load cuda version to ensure backward compatibility
        if self.h.use_cuda_kernel:
            from .cuda import (
                Activation1d as CudaActivation1d,
            )

            Activation1d = CudaActivation1d
        else:
            Activation1d = TorchActivation1d

        # Activation functions
        if activation == "snake":
            self.activations = nn.ModuleList(
                [
                    Activation1d(
                        activation=activations.Snake(
                            channels, alpha_logscale=h.snake_logscale
                        )
                    )
                    for _ in range(self.num_layers)
                ]
            )
        elif activation == "snakebeta":
            self.activations = nn.ModuleList(
                [
                    Activation1d(
                        activation=activations.SnakeBeta(
                            channels, alpha_logscale=h.snake_logscale
                        )
                    )
                    for _ in range(self.num_layers)
                ]
            )
        else:
            raise NotImplementedError(
                "activation incorrectly specified. check the config file and look for 'activation'."
            )

    def forward(self, x):
        for c, a in zip(self.convs, self.activations):
            xt = a(x)
            xt = c(xt)
            x = xt + x

    def remove_weight_norm(self):
        for l in self.convs:
            remove_weight_norm(l)


class BigVGAN(ConvNets):
    """
    BigVGAN is a neural vocoder model that applies anti-aliased periodic activation for residual blocks (resblocks).
    New in BigVGAN-v2: it can optionally use optimized CUDA kernels for AMP (anti-aliased multi-periodicity) blocks.
    Args:
        h (AttrDict): Hyperparameters.
        use_cuda_kernel (bool): If set to True, loads optimized CUDA kernels for AMP. This should be used for inference only, as training is not supported with CUDA kernels.
    Note:
        - The `use_cuda_kernel` parameter should be used for inference only, as training with CUDA kernels is not supported.
        - Ensure that the activation function is correctly specified in the hyperparameters (h.activation).
    """

    def __init__(self, h: BigVGANConfig):
        super().__init__()
        self.h = h

        # Select which Activation1d, lazy-load cuda version to ensure backward compatibility
        if self.h.use_cuda_kernel:
            from .cuda import (
                Activation1d as CudaActivation1d,
            )

            Activation1d = CudaActivation1d
        else:
            Activation1d = TorchActivation1d

        self.num_kernels = len(h.resblock_kernel_sizes)
        self.num_upsamples = len(h.upsample_rates)

        # Pre-conv
        self.conv_pre = weight_norm(
            nn.Conv1d(h.num_mels, h.upsample_initial_channel, 7, 1, padding=3)
        )

        # Define which AMPBlock to use. BigVGAN uses AMPBlock1 as default
        if h.resblock == 0:
            resblock_class = AMPBlock1
        elif h.resblock == 1:
            resblock_class = AMPBlock2
        else:
            raise ValueError(
                f"Incorrect resblock class specified in hyperparameters. Got {h.resblock}"
            )

        # Transposed conv-based upsamplers. does not apply anti-aliasing
        self.ups = nn.ModuleList()
        for i, (u, k) in enumerate(zip(h.upsample_rates, h.upsample_kernel_sizes)):
            self.ups.append(
                nn.ModuleList(
                    [
                        weight_norm(
                            nn.ConvTranspose1d(
                                h.upsample_initial_channel // (2**i),
                                h.upsample_initial_channel // (2 ** (i + 1)),
                                k,
                                u,
                                padding=(k - u) // 2,
                            )
                        )
                    ]
                )
            )

        # Residual blocks using anti-aliased multi-periodicity composition modules (AMP)
        self.resblocks = nn.ModuleList()
        for i in range(len(self.ups)):
            ch = h.upsample_initial_channel // (2 ** (i + 1))
            for j, (k, d) in enumerate(
                zip(h.resblock_kernel_sizes, h.resblock_dilation_sizes)
            ):
                self.resblocks.append(
                    resblock_class(h, ch, k, d, activation=h.activation)
                )

        # Post-conv
        activation_post = (
            activations.Snake(ch, alpha_logscale=h.snake_logscale)
            if h.activation == "snake"
            else (
                activations.SnakeBeta(ch, alpha_logscale=h.snake_logscale)
                if h.activation == "snakebeta"
                else None
            )
        )
        if activation_post is None:
            raise NotImplementedError(
                "activation incorrectly specified. check the config file and look for 'activation'."
            )

        self.activation_post = Activation1d(activation=activation_post)

        # Whether to use bias for the final conv_post. Default to True for backward compatibility
        self.use_bias_at_final = h.get("use_bias_at_final", True)
        self.conv_post = weight_norm(
            nn.Conv1d(ch, 1, 7, 1, padding=3, bias=self.use_bias_at_final)
        )

        # Weight initialization
        for i in range(len(self.ups)):
            self.ups[i].apply(self.init_weights)
        self.conv_post.apply(self.init_weights)

        # Final tanh activation. Defaults to True for backward compatibility
        self.use_tanh_at_final = h.get("use_tanh_at_final", True)

    def forward(self, x):
        # Pre-conv
        x = self.conv_pre(x)

        for i in range(self.num_upsamples):
            # Upsampling
            for i_up in range(len(self.ups[i])):
                x = self.ups[i][i_up](x)
            # AMP blocks
            xs = None
            for j in range(self.num_kernels):
                if xs is None:
                    xs = self.resblocks[i * self.num_kernels + j](x)
                else:
                    xs += self.resblocks[i * self.num_kernels + j](x)
            x = xs / self.num_kernels

        # Post-conv
        x = self.activation_post(x)
        x = self.conv_post(x)
        # Final tanh activation
        if self.use_tanh_at_final:
            x = torch.tanh(x)
        else:
            x = torch.clamp(x, min=-1.0, max=1.0)  # Bound the output to [-1, 1]

        return x

    @classmethod
    def from_pretrained(
        cls,
        model_id: str,
        map_location: str = "cpu",
        local_files_only: bool = False,
        strict: bool = False,
        *,
        subfolder: str | None = None,
        repo_type: str | None = None,
        revision: str | None = None,
        cache_dir: str | Path | None = None,
        force_download: bool = False,
        proxies: Dict | None = None,
        token: bool | str | None = None,
        resume_download: bool | None = None,
        local_dir_use_symlinks: bool | Literal["auto"] = "auto",
        **kwargs,
    ):
        """Load Pytorch pretrained weights and return the loaded model."""
        hub_kwargs = dict(
            repo_id=model_id,
            subfolder=subfolder,
            repo_type=repo_type,
            revision=revision,
            cache_dir=cache_dir,
            force_download=force_download,
            proxies=proxies,
            resume_download=resume_download,
            token=token,
            local_files_only=local_files_only,
            local_dir_use_symlinks=local_dir_use_symlinks,
        )

        # Download and load hyperparameters (h) used by BigVGAN
        _model_path = Path(model_id)
        if is_path_valid(model_id):
            if is_file(model_id):
                _p_conf = _model_path.parent / "config.json"
            else:
                _p_conf = _model_path / "config.json"

            if is_file(_p_conf):
                print("Loading config.json from local directory")
                config_file = Path(model_id, "config.json")
            else:
                print(f"Loading config from {model_id}")
                config_file = hf_hub_download(filename="config.json", **hub_kwargs)
        else:
            print(f"Loading config from {model_id}")
            config_file = hf_hub_download(filename="config.json", **hub_kwargs)

        h = BigVGANConfig(**load_json(config_file))
        # instantiate BigVGAN using h
        if h.use_cuda_kernel:
            print(
                f"[WARNING] You have specified use_cuda_kernel=True during BigVGAN.from_pretrained(). Only inference is supported (training is not implemented)!"
            )
            print(
                f"[WARNING] You need nvcc and ninja installed in your system that matches your PyTorch build is using to build the kernel. If not, the model will fail to initialize or generate incorrect waveform!"
            )
            print(
                f"[WARNING] For detail, see the official GitHub repository: https://github.com/NVIDIA/BigVGAN?tab=readme-ov-file#using-custom-cuda-kernel-for-synthesis"
            )

        model = cls(h)

        # Download and load pretrained generator weight
        _retrieve_kwargs = dict(
            **hub_kwargs,
            filename="bigvgan_generator.pt",
        )
        path = Path(model_id)
        if path.exists():
            if path.is_dir():
                path = path / "bigvgan_generator.pt"
                if path.exists():
                    print("Loading weights from local directory")
                    model_file = str(path)
                else:
                    print(f"Loading weights from {model_id}")
                    model_file = hf_hub_download(**_retrieve_kwargs)
            else:
                print("Loading weights from local directory")
                model_file = str(path)
        else:
            print(f"Loading weights from {model_id}")
            model_file = hf_hub_download(**_retrieve_kwargs)
        checkpoint_dict = torch.load(model_file, map_location=map_location)

        try:
            model.load_state_dict(checkpoint_dict["generator"], strict=strict)
        except RuntimeError:
            print(
                f"[INFO] the pretrained checkpoint does not contain weight norm. Loading the checkpoint after removing weight norm!"
            )
            model.remove_norms()
            model.load_state_dict(checkpoint_dict["generator"], strict=strict)

        return model
