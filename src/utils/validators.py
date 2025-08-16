"""
Utilitários para validação de dados.
"""
from typing import Dict, Any, Optional


def validate_request_data(data: Dict[str, Any]) -> Optional[str]:
    """
    Valida os dados recebidos na requisição.
    Retorna uma mensagem de erro ou None se os dados forem válidos.
    """
    if not data or 'text' not in data:
        return 'Campo "text" é obrigatório no corpo da requisição.'
    
    config = data.get('config', {})
    
    wc = config.get('word_compression')
    if wc is not None and not (0 <= wc <= 1):
        return 'O valor de "word_compression" deve estar entre 0 e 1.'
        
    swr = config.get('stop_word_removal')
    if swr is not None and not (0 <= swr <= 1):
        return 'O valor de "stop_word_removal" deve estar entre 0 e 1.'
        
    return None
