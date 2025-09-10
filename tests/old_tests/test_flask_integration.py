import json
from src.app import create_api_app

def test_flask_app():
    print("=== Testando Flask App com Test Client ===\n")
    
    app = create_api_app()
    
    with app.test_client() as client:
        print("1. Testando Health Check...")
        response = client.get('/api/v1/system/health')
        print(f"   Status Code: {response.status_code}")
        data = json.loads(response.data)
        print(f"   Response: {data}")
        assert response.status_code == 200
        assert data['status'] == 'healthy'
        print("   [OK] Health check passou!\n")
        
        print("2. Testando Presets...")
        response = client.get('/api/v1/config/presets')
        print(f"   Status Code: {response.status_code}")
        data = json.loads(response.data)
        print(f"   Presets encontrados: {list(data.keys())}")
        assert response.status_code == 200
        assert 'conservative' in data
        assert 'moderate' in data
        print("   [OK] Presets funcionando!\n")
        
        print("3. Testando OtimizaÃ§Ã£o...")
        payload = {
            "text": "Este Ã© um texto de exemplo para testar a API de otimizaÃ§Ã£o.",
            "remove_accents": True,
            "stop_word_removal": 0.2,
            "word_compression": 0.8
        }
        
        response = client.post('/api/v1/optimization/optimize', 
                             data=json.dumps(payload),
                             content_type='application/json')
        
        print(f"   Status Code: {response.status_code}")
        data = json.loads(response.data)
        
        if response.status_code == 200:
            print(f"   Texto original: {data['original_text']}")
            print(f"   Texto otimizado: {data['optimized_text']}")
            print(f"   Economia: {data['stats']['compression_ratio_percent']}%")
            print("   [OK] OtimizaÃ§Ã£o funcionando!\n")
        else:
            print(f"   Erro: {data}")
            
        assert response.status_code == 200
        
        print("4. Testando validaÃ§Ã£o de erro...")
        invalid_payload = {"invalid": "data"}
        
        response = client.post('/api/v1/optimization/optimize',
                             data=json.dumps(invalid_payload),
                             content_type='application/json')
        
        print(f"   Status Code: {response.status_code}")
        assert response.status_code == 400
        print("   [OK] ValidaÃ§Ã£o de erro funcionando!\n")
        
    print("SUCESSO: Todos os testes do Flask app passaram!")

if __name__ == "__main__":
    try:
        test_flask_app()
    except Exception as e:
        print(f"ERRO: Erro durante os testes: {e}")
        import traceback
        traceback.print_exc()
