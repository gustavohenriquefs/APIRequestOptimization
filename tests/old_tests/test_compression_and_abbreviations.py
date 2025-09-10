import pytest
from src.services.optimization_service import OptimizationService
from src.config.settings import TestingConfig


class TestCompressionAndAbbreviations:

    def setup_method(self):
        config = TestingConfig()
        self.service = OptimizationService(config)

    def test_word_compression_with_number_preservation(self):
        text = "Criar imagem de viralata correndo no ceara durante o meio dia com corre 4."
        
        config_options = {
            'preset': 'moderate',
            'translate_to_english': False,
            'language': 'pt',
            'stop_word_removal': 0.3,
            'remove_accents': True,
            'word_compression': 0.2,
            'min_word_length': 3,
            'remove_punctuation': False
        }

        result = self.service.optimize(text, config_options)

        assert len(result.optimized_text) < len(text), "Texto deveria ser comprimido"
        assert result.stats.compression_ratio_percent > 25, f"Deveria ter mais de 25% de economia, obteve {result.stats.compression_ratio_percent}%"
        
        assert "4" in result.optimized_text, "NÃºmero '4' deveria ser preservado"
        
        assert "CE" in result.optimized_text or "ceara" not in result.optimized_text.lower(), "LocalizaÃ§Ã£o deveria ser abreviada"
        
        long_words_compressed = all(
            len(word) <= 4 or any(char.isdigit() for char in word) 
            for word in result.optimized_text.split()
            if len(word) > 4
        )
        assert long_words_compressed, "Palavras longas deveriam estar comprimidas"

    def test_number_preservation_comprehensive(self):
        test_cases = [
            ("Preciso de 10 kg de aÃ§Ãºcar", "10"),
            ("VersÃ£o 2.1.4 do sistema", "2.1.4"), 
            ("Chegou Ã s 15:30", "15:30"),
            ("Custa R$ 25,50", "25,50"),
            ("Temperatura de 23Â°C", "23"),
            ("Arquivo de 500 MB", "500"),
            ("Velocidade de 80 km/h", "80"),
            ("Apenas 1 item restante", "1"),
        ]
        
        for text, number_to_preserve in test_cases:
            config = {
                'word_compression': 0.3,
                'min_word_length': 2,
                'preserve_entities': True,
                'abbreviation_level': 0.7,
                'remove_accents': False,
                'stop_word_removal': 0.2
            }
            
            result = self.service.optimize(text, config)
            
            assert number_to_preserve in result.optimized_text, \
                f"NÃºmero '{number_to_preserve}' nÃ£o foi preservado em '{text}' -> '{result.optimized_text}'"

    def test_abbreviations_with_location_variations(self):
        location_test_cases = [
            ("Vou para Ceara amanha", "CE"),
            ("Estive no ceara ontem", "CE"),
            ("O estado do Ceara", "CE"),
            ("Sao Paulo e grande", "SP"),
            ("sao paulo tem transito", "SP"),
            ("Rio de Janeiro e lindo", "RJ"),
            ("Brasilia e a capital", "BSB"),
            ("Minas Gerais produz cafe", "MG"),
        ]
        
        for text, expected_abbrev in location_test_cases:
            config = {
                'abbreviation_level': 0.8,
                'preserve_entities': True,
                'word_compression': 1.0,
                'remove_accents': False,
                'stop_word_removal': 0.0
            }
            
            result = self.service.optimize(text, config)
            
            assert expected_abbrev in result.optimized_text, \
                f"Localizacao deveria ser abreviada para '{expected_abbrev}' em '{text}' -> '{result.optimized_text}'"

    def test_technical_abbreviations(self):
        technical_cases = [
            ("A universidade brasileira", ["univ", "BR"]),
            ("desenvolvimento de software", ["dev", "sw"]),
            ("tecnologia avanÃ§ada", ["tech", "adv"]),
            ("aplicaÃ§Ã£o web moderna", ["app", "web", "mod"]),
        ]
        
        for text, expected_abbrevs in technical_cases:
            config = {
                'abbreviation_level': 0.8,
                'preserve_entities': True,
                'word_compression': 1.0,
                'remove_accents': False,
                'stop_word_removal': 0.0
            }
            
            result = self.service.optimize(text, config)
            
            found_abbrevs = [abbrev for abbrev in expected_abbrevs 
                           if abbrev.lower() in result.optimized_text.lower()]
            
            assert len(found_abbrevs) > 0, \
                f"Deveria conter pelo menos uma abreviaÃ§Ã£o de {expected_abbrevs} em '{text}' -> '{result.optimized_text}'"

    def test_combined_optimization_aggressive(self):
        text = "A universidade brasileira de SÃ£o Paulo precisa de 15 computadores para desenvolvimento de tecnologia em 2024."
        
        config = {
            'abbreviation_level': 0.9,
            'preserve_entities': True,
            'word_compression': 0.4,
            'min_word_length': 3,
            'remove_accents': True,
            'stop_word_removal': 0.4,
            'remove_punctuation': False
        }
        
        result = self.service.optimize(text, config)
        
        print(f"\nTeste agressivo:")
        print(f"Original: {text}")
        print(f"Otimizado: {result.optimized_text}")
        print(f"Economia: {result.stats.compression_ratio_percent}%")
        
        assert result.stats.compression_ratio_percent > 40, \
            f"Deveria ter mais de 40% de economia, obteve {result.stats.compression_ratio_percent}%"
        
        assert "15" in result.optimized_text, "NÃºmero '15' deveria ser preservado"
        assert "2024" in result.optimized_text, "Ano '2024' deveria ser preservado"
        
        has_abbreviations = any(abbrev in result.optimized_text.upper() 
                              for abbrev in ['SP', 'BR', 'UNIV', 'DEV', 'TECH'])
        assert has_abbreviations, "Deveria conter algumas abreviaÃ§Ãµes tÃ©cnicas ou geogrÃ¡ficas"

    def test_measurement_units_preservation(self):
        measurement_cases = [
            "Preciso de 2 kg de farinha",
            "DistÃ¢ncia de 100 km",
            "Arquivo de 50 MB", 
            "Temperatura de 25Â°C",
            "Velocidade de 60 km/h",
            "Capacidade de 500 GB",
        ]
        
        for text in measurement_cases:
            config = {
                'word_compression': 0.2,
                'min_word_length': 2,
                'preserve_entities': True,
                'abbreviation_level': 0.8
            }
            
            result = self.service.optimize(text, config)
            
            import re
            original_numbers = re.findall(r'\d+(?:\.\d+)?', text)
            
            for number in original_numbers:
                assert number in result.optimized_text, \
                    f"NÃºmero '{number}' nÃ£o foi preservado em '{text}' -> '{result.optimized_text}'"

    def test_preset_moderate_real_case(self):
        text = "Criar imagem de viralata correndo no ceara durante o meio dia com corre 4."
        
        config_options = {
            'preset': 'moderate',
            'translate_to_english': False,
            'language': 'pt',
            'stop_word_removal': 0.3,
            'remove_accents': True,
            'word_compression': 0.2,
            'min_word_length': 3,
            'remove_punctuation': False
        }

        result = self.service.optimize(text, config_options)
        
        assert result.stats.compression_ratio_percent >= 30, \
            f"Deveria ter pelo menos 30% de economia, obteve {result.stats.compression_ratio_percent}%"
        
        assert "4" in result.optimized_text, "NÃºmero '4' deveria ser preservado"
        
        assert "CE" in result.optimized_text, "CearÃ¡ deveria ser abreviado para 'CE'"
        
        compressed_words = [word for word in result.optimized_text.split() 
                          if len(word) <= 3 and word.isalpha()]
        assert len(compressed_words) >= 5, \
            f"Deveria ter pelo menos 5 palavras comprimidas, encontrou {len(compressed_words)}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
