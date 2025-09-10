import pytest
from src.config.settings import TestingConfig
from src.services.optimization_service import OptimizationService


class TestOptimizationService:

    @pytest.fixture
    def optimization_service(self):
        config = TestingConfig()
        return OptimizationService(config)

    def test_remove_accents(self):
        text = "Acentuacao com cao, nao e otimo"
        expected = "Acentuacao com cao, nao e otimo"
        result = OptimizationService.remove_accents(text)
        assert result == expected

    def test_remove_excessive_whitespace(self):
        text = "Texto  com    muitos   espaÃ§os"
        expected = "Texto com muitos espaÃ§os"
        result = OptimizationService.remove_excessive_whitespace(text)
        assert result == expected

    def test_compress_word(self):
        word = "exemplo"
        result = OptimizationService._compress_word(word, 0.7, 2)
        assert len(result) < len(word)
        assert result.startswith('e')
        assert result.endswith('o')

    def test_compress_word_with_min_length(self):
        word = "teste"
        
        result = OptimizationService._compress_word(word, 0.4, 3)
        assert len(result) >= 3
        
        result = OptimizationService._compress_word(word, 0.5, 10)
        assert result == word

    def test_optimize_basic(self, optimization_service):
        text = "Este Ã© um texto de exemplo para otimizaÃ§Ã£o."
        config = {}
        result = optimization_service.optimize(text, config)
        
        assert result.original_text == text
        assert result.stats.original_length == len(text)
        assert result.stats.optimized_length > 0
