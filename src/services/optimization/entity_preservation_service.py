import re
from typing import List, Dict, Set, Tuple, Optional
from dataclasses import dataclass
from enum import Enum

from src.data.locations import is_known_location, get_all_locations
from src.data.animals import is_nature_element, PRESERVATION_CATEGORIES
from src.data.technology import is_tech_term, TECH_PRESERVATION

class EntityType(Enum):
    MONEY = "money"
    PERCENTAGE = "percentage"
    DATE = "date"
    TIME = "time"
    MEASUREMENT = "measurement"
    LOCATION = "location"
    ANIMAL = "animal"
    TECHNOLOGY = "technology"
    EMAIL = "email"
    URL = "url"
    PHONE = "phone"

class PreservationLevel(Enum):
    NEVER_COMPRESS = "never"      # Nunca comprimir (ex: URLs, emails)
    HIGH_PRESERVE = "high"        # Compressão mínima (ex: dinheiro, datas)
    MEDIUM_PRESERVE = "medium"    # Compressão moderada (ex: locais)
    LOW_PRESERVE = "low"          # Pode comprimir mais (ex: alguns animais)

@dataclass
class Entity:
    text: str
    entity_type: EntityType
    start: int
    end: int
    preservation_level: PreservationLevel
    confidence: float = 0.9

