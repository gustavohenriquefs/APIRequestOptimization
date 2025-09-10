from .locations import (
    BRAZILIAN_STATES, 
    STATE_ABBREVIATIONS, 
    COUNTRIES,
    get_all_locations,
    is_known_location
)
from .animals import (
    DOMESTIC_ANIMALS,
    WILD_ANIMALS,
    get_all_animals,
    is_animal,
    is_nature_element
)
from .technology import (
    PROGRAMMING_TECHNOLOGIES,
    AI_ML_TERMS,
    get_all_tech_terms,
    is_tech_term
)
from .abbreviations import (
    MEASUREMENTS,
    TIME_UNITS,
    get_all_abbreviations,
    get_savings_potential
)

__all__ = [
    'BRAZILIAN_STATES',
    'STATE_ABBREVIATIONS', 
    'COUNTRIES',
    'get_all_locations',
    'is_known_location',
    
    'DOMESTIC_ANIMALS',
    'WILD_ANIMALS', 
    'get_all_animals',
    'is_animal',
    'is_nature_element',
    
    'PROGRAMMING_TECHNOLOGIES',
    'AI_ML_TERMS',
    'get_all_tech_terms',
    'is_tech_term',
    
    'MEASUREMENTS',
    'TIME_UNITS',
    'get_all_abbreviations',
    'get_savings_potential'
]
