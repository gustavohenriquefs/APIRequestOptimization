"""
Teste do Flask app usando o test client interno.
"""
import json
from src.app import create_app

def test_flask_app():
    """Testa os endpoints da aplicação Flask usando o test client."""
    print("=== Testando Flask App com Test Client ===\n")
    
    app = create_app('testing')
    
    with app.test_client() as client:
        # Teste 1: Health Check
        print("1. Testando Health Check...")
        response = client.get('/health')
        print(f"   Status Code: {response.status_code}")
        data = json.loads(response.data)
        print(f"   Response: {data}")
        assert response.status_code == 200
        assert data['status'] == 'healthy'
        print("   [OK] Health check passou!\n")
        
        # Teste 2: Presets
        print("2. Testando Presets...")
        response = client.get('/presets')
        print(f"   Status Code: {response.status_code}")
        data = json.loads(response.data)
        print(f"   Presets encontrados: {list(data.keys())}")
        assert response.status_code == 200
        assert 'conservative' in data
        assert 'moderate' in data
        print("   [OK] Presets funcionando!\n")
        
        # Teste 3: Otimização básica
        print("3. Testando Otimização...")
        payload = {
            "text": "Este é um texto de exemplo para testar a API de otimização.",
            "config": {
                "remove_accents": True,
                "stop_word_removal": 0.2,
                "word_compression": 0.8
            }
        }
        
        response = client.post('/optimize', 
                             data=json.dumps(payload),
                             content_type='application/json')
        
        print(f"   Status Code: {response.status_code}")
        data = json.loads(response.data)
        
        if response.status_code == 200:
            print(f"   Texto original: {data['original_text']}")
            print(f"   Texto otimizado: {data['optimized_text']}")
            print(f"   Economia: {data['stats']['compression_ratio_percent']}%")
            print("   [OK] Otimização funcionando!\n")
        else:
            print(f"   Erro: {data}")
            
        assert response.status_code == 200
        
        # Teste 4: Validação de erro
        print("4. Testando validação de erro...")
        invalid_payload = {"invalid": "data"}
        
        response = client.post('/optimize',
                             data=json.dumps(invalid_payload),
                             content_type='application/json')
        
        print(f"   Status Code: {response.status_code}")
        data = json.loads(response.data)
        print(f"   Mensagem de erro: {data['error']}")
        assert response.status_code == 400
        print("   [OK] Validação de erro funcionando!\n")
        
    print("SUCESSO: Todos os testes do Flask app passaram!")

if __name__ == "__main__":
    try:
        test_flask_app()
    except Exception as e:
        print(f"ERRO: Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
