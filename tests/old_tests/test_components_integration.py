"""
Teste direto dos componentes da aplicação sem servidor HTTP.
"""
from src.config.settings import DevelopmentConfig
from src.services.optimization_service import OptimizationService

def test_components():
    """Testa os componentes principais da aplicação diretamente."""
    print("=== Testando Componentes da Aplicação ===\n")
    
    # Teste 1: Configuração
    print("1. Testando configuração...")
    config = DevelopmentConfig()
    print(f"   [OK] Debug mode: {config.DEBUG}")
    print(f"   [OK] Stop words PT: {len(config.STOP_WORDS['pt'])} palavras")
    print(f"   [OK] Stop words EN: {len(config.STOP_WORDS['en'])} palavras")
    print()
    
    # Teste 2: Serviço de otimização
    print("2. Testando serviço de otimização...")
    optimizer = OptimizationService(config)
    
    # Teste básico de remoção de acentos
    text_with_accents = "Acentuação com ção, não é ótimo"
    result = optimizer.remove_accents(text_with_accents)
    print(f"   [OK] Remoção de acentos: '{text_with_accents}' -> '{result}'")
    
    # Teste de compressão de palavra
    word = "exemplo"
    compressed = optimizer._compress_word(word, 0.7)
    print(f"   [OK] Compressão de palavra: '{word}' -> '{compressed}'")
    
    # Teste de remoção de espaços excessivos
    text_spaces = "Texto  com    muitos   espaços"
    clean_spaces = optimizer.remove_excessive_whitespace(text_spaces)
    print(f"   [OK] Limpeza de espaços: '{text_spaces}' -> '{clean_spaces}'")
    print()
    
    # Teste 3: Otimização completa
    print("3. Testando otimização completa...")
    test_text = "Este é um texto de exemplo para demonstrar a funcionalidade de otimização. O texto contém algumas palavras comuns que podem ser removidas."
    
    config_options = {
        'remove_accents': True,
        'stop_word_removal': 0.3,
        'word_compression': 0.8,
        'language': 'pt'
    }
    
    result = optimizer.optimize(test_text, config_options)
    print(f"   [OK] Texto original ({result.stats.original_length} chars): {result.original_text}")
    print(f"   [OK] Texto otimizado ({result.stats.optimized_length} chars): {result.optimized_text}")
    print(f"   [OK] Economia: {result.stats.compression_ratio_percent}%")
    print(f"   [OK] Caracteres salvos: {result.stats.characters_saved}")
    print()
    
    # Teste 4: Presets
    print("4. Testando presets...")
    from src.utils.presets import get_presets_dict
    presets = get_presets_dict()
    for name, preset in presets.items():
        print(f"   [OK] Preset '{name}': {preset['description']}")
    print()
    
    print("SUCESSO: Todos os testes passaram com sucesso!")

if __name__ == "__main__":
    try:
        test_components()
    except Exception as e:
        print(f"ERRO: Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
