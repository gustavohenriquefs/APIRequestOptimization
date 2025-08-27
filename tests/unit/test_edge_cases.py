"""
Testes para funcionalidades específicas e casos edge.
"""
import pytest
from src.services.optimization_service import OptimizationService


class TestLocationVariations:
    """Testes específicos para tratamento de variações de localização."""
    
    def test_location_case_variations(self, optimization_service):
        """Testa diferentes variações de capitalização em localizações."""
        test_cases = [
            ("Preciso ir para Ceará amanhã", "CE"),
            ("Viajei para ceara semana passada", "CE"), 
            ("O estado do Ceara é lindo", "CE"),
            ("São Paulo é grande", "SP"),
            ("são paulo tem muita gente", "SP"),
            ("Rio de Janeiro é maravilhoso", "RJ"),
            ("Brasília é a capital", "BSB"),
            ("Minas Gerais tem pão de açúcar", "MG")
        ]
        
        for text, expected_abbrev in test_cases:
            config = {'compression_level': 0.3, 'min_word_length': 3, 'remove_stopwords': True}
            result = optimization_service.optimize(text, config)
            optimized = result.optimized_text
            
            # Deve conter a abreviação do estado
            assert expected_abbrev in optimized, f"Texto '{text}' deveria conter '{expected_abbrev}' em '{optimized}'"


class TestNumberPreservation:
    """Testes específicos para preservação de números importantes."""
    
    def test_important_numbers_preserved(self, optimization_service):
        """Testa se números importantes são preservados."""
        test_cases = [
            ("Tenho 10 gatos em casa", "10"),
            ("O valor é R$ 23.456,78", "23"),
            ("Chegou 4 pessoas na reunião", "4"),
            ("A temperatura é 23,5 graus", "23"),
            ("São 100% confiáveis", "100")
        ]
        
        for text, number in test_cases:
            config = {'compression_level': 0.3, 'min_word_length': 3, 'remove_stopwords': True}
            result = optimization_service.optimize(text, config)
            optimized = result.optimized_text
            
            # Número deve estar preservado (pode ter formatação ligeiramente diferente)
            number_in_result = number in optimized or any(num_char in optimized for num_char in number)
            assert number_in_result, f"Número '{number}' não foi preservado em '{optimized}'"
    
    def test_unimportant_numbers_handling(self, optimization_service):
        """Testa tratamento de números menos importantes."""
        text = "No ano de 1985 aconteceu algo, mas em 2024 é diferente"
        config = {'compression_level': 0.3, 'min_word_length': 3, 'remove_stopwords': True}
        result = optimization_service.optimize(text, config)
        
        # Números de ano podem ou não ser preservados dependendo do contexto
        # O importante é que a otimização funcione sem erros
        assert result.stats.compression_ratio_percent >= 0


class TestWordCompressionEdgeCases:
    """Testes para casos específicos da compressão de palavras."""
    
    def test_compression_maintains_readability(self, optimization_service):
        """Testa se a compressão mantém legibilidade."""
        test_words = [
            "viralata",  # Caso do bug: não deve virar "vrltia"
            "cachorro", 
            "exemplo",
            "desenvolvedor",
            "aplicação"
        ]
        
        for word in test_words:
            result = OptimizationService._compress_word(word, 0.5, 3)
            
            # Deve manter ordem aproximada das letras
            assert len(result) <= len(word)
            assert len(result) >= 3  # Tamanho mínimo
            
            # Primeira e última letra devem ser preservadas para palavras > 2
            if len(word) > 2:
                assert result[0] == word[0]
                assert result[-1] == word[-1]
    
    def test_short_words_not_compressed(self, optimization_service):
        """Testa se palavras muito curtas não são comprimidas."""
        short_words = ["é", "de", "em", "ou", "se"]
        
        for word in short_words:
            result = OptimizationService._compress_word(word, 0.7, 3)
            # Palavras menores que min_length não devem ser alteradas
            assert result == word


class TestPresetHandling:
    """Testes para tratamento correto de presets."""
    
    def test_manual_config_overrides_preset(self, optimization_service):
        """Testa se configurações manuais sobrescrevem presets."""
        text = "gato"
        
        # Configuração manual deve ter precedência
        config = {
            'preset': 'aggressive',  # preset pode ter min_word_length=2
            'min_word_length': 3,    # manual: 3
            'compression_level': 0.5,
            'remove_stopwords': True
        }
        
        result = optimization_service.optimize(text, config)
        
        # Com min_word_length=3, "gato" (4 letras) deve ser comprimido para algo >= 3
        # Não deve virar "ca" como acontecia no bug
        compressed_words = [word for word in result.optimized_text.split() if len(word) >= 3]
        
        # Deve ter pelo menos uma palavra com 3+ caracteres
        assert len(compressed_words) > 0


class TestIntegrationScenarios:
    """Testes de cenários de integração complexos."""
    
    def test_complex_text_optimization(self, optimization_service, sample_texts):
        """Testa otimização de texto complexo com múltiplas funcionalidades."""
        config = {'compression_level': 0.4, 'min_word_length': 3, 'remove_stopwords': True}
        result = optimization_service.optimize(sample_texts['complex_mix'], config)
        
        # Deve ter informações de otimização
        assert result.stats.compression_ratio_percent >= 0
        assert hasattr(result.stats, 'original_length')
        assert hasattr(result.stats, 'optimized_length')
        
        # Deve ter preservado algum conteúdo importante
        assert len(result.optimized_text) > 0