class EntityPreservationService:
    
    def __init__(self):
        self.patterns = self._build_entity_patterns()
        self.preservation_rules = self._build_preservation_rules()
    
    def _build_entity_patterns(self) -> Dict[EntityType, List[re.Pattern]]:
        return {
            EntityType.MONEY: [
                re.compile(r'\$\d+(?:\.\d{2})?', re.I),
                re.compile(r'R\$\s?\d+(?:,\d{2})?', re.I),
                re.compile(r'\d+\s*(?:reais?|dólares?|euros?|libras?)', re.I),
                re.compile(r'(?:US\$|USD)\s?\d+', re.I),
            ],
            
            EntityType.PERCENTAGE: [
                re.compile(r'\d+(?:\.\d+)?\s*%'),
                re.compile(r'\d+\s*por\s*cento', re.I),
            ],
            
            EntityType.DATE: [
                re.compile(r'\d{1,2}[/-]\d{1,2}[/-]\d{2,4}'),
                re.compile(r'\d{1,2}\s+de\s+\w+\s+de\s+\d{4}', re.I),
                re.compile(r'(?:janeiro|fevereiro|março|abril|maio|junho|julho|agosto|setembro|outubro|novembro|dezembro)\s+\d{1,2}', re.I),
            ],
            
            EntityType.TIME: [
                re.compile(r'\d{1,2}:\d{2}(?::\d{2})?'),
                re.compile(r'\d{1,2}h\d{2}(?:min)?', re.I),
                re.compile(r'\d{1,2}\s*(?:am|pm)', re.I),
            ],
            
            EntityType.MEASUREMENT: [
                re.compile(r'\d+(?:\.\d+)?\s*(?:km|m|cm|mm|kg|g|mg|l|ml|°C|°F)', re.I),
                re.compile(r'\d+\s*(?:metros?|quilômetros?|centímetros?|quilogramas?|gramas?|litros?)', re.I),
            ],
            
            EntityType.EMAIL: [
                re.compile(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'),
            ],
            
            EntityType.URL: [
                re.compile(r'https?://[^\s]+'),
                re.compile(r'www\.[^\s]+'),
            ],
            
            EntityType.PHONE: [
                re.compile(r'\(\d{2}\)\s*\d{4,5}-\d{4}'),  # (11) 99999-9999
                re.compile(r'\d{2}\s*\d{4,5}-\d{4}'),      # 11 99999-9999
                re.compile(r'\+\d{2}\s*\d{2}\s*\d{4,5}-\d{4}'),  # +55 11 99999-9999
            ],
        }
    
    def _build_preservation_rules(self) -> Dict[EntityType, PreservationLevel]:
        return {
            EntityType.MONEY: PreservationLevel.NEVER_COMPRESS,
            EntityType.PERCENTAGE: PreservationLevel.NEVER_COMPRESS,
            EntityType.DATE: PreservationLevel.HIGH_PRESERVE,
            EntityType.TIME: PreservationLevel.HIGH_PRESERVE,
            EntityType.MEASUREMENT: PreservationLevel.HIGH_PRESERVE,
            EntityType.EMAIL: PreservationLevel.NEVER_COMPRESS,
            EntityType.URL: PreservationLevel.NEVER_COMPRESS,
            EntityType.PHONE: PreservationLevel.NEVER_COMPRESS,
            EntityType.LOCATION: PreservationLevel.MEDIUM_PRESERVE,
            EntityType.ANIMAL: PreservationLevel.MEDIUM_PRESERVE,
            EntityType.TECHNOLOGY: PreservationLevel.LOW_PRESERVE,
        }
    
    def extract_entities(self, text: str) -> List[Entity]:
        entities = []
        
        for entity_type, patterns in self.patterns.items():
            for pattern in patterns:
                for match in pattern.finditer(text):
                    entity = Entity(
                        text=match.group(),
                        entity_type=entity_type,
                        start=match.start(),
                        end=match.end(),
                        preservation_level=self.preservation_rules[entity_type]
                    )
                    entities.append(entity)
        
        entities.extend(self._extract_dictionary_entities(text))
        
        entities = self._remove_overlaps(entities)
        
        return sorted(entities, key=lambda e: e.start)
    
    def _extract_dictionary_entities(self, text: str) -> List[Entity]:
        entities = []
        words = re.finditer(r'\b\w+(?:\s+\w+)*\b', text)
        
        for word_match in words:
            word_text = word_match.group()
            
            if is_known_location(word_text):
                entities.append(Entity(
                    text=word_text,
                    entity_type=EntityType.LOCATION,
                    start=word_match.start(),
                    end=word_match.end(),
                    preservation_level=PreservationLevel.MEDIUM_PRESERVE
                ))
            
            elif is_nature_element(word_text):
                if word_text.lower() in PRESERVATION_CATEGORIES['high_preserve']:
                    level = PreservationLevel.HIGH_PRESERVE
                elif word_text.lower() in PRESERVATION_CATEGORIES['medium_preserve']:
                    level = PreservationLevel.MEDIUM_PRESERVE
                else:
                    level = PreservationLevel.LOW_PRESERVE
                
                entities.append(Entity(
                    text=word_text,
                    entity_type=EntityType.ANIMAL,
                    start=word_match.start(),
                    end=word_match.end(),
                    preservation_level=level
                ))
            
            elif is_tech_term(word_text):
                if word_text in TECH_PRESERVATION['never_compress']:
                    level = PreservationLevel.NEVER_COMPRESS
                elif word_text in TECH_PRESERVATION['minimal_compress']:
                    level = PreservationLevel.HIGH_PRESERVE
                elif word_text in TECH_PRESERVATION['moderate_compress']:
                    level = PreservationLevel.MEDIUM_PRESERVE
                else:
                    level = PreservationLevel.LOW_PRESERVE
                
                entities.append(Entity(
                    text=word_text,
                    entity_type=EntityType.TECHNOLOGY,
                    start=word_match.start(),
                    end=word_match.end(),
                    preservation_level=level
                ))
        
        return entities
    
    def _remove_overlaps(self, entities: List[Entity]) -> List[Entity]:
        if not entities:
            return entities
        
        sorted_entities = sorted(entities, key=lambda e: (e.start, -(e.end - e.start)))
        
        filtered = []
        last_end = -1
        
        for entity in sorted_entities:
            if entity.start >= last_end:
                filtered.append(entity)
                last_end = entity.end
        
        return filtered
    
    def get_compression_limits(self, entities: List[Entity]) -> Dict[str, float]:
        return {
            PreservationLevel.NEVER_COMPRESS.value: 1.0,
            PreservationLevel.HIGH_PRESERVE.value: 0.9,
            PreservationLevel.MEDIUM_PRESERVE.value: 0.7,
            PreservationLevel.LOW_PRESERVE.value: 0.5,
        }
    
    def should_preserve_word(self, word: str, position: int, entities: List[Entity]) -> Tuple[bool, Optional[float]]:
        for entity in entities:
            if entity.start <= position < entity.end:
                limits = self.get_compression_limits([entity])
                limit = limits[entity.preservation_level.value]
                return True, limit
        
        return False, None
