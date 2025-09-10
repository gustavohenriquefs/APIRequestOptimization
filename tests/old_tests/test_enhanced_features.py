import pytest
from src.config.settings import TestingConfig
from src.services.optimization_service import OptimizationService


class TestEnhancedFeatures:

    def setup_method(self):
        config = TestingConfig()
        self.service = OptimizationService(config)
    
    def test_location_variations_handling(self):
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
        
        for original_text, expected_abbrev in test_cases:
            config = {
                'abbreviation_level': 0.8,
                'preserve_entities': True,
                'word_compression': 1.0,
                'remove_accents': False,
                'stop_word_removal': 0.0
            }
            
            result = self.service.optimize(original_text, config)
            
            assert expected_abbrev in result.optimized_text, \
                f"Esperava '{expected_abbrev}' em '{result.optimized_text}' para '{original_text}'"
    
    def test_number_preservation(self):
        test_cases = [
            "Preciso de 10 gatos para o projeto",
            "Temos 4 desenvolvedores na equipe", 
            "O preÃ§o Ã© 23.3 reais",
            "ComeÃ§amos Ã s 15:30 horas",
            "VersÃ£o 2.1.4 do software",
            "Ano de 2024 foi importante"
        ]
        
        for text in test_cases:
            config = {
                'word_compression': 0.5,
                'min_word_length': 2,
                'abbreviation_level': 0.8,
                'preserve_entities': True,
                'remove_accents': False,
                'stop_word_removal': 0.0
            }
            
            result = self.service.optimize(text, config)
            
            import re
            original_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', text)
            optimized_numbers = re.findall(r'\b\d+(?:\.\d+)?\b', result.optimized_text)
            
            for number in original_numbers:
                if self.service.abbreviation_service.number_service.is_important_number(number):
                    assert number in optimized_numbers, \
                        f"NÃºmero importante '{number}' nÃ£o foi preservado em '{result.optimized_text}'"
    
    def test_abbreviation_with_context_preservation(self):
        text = "A universidade brasileira tem problemas com desenvolvimento de tecnologia"
        
        config = {
            'abbreviation_level': 0.7,
            'preserve_entities': True,
            'word_compression': 1.0,
            'remove_accents': False,
            'stop_word_removal': 0.0
        }
        
        result = self.service.optimize(text, config)
        
        expected_abbreviations = ['univ', 'BR', 'dev', 'tech']
        found_abbreviations = []
        
        for abbrev in expected_abbreviations:
            if abbrev.lower() in result.optimized_text.lower():
                found_abbreviations.append(abbrev)
        
        assert len(found_abbreviations) > 0, \
            f"Nenhuma abreviaÃ§Ã£o encontrada em '{result.optimized_text}'"
        
        assert result.stats.characters_saved > 0, \
            "Deveria ter economizado alguns caracteres"
    
    def test_combined_optimizations(self):
        text = "O gato de Ceara precisa de 10 unidades de desenvolvimento para universidade brasileira em Sao Paulo com tecnologia avancada."
        
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
        
        assert len(result.optimized_text) < len(text.strip()), \
            "Texto otimizado deveria ser menor que o original"
        
        assert result.stats.compression_ratio_percent > 0, \
            "Deveria ter alguma compressÃ£o"
        
        assert "10" in result.optimized_text, \
            "NÃºmero '10' deveria ser preservado"
        
        locations_abbreviated = ("CE" in result.optimized_text or "SP" in result.optimized_text)
        assert locations_abbreviated, \
            "Pelo menos uma localizaÃ§Ã£o deveria ser abreviada"
        
        print(f"Original: {text.strip()}")
        print(f"Otimizado: {result.optimized_text}")
        print(f"Economia: {result.stats.compression_ratio_percent}%")
    
    def test_preset_with_enhancements(self):
        text = "O desenvolvedor de Brasilia precisa de 5 computadores para universidade"
        
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
        
        assert "5" in result.optimized_text
        
        assert "BSB" in result.optimized_text
        
        assert result.stats.compression_ratio_percent > 20


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
