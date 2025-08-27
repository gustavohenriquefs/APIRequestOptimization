"""
Serviço para aplicação inteligente de abreviações.
"""
import re
from typing import Dict, List, Tuple, Optional
from dataclasses import dataclass

from src.data.locations import get_all_locations, find_location_match, LOCATION_VARIATIONS
from src.data.animals import get_all_nature
from src.data.technology import get_all_tech_terms
from src.data.abbreviations import get_all_abbreviations
from src.data.numbers import NumberPreservationService

@dataclass
class ReplacementResult:
    """Resultado de uma substituição de abreviação."""
    original: str
    replacement: str
    position: int
    savings: int
    category: str = "general"

class AbbreviationService:
    """Serviço para aplicação inteligente de abreviações."""
    
    def __init__(self):
        self.abbreviations = self._build_abbreviation_map()
        self.number_service = NumberPreservationService()
        
    def _build_abbreviation_map(self) -> Dict[str, str]:
        """Constrói mapa unificado de abreviações."""
        all_abbrevs = {}
        
        # Adiciona todas as categorias
        all_abbrevs.update(get_all_locations())
        all_abbrevs.update(get_all_nature())
        all_abbrevs.update(get_all_tech_terms())
        all_abbrevs.update(get_all_abbreviations())
        
        # Adiciona variações de localização
        all_abbrevs.update(LOCATION_VARIATIONS)
        
        return all_abbrevs
    
    def apply_abbreviations(
        self, 
        text: str, 
        aggressiveness: float = 0.5,
        preserve_context: bool = True
    ) -> Tuple[str, List[ReplacementResult]]:
        """
        Aplica abreviações no texto baseado no nível de agressividade.
        Versão melhorada com suporte a variações de capitalização e números.
        """
        processed_text = text
        replacements = []
        
        # Primeiro, trata localizações com variações especiais
        processed_text, location_replacements = self._handle_location_variations(processed_text)
        replacements.extend(location_replacements)
        
        # Depois aplica abreviações gerais
        sorted_abbrevs = sorted(
            self.abbreviations.items(),
            key=lambda x: len(x[0]),
            reverse=True
        )
        
        for original, abbrev in sorted_abbrevs:
            if self._should_abbreviate(original, abbrev, aggressiveness):
                new_text, found_replacements = self._replace_with_context(
                    processed_text, original, abbrev, preserve_context
                )
                
                if found_replacements:
                    processed_text = new_text
                    replacements.extend(found_replacements)
        
        return processed_text, replacements
    
    def _handle_location_variations(self, text: str) -> Tuple[str, List[ReplacementResult]]:
        """Trata variações específicas de localização como Ceará/ceara/Ceara."""
        replacements = []
        processed_text = text
        
        # Padrões específicos para variações comuns
        location_patterns = [
            # Ceará e variações
            (r'\b[Cc]ear[aá]\b', 'CE', 'location'),
            # São Paulo variações  
            (r'\b[Ss][ãa]o\s+[Pp]aulo\b', 'SP', 'location'),
            # Rio de Janeiro
            (r'\b[Rr]io\s+de\s+[Jj]aneiro\b', 'RJ', 'location'),
            # Brasília
            (r'\b[Bb]ras[ií]lia\b', 'BSB', 'location'),
            # Minas Gerais
            (r'\b[Mm]inas\s+[Gg]erais\b', 'MG', 'location'),
        ]
        
        for pattern, abbrev, category in location_patterns:
            regex = re.compile(pattern)
            for match in regex.finditer(processed_text):
                original_text = match.group()
                savings = len(original_text) - len(abbrev)
                
                if savings > 0:  # Só substitui se economiza caracteres
                    replacements.append(ReplacementResult(
                        original=original_text,
                        replacement=abbrev,
                        position=match.start(),
                        savings=savings,
                        category=category
                    ))
            
            processed_text = regex.sub(abbrev, processed_text)
        
        return processed_text, replacements
    
    def _should_abbreviate(
        self, 
        original: str, 
        abbrev: str, 
        aggressiveness: float
    ) -> bool:
        """Determina se uma palavra deve ser abreviada."""
        if len(abbrev) >= len(original):
            return False
            
        savings_ratio = (len(original) - len(abbrev)) / len(original)
        min_savings_threshold = 1.0 - aggressiveness
        
        return savings_ratio >= min_savings_threshold
    
    def _replace_with_context(
        self, 
        text: str, 
        original: str, 
        abbrev: str,
        preserve_context: bool
    ) -> Tuple[str, List[ReplacementResult]]:
        """Substitui palavra preservando contexto e capitalização."""
        replacements = []
        
        # Verifica se é um número importante antes de processar
        if preserve_context and self.number_service.is_important_number(original)[0]:
            return text, []
        
        # Pattern para busca case-insensitive com word boundaries
        pattern = re.compile(r'\b' + re.escape(original) + r'\b', re.IGNORECASE)
        
        def replace_func(match):
            matched_text = match.group()
            start_pos = match.start()
            
            # Preserva capitalização
            if matched_text[0].isupper():
                if len(abbrev) <= 3:
                    replacement = abbrev.upper()
                else:
                    replacement = abbrev.capitalize()
            else:
                replacement = abbrev.lower()
            
            # Verifica contexto se solicitado
            if preserve_context and not self._is_safe_context(text, start_pos):
                return matched_text  # Não substitui em contexto duvidoso
            
            savings = len(matched_text) - len(replacement)
            replacements.append(ReplacementResult(
                original=matched_text,
                replacement=replacement,
                position=start_pos,
                savings=savings,
                category='abbreviation'
            ))
            
            return replacement
        
        new_text = pattern.sub(replace_func, text)
        return new_text, replacements
    
    def _is_safe_context(self, text: str, position: int, window: int = 20) -> bool:
        """Verifica se o contexto ao redor da palavra é seguro para abreviação."""
        start = max(0, position - window)
        end = min(len(text), position + window)
        context = text[start:end].lower()
        
        # Contextos onde é menos seguro abreviar
        unsafe_patterns = [
            r'\b(?:não|never|not)\b.*',  # Negações próximas
            r'[.!?]\s*$',  # Final de frases importantes
            r'^\s*[A-Z]',  # Início de frases/títulos
        ]
        
        for pattern in unsafe_patterns:
            if re.search(pattern, context):
                return False
                
        return True
    
    def estimate_savings(self, text: str, aggressiveness: float = 0.5) -> Dict[str, int]:
        """Estima economia potencial sem aplicar as mudanças."""
        _, replacements = self.apply_abbreviations(text, aggressiveness, preserve_context=False)
        
        total_savings = sum(r.savings for r in replacements)
        
        return {
            'original_length': len(text),
            'estimated_savings': total_savings,
            'estimated_final_length': len(text) - total_savings,
            'opportunities_found': len(replacements),
            'savings_percentage': round((total_savings / len(text)) * 100, 2) if text else 0
        }
