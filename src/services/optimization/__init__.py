"""
Serviços de otimização modularizados.
"""
from .abbreviation_service import AbbreviationService, ReplacementResult
from .entity_preservation_service import (
    EntityPreservationService, 
    Entity, 
    EntityType, 
    PreservationLevel
)

__all__ = [
    'AbbreviationService',
    'ReplacementResult', 
    'EntityPreservationService',
    'Entity',
    'EntityType',
    'PreservationLevel'
]
