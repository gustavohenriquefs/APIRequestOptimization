"""
Dados de localização para otimização de textos.
Incluindo estados, países, cidades e suas abreviações.
"""
from typing import Dict, List

# Estados brasileiros completos
BRAZILIAN_STATES = [
    'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará',
    'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão',
    'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 
    'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 
    'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 
    'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
]

# Mapeamento de estados para siglas
STATE_ABBREVIATIONS = {
    'Acre': 'AC',
    'Alagoas': 'AL',
    'Amapá': 'AP',
    'Amazonas': 'AM',
    'Bahia': 'BA',
    'Ceará': 'CE',
    'Distrito Federal': 'DF',
    'Espírito Santo': 'ES',
    'Goiás': 'GO',
    'Maranhão': 'MA',
    'Mato Grosso': 'MT',
    'Mato Grosso do Sul': 'MS',
    'Minas Gerais': 'MG',
    'Pará': 'PA',
    'Paraíba': 'PB',
    'Paraná': 'PR',
    'Pernambuco': 'PE',
    'Piauí': 'PI',
    'Rio de Janeiro': 'RJ',
    'Rio Grande do Norte': 'RN',
    'Rio Grande do Sul': 'RS',
    'Rondônia': 'RO',
    'Roraima': 'RR',
    'Santa Catarina': 'SC',
    'São Paulo': 'SP',
    'Sergipe': 'SE',
    'Tocantins': 'TO'
}

# Capitais brasileiras importantes
BRAZILIAN_CAPITALS = {
    'São Paulo': 'SP',
    'Rio de Janeiro': 'RJ',
    'Brasília': 'BSB',
    'Salvador': 'SSA',
    'Fortaleza': 'FOR',
    'Belo Horizonte': 'BH',
    'Curitiba': 'CWB',
    'Recife': 'REC',
    'Porto Alegre': 'POA',
    'Goiânia': 'GYN',
    'Belém': 'BEL',
    'Manaus': 'MAO',
    'Campinas': 'CGN',
    'Guarulhos': 'GRU'
}

# Países e suas abreviações
COUNTRIES = {
    'Brasil': 'BR',
    'Argentina': 'AR',
    'Chile': 'CL',
    'Uruguai': 'UY',
    'Paraguai': 'PY',
    'Peru': 'PE',
    'Colômbia': 'CO',
    'Venezuela': 'VE',
    'Equador': 'EC',
    'Bolívia': 'BO',
    'Estados Unidos': 'EUA',
    'United States': 'US',
    'Canadá': 'CA',
    'México': 'MX',
    'França': 'FR',
    'Alemanha': 'DE',
    'Espanha': 'ES',
    'Itália': 'IT',
    'Portugal': 'PT',
    'Reino Unido': 'UK',
    'China': 'CN',
    'Japão': 'JP',
    'Coreia do Sul': 'KR',
    'Índia': 'IN',
    'Austrália': 'AU'
}

# Continentes
CONTINENTS = {
    'América do Sul': 'AS',
    'América do Norte': 'AN',
    'Europa': 'EU',
    'Ásia': 'AS',
    'África': 'AF',
    'Oceania': 'OC',
    'Antártida': 'AT'
}

# Função para obter todas as localizações
def get_all_locations() -> Dict[str, str]:
    """Retorna todos os mapeamentos de localização."""
    all_locations = {}
    all_locations.update(STATE_ABBREVIATIONS)
    all_locations.update(BRAZILIAN_CAPITALS)
    all_locations.update(COUNTRIES)
    all_locations.update(CONTINENTS)
    return all_locations

def normalize_text(text: str) -> str:
    """Normaliza texto removendo acentos e convertendo para minúsculas."""
    import unicodedata
    normalized = unicodedata.normalize('NFD', text.lower())
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')

def find_location_match(text: str) -> str:
    """Encontra correspondência de localização considerando variações."""
    all_locations = get_all_locations()
    text_normalized = normalize_text(text)
    
    # Busca exata primeiro
    if text in all_locations:
        return all_locations[text]
    
    # Busca normalizada (sem acentos, case-insensitive)
    for location, abbrev in all_locations.items():
        if normalize_text(location) == text_normalized:
            return abbrev
    
    return None

# Função para verificar se é uma localização conhecida
def is_known_location(text: str) -> bool:
    """Verifica se o texto é uma localização conhecida."""
    match = find_location_match(text)
    return match is not None

# Mapeamentos adicionais com variações comuns
LOCATION_VARIATIONS = {
    # Ceará com suas variações
    'ceara': 'CE',
    'Ceara': 'CE', 
    'ceará': 'CE',
    'Ceará': 'CE',
    
    # São Paulo variações
    'sao paulo': 'SP',
    'são paulo': 'SP',
    'Sao Paulo': 'SP',
    
    # Rio de Janeiro variações  
    'rio': 'RJ',
    'Rio': 'RJ',
    'rio de janeiro': 'RJ',
    
    # Outras variações comuns
    'brasilia': 'BSB',
    'Brasilia': 'BSB',
    'salvador': 'SSA',
    'Salvador': 'SSA',
    'fortaleza': 'FOR',
    'Fortaleza': 'FOR',
}
