"""
Common data structures shared across preset formats.
"""

from dataclasses import dataclass, field
from typing import Any, Dict, Optional


@dataclass
class PresetData:
    """
    Generic preset data container.

    This structure holds parsed preset data before conversion
    to format-specific models.
    """

    format: str
    version: str
    name: str
    parameters: Dict[str, Any] = field(default_factory=dict)
    raw_data: Optional[bytes] = None

    def __post_init__(self) -> None:
        """Validate preset data after initialization."""
        if not self.name:
            self.name = "Unnamed Preset"


@dataclass
class EffectParameters:
    """Common effect parameters across all formats."""

    enabled: bool = True
    bypass: bool = False
    mix: float = 50.0  # 0-100%
    level: float = 50.0  # 0-100%


@dataclass
class OverdriveEffect(EffectParameters):
    """Overdrive/distortion effect parameters."""

    type: str = "overdrive"
    drive: float = 50.0  # 0-100%
    tone: float = 50.0  # 0-100%
    gain: float = 50.0  # 0-100%


@dataclass
class DelayEffect(EffectParameters):
    """Delay effect parameters."""

    type: str = "delay"
    time: int = 500  # milliseconds
    feedback: float = 30.0  # 0-100%
    tap_tempo: bool = False


@dataclass
class ReverbEffect(EffectParameters):
    """Reverb effect parameters."""

    type: str = "reverb"
    room_size: float = 50.0  # 0-100%
    decay: float = 50.0  # 0-100%
    pre_delay: int = 0  # milliseconds


@dataclass
class ChorusEffect(EffectParameters):
    """Chorus effect parameters."""

    type: str = "chorus"
    rate: float = 50.0  # 0-100%
    depth: float = 50.0  # 0-100%
    feedback: float = 30.0  # 0-100%


@dataclass
class CompressorEffect(EffectParameters):
    """Compressor effect parameters."""

    type: str = "compressor"
    threshold: float = -20.0  # dB
    ratio: float = 4.0  # X:1
    attack: float = 10.0  # milliseconds
    release: float = 100.0  # milliseconds


@dataclass
class EQEffect(EffectParameters):
    """Equalizer effect parameters."""

    type: str = "eq"
    bass: float = 50.0  # 0-100%
    mid: float = 50.0  # 0-100%
    treble: float = 50.0  # 0-100%
    presence: float = 50.0  # 0-100%


@dataclass
class AmpSimulation(EffectParameters):
    """Amplifier simulation parameters."""

    type: str = "amp_sim"
    amp_model: str = "clean"
    gain: float = 50.0  # 0-100%
    bass: float = 50.0  # 0-100%
    mid: float = 50.0  # 0-100%
    treble: float = 50.0  # 0-100%
    presence: float = 50.0  # 0-100%
    master: float = 50.0  # 0-100%
    cabinet: str = "4x12"
