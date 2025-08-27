from src.services.optimization_service import OptimizationService
from src.config.settings import Config

config = Config()
service = OptimizationService(config)

# Configuração do teste
config_options = {
    'translate_to_english': True,
    'word_compression': 0.5,
    'min_word_length': 3
}

print('=== Testando: gato → traduzir + comprimir (min_len=3) ===')
result = service.optimize('gato', config_options)

print(f'Original: "gato"')
print(f'Resultado: "{result.optimized_text}"')
print(f'Estatísticas: {result.stats.__dict__}')

print('\n=== Testando cada etapa separadamente ===')

# 1. Tradução
translated = service.translation_service.translate_to_english('gato')
print(f'1. Tradução: gato → {translated}')

# 2. Compressão da palavra traduzida
compressed = service._compress_word(translated, 0.5, 3)
print(f'2. Compressão: {translated} → {compressed} (min_len=3)')

print(f'\nPor que o resultado final é "{result.optimized_text}" e não "{compressed}"?')
