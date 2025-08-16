"""
Testes para o serviço de otimização.
"""
import pytest
from src.config.settings import TestingConfig
from src.services.optimization_service import OptimizationService


class TestOptimizationService:
    """Testes para o OptimizationService."""

    @pytest.fixture
    def optimization_service(self):
        """Fixture que cria uma instância do serviço de otimização."""
        config = TestingConfig()
        return OptimizationService(config)

    def test_remove_accents(self):
        """Testa a remoção de acentos."""
        text = "Acentuação com ção, não e ótimo"
        expected = "Acentuacao com cao, nao e otimo"
        result = OptimizationService.remove_accents(text)
        assert result == expected

    def test_remove_excessive_whitespace(self):
        """Testa a remoção de espaços excessivos."""
        text = "Texto  com    muitos   espaços"
        expected = "Texto com muitos espaços"
        result = OptimizationService.remove_excessive_whitespace(text)
        assert result == expected

    def test_compress_word(self):
        """Testa a compressão de palavras."""
        word = "exemplo"
        result = OptimizationService._compress_word(word, 0.7)
        assert len(result) < len(word)
        assert result.startswith('e')
        assert result.endswith('o')

    def test_optimize_basic(self, optimization_service):
        """Testa a otimização básica sem configurações especiais."""
        text = "Este é um texto de exemplo para otimização."
        config = {}
        result = optimization_service.optimize(text, config)
        
        assert result.original_text == text
        assert result.stats.original_length == len(text)
        assert result.stats.optimized_length > 0
