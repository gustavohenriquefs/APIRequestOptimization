import pytest
from src.services.optimization_service import OptimizationService
from src.config.settings import TestingConfig


class TestCompressionImprovement:

    def setup_method(self):
        config = TestingConfig()
        self.service = OptimizationService(config)

    def test_word_compression_order_preservation(self):
        test_cases = [
            ('viralata', 0.8, 'virlta'),
            ('correndo', 0.8, 'crrndo'),
            ('durante', 0.8, 'drnte'),
            ('brasileiro', 0.8, 'brasilro'),
        ]
        
        for word, ratio, expected_pattern in test_cases:
            compressed = self.service._compress_word(word, ratio, 3)
            
            assert len(compressed) == len(expected_pattern), \
                f"Comprimento incorreto para '{word}': esperado {len(expected_pattern)}, obteve {len(compressed)}"
            
            assert compressed[0] == word[0], f"Primeiro caractere deve ser preservado em '{word}'"
            assert compressed[-1] == word[-1], f"Ãšltimo caractere deve ser preservado em '{word}'"
            
            middle_compressed = compressed[1:-1]
            middle_original = word[1:-1]
            
            preserved_order = 0
            for i, char in enumerate(middle_compressed):
                if char in middle_original:
                    original_pos = middle_original.index(char)
                    if abs(i - original_pos) <= 2:
                        preserved_order += 1
            
            order_ratio = preserved_order / len(middle_compressed)
            assert order_ratio >= 0.5, \
                f"Ordem muito alterada em '{word}' -> '{compressed}': apenas {order_ratio:.1%} mantida"

    def test_user_reported_case_fixed(self):
        text = 'Criar imagem de viralata correndo no ceara durante o meio dia com corre 4 na br 222 com um cheque de 20000 reais.'
        
        config_options = {
            'preset': 'moderate',
            'translate_to_english': False,
            'language': 'pt',
            'stop_word_removal': 0.3,
            'remove_accents': True,
            'word_compression': 0.8,
            'min_word_length': 3,
            'remove_punctuation': False
        }

        result = self.service.optimize(text, config_options)
        
        assert 'vrltia' not in result.optimized_text, \
            "NÃ£o deveria conter 'vrltia' (ordem incorreta)"
        
        assert 'virlta' in result.optimized_text or 'virlt' in result.optimized_text, \
            f"Deveria conter compressÃ£o mais legÃ­vel de viralata em: '{result.optimized_text}'"
        
        assert result.stats.compression_ratio_percent > 15, \
            f"Deveria ter pelo menos 15% de economia, obteve {result.stats.compression_ratio_percent}%"
        
        assert '4' in result.optimized_text, "NÃºmero '4' deve ser preservado"
        assert '222' in result.optimized_text, "NÃºmero '222' deve ser preservado"
        assert '20000' in result.optimized_text, "NÃºmero '20000' deve ser preservado"

    def test_compression_readability_improvement(self):
        readable_cases = [
            'universidade',
            'desenvolvimento',
            'brasileiro',
            'tecnologia',
        ]
        
        for word in readable_cases:
            compressed = self.service._compress_word(word, 0.7, 3)
            
            common_letters = set(compressed.lower()) & set(word.lower())
            coverage = len(common_letters) / len(set(word.lower()))
            
            assert coverage >= 0.6, \
                f"Palavra '{compressed}' nÃ£o mantÃ©m suficiente similaridade com '{word}' ({coverage:.1%})"
            
            adjacent_repeats = sum(1 for i in range(len(compressed)-1) 
                                 if compressed[i] == compressed[i+1])
            
            repeat_ratio = adjacent_repeats / max(1, len(compressed)-1)
            assert repeat_ratio <= 0.3, \
                f"Muitas repetiÃ§Ãµes adjacentes em '{compressed}': {repeat_ratio:.1%}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
