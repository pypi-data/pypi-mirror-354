import numpy as np
import torch

from .compress import power_uncompress
from .feature_generator import FeatureGenerator
from .forward_transform import ForwardTransform
from .inverse_transform import InverseTransform
from .stacked_complex import unstack_complex


def _create_forward_transform(feature_generator: FeatureGenerator) -> ForwardTransform:
    """Create a ForwardTransform instance with parameters from FeatureGenerator."""
    return ForwardTransform(
        length=feature_generator.ftransform_length,
        overlap=feature_generator.ftransform_overlap,
        bin_start=feature_generator.bin_start,
        bin_end=feature_generator.bin_end,
        ttype=feature_generator.ftransform_ttype,
    )


def _create_inverse_transform(feature_generator: FeatureGenerator) -> InverseTransform:
    """Create an InverseTransform instance with parameters from FeatureGenerator."""
    return InverseTransform(
        length=feature_generator.itransform_length,
        overlap=feature_generator.itransform_overlap,
        bin_start=feature_generator.bin_start,
        bin_end=feature_generator.bin_end,
        ttype=feature_generator.itransform_ttype,
    )


def _pad_transform_data(audio_f: np.ndarray, step: int) -> np.ndarray:
    """Pad transform data to account for SOV modes."""
    original_frames = audio_f.shape[0]
    total_frames = int(np.ceil(original_frames / step)) * step
    pad_frames = total_frames - original_frames
    return np.pad(audio_f, ((0, pad_frames), (0, 0)), mode="constant", constant_values=0)


def _is_power_compressed_mode(feature_mode: str) -> bool:
    """Check if the feature mode uses power compression (starts with 'h')."""
    return feature_mode.startswith("h")


def get_feature_from_audio(audio: np.ndarray, feature_mode: str) -> np.ndarray:
    """Apply forward transform and generate feature data from audio data
    :param audio: Time domain audio data [samples]
    :param feature_mode: Feature mode
    :return: Feature data [frames, strides, feature_parameters]
    """
    feature_generator = FeatureGenerator(feature_mode)
    forward_transform = _create_forward_transform(feature_generator)

    audio_tensor = torch.from_numpy(audio)
    audio_f, _ = forward_transform.execute_all(audio_tensor)

    padded_audio_f = _pad_transform_data(audio_f.numpy(), feature_generator.step)
    return feature_generator.execute_all(padded_audio_f)[0]


def get_audio_from_feature(feature: np.ndarray, feature_mode: str) -> np.ndarray:
    """Apply inverse transform to feature data to generate audio data
    :param feature: Feature data [frames, stride=1, feature_parameters]
    :param feature_mode: Feature mode
    :return: Audio data [samples]
    """
    if feature.ndim != 3:
        raise ValueError("feature must have 3 dimensions: [frames, stride=1, feature_parameters]")
    if feature.shape[1] != 1:
        raise ValueError("feature data with stride != 1 is not supported for audio extraction.")

    feature_generator = FeatureGenerator(feature_mode)
    inverse_transform = _create_inverse_transform(feature_generator)

    feature_complex = unstack_complex(feature.squeeze())
    if _is_power_compressed_mode(feature_mode):
        feature_complex = power_uncompress(feature_complex)

    feature_tensor = torch.from_numpy(feature_complex)
    audio, _ = inverse_transform.execute_all(feature_tensor)
    return np.squeeze(audio.numpy())
