"""
Testes de integração para a API Flask.
"""
import json
import pytest


class TestFlaskAPI:
    """Testes de integração para endpoints da API Flask."""
    
    def test_health_endpoint(self, client):
        """Testa o endpoint de health check."""
        response = client.get('/api/v1/system/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
    
    def test_presets_endpoint(self, client):
        """Testa o endpoint de presets."""
        response = client.get('/api/v1/config/presets')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Deve retornar os presets configurados
        expected_presets = ['aggressive', 'conservative', 'gpt_optimized', 'business_context', 'technical_context']
        for preset in expected_presets:
            assert preset in data
        
        # Cada preset deve ter as configurações necessárias
        for preset_name, preset_config in data.items():
            assert 'config' in preset_config
            assert 'description' in preset_config
    
    def test_optimization_endpoint_basic(self, client, sample_texts):
        """Testa o endpoint de otimização com configuração básica."""
        payload = {
            'text': sample_texts['simple'],
            'config': {
                'stop_word_removal': 0.3,
                'word_compression': 0.7,
                'min_word_length': 3
            }
        }
        
        response = client.post('/api/v1/optimization/optimize', 
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Deve retornar estrutura esperada
        assert 'optimized_text' in data
        assert 'original_text' in data
        assert 'stats' in data
        assert 'config_used' in data
        
        # Texto deve ser otimizado
        assert len(data['optimized_text']) <= len(sample_texts['simple'])
    
    def test_optimization_endpoint_with_manual_config(self, client, sample_texts):
        """Testa o endpoint de otimização com configurações manuais."""
        payload = {
            'text': sample_texts['with_accents'],
            'config': {
                'remove_accents': True,
                'stop_word_removal': 0.5,
                'word_compression': 0.6,
                'min_word_length': 3
            }
        }
        
        response = client.post('/api/v1/optimization/optimize',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Deve ter aplicado as configurações manuais
        assert len(data['optimized_text']) > 0
        
        # Deve ter informações sobre estatísticas
        stats = data['stats']
        assert 'compression_ratio_percent' in stats or 'original_length' in stats
    
    def test_optimization_endpoint_validation(self, client):
        """Testa validação do endpoint de otimização."""
        # Teste sem texto (campo obrigatório)
        response = client.post('/api/v1/optimization/optimize',
                             data=json.dumps({}),
                             content_type='application/json')
        # Pode retornar 400 (validação) ou 422 (unprocessable entity)
        assert response.status_code in [400, 422]
        
        # Teste com texto vazio (pode ser aceito dependendo da implementação)
        response = client.post('/api/v1/optimization/optimize',
                             data=json.dumps({'text': ''}),
                             content_type='application/json')
        # API pode aceitar texto vazio e retornar resultado vazio
        assert response.status_code in [200, 400]
    
    def test_swagger_documentation(self, client):
        """Testa se a documentação Swagger está disponível."""
        response = client.get('/docs/')
        assert response.status_code == 200
        
        # Deve conter conteúdo HTML da documentação
        assert b'swagger' in response.data.lower() or b'openapi' in response.data.lower()


class TestFlaskAPIComplexScenarios:
    """Testes de cenários complexos da API."""
    
    def test_optimization_preserves_entities(self, client):
        """Testa se a API preserva entidades importantes."""
        payload = {
            'text': "Desenvolvendo aplicação em Python para 15 empresas no Ceará com JavaScript",
            'config': {
                'stop_word_removal': 0.3,
                'word_compression': 0.6,
                'min_word_length': 3
            }
        }
        
        response = client.post('/api/v1/optimization/optimize',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Deve preservar alguns elementos importantes
        optimized_text = data['optimized_text'].lower()
        # Deve conter pelo menos algumas palavras importantes
        important_found = any(word in optimized_text for word in ['python', 'javascript', '15', 'ceará', 'ce'])
        assert important_found, f"Nenhum elemento importante preservado em: {data['optimized_text']}"
    
    def test_optimization_with_all_features(self, client):
        """Testa otimização com todas as funcionalidades ativas."""
        complex_text = """
        Desenvolvendo uma aplicação web moderna em JavaScript e Python para 25 empresas
        localizadas em São Paulo, Rio de Janeiro e Ceará. O projeto custará R$ 150.000,00
        e será finalizado em 6 meses. A equipe tem 12 desenvolvedores especializados em
        tecnologias como React, Django, PostgreSQL e MongoDB.
        """
        
        payload = {
            'text': complex_text,
            'config': {
                'translate_to_english': False,
                'stop_word_removal': 0.4,
                'remove_accents': True,
                'word_compression': 0.7,
                'min_word_length': 2,
                'remove_punctuation': False
            }
        }
        
        response = client.post('/api/v1/optimization/optimize',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        
        # Deve ter otimizado significativamente
        original_len = len(complex_text)
        optimized_len = len(data['optimized_text'])
        reduction_percent = ((original_len - optimized_len) / original_len) * 100
        
        assert reduction_percent > 10, f"Otimização insuficiente: {reduction_percent:.1f}%"
        assert reduction_percent < 80, f"Otimização muito agressiva: {reduction_percent:.1f}%"
        
        # Deve ter estatísticas
        assert 'stats' in data
        assert data['stats']['original_length'] > 0
