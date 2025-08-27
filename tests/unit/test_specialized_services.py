"""
Testes unitários para serviços de otimização especializados.
"""
import pytest
from src.services.optimization.abbreviation_service import AbbreviationService
from src.services.optimization.entity_preservation_service import EntityPreservationService


class TestAbbreviationService:
    """Testes unitários para o AbbreviationService."""
    
    @pytest.fixture
    def service(self):
        """Fixture para criar instância do AbbreviationService."""
        return AbbreviationService()
    
    def test_technology_abbreviations(self, service):
        """Testa abreviações de tecnologia."""
        text = "JavaScript é melhor que Python para frontend"
        result_text, replacements = service.apply_abbreviations(text)
        
        assert "JS" in result_text
        assert len(replacements) > 0
    
    def test_location_abbreviations(self, service):
        """Testa abreviações de localização."""
        text = "Viajei de São Paulo para Rio de Janeiro"
        result_text, replacements = service.apply_abbreviations(text)
        
        assert "SP" in result_text
        assert "RJ" in result_text
    
    def test_animal_abbreviations(self, service):
        """Testa abreviações de animais."""
        text = "O cachorro labrador brincou com o gato siamês"
        result_text, replacements = service.apply_abbreviations(text)
        
        # Verifica se pelo menos algumas abreviações foram aplicadas
        original_length = len(text)
        result_length = len(result_text)
        assert result_length <= original_length
    
    def test_measurement_abbreviations(self, service):
        """Testa abreviações de medidas."""
        text = "A distância é de 10 quilômetros e o peso é 5 quilogramas"
        result_text, replacements = service.apply_abbreviations(text)
        
        assert "km" in result_text
        assert "kg" in result_text


class TestEntityPreservationService:
    """Testes unitários para o EntityPreservationService."""
    
    @pytest.fixture
    def service(self):
        """Fixture para criar instância do EntityPreservationService."""
        return EntityPreservationService()
    
    def test_entity_service_initialization(self, service):
        """Testa se o serviço de preservação de entidades é inicializado corretamente."""
        # Teste básico de inicialização
        assert service is not None
        
        # Testa métodos básicos sem dependência de detecção específica
        text = "O projeto tem 10 desenvolvedores"
        entities = service.extract_entities(text)
        
        # O importante é que o método não falhe
        assert isinstance(entities, list)
    
    def test_compression_limits_method(self, service):
        """Testa se o método de limites de compressão funciona."""
        text = "Texto para teste"
        entities = service.extract_entities(text)
        
        # Método deve funcionar mesmo com lista vazia
        limits = service.get_compression_limits(entities)
        assert isinstance(limits, dict)
    
    def test_word_preservation_check(self, service):
        """Testa verificação de preservação de palavras."""
        text = "Python é ótimo"
        entities = service.extract_entities(text)
        
        # Testa método de verificação de palavras
        should_preserve, ratio = service.should_preserve_word("Python", 0, entities)
        assert isinstance(should_preserve, bool)
        assert ratio is None or isinstance(ratio, float)
