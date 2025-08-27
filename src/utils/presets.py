"""
Presets de configuração para diferentes níveis de otimização.
"""
from typing import Dict, Any

from src.models.optimization import PresetConfig


PRESETS: Dict[str, PresetConfig] = {
    'conservative': PresetConfig(
        description='Otimização leve - remove apenas elementos redundantes.',
        config={
            'word_compression': 0.9, 
            'stop_word_removal': 0.1, 
            'min_word_length': 3,
            'language': 'pt'
        }
    ),
    'moderate': PresetConfig(
        description='Balanceio entre economia e legibilidade, incluindo tradução.',
        config={
            'word_compression': 0.75, 
            'remove_accents': True, 
            'translate_to_english': True, 
            'stop_word_removal': 0.3, 
            'min_word_length': 2,
            'language': 'pt'
        }
    ),
    'aggressive': PresetConfig(
        description='Otimização máxima - maior economia, menor legibilidade.',
        config={
            'word_compression': 0.6, 
            'remove_accents': True, 
            'remove_punctuation': True, 
            'translate_to_english': True, 
            'stop_word_removal': 0.5, 
            'min_word_length': 1,
            'language': 'pt'
        }
    ),
    'translation_only': PresetConfig(
        description='Apenas tradução para inglês (mais eficiente para IAs).',
        config={'translate_to_english': True, 'language': 'pt'}
    )
}


def get_presets_dict() -> Dict[str, Dict[str, Any]]:
    """Retorna os presets em formato de dicionário para serialização JSON."""
    return {
        name: {
            'description': preset.description,
            'config': preset.config
        }
        for name, preset in PRESETS.items()
    }
