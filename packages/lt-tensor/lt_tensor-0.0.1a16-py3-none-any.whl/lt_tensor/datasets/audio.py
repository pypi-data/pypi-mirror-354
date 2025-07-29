__all__ = ["WaveMelDataset"]
from lt_tensor.torch_commons import *
from lt_utils.common import *
from lt_utils.misc_utils import default
import random
from torch.utils.data import Dataset, DataLoader, Sampler
from lt_tensor.processors import AudioProcessor
import torch.nn.functional as FT
from lt_tensor.misc_utils import log_tensor
from tqdm import tqdm


DEFAULT_DEVICE = torch.tensor([0]).device


class WaveMelDataset(Dataset):
    cached_data: Union[list[dict[str, Tensor]], Tuple[Tensor, Tensor]] = []
    loaded_files: Dict[str, List[Dict[str, Tensor]]] = {}
    normalize_waves: bool = False
    randomize_ranges: bool = False
    alpha_wv: float = 1.0
    limit_files: Optional[int] = None
    min_frame_length: Optional[int] = None
    max_frame_length: Optional[int] = None

    def __init__(
        self,
        audio_processor: AudioProcessor,
        dataset_path: PathLike,
        limit_files: Optional[int] = None,
        min_frame_length: Optional[int] = None,
        max_frame_length: Optional[int] = None,
        randomize_ranges: Optional[bool] = None,
        pre_load: bool = False,
        normalize_waves: Optional[bool] = None,
        alpha_wv: Optional[float] = None,
        lib_norm: bool = True,
    ):
        super().__init__()
        assert max_frame_length is None or max_frame_length >= (
            (audio_processor.n_fft // 2) + 1
        )
        self.ap = audio_processor
        self.dataset_path = dataset_path
        if limit_files:
            self.limit_files = limit_files
        if normalize_waves is not None:
            self.normalize_waves = normalize_waves
        if alpha_wv is not None:
            self.alpha_wv = alpha_wv
        if pre_load is not None:
            self.pre_loaded = pre_load
        if randomize_ranges is not None:
            self.randomize_ranges = randomize_ranges

        self.post_n_fft = (audio_processor.n_fft // 2) + 1
        self.lib_norm = lib_norm
        if max_frame_length is not None:
            max_frame_length = max(self.post_n_fft + 1, max_frame_length)
            self.r_range = max(self.post_n_fft + 1, max_frame_length // 3)
            self.max_frame_length = max_frame_length
        if min_frame_length is not None:
            self.min_frame_length = max(
                self.post_n_fft + 1, min(min_frame_length, max_frame_length)
            )

        self.files = self.ap.find_audios(dataset_path, maximum=None)
        if limit_files:
            random.shuffle(self.files)
            self.files = self.files[-self.limit_files :]
        if pre_load:
            for file in tqdm(self.files, "Loading files"):
                results = self.load_data(file)
                if not results:
                    continue
                self.cached_data.extend(results)

    def renew_dataset(self, new_path: Optional[PathLike] = None):
        new_path = default(new_path, self.dataset_path)
        self.files = self.ap.find_audios(new_path, maximum=None)
        random.shuffle(self.files)
        for file in tqdm(self.files, "Loading files"):
            results = self.load_data(file)
            if not results:
                continue
            self.cached_data.extend(results)

    def _add_dict(
        self,
        audio_wave: Tensor,
        audio_mel: Tensor,
        pitch: Tensor,
        rms: Tensor,
        file: PathLike,
    ):
        return {
            "wave": audio_wave,
            "pitch": pitch,
            "rms": rms,
            "mel": audio_mel,
            "file": file,
        }

    def load_data(self, file: PathLike):
        initial_audio = self.ap.load_audio(
            file, normalize=self.lib_norm, alpha=self.alpha_wv
        )
        if self.normalize_waves:
            initial_audio = self.ap.normalize_audio(initial_audio)
        if initial_audio.shape[-1] < self.post_n_fft:
            return None

        if self.min_frame_length is not None:
            if self.min_frame_length > initial_audio.shape[-1]:
                return None
        if (
            not self.max_frame_length
            or initial_audio.shape[-1] <= self.max_frame_length
        ):

            audio_rms = self.ap.compute_rms(initial_audio)
            audio_pitch = self.ap.compute_pitch(initial_audio)
            audio_mel = self.ap.compute_mel(initial_audio, add_base=True)

            return [
                self._add_dict(initial_audio, audio_mel, audio_pitch, audio_rms, file)
            ]
        results = []

        if self.randomize_ranges:
            frame_limit = random.randint(self.r_range, self.max_frame_length)
        else:
            frame_limit = self.max_frame_length

        fragments = list(
            torch.split(initial_audio, split_size_or_sections=frame_limit, dim=-1)
        )
        random.shuffle(fragments)
        for fragment in fragments:
            if fragment.shape[-1] < self.post_n_fft:
                # Too small
                continue
            if (
                self.min_frame_length is not None
                and self.min_frame_length > fragment.shape[-1]
            ):
                continue

            audio_rms = self.ap.compute_rms(fragment)
            audio_pitch = self.ap.compute_pitch(fragment)
            audio_mel = self.ap.compute_mel(fragment, add_base=True)
            results.append(
                self._add_dict(fragment, audio_mel, audio_pitch, audio_rms, file)
            )
        return results

    def get_data_loader(
        self,
        batch_size: int = 1,
        shuffle: Optional[bool] = None,
        sampler: Optional[Union[Sampler, Iterable]] = None,
        batch_sampler: Optional[Union[Sampler[list], Iterable[list]]] = None,
        num_workers: int = 0,
        pin_memory: bool = False,
        drop_last: bool = False,
        timeout: float = 0,
    ):
        return DataLoader(
            self,
            batch_size=batch_size,
            shuffle=shuffle,
            sampler=sampler,
            batch_sampler=batch_sampler,
            num_workers=num_workers,
            pin_memory=pin_memory,
            drop_last=drop_last,
            timeout=timeout,
            collate_fn=self.collate_fn,
        )

    def collate_fn(self, batch: Sequence[Dict[str, Tensor]]):
        mel = []
        wave = []
        file = []
        rms = []
        pitch = []
        for x in batch:
            mel.append(x["mel"])
            wave.append(x["wave"])
            file.append(x["file"])
            rms.append(x["rms"])
            pitch.append(x["pitch"])
        # Find max time in mel (dim -1), and max audio length
        max_mel_len = max([m.shape[-1] for m in mel])
        max_audio_len = max([a.shape[-1] for a in wave])
        max_pitch_len = max([a.shape[-1] for a in pitch])
        max_rms_len = max([a.shape[-1] for a in rms])

        padded_mel = torch.stack(
            [FT.pad(m, (0, max_mel_len - m.shape[-1])) for m in mel]
        )  # shape: [B, 80, T_max]

        padded_wave = torch.stack(
            [FT.pad(a, (0, max_audio_len - a.shape[-1])) for a in wave]
        )  # shape: [B, L_max]

        padded_pitch = torch.stack(
            [FT.pad(a, (0, max_pitch_len - a.shape[-1])) for a in pitch]
        )  # shape: [B, L_max]
        padded_rms = torch.stack(
            [FT.pad(a, (0, max_rms_len - a.shape[-1])) for a in rms]
        )  # shape: [B, L_max]
        return dict(
            mel=padded_mel,
            wave=padded_wave,
            pitch=padded_pitch,
            rms=padded_rms,
            file=file,
        )

    def get_item(self, idx: int):
        if self.pre_loaded:
            return self.cached_data[idx]
        file = self.files[idx]
        if file not in self.loaded_files:
            self.loaded_files[file] = self.load_data(file)
        return random.choice(self.loaded_files[file])

    def __len__(self):
        if self.pre_loaded:
            return len(self.cached_data)
        return len(self.files)

    def __getitem__(self, index: int):
        return self.get_item(index)
