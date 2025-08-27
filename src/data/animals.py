"""
Dados de animais e natureza para preservação durante otimização.
"""
from typing import Dict, List, Set

# Animais domésticos
DOMESTIC_ANIMALS = {
    'gato': 'cat',
    'cachorro': 'dog',
    'cão': 'dog',
    'pássaro': 'bird',
    'peixe': 'fish',
    'cavalo': 'horse',
    'vaca': 'cow',
    'porco': 'pig',
    'ovelha': 'sheep',
    'cabra': 'goat',
    'coelho': 'rabbit',
    'hamster': 'hamster',
    'rato': 'rat',
    'galinha': 'chicken',
    'pato': 'duck',
    'ganso': 'goose'
}

# Animais selvagens
WILD_ANIMALS = {
    'leão': 'lion',
    'tigre': 'tiger',
    'elefante': 'elephant',
    'girafa': 'giraffe',
    'zebra': 'zebra',
    'macaco': 'monkey',
    'urso': 'bear',
    'lobo': 'wolf',
    'raposa': 'fox',
    'veado': 'deer',
    'águia': 'eagle',
    'falcão': 'hawk',
    'coruja': 'owl',
    'cobra': 'snake',
    'jacaré': 'alligator',
    'tubarão': 'shark',
    'baleia': 'whale',
    'golfinho': 'dolphin'
}

# Insetos
INSECTS = {
    'abelha': 'bee',
    'borboleta': 'butterfly',
    'formiga': 'ant',
    'mosca': 'fly',
    'mosquito': 'mosquito',
    'aranha': 'spider',
    'barata': 'cockroach',
    'grilo': 'cricket',
    'libélula': 'dragonfly'
}

# Animais aquáticos
AQUATIC_ANIMALS = {
    'peixe': 'fish',
    'tubarão': 'shark',
    'baleia': 'whale',
    'golfinho': 'dolphin',
    'polvo': 'octopus',
    'lula': 'squid',
    'caranguejo': 'crab',
    'camarão': 'shrimp',
    'tartaruga': 'turtle',
    'foca': 'seal'
}

# Plantas e vegetação
PLANTS = {
    'árvore': 'tree',
    'flor': 'flower',
    'rosa': 'rose',
    'grama': 'grass',
    'folha': 'leaf',
    'galho': 'branch',
    'raiz': 'root',
    'semente': 'seed',
    'fruto': 'fruit',
    'planta': 'plant'
}

def get_all_animals() -> Dict[str, str]:
    """Retorna todos os animais mapeados."""
    all_animals = {}
    all_animals.update(DOMESTIC_ANIMALS)
    all_animals.update(WILD_ANIMALS)
    all_animals.update(INSECTS)
    all_animals.update(AQUATIC_ANIMALS)
    return all_animals

def get_all_nature() -> Dict[str, str]:
    """Retorna todos os elementos da natureza."""
    all_nature = {}
    all_nature.update(get_all_animals())
    all_nature.update(PLANTS)
    return all_nature

def is_animal(text: str) -> bool:
    """Verifica se o texto é um animal conhecido."""
    animals = get_all_animals()
    text_lower = text.lower().rstrip('s')  # Remove plural
    return text_lower in animals or text_lower in animals.values()

def is_nature_element(text: str) -> bool:
    """Verifica se o texto é um elemento da natureza."""
    nature = get_all_nature()
    text_lower = text.lower().rstrip('s')  # Remove plural
    return text_lower in nature or text_lower in nature.values()

# Categorias para preservação diferenciada
PRESERVATION_CATEGORIES = {
    'high_preserve': set(DOMESTIC_ANIMALS.keys()) | set(WILD_ANIMALS.keys()),
    'medium_preserve': set(INSECTS.keys()) | set(AQUATIC_ANIMALS.keys()),
    'low_preserve': set(PLANTS.keys())
}
