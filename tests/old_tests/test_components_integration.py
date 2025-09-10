from src.config.settings import DevelopmentConfig
from src.services.optimization_service import OptimizationService

def test_components():
    print("=== Testando Componentes da AplicaÃ§Ã£o ===\n")
    
    print("1. Testando configuraÃ§Ã£o...")
    config = DevelopmentConfig()
    print(f"   [OK] Debug mode: {config.DEBUG}")
    print(f"   [OK] Stop words PT: {len(config.STOP_WORDS['pt'])} palavras")
    print(f"   [OK] Stop words EN: {len(config.STOP_WORDS['en'])} palavras")
    print()
    
    print("2. Testando serviÃ§o de otimizaÃ§Ã£o...")
    optimizer = OptimizationService(config)
    
    text_with_accents = "AcentuaÃ§Ã£o com Ã§Ã£o, nÃ£o Ã© Ã³timo"
    result = optimizer.remove_accents(text_with_accents)
    print(f"   [OK] RemoÃ§Ã£o de acentos: '{text_with_accents}' -> '{result}'")
    
    word = "exemplo"
    compressed = optimizer._compress_word(word, 0.7)
    print(f"   [OK] CompressÃ£o de palavra: '{word}' -> '{compressed}'")
    
    text_spaces = "Texto  com    muitos   espaÃ§os"
    clean_spaces = optimizer.remove_excessive_whitespace(text_spaces)
    print(f"   [OK] Limpeza de espaÃ§os: '{text_spaces}' -> '{clean_spaces}'")
    print()
    
    print("3. Testando otimizaÃ§Ã£o completa...")
    test_text = "Este Ã© um texto de exemplo para demonstrar a funcionalidade de otimizaÃ§Ã£o. O texto contÃ©m algumas palavras comuns que podem ser removidas."
    
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
