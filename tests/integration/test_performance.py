"""
Testes de performance e benchmarks para avaliar eficiência da otimização.
"""
import time
import pytest
from src.services.optimization_service import OptimizationService


class TestPerformanceBenchmarks:
    """Testes de performance para avaliar eficiência do sistema."""
    
    @pytest.fixture
    def large_text(self):
        """Fixture com texto grande para testes de performance."""
        base_text = """
        Desenvolvendo uma aplicação web moderna em JavaScript e Python para empresas
        localizadas em São Paulo, Rio de Janeiro e Ceará. O projeto custará muito dinheiro
        e será finalizado em alguns meses. A equipe tem desenvolvedores especializados em
        tecnologias como React, Django, PostgreSQL e MongoDB. Os animais da equipe, incluindo
        cachorros labradores e gatos siameses, também participam das atividades diárias.
        """
        # Repetir o texto para criar um texto maior
        return base_text * 20
    
    def test_optimization_performance(self, optimization_service, large_text):
        """Testa a performance da otimização em textos grandes."""
        start_time = time.time()
        
        config = {'stop_word_removal': 0.3, 'word_compression': 0.7, 'min_word_length': 3}
        result = optimization_service.optimize(large_text, config)
        
        end_time = time.time()
        processing_time = end_time - start_time
        
        # Deve processar em tempo razoável (< 5 segundos para texto médio)
        assert processing_time < 5.0, f"Processamento demorou {processing_time:.2f}s"
        
        # Deve ter otimizado
        assert result.stats.compression_ratio_percent >= 0
        assert len(result.optimized_text) > 0
    
    def test_multiple_optimizations_consistency(self, optimization_service, sample_texts):
        """Testa se múltiplas otimizações do mesmo texto são consistentes."""
        text = sample_texts['complex_mix']
        config = {'stop_word_removal': 0.3, 'word_compression': 0.7, 'min_word_length': 3}
        
        results = []
        for _ in range(3):
            result = optimization_service.optimize(text, config)
            results.append(result)
        
        # Resultados devem ser idênticos (algoritmo determinístico)
        first_result = results[0].optimized_text
        for result in results[1:]:
            assert result.optimized_text == first_result
    
    def test_compression_efficiency_by_level(self, optimization_service, sample_texts):
        """Testa eficiência de compressão por nível."""
        text = sample_texts['long_text']
        compression_levels = [0.9, 0.7, 0.5, 0.3, 0.1]  # De menos para mais agressivo
        
        previous_length = len(text)
        
        for level in compression_levels:
            config = {
                'word_compression': level,
                'min_word_length': 2,
                'stop_word_removal': 0.2
            }
            result = optimization_service.optimize(text, config)
            
            current_length = len(result.optimized_text)
            
            # Maior agressividade deve resultar em texto menor ou igual
            assert current_length <= previous_length, f"Nível {level} resultou em texto maior que {previous_length}"
            previous_length = current_length
    
    def test_processing_stability(self, optimization_service):
        """Testa se o processamento permanece estável com múltiplas execuções."""
        # Processa múltiplos textos sem erros
        for i in range(10):
            text = f"Texto de teste número {i} com conteúdo variável para análise de estabilidade"
            config = {'stop_word_removal': 0.3, 'word_compression': 0.7, 'min_word_length': 2}
            result = optimization_service.optimize(text, config)
            
            # Cada resultado deve ser válido
            assert result.stats.compression_ratio_percent >= 0
            assert len(result.optimized_text) > 0
            assert hasattr(result, 'stats')
            assert hasattr(result, 'config_used')


class TestOptimizationQuality:
    """Testes para avaliar a qualidade da otimização."""
    
    def test_optimization_maintains_readability(self, optimization_service):
        """Testa se a otimização mantém legibilidade do texto."""
        readable_text = "O gato subiu no telhado da casa amarela"
        config = {'word_compression': 0.6, 'min_word_length': 2, 'stop_word_removal': 0.3}
        
        result = optimization_service.optimize(readable_text, config)
        optimized = result.optimized_text
        
        # Deve manter estrutura básica
        words = optimized.split()
        assert len(words) > 0
        
        # Não deve ter palavras muito pequenas (< 2 chars) exceto artigos/preposições
        short_words = [w for w in words if len(w) < 2]
        common_short_words = ['é', 'e', 'o', 'a', 'de', 'da', 'do', 'em', 'no', 'na']
        unexpected_short = [w for w in short_words if w.lower() not in common_short_words]
        assert len(unexpected_short) <= 1, f"Muitas palavras muito curtas: {unexpected_short}"
    
    def test_entity_preservation_accuracy(self, optimization_service):
        """Testa preservação básica em otimização."""
        text_with_entities = """
        A empresa tem 50 funcionários em São Paulo, desenvolvendo em Python e JavaScript.
        O projeto custa R$ 250.000,00 e envolve desenvolvimento de aplicações web.
        """
        
        config = {'word_compression': 0.6, 'min_word_length': 3, 'stop_word_removal': 0.3}
        result = optimization_service.optimize(text_with_entities, config)
        optimized = result.optimized_text.lower()
        
        # Números importantes devem estar preservados ou parcialmente preservados
        number_preserved = '50' in optimized or '250' in optimized
        assert number_preserved, f"Números não preservados em: {result.optimized_text}"
        
        # Pelo menos algumas palavras importantes devem estar preservadas
        tech_preserved = any(tech in optimized for tech in ['python', 'javascript', 'py', 'js'])
        location_preserved = 'sp' in optimized or 'paulo' in optimized or 'são' in optimized
        
        # Pelo menos uma categoria deve estar preservada
        assert tech_preserved or location_preserved, f"Nenhuma entidade importante preservada em: {result.optimized_text}"
    
    def test_abbreviation_quality(self, optimization_service):
        """Testa qualidade básica da otimização."""
        text = "Desenvolvimento de aplicação web com JavaScript, Python, PostgreSQL e MongoDB"
        
        config = {'word_compression': 0.7, 'min_word_length': 2, 'stop_word_removal': 0.4}
        result = optimization_service.optimize(text, config)
        optimized = result.optimized_text
        
        # Deve ter otimizado o texto
        assert len(optimized) < len(text), "Texto não foi otimizado"
        
        # Deve manter pelo menos algumas palavras reconhecíveis
        words_found = 0
        important_words = ['javascript', 'js', 'python', 'py', 'postgresql', 'mongodb', 'web', 'aplicacao', 'desenvolvimento']
        for word in important_words:
            if word in optimized.lower():
                words_found += 1
        
        assert words_found >= 2, f"Poucas palavras importantes preservadas ({words_found}) em: {optimized}"
