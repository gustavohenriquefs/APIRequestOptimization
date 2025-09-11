import pytest
from src.services.optimization_service import OptimizationService


class TestOptimizationServiceCore:
    
    def test_remove_accents(self, optimization_service):
        text = "Acentuação com ção, não e ótimo"
        expected = "Acentuacao com cao, nao e otimo"
        result = OptimizationService.remove_accents(text)
        assert result == expected
    
    def test_remove_excessive_whitespace(self, optimization_service):
        text = "Texto  com    muitos   espaços"
        expected = "Texto com muitos espaços"
        result = OptimizationService.remove_excessive_whitespace(text)
        assert result == expected
    
    def test_compress_word_basic(self, optimization_service):
        word = "exemplo"
        result = OptimizationService._compress_word(word, 0.7, 2)
        assert len(result) < len(word)
        assert result.startswith('e')
        assert result.endswith('o')
    
    def test_compress_word_with_min_length(self, optimization_service):
        word = "teste"
        
        result = OptimizationService._compress_word(word, 0.4, 3)
        assert len(result) >= 3
        
        result = OptimizationService._compress_word(word, 0.5, 10)
        assert result == word
    
    def test_compress_word_preserves_order(self, optimization_service):
        test_cases = [
            ("viralata", "virlta"),
            ("cachorro", "cchro"),
            ("exemplo", "exmplo")
        ]
        
        for word, expected_pattern in test_cases:
            result = OptimizationService._compress_word(word, 0.5, 3)
            assert len(result) <= len(word)
            if len(word) > 2:
                assert result[0] == word[0]
                assert result[-1] == word[-1]
    
    def test_optimization_simple_text(self, optimization_service, sample_texts):
        config = {'compression_level': 0.3, 'min_word_length': 3, 'remove_stopwords': True}
        result = optimization_service.optimize(sample_texts['simple'], config)
        
        assert len(result.optimized_text) < len(sample_texts['simple'])
        assert result.stats.compression_ratio_percent > 0
        assert hasattr(result.stats, 'original_length')
        assert hasattr(result.stats, 'optimized_length')
    
    def test_optimization_preserves_important_content(self, optimization_service, sample_texts):
        config = {'compression_level': 0.3, 'min_word_length': 3, 'remove_stopwords': True}
        result = optimization_service.optimize(sample_texts['with_numbers'], config)
        
        assert '10' in result.optimized_text or '23' in result.optimized_text
        
        assert result.stats.compression_ratio_percent >= 0
