"""
Teste específico para validar a correção do algoritmo de compressão.
Verifica se palavras são comprimidas preservando melhor a ordem natural.
"""
import pytest
from src.services.optimization_service import OptimizationService
from src.config.settings import TestingConfig


class TestCompressionImprovement:
    """Testes para validar melhorias no algoritmo de compressão."""

    def setup_method(self):
        """Inicializa o serviço de otimização antes de cada teste."""
        config = TestingConfig()
        self.service = OptimizationService(config)

    def test_word_compression_order_preservation(self):
        """
        Testa se a compressão preserva melhor a ordem natural das letras.
        """
        test_cases = [
            # (palavra, ratio, resultado_esperado_melhorado)
            ('viralata', 0.8, 'virlta'),  # Não deve ser 'vrltia'
            ('correndo', 0.8, 'crrndo'),  # Mantém sequência lógica
            ('durante', 0.8, 'drnte'),    # Remove vogais duplas primeiro
            ('brasileiro', 0.8, 'brasilro'), # Preserva estrutura
        ]
        
        for word, ratio, expected_pattern in test_cases:
            compressed = self.service._compress_word(word, ratio, 3)
            
            # Verifica se o resultado é mais legível (não fora de ordem)
            assert len(compressed) == len(expected_pattern), \
                f"Comprimento incorreto para '{word}': esperado {len(expected_pattern)}, obteve {len(compressed)}"
            
            # Verifica se mantém primeiro e último caractere
            assert compressed[0] == word[0], f"Primeiro caractere deve ser preservado em '{word}'"
            assert compressed[-1] == word[-1], f"Último caractere deve ser preservado em '{word}'"
            
            # Verifica se não há ordenação completamente fora da sequência original
            # (isso é uma heurística - caracteres não devem estar muito fora de ordem)
            middle_compressed = compressed[1:-1]
            middle_original = word[1:-1]
            
            # Conta quantos caracteres mantiveram posição relativa aproximada
            preserved_order = 0
            for i, char in enumerate(middle_compressed):
                if char in middle_original:
                    original_pos = middle_original.index(char)
                    # Se a posição relativa é aproximadamente mantida
                    if abs(i - original_pos) <= 2:  # Tolerância de 2 posições
                        preserved_order += 1
            
            order_ratio = preserved_order / len(middle_compressed)
            assert order_ratio >= 0.5, \
                f"Ordem muito alterada em '{word}' -> '{compressed}': apenas {order_ratio:.1%} mantida"

    def test_user_reported_case_fixed(self):
        """
        Testa o caso específico reportado pelo usuário.
        """
        text = 'Criar imagem de viralata correndo no ceara durante o meio dia com corre 4 na br 222 com um cheque de 20000 reais.'
        
        config_options = {
            'preset': 'moderate',
            'translate_to_english': False,
            'language': 'pt',
            'stop_word_removal': 0.3,
            'remove_accents': True,
            'word_compression': 0.8,  # Caso específico do usuário
            'min_word_length': 3,
            'remove_punctuation': False
        }

        result = self.service.optimize(text, config_options)
        
        # Verifica se viralata não está como 'vrltia' (problema reportado)
        assert 'vrltia' not in result.optimized_text, \
            "Não deveria conter 'vrltia' (ordem incorreta)"
        
        # Verifica se viralata foi comprimido para algo mais legível
        assert 'virlta' in result.optimized_text or 'virlt' in result.optimized_text, \
            f"Deveria conter compressão mais legível de viralata em: '{result.optimized_text}'"
        
        # Verifica economia geral
        assert result.stats.compression_ratio_percent > 15, \
            f"Deveria ter pelo menos 15% de economia, obteve {result.stats.compression_ratio_percent}%"
        
        # Números importantes devem ser preservados
        assert '4' in result.optimized_text, "Número '4' deve ser preservado"
        assert '222' in result.optimized_text, "Número '222' deve ser preservado"
        assert '20000' in result.optimized_text, "Número '20000' deve ser preservado"

    def test_compression_readability_improvement(self):
        """
        Testa se as palavras comprimidas ficaram mais legíveis.
        """
        readable_cases = [
            'universidade',  # Não deve virar algo como 'unvrstd'
            'desenvolvimento', # Deve manter estrutura reconhecível
            'brasileiro',      # Não deve embaralhar muito
            'tecnologia',      # Deve ser legível
        ]
        
        for word in readable_cases:
            compressed = self.service._compress_word(word, 0.7, 3)  # 70% compressão
            
            # Verifica se ainda é reconhecível (heurística simples)
            common_letters = set(compressed.lower()) & set(word.lower())
            coverage = len(common_letters) / len(set(word.lower()))
            
            assert coverage >= 0.6, \
                f"Palavra '{compressed}' não mantém suficiente similaridade com '{word}' ({coverage:.1%})"
            
            # Verifica se não há repetições desnecessárias adjacentes
            adjacent_repeats = sum(1 for i in range(len(compressed)-1) 
                                 if compressed[i] == compressed[i+1])
            
            # Permite algumas repetições, mas não muitas
            repeat_ratio = adjacent_repeats / max(1, len(compressed)-1)
            assert repeat_ratio <= 0.3, \
                f"Muitas repetições adjacentes em '{compressed}': {repeat_ratio:.1%}"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
