import string


class Config:
    
    MYMEMORY_API_URL = "https://api.mymemory.translated.net/get"
    LIBRETRANSLATE_API_URL = "https://libretranslate.de/translate"
    
    REQUESTS_TIMEOUT = 10
    
    TRANSLATION_CHAR_LIMIT = 500

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

    REMOVABLE_CHARS = set(string.punctuation)


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    DEBUG = True


config_by_name = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig
}
