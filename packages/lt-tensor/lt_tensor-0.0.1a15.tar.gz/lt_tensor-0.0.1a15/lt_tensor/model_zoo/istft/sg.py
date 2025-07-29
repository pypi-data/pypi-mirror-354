import torch
import torch.nn as nn
import math
from einops import repeat


class SineGen(nn.Module):
    def __init__(
        self,
        samp_rate,
        upsample_scale,
        harmonic_num=0,
        sine_amp=0.1,
        noise_std=0.003,
        voiced_threshold=0,
        flag_for_pulse=False,
    ):
        super().__init__()
        self.sampling_rate = samp_rate
        self.upsample_scale = upsample_scale
        self.harmonic_num = harmonic_num
        self.sine_amp = sine_amp
        self.noise_std = noise_std
        self.voiced_threshold = voiced_threshold
        self.flag_for_pulse = flag_for_pulse
        self.dim = self.harmonic_num + 1  # fundamental + harmonics

    def _f02uv_b(self, f0):
        return (f0 > self.voiced_threshold).float()  # [B, T]

    def _f02uv(self, f0):
        return (f0 > self.voiced_threshold).float().unsqueeze(-1)  # -> (B, T, 1)

    @torch.no_grad()
    def _f02sine(self, f0_values):
        """
        f0_values: (B, T, 1)
        Output: sine waves (B, T * upsample, dim)
        """
        B, T, _ = f0_values.size()
        f0_upsampled = repeat(
            f0_values, "b t d -> b (t r) d", r=self.upsample_scale
        )  # (B, T_up, 1)

        # Create harmonics
        harmonics = (
            torch.arange(1, self.dim + 1, device=f0_values.device)
            .float()
            .view(1, 1, -1)
        )
        f0_harm = f0_upsampled * harmonics  # (B, T_up, dim)

        # Convert Hz to radians (2πf/sr), then integrate to get phase
        rad_values = f0_harm / self.sampling_rate  # normalized freq
        rad_values = rad_values % 1.0  # remove multiples of 2π

        # Random initial phase for each harmonic (except 0th if pulse mode)
        if self.flag_for_pulse:
            rand_ini = torch.zeros((B, 1, self.dim), device=f0_values.device)
        else:
            rand_ini = torch.rand((B, 1, self.dim), device=f0_values.device)

        rand_ini = rand_ini * 2 * math.pi

        # Compute cumulative phase
        rad_values = rad_values * 2 * math.pi
        phase = torch.cumsum(rad_values, dim=1) + rand_ini  # (B, T_up, dim)

        sine_waves = torch.sin(phase)  # (B, T_up, dim)
        return sine_waves

    def _forward(self, f0):
        """
        f0: (B, T, 1)
        returns: sine signal with harmonics and noise added
        """
        sine_waves = self._f02sine(f0)  # (B, T_up, dim)
        uv = self._f02uv_b(f0) # (B, T, 1)
        uv = repeat(uv, "b t d -> b (t r) d", r=self.upsample_scale)  # (B, T_up, 1)

        # voiced sine + unvoiced noise
        sine_signal = self.sine_amp * sine_waves * uv  # (B, T_up, dim)
        noise = torch.randn_like(sine_signal) * self.noise_std
        output = sine_signal + noise * (1.0 - uv)  # noise added only on unvoiced

        return output  # (B, T_up, dim)

    def forward(self, f0):
        """
        Args:
            f0: (B, T) in Hz (before upsampling)
        Returns:
            sine_waves: (B, T_up, dim)
            uv: (B, T_up, 1)
            noise: (B, T_up, 1)
        """
        B, T = f0.shape
        device = f0.device

        # Get uv mask (before upsampling)
        uv = self._f02uv(f0)  # (B, T, 1)

        # Expand f0 to include harmonics: (B, T, dim)
        f0 = f0.unsqueeze(-1)  # (B, T, 1)
        harmonics = (
            torch.arange(1, self.dim + 1, device=device).float().view(1, 1, -1)
        )  # (1, 1, dim)
        f0_harm = f0 * harmonics  # (B, T, dim)

        # Upsample
        f0_harm_up = repeat(
            f0_harm, "b t d -> b (t r) d", r=self.upsample_scale
        )  # (B, T_up, dim)
        uv_up = repeat(uv, "b t d -> b (t r) d", r=self.upsample_scale)  # (B, T_up, 1)

        # Convert to radians
        rad_per_sample = f0_harm_up / self.sampling_rate  # Hz → cycles/sample
        rad_per_sample = rad_per_sample * 2 * math.pi  # cycles → radians/sample

        # Random phase init for each sample
        B, T_up, D = rad_per_sample.shape
        rand_phase = torch.rand(B, D, device=device) * 2 * math.pi  # (B, D)

        # Compute cumulative phase
        phase = torch.cumsum(rad_per_sample, dim=1) + rand_phase.unsqueeze(
            1
        )  # (B, T_up, D)

        # Apply sine
        sine_waves = torch.sin(phase) * self.sine_amp  # (B, T_up, D)

        # Handle unvoiced: create noise only for fundamental
        noise = torch.randn(B, T_up, 1, device=device) * self.noise_std
        if self.flag_for_pulse:
            # If pulse mode is on, align phase at start of voiced segments
            # Optional and tricky to implement — may require segmenting uv
            pass

        # Replace sine by noise for unvoiced (only on fundamental)
        sine_waves[:, :, 0:1] = sine_waves[:, :, 0:1] * uv_up + noise * (1 - uv_up)

        return sine_waves, uv_up, noise
