__all__ = ["iSTFTGenerator"]
from lt_utils.common import *
from lt_tensor.torch_commons import *
from lt_tensor.model_zoo.residual import ConvNets, ResBlocks1D, ResBlock1D, ResBlock1D2


class iSTFTGenerator(ConvNets):
    def __init__(
        self,
        in_channels: int = 80,
        upsample_rates: List[Union[int, List[int]]] = [8, 8],
        upsample_kernel_sizes: List[Union[int, List[int]]] = [16, 16],
        upsample_initial_channel: int = 512,
        resblock_kernel_sizes: List[Union[int, List[int]]] = [3, 7, 11],
        resblock_dilation_sizes: List[Union[int, List[int]]] = [
            [1, 3, 5],
            [1, 3, 5],
            [1, 3, 5],
        ],
        n_fft: int = 16,
        activation: nn.Module = nn.LeakyReLU(0.1),
        hop_length: int = 256,
        residual_cls: Union[ResBlock1D, ResBlock1D2] = ResBlock1D
    ):
        super().__init__()
        self.num_kernels = len(resblock_kernel_sizes)
        self.num_upsamples = len(upsample_rates)
        self.hop_length = hop_length
        self.conv_pre = weight_norm(
            nn.Conv1d(in_channels, upsample_initial_channel, 7, 1, padding=3)
        )
        self.blocks = nn.ModuleList()
        self.activation = activation
        for i, (u, k) in enumerate(zip(upsample_rates, upsample_kernel_sizes)):
            self.blocks.append(
                self._make_blocks(
                    (i, k, u),
                    upsample_initial_channel,
                    resblock_kernel_sizes,
                    resblock_dilation_sizes,
                    residual_cls
                )
            )

        ch = upsample_initial_channel // (2 ** (i + 1))
        self.post_n_fft = n_fft // 2 + 1
        self.conv_post = weight_norm(nn.Conv1d(ch, n_fft + 2, 7, 1, padding=3))
        self.conv_post.apply(self.init_weights)
        self.reflection_pad = nn.ReflectionPad1d((1, 0))

    def _make_blocks(
        self,
        state: Tuple[int, int, int],
        upsample_initial_channel: int,
        resblock_kernel_sizes: List[Union[int, List[int]]],
        resblock_dilation_sizes: List[int | List[int]],
        residual: nn.Module
    ):
        i, k, u = state
        channels = upsample_initial_channel // (2 ** (i + 1))
        return nn.ModuleDict(
            dict(
                up=nn.Sequential(
                    self.activation,
                    weight_norm(
                        nn.ConvTranspose1d(
                            upsample_initial_channel // (2**i),
                            channels,
                            k,
                            u,
                            padding=(k - u) // 2,
                        )
                    ).apply(self.init_weights),
                ),
                residual=ResBlocks1D(
                    channels,
                    resblock_kernel_sizes,
                    resblock_dilation_sizes,
                    self.activation,
                    residual
                ),
            )
        )

    def forward(self, x):
        x = self.conv_pre(x)
        for block in self.blocks:
            x = block["up"](x)
            x = block["residual"](x)

        x = self.conv_post(self.activation(self.reflection_pad(x)))
        spec = torch.exp(x[:, : self.post_n_fft, :])
        phase = torch.sin(x[:, self.post_n_fft :, :])
        return spec, phase
