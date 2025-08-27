"""
Fixtures compartilhadas para todos os testes.
"""
import pytest
from src.app import create_api_app
from src.config.settings import TestingConfig
from src.services.optimization_service import OptimizationService


@pytest.fixture
def app():
    """Fixture que cria a aplicação Flask para testes."""
    app = create_api_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Fixture que cria um cliente de teste."""
    return app.test_client()


@pytest.fixture
def config():
    """Fixture que cria uma configuração de teste."""
    return TestingConfig()


@pytest.fixture
def optimization_service(config):
    """Fixture que cria uma instância do serviço de otimização."""
    return OptimizationService(config)


@pytest.fixture
def sample_texts():
    """Fixture com textos de exemplo para testes."""
    return {
        'simple': "Este é um texto simples para otimização.",
        'with_accents': "Acentuação com ção, não e ótimo texto com muitos acentos.",
        'with_numbers': "O projeto tem 10 desenvolvedores e custa R$ 23.456,78 reais.",
        'with_locations': "Preciso ir para Ceará e depois para São Paulo.",
        'with_animals': "O gato viralata subiu na árvore do cachorro labrador.",
        'with_technology': "A aplicação usa JavaScript, Python e banco de dados PostgreSQL.",
        'complex_mix': "Desenvolvendo aplicação em Python para 15 empresas no Ceará com tecnologia moderna.",
        'long_text': "Este é um texto muito longo que precisa ser otimizado para reduzir custos de API do ChatGPT. O texto contém várias informações importantes que devem ser preservadas durante o processo de otimização, incluindo números importantes como 42 e localização como São Paulo."
    }


@pytest.fixture
def preset_configs():
    """Fixture com configurações de presets para testes."""
    return {
        'basic': {
            'remove_stopwords': True,
            'compression_level': 0.3,
            'min_word_length': 3
        },
        'aggressive': {
            'remove_stopwords': True,
            'compression_level': 0.7,
            'min_word_length': 2
        },
        'conservative': {
            'remove_stopwords': False,
            'compression_level': 0.1,
            'min_word_length': 4
        }
    }
