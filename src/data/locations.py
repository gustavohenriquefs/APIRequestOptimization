from typing import Dict, List

BRAZILIAN_STATES = [
    'Acre', 'Alagoas', 'Amapá', 'Amazonas', 'Bahia', 'Ceará',
    'Distrito Federal', 'Espírito Santo', 'Goiás', 'Maranhão',
    'Mato Grosso', 'Mato Grosso do Sul', 'Minas Gerais', 'Pará', 
    'Paraíba', 'Paraná', 'Pernambuco', 'Piauí', 'Rio de Janeiro', 
    'Rio Grande do Norte', 'Rio Grande do Sul', 'Rondônia', 
    'Roraima', 'Santa Catarina', 'São Paulo', 'Sergipe', 'Tocantins'
]

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

CONTINENTS = {
    'América do Sul': 'AS',
    'América do Norte': 'AN',
    'Europa': 'EU',
    'Ásia': 'AS',
    'África': 'AF',
    'Oceania': 'OC',
    'Antártida': 'AT'
}

def get_all_locations() -> Dict[str, str]:
    all_locations = {}
    all_locations.update(STATE_ABBREVIATIONS)
    all_locations.update(BRAZILIAN_CAPITALS)
    all_locations.update(COUNTRIES)
    all_locations.update(CONTINENTS)
    return all_locations

def normalize_text(text: str) -> str:
    import unicodedata
    normalized = unicodedata.normalize('NFD', text.lower())
    return ''.join(c for c in normalized if unicodedata.category(c) != 'Mn')

def find_location_match(text: str) -> str:
    all_locations = get_all_locations()
    text_normalized = normalize_text(text)
    
    if text in all_locations:
        return all_locations[text]
    
    for location, abbrev in all_locations.items():
        if normalize_text(location) == text_normalized:
            return abbrev
    
    return None

def is_known_location(text: str) -> bool:
    match = find_location_match(text)
    return match is not None

LOCATION_VARIATIONS = {
    'ceara': 'CE',
    'Ceara': 'CE', 
    'ceará': 'CE',
    'Ceará': 'CE',
    
    'sao paulo': 'SP',
    'são paulo': 'SP',
    'Sao Paulo': 'SP',
    
    'rio': 'RJ',
    'Rio': 'RJ',
    'rio de janeiro': 'RJ',
    
    'brasilia': 'BSB',
    'Brasilia': 'BSB',
    'salvador': 'SSA',
    'Salvador': 'SSA',
    'fortaleza': 'FOR',
    'Fortaleza': 'FOR',
}
