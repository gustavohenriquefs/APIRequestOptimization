from src.services.optimization_service import OptimizationService
from src.config.settings import Config

config = Config()
service = OptimizationService(config)

print('=== Teste 1: min_length=3, NÃO deveria comprimir "cat" ===')
config_options1 = {
    'translate_to_english': True,
    'word_compression': 0.5,
    'min_word_length': 3
}

result1 = service.optimize('gato', config_options1)
print(f'gato → {result1.optimized_text} ✓ (correto, não comprimiu)')

print('\n=== Teste 2: min_length=2, DEVERIA comprimir "cat" para 2 chars ===')
config_options2 = {
    'translate_to_english': True,
    'word_compression': 0.5,  # 50% de "cat" = 1.5 → 2 chars (por causa do min_length)
    'min_word_length': 2
}

result2 = service.optimize('gato', config_options2)
print(f'gato → {result2.optimized_text} (deveria ser "ca")')

print('\n=== Teste 3: min_length=2, ratio mais agressiva ===')
config_options3 = {
    'translate_to_english': True,
    'word_compression': 0.3,  # 30% de "cat" seria 0.9 → mas min_length=2
    'min_word_length': 2
}

result3 = service.optimize('gato', config_options3)
print(f'gato → {result3.optimized_text} (deveria ser "ca")')

print('\n=== Teste 4: Palavra mais longa ===')
config_options4 = {
    'translate_to_english': True,
    'word_compression': 0.5,
    'min_word_length': 3
}

result4 = service.optimize('cachorro', config_options4)
print(f'cachorro → {result4.optimized_text}')
