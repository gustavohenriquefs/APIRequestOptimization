"""
Script de exemplo para testar a API de otimização de prompts.
"""
import requests
import json


def test_api():
    """Testa os endpoints da API."""
    base_url = "http://localhost:5000"
    
    print("=== Testando API de Otimização de Prompts ===\n")
    
    # Teste do health check
    print("1. Testando Health Check...")
    response = requests.get(f"{base_url}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {response.json()}\n")
    
    # Teste dos presets
    print("2. Testando Presets...")
    response = requests.get(f"{base_url}/presets")
    print(f"Status: {response.status_code}")
    presets = response.json()
    print("Presets disponíveis:")
    for name, preset in presets.items():
        print(f"  - {name}: {preset['description']}")
    print()
    
    # Teste de otimização básica
    print("3. Testando Otimização Básica...")
    test_text = "Este é um texto de exemplo para demonstrar a funcionalidade de otimização da API. O texto contém algumas palavras comuns que podem ser removidas para reduzir o tamanho."
    
    payload = {
        "text": test_text,
        "config": {
            "remove_accents": True,
            "stop_word_removal": 0.3,
            "word_compression": 0.8
        }
    }
    
    response = requests.post(f"{base_url}/optimize", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Texto original: {result['original_text']}")
        print(f"Texto otimizado: {result['optimized_text']}")
        print(f"Economia: {result['stats']['compression_ratio_percent']}%")
        print(f"Caracteres salvos: {result['stats']['characters_saved']}")
    else:
        print(f"Erro: {response.text}")
    print()
    
    # Teste com preset
    print("4. Testando com Preset 'moderate'...")
    payload = {
        "text": test_text,
        "config": presets['moderate']['config']
    }
    
    response = requests.post(f"{base_url}/optimize", json=payload)
    print(f"Status: {response.status_code}")
    if response.status_code == 200:
        result = response.json()
        print(f"Texto otimizado: {result['optimized_text']}")
        print(f"Economia: {result['stats']['compression_ratio_percent']}%")
    print()


if __name__ == "__main__":
    try:
        test_api()
    except requests.exceptions.ConnectionError:
        print("Erro: Não foi possível conectar à API. Certifique-se de que o servidor está rodando em http://localhost:5000")
    except Exception as e:
        print(f"Erro inesperado: {e}")
