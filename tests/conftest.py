import pytest
from src.app import create_api_app
from src.config.settings import TestingConfig
from src.services.optimization_service import OptimizationService


@pytest.fixture
def app():
    app = create_api_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def config():
    return TestingConfig()


@pytest.fixture
def optimization_service(config):
    return OptimizationService(config)


@pytest.fixture
def sample_texts():
    return {
        'simple': "Este Ã© um texto simples para otimizaÃ§Ã£o.",
        'with_accents': "AcentuaÃ§Ã£o com Ã§Ã£o, nÃ£o e Ã³timo texto com muitos acentos.",
        'with_numbers': "O projeto tem 10 desenvolvedores e custa R$ 23.456,78 reais.",
        'with_locations': "Preciso ir para CearÃ¡ e depois para SÃ£o Paulo.",
        'with_animals': "O gato viralata subiu na Ã¡rvore do cachorro labrador.",
        'with_technology': "A aplicaÃ§Ã£o usa JavaScript, Python e banco de dados PostgreSQL.",
        'complex_mix': "Desenvolvendo aplicaÃ§Ã£o em Python para 15 empresas no CearÃ¡ com tecnologia moderna.",
        'long_text': "Este Ã© um texto muito longo que precisa ser otimizado para reduzir custos de API do ChatGPT. O texto contÃ©m vÃ¡rias informaÃ§Ãµes importantes que devem ser preservadas durante o processo de otimizaÃ§Ã£o, incluindo nÃºmeros importantes como 42 e localizaÃ§Ã£o como SÃ£o Paulo."
    }


@pytest.fixture
def preset_configs():
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
