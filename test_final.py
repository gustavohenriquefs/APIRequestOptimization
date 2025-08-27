"""Teste final do exemplo do usuário"""
from src.config.settings import TestingConfig
from src.services.optimization_service import OptimizationService

config = TestingConfig()
service = OptimizationService(config)

# Teste com o exemplo exato do usuário
text = 'Criar imagem de viralata    correndo no ceara durante o meio dia com corre 4.'

request_config = {
    'preset': 'moderate',
    'translate_to_english': False,
    'language': 'pt',
    'stop_word_removal': 0.3,
    'remove_accents': True,
    'word_compression': 0.2,
    'min_word_length': 3,
    'remove_punctuation': False
}

print('=== RESULTADO FINAL ===')
print('Texto original:')
print(f'  "{text}"')
print(f'  Comprimento: {len(text)} caracteres')
print()

result = service.optimize(text, request_config)

print('Texto otimizado:')
print(f'  "{result.optimized_text}"') 
print(f'  Comprimento: {len(result.optimized_text)} caracteres')
print()
print('Estatísticas:')
print(f'  Economia: {result.stats.characters_saved} caracteres')
print(f'  Porcentagem: {result.stats.compression_ratio_percent}%')
print()
print('Verificações:')
print(f'  ✓ Número "4" preservado: {"4" in result.optimized_text}')
print(f'  ✓ Localização abreviada: {"CE" in result.optimized_text}')
print(f'  ✓ Compressão aplicada: {result.stats.compression_ratio_percent > 30}')
print(f'  ✓ Palavras comprimidas: {len([w for w in result.optimized_text.split() if len(w) <= 3 and w.isalpha()])} palavras <= 3 chars')
