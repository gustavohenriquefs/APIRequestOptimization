"""
Configurações da aplicação.
"""
import string


class Config:
    """Configurações da aplicação."""
    
    # URLs das APIs de tradução
    MYMEMORY_API_URL = "https://api.mymemory.translated.net/get"
    LIBRETRANSLATE_API_URL = "https://libretranslate.de/translate"
    
    # Timeout padrão para requisições externas
    REQUESTS_TIMEOUT = 10
    
    # Limite de caracteres para as APIs de tradução para evitar erros
    TRANSLATION_CHAR_LIMIT = 500

    # Palavras comuns (stop words) que podem ser removidas
    # Em uma aplicação maior, isso poderia vir de um arquivo JSON/YAML
    STOP_WORDS = {
        'pt': {
            'o', 'a', 'os', 'as', 'um', 'uma', 'uns', 'umas', 'de', 'do', 'da', 'dos', 'das', 
            'em', 'no', 'na', 'nos', 'nas', 'para', 'por', 'com', 'sem', 'que', 'e', 'ou',
            'mas', 'então', 'muito', 'mais', 'menos', 'bem', 'mal', 'já', 'ainda', 'sempre'
        },
        'en': {
            'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with',
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 'after',
            'above', 'below', 'between', 'among', 'is', 'are', 'was', 'were', 'be', 'been',
            'being', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
            'should', 'may', 'might', 'must', 'shall', 'can', 'very', 'quite', 'rather'
        }
    }

    # Caracteres de pontuação que podem ser removidos
    REMOVABLE_CHARS = set(string.punctuation)


class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurações para ambiente de produção."""
    DEBUG = False


class TestingConfig(Config):
    """Configurações para ambiente de teste."""
    TESTING = True
    DEBUG = True


# Mapeamento de configurações por ambiente
config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
