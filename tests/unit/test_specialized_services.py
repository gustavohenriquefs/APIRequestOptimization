import pytest
from src.services.optimization.abbreviation_service import AbbreviationService
from src.services.optimization.entity_preservation_service import EntityPreservationService


class TestAbbreviationService:
    
    @pytest.fixture
    def service(self):
        return AbbreviationService()
    
    def test_technology_abbreviations(self, service):
        text = "JavaScript e melhor que Python para frontend"
        result_text, replacements = service.apply_abbreviations(text)
        
        assert "JS" in result_text
        assert len(replacements) > 0
    
    def test_location_abbreviations(self, service):
        text = "Viajei de Sao Paulo para Rio de Janeiro"
        result_text, replacements = service.apply_abbreviations(text)
        
        assert "SP" in result_text
        assert "RJ" in result_text
    
    def test_animal_abbreviations(self, service):
        text = "O cachorro labrador brincou com o gato siames"
        result_text, replacements = service.apply_abbreviations(text)
        
        original_length = len(text)
        result_length = len(result_text)
        assert result_length <= original_length
    
    def test_measurement_abbreviations(self, service):
        text = "A distancia e de 10 quilometros e o peso e 5 quilogramas"
        result_text, replacements = service.apply_abbreviations(text)
        
        assert "kg" in result_text
        original_length = len(text)
        result_length = len(result_text)
        assert result_length <= original_length


class TestEntityPreservationService:
    
    @pytest.fixture
    def service(self):
        return EntityPreservationService()
    
    def test_entity_service_initialization(self, service):
        assert service is not None
        
        text = "O projeto tem 10 desenvolvedores"
        entities = service.extract_entities(text)
        
        assert isinstance(entities, list)
    
    def test_compression_limits_method(self, service):
        text = "Texto para teste"
        entities = service.extract_entities(text)
        
        limits = service.get_compression_limits(entities)
        assert isinstance(limits, dict)
    
    def test_word_preservation_check(self, service):
        text = "Python e otimo"
        entities = service.extract_entities(text)
        
        should_preserve, ratio = service.should_preserve_word("Python", 0, entities)
        assert isinstance(should_preserve, bool)
        assert ratio is None or isinstance(ratio, float)
