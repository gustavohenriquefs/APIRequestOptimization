"""
Testes específicos para funcionalidades melhoradas:
- Variações de localização (ceara/Ceará/Ceara)
- Preservação de números importantes
- Integração com abreviações inteligentes
"""
import pytest
from src.config.settings import TestingConfig
from src.services.optimization_service import OptimizationService


class TestEnhancedFeatures:
    """Testes para funcionalidades melhoradas de otimização."""

    def setup_method(self):
        """Inicializa o serviço de otimização antes de cada teste."""
        config = TestingConfig()
        self.service = OptimizationService(config)
    
    def test_location_variations_handling(self):
        """Testa o tratamento de variações de capitalização/acentuação em localizações."""
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
        
        for original_text, expected_abbrev in test_cases:
            config = {
                'abbreviation_level': 0.8,  # Alto nível para garantir abreviação
                'preserve_entities': True,
                'word_compression': 1.0,  # Sem compressão para focar nas abreviações
                'remove_accents': False,
                'stop_word_removal': 0.0
            }
            
            result = self.service.optimize(original_text, config)
            
            # Verifica se a abreviação da localização aparece no texto otimizado
            assert expected_abbrev in result.optimized_text, \
                f"Esperava '{expected_abbrev}' em '{result.optimized_text}' para '{original_text}'"
    
    def test_number_preservation(self):
        """Testa a preservação de números importantes."""
        test_cases = [
            "Preciso de 10 gatos para o projeto",
            "Temos 4 desenvolvedores na equipe", 
            "O preço é 23.3 reais",
            "Começamos às 15:30 horas",
            "Versão 2.1.4 do software",
            "Ano de 2024 foi importante"
        ]
        
        for text in test_cases:
            config = {
                'word_compression': 0.5,  # Compressão agressiva
                'min_word_length': 2,
                'abbreviation_level': 0.8,
                'preserve_entities': True,
                'remove_accents': False,
                'stop_word_removal': 0.0
            }
            
            result = self.service.optimize(text, config)
            
            # Extrai números do texto original
            import re
            original_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
            optimized_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', result.optimized_text)
            
            # Verifica se números importantes foram preservados
            for number in original_numbers:
                if self.service.abbreviation_service.number_service.is_important_number(number):
                    assert number in optimized_numbers, \
                        f"Número importante '{number}' não foi preservado em '{result.optimized_text}'"
    
    def test_abbreviation_with_context_preservation(self):
        """Testa abreviações inteligentes com preservação de contexto."""
        text = "A universidade brasileira tem problemas com desenvolvimento de tecnologia"
        
        config = {
            'abbreviation_level': 0.7,
            'preserve_entities': True,
            'word_compression': 1.0,
            'remove_accents': False,
            'stop_word_removal': 0.0
        }
        
        result = self.service.optimize(text, config)
        
        # Deve conter algumas abreviações esperadas
        expected_abbreviations = ['univ', 'BR', 'dev', 'tech']
        found_abbreviations = []
        
        for abbrev in expected_abbreviations:
            if abbrev.lower() in result.optimized_text.lower():
                found_abbreviations.append(abbrev)
        
        # Deve ter pelo menos algumas abreviações
        assert len(found_abbreviations) > 0, \
            f"Nenhuma abreviação encontrada em '{result.optimized_text}'"
        
        # Deve ter economizado caracteres
        assert result.stats.characters_saved > 0, \
            "Deveria ter economizado alguns caracteres"
    
    def test_combined_optimizations(self):
        """Testa a combinação de todas as otimizações melhoradas."""
        text = """
        O gato de Ceará precisa de 10 unidades de desenvolvimento 
        para universidade brasileira em São Paulo com tecnologia avançada.
        """
        
        config = {
            'abbreviation_level': 0.8,
            'preserve_entities': True,
            'word_compression': 0.7,
            'min_word_length': 2,
            'remove_accents': False,
            'stop_word_removal': 0.3,
            'remove_punctuation': False,
            'translate_to_english': False
        }
        
        result = self.service.optimize(text.strip(), config)
        
        # Verificações gerais
        assert len(result.optimized_text) < len(text.strip()), \
            "Texto otimizado deveria ser menor que o original"
        
        assert result.stats.compression_ratio_percent > 0, \
            "Deveria ter alguma compressão"
        
        # Números importantes devem ser preservados
        assert "10" in result.optimized_text, \
            "Número '10' deveria ser preservado"
        
        # Localizações devem ser abreviadas
        locations_abbreviated = ("CE" in result.optimized_text or "SP" in result.optimized_text)
        assert locations_abbreviated, \
            "Pelo menos uma localização deveria ser abreviada"
        
        print(f"Original: {text.strip()}")
        print(f"Otimizado: {result.optimized_text}")
        print(f"Economia: {result.stats.compression_ratio_percent}%")
    
    def test_preset_with_enhancements(self):
        """Testa um preset que utiliza as funcionalidades melhoradas."""
        text = "O desenvolvedor de Brasília precisa de 5 computadores para universidade"
        
        # Simula um preset que usa as funcionalidades melhoradas
        config = {
            'abbreviation_level': 0.9,
            'preserve_entities': True,
            'word_compression': 0.6,
            'min_word_length': 3,
            'remove_accents': True,
            'stop_word_removal': 0.4,
            'remove_punctuation': False
        }
        
        result = self.service.optimize(text, config)
        
        # Deve preservar o número
        assert "5" in result.optimized_text
        
        # Deve abreviar localização
        assert "BSB" in result.optimized_text
        
        # Deve ter economia significativa
        assert result.stats.compression_ratio_percent > 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
