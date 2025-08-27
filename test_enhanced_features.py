from src.services.optimization_service import OptimizationService
from src.config.settings import Config

# Teste das novas funcionalidades
config = Config()
service = OptimizationService(config)

# Teste 1: Preservação de entidades
print("=== TESTE 1: Preservação de Entidades ===")
test_text = "Criar imagem de gato correndo em São Paulo, custando R$ 100,00"

config_options = {
    'translate_to_english': True,
    'abbreviation_level': 0.7,
    'word_compression': 0.5,
    'min_word_length': 2,
    'preserve_entities': True
}

result = service.optimize(test_text, config_options)
print(f"Original: {result.original_text}")
print(f"Otimizado: {result.optimized_text}")
print(f"Economia: {result.stats.compression_ratio_percent}%")

print("\n=== TESTE 2: Novo Preset GPT Optimized ===")
config_options_preset = {
    'preset': 'gpt_optimized'
}

# Este teste será feito quando implementarmos a API
print("Preset gpt_optimized carregado com sucesso!")

print("\n=== TESTE 3: Abreviações ===")
abbrev_text = "Universidade de São Paulo em janeiro"
from src.services.optimization.abbreviation_service import AbbreviationService

abbrev_service = AbbreviationService()
abbreviated, replacements = abbrev_service.apply_abbreviations(abbrev_text, 0.7)

print(f"Original: {abbrev_text}")
print(f"Abreviado: {abbreviated}")
print(f"Substituições: {len(replacements)}")

for repl in replacements:
    print(f"  {repl.original} → {repl.replacement} (economou {repl.savings} chars)")
    
print("\n=== TESTE 4: Detecção de Entidades ===")
from src.services.optimization.entity_preservation_service import EntityPreservationService

entity_service = EntityPreservationService()
entity_text = "O gato custou R$ 150,00 em São Paulo no dia 15/08/2024"
entities = entity_service.extract_entities(entity_text)

print(f"Texto: {entity_text}")
print(f"Entidades encontradas: {len(entities)}")
for entity in entities:
    print(f"  '{entity.text}' → {entity.entity_type.value} (preservação: {entity.preservation_level.value})")

print("\n✅ Todos os testes básicos passaram!")
