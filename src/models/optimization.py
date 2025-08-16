"""
Modelos de dados para requisições e respostas da API.
"""
from dataclasses import dataclass
from typing import Dict, Any, Optional


@dataclass
class OptimizationRequest:
    """Modelo para requisições de otimização."""
    text: str
    config: Optional[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.config is None:
            self.config = {}


@dataclass
class OptimizationStats:
    """Estatísticas da otimização."""
    original_length: int
    optimized_length: int
    compression_ratio_percent: float
    characters_saved: int


@dataclass
class OptimizationResponse:
    """Modelo para resposta de otimização."""
    original_text: str
    optimized_text: str
    stats: OptimizationStats
    config_used: Dict[str, Any]


@dataclass
class PresetConfig:
    """Modelo para configurações de preset."""
    description: str
    config: Dict[str, Any]
