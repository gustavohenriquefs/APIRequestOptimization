from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class OptimizationRequest:
    text: str
    config: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}


@dataclass
class OptimizationStats:
    original_length: int
    optimized_length: int
    compression_ratio_percent: float
    characters_saved: int


@dataclass
class OptimizationResponse:
    original_text: str
    optimized_text: str
    stats: OptimizationStats
    config_used: Dict[str, Any]


@dataclass
class PresetConfig:
    description: str
    config: Dict[str, Any]
