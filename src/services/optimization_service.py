import re
import string
import unicodedata
from typing import Dict, Any, List, Tuple

from src.config.settings import Config
from src.models.optimization import OptimizationResponse, OptimizationStats
from src.services.translation_service import TranslationService
from src.services.optimization import AbbreviationService, EntityPreservationService

class OptimizationService:

    def __init__(self, config: Config):
        self.config = config
        self.translation_service = TranslationService(config)
        self.abbreviation_service = AbbreviationService()
        self.entity_service = EntityPreservationService()

    @staticmethod
    def remove_accents(text: str) -> str:
        normalized_text = unicodedata.normalize('NFD', text)
        return "".join(c for c in normalized_text if unicodedata.category(c) != 'Mn')

    @staticmethod
    def _compress_word(word: str, compression_ratio: float, min_word_length: int = 2) -> str:
        if len(word) <= min_word_length or not (0.0 < compression_ratio < 1.0):
            return word

        min_ratio_for_min_length = min_word_length / len(word)
        
        effective_ratio = max(compression_ratio, min_ratio_for_min_length)
        
        target_length = int(len(word) * effective_ratio)
        
        target_length = max(min_word_length, target_length)
        
        if target_length >= len(word):
            return word

        if len(word) <= 3:
            return word[:target_length]

        if target_length <= 2:
            return word[0] + word[-1]
        
        first_char = word[0]
        last_char = word[-1]
        middle_chars = list(word[1:-1])

        middle_chars_to_keep = target_length - 2
        
        middle_chars_to_keep = min(middle_chars_to_keep, len(middle_chars))
        
        if middle_chars_to_keep <= 0:
            compressed = first_char + last_char
        else:
            
            if middle_chars_to_keep >= len(middle_chars):
                kept_middle = "".join(middle_chars)
            else:
                vowels = "aeiouáéíóúàèìòùâêîôûãõAEIOUÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕ"
                
                chars_with_priority = []
                for i, char in enumerate(middle_chars):
                    is_vowel = char.lower() in vowels
                    is_duplicate_vowel = (is_vowel and i > 0 and 
                                        middle_chars[i-1].lower() in vowels and 
                                        middle_chars[i-1].lower() == char.lower())
                    
                    priority = 2 if is_duplicate_vowel else (1 if is_vowel else 0)
                    chars_with_priority.append((char, i, priority))
                
                chars_with_priority.sort(key=lambda x: (x[2], x[1]))
                
                selected_chars = chars_with_priority[:middle_chars_to_keep]
                
                selected_chars.sort(key=lambda x: x[1])
                
                kept_middle = "".join([char for char, _, _ in selected_chars])
            
            compressed = first_char + kept_middle + last_char
            
        return compressed

    @staticmethod
    def remove_excessive_whitespace(text: str) -> str:
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def remove_redundant_punctuation(text: str) -> str:
        text = re.sub(r'([.!?,\-;:"])\1+', r'\1', text)
        return re.sub(r'[.,;:]+\s*$', '', text)

    def remove_stop_words(self, text: str, language: str, removal_ratio: float) -> str:
        if not (0.0 < removal_ratio <= 1.0):
            return text

        words = text.split()
        stop_words_set = self.config.STOP_WORDS.get(language, set())
        
        stop_word_indices = [
            i for i, word in enumerate(words) 
            if word.lower().strip(string.punctuation) in stop_words_set
        ]
        
        num_to_remove = int(len(stop_word_indices) * removal_ratio)
        indices_to_remove = set(stop_word_indices[:num_to_remove])
        
        return ' '.join(word for i, word in enumerate(words) if i not in indices_to_remove)

    def optimize(self, text: str, config_options: Dict[str, Any]) -> OptimizationResponse:
        original_length = len(text)
        
        should_translate = config_options.get('translate_to_english', False)
        language = config_options.get('language', 'pt')
        stop_word_ratio = config_options.get('stop_word_removal', 0.0)
        should_remove_accents = config_options.get('remove_accents', False)
        word_compression_ratio = config_options.get('word_compression', 1.0)
        min_word_length = config_options.get('min_word_length', 2)
        should_remove_punctuation = config_options.get('remove_punctuation', False)
        
        abbreviation_level = config_options.get('abbreviation_level', 0.5)
        preserve_entities = config_options.get('preserve_entities', True)

        processed_text = text

        entities = []
        if preserve_entities:
            entities = self.entity_service.extract_entities(processed_text)

        if abbreviation_level > 0:
            processed_text, replacements = self.abbreviation_service.apply_abbreviations(
                processed_text, 
                aggressiveness=abbreviation_level,
                preserve_context=True
            )

        if should_translate:
            processed_text = self.translation_service.translate_to_english(processed_text)
            language = 'en'
        
        processed_text = self.remove_excessive_whitespace(processed_text)
        processed_text = self.remove_redundant_punctuation(processed_text)

        if stop_word_ratio > 0:
            processed_text = self.remove_stop_words(processed_text, language, stop_word_ratio)

        if should_remove_accents:
            processed_text = self.remove_accents(processed_text)

        if should_remove_punctuation:
            punct_regex = f'[{re.escape("".join(self.config.REMOVABLE_CHARS))}]'
            processed_text = re.sub(punct_regex, '', processed_text)

        if word_compression_ratio < 1.0:
            processed_text = self._compress_words_with_preservation(
                processed_text, 
                word_compression_ratio, 
                min_word_length,
                entities
            )
        
        processed_text = self.remove_excessive_whitespace(processed_text)

        final_length = len(processed_text)
        compression_percentage = (
            ((original_length - final_length) / original_length * 100) 
            if original_length > 0 else 0
        )

        stats = OptimizationStats(
            original_length=original_length,
            optimized_length=final_length,
            compression_ratio_percent=round(compression_percentage, 2),
            characters_saved=original_length - final_length
        )

        return OptimizationResponse(
            original_text=text,
            optimized_text=processed_text,
            stats=stats,
            config_used=config_options
        )
    
    def _compress_words_with_preservation(
        self, 
        text: str, 
        compression_ratio: float, 
        min_word_length: int,
        entities: List
    ) -> str:
        words = text.split(' ')
        compressed_words = []
        
        for word in words:
            if not word.strip():
                continue
            
            is_important, _ = self.abbreviation_service.number_service.is_important_number(word)
            if is_important:
                compressed_words.append(word)
                continue
                
            word_position = text.find(word)
            
            should_preserve, compression_limit = self.entity_service.should_preserve_word(
                word, word_position, entities
            )
            
            if should_preserve and compression_limit:
                effective_ratio = max(compression_ratio, compression_limit)
            else:
                effective_ratio = compression_ratio
            
            compressed_word = self._compress_word(word, effective_ratio, min_word_length)
            compressed_words.append(compressed_word)
        
        return ' '.join(compressed_words)
