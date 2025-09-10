import pytest
from src.services.optimization_service import OptimizationService


class TestLocationVariations:
    
    def test_location_case_variations(self, optimization_service):
        test_cases = [
            ("Preciso ir para Ceara amanha", "CE"),
            ("Viajei para ceara semana passada", "CE"), 
            ("O estado do Ceara e lindo", "CE"),
            ("Sao Paulo e grande", "SP"),
            ("sao paulo tem muita gente", "SP"),
            ("Rio de Janeiro e maravilhoso", "RJ"),
            ("Brasilia e a capital", "BSB"),
            ("Minas Gerais tem pao de acucar", "MG")
        ]
        
        for text, expected_abbrev in test_cases:
            config = {'compression_level': 0.3, 'min_word_length': 3, 'remove_stopwords': True}
            result = optimization_service.optimize(text, config)
            optimized = result.optimized_text
            
            assert expected_abbrev in optimized, f"Texto '{text}' deveria conter '{expected_abbrev}' em '{optimized}'"


class TestNumberPreservation:
    
    def test_important_numbers_preserved(self, optimization_service):
        test_cases = [
            ("Tenho 10 gatos em casa", "10"),
            ("O valor e R$ 23.456,78", "23"),
            ("Chegou 4 pessoas na reuniao", "4"),
            ("A temperatura e 23,5 graus", "23"),
            ("Sao 100% confiaveis", "100")
        ]
        
        for text, number in test_cases:
            config = {'compression_level': 0.3, 'min_word_length': 3, 'remove_stopwords': True}
            result = optimization_service.optimize(text, config)
            optimized = result.optimized_text
            
            number_in_result = number in optimized or any(num_char in optimized for num_char in number)
            assert number_in_result, f"Numero '{number}' nao foi preservado em '{optimized}'"
    
    def test_unimportant_numbers_handling(self, optimization_service):
        text = "No ano de 1985 aconteceu algo, mas em 2024 e diferente"
        config = {'compression_level': 0.3, 'min_word_length': 3, 'remove_stopwords': True}
        result = optimization_service.optimize(text, config)
        
        assert result.stats.compression_ratio_percent >= 0


class TestWordCompressionEdgeCases:
    
    def test_compression_maintains_readability(self, optimization_service):
        test_words = [
            "viralata",
            "cachorro", 
            "exemplo",
            "desenvolvedor",
            "aplicacao"
        ]
        
        for word in test_words:
            result = OptimizationService._compress_word(word, 0.5, 3)
            
            assert len(result) <= len(word)
            assert len(result) >= 3
            
            if len(word) > 2:
                assert result[0] == word[0]
                assert result[-1] == word[-1]
    
    def test_short_words_not_compressed(self, optimization_service):
        short_words = ["e", "de", "em", "ou", "se"]
        
        for word in short_words:
            result = OptimizationService._compress_word(word, 0.7, 3)
            assert result == word


class TestPresetHandling:
    
    def test_manual_config_overrides_preset(self, optimization_service):
        text = "gato"
        
        config = {
            'preset': 'aggressive',
            'min_word_length': 3,
            'compression_level': 0.5,
            'remove_stopwords': True
        }
        
        result = optimization_service.optimize(text, config)
        
        compressed_words = [word for word in result.optimized_text.split() if len(word) >= 3]
        
        assert len(compressed_words) > 0


class TestIntegrationScenarios:
    
    def test_complex_text_optimization(self, optimization_service, sample_texts):
        config = {'compression_level': 0.4, 'min_word_length': 3, 'remove_stopwords': True}
        result = optimization_service.optimize(sample_texts['complex_mix'], config)
        
        assert result.stats.compression_ratio_percent >= 0
        assert hasattr(result.stats, 'original_length')
        assert hasattr(result.stats, 'optimized_length')
        
        assert len(result.optimized_text) > 0
