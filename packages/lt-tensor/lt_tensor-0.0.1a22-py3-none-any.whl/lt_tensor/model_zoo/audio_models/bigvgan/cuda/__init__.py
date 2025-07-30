import os
import pathlib
import subprocess
import torch
import torch.nn as nn
from torch.utils import cpp_extension

"""
Setting this param to a list has a problem of generating different compilation commands 
(with different order of architectures) and leading to recompilation of fused kernels. 
Set it to empty string to avoid recompilation and assign arch flags explicitly in extra_cuda_cflags below
"""
os.environ["TORCH_CUDA_ARCH_LIST"] = ""


def load():
    # Check if cuda 11 is installed for compute capability 8.0
    cc_flag = []
    _, bare_metal_major, _ = _get_cuda_bare_metal_version(cpp_extension.CUDA_HOME)
    if int(bare_metal_major) >= 11:
        cc_flag.append("-gencode")
        cc_flag.append("arch=compute_80,code=sm_80")

    # Build path
    srcpath = pathlib.Path(__file__).parent.absolute()
    buildpath = srcpath / "build"
    _create_build_dir(buildpath)

    # Helper function to build the kernels.
    def _cpp_extention_load_helper(name, sources, extra_cuda_flags):
        return cpp_extension.load(
            name=name,
            sources=sources,
            build_directory=buildpath,
            extra_cflags=[
                "-O3",
            ],
            extra_cuda_cflags=[
                "-O3",
                "-gencode",
                "arch=compute_70,code=sm_70",
                "--use_fast_math",
            ]
            + extra_cuda_flags
            + cc_flag,
            verbose=True,
        )

    extra_cuda_flags = [
        "-U__CUDA_NO_HALF_OPERATORS__",
        "-U__CUDA_NO_HALF_CONVERSIONS__",
        "--expt-relaxed-constexpr",
        "--expt-extended-lambda",
    ]

    sources = [
        srcpath / "anti_alias_activation.cpp",
        srcpath / "anti_alias_activation_cuda.cu",
    ]
    anti_alias_activation_cuda = _cpp_extention_load_helper(
        "anti_alias_activation_cuda", sources, extra_cuda_flags
    )

    return anti_alias_activation_cuda


def _get_cuda_bare_metal_version(cuda_dir):
    raw_output = subprocess.check_output(
        [cuda_dir + "/bin/nvcc", "-V"], universal_newlines=True
    )
    output = raw_output.split()
    release_idx = output.index("release") + 1
    release = output[release_idx].split(".")
    bare_metal_major = release[0]
    bare_metal_minor = release[1][0]

    return raw_output, bare_metal_major, bare_metal_minor


def _create_build_dir(buildpath):
    try:
        os.mkdir(buildpath)
    except OSError:
        if not os.path.isdir(buildpath):
            print(f"Creation of the build directory {buildpath} failed")


import torch.nn as nn
from lt_tensor.model_zoo.activations.alias_free_torch.resample import (
    UpSample1d,
    DownSample1d,
)

anti_alias_activation_cuda = load.load()


class FusedAntiAliasActivation(torch.autograd.Function):
    """
    Assumes filter size 12, replication padding on upsampling/downsampling, and logscale alpha/beta parameters as inputs.
    The hyperparameters are hard-coded in the kernel to maximize speed.
    NOTE: The fused kernel is incorrect for Activation1d with different hyperparameters.
    """

    @staticmethod
    def forward(ctx, inputs, up_ftr, down_ftr, alpha, beta):
        activation_results = anti_alias_activation_cuda.forward(
            inputs, up_ftr, down_ftr, alpha, beta
        )

        return activation_results

    @staticmethod
    def backward(ctx, output_grads):
        raise NotImplementedError
        return output_grads, None, None


class Activation1d(nn.Module):
    def __init__(
        self,
        activation,
        up_ratio: int = 2,
        down_ratio: int = 2,
        up_kernel_size: int = 12,
        down_kernel_size: int = 12,
        fused: bool = True,
    ):
        super().__init__()
        self.up_ratio = up_ratio
        self.down_ratio = down_ratio
        self.act = activation
        self.upsample = UpSample1d(up_ratio, up_kernel_size)
        self.downsample = DownSample1d(down_ratio, down_kernel_size)

        self.fused = fused  # Whether to use fused CUDA kernel or not

    def forward(self, x):
        if not self.fused:
            x = self.upsample(x)
            x = self.act(x)
            x = self.downsample(x)
            return x
        else:
            if self.act.__class__.__name__ == "Snake":
                beta = self.act.alpha.data  # Snake uses same params for alpha and beta
            else:
                beta = (
                    self.act.beta.data
                )  # Snakebeta uses different params for alpha and beta
            alpha = self.act.alpha.data
            if (
                not self.act.alpha_logscale
            ):  # Exp baked into cuda kernel, cancel it out with a log
                alpha = torch.log(alpha)
                beta = torch.log(beta)

            x = FusedAntiAliasActivation.apply(
                x, self.upsample.filter, self.downsample.lowpass.filter, alpha, beta
            )
            return x
