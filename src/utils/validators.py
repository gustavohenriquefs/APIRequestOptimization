from typing import Dict, Any, Optional


def validate_request_data(data: Dict[str, Any]) -> Optional[str]:
    if not data or 'text' not in data:
        return 'Campo "text" é obrigatório no corpo da requisição.'
    
    config = data.get('config', {})
    
    wc = config.get('word_compression')
    if wc is not None and not (0 <= wc <= 1):
        return 'O valor de "word_compression" deve estar entre 0 e 1.'
        
    swr = config.get('stop_word_removal')
    if swr is not None and not (0 <= swr <= 1):
        return 'O valor de "stop_word_removal" deve estar entre 0 e 1.'
        
    mwl = config.get('min_word_length')
    if mwl is not None and not (isinstance(mwl, int) and mwl >= 1):
        return 'O valor de "min_word_length" deve ser um número inteiro maior ou igual a 1.'
        
    return None
