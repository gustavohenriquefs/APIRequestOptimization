import re
from typing import Dict, List, Tuple, Optional

IMPORTANT_NUMBER_PATTERNS = [
    r'\b(?:10|20|30|40|50|60|70|80|90|100|1000)\b',
    
    r'\b\d+(?:\.\d+)?\s*(?:por\s*cento|percent)\b',
    
    r'\b(?:[1-9]|[1-9][0-9])\s*anos?\b',
    
    r'\b\d+\s*(?:unidades?|peças?|itens?|vezes?)\b',
    
    r'(?:versão|version|v\.?)\s*\d+(?:\.\d+)*',
    r'(?:capítulo|chapter|cap\.?)\s*\d+',
    r'(?:página|page|p\.?)\s*\d+',
    
    r'\b\d+\.\d+\b',
    
    r'\b\d+[.,]\s*\d+[.,]?\s*\d*',
]

class NumberPreservationService:
    
    def __init__(self):
        self.patterns = [re.compile(pattern, re.IGNORECASE) for pattern in IMPORTANT_NUMBER_PATTERNS]
        self.context_keywords = {
            'financial': ['preço', 'custo', 'valor', 'price', 'cost', 'value', 'real', 'dollar', 'euro'],
            'measurement': ['metros', 'km', 'kg', 'litros', 'meters', 'kilometers', 'kilograms'],
            'temporal': ['anos', 'meses', 'dias', 'horas', 'years', 'months', 'days', 'hours'],
            'version': ['versão', 'version', 'release', 'update'],
            'quantity': ['quantidade', 'total', 'quantity', 'amount']
        }
    
    def is_important_number(self, text: str, position: int = 0, context_window: int = 50) -> Tuple[bool, str]:
        text_clean = text.strip()
        
        if re.search(r'\d', text_clean):
            return True, "contains_digits"
        
        measurement_units = {
            'kg', 'g', 'mg', 'ton', 't',  # peso
            'km', 'm', 'cm', 'mm',        # distância  
            'l', 'ml', 'cl',              # volume
            'h', 'min', 's', 'ms',        # tempo
            'º', '°', 'c',                # temperatura/ângulo
            
            'mb', 'gb', 'tb', 'kb',       # armazenamento
            'hz', 'khz', 'mhz', 'ghz',    # frequência
            'v', 'w', 'kw', 'mw',         # elétrica
            'a', 'ma', 'ka',              # corrente
            
            'r$', 'usd', 'eur', '$',      # moedas
            
            '%', 'pct', 'x', '×',         # operações
        }
        
        text_lower = text_clean.lower().strip('.,!?()[]{}')
        if text_lower in measurement_units:
            return True, 'measurement_unit'
        
        for pattern in self.patterns:
            if pattern.search(text_clean):
                return True, "matched_pattern"
        
        if position > 0:
            start = max(0, position - context_window)
            end = min(len(text), position + context_window)
            context = text[start:end].lower()
            
            for category, keywords in self.context_keywords.items():
                if any(keyword in context for keyword in keywords):
                    return True, f"context_{category}"
        
        return False, "no_importance_indicators"
    
    def extract_important_numbers(self, text: str) -> List[Dict]:
        important_numbers = []
        
        number_pattern = re.compile(r'\b\d+(?:\.\d+)?\b')
        
        for match in number_pattern.finditer(text):
            number_text = match.group()
            is_important, reason = self.is_important_number(text, match.start())
            
            if is_important:
                important_numbers.append({
                    'text': number_text,
                    'position': match.start(),
                    'end': match.end(), 
                    'reason': reason,
                    'preserve': True
                })
        
        return important_numbers
    
    def should_preserve_number(self, number: str, context: str = "") -> bool:
        is_important, _ = self.is_important_number(f"{context} {number}")
        return is_important

CONTEXTUAL_IMPORTANT_NUMBERS = {
    'business': [10, 20, 50, 100, 1000, 5000, 10000],
    'technical': [1, 2, 4, 8, 16, 32, 64, 128, 256, 512, 1024],
    'common': [1, 2, 3, 5, 10, 100, 1000],
    'percentages': [10, 20, 25, 30, 40, 50, 60, 70, 75, 80, 90, 100]
}

def get_number_preservation_rules() -> Dict[str, float]:
    return {
        'financial': 1.0,      # 100% preservação para números financeiros
        'measurement': 0.9,    # 90% preservação para medidas
        'version': 1.0,        # 100% preservação para versões
        'decimal': 0.95,       # 95% preservação para decimais
        'large': 0.8,          # 80% preservação para números grandes
        'small': 0.5,          # 50% preservação para números pequenos
        'contextual': 0.9      # 90% preservação por contexto
    }
