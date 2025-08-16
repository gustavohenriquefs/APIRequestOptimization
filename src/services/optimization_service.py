"""
Serviço principal para otimização de prompts.
"""
import re
import string
import unicodedata
from typing import Dict, Any

from src.config.settings import Config
from src.models.optimization import OptimizationResponse, OptimizationStats
from src.services.translation_service import TranslationService

# trocar algumas palavras por siglas

class OptimizationService:
    """Encapsula toda a lógica para otimização de texto."""

    def __init__(self, config: Config):
        self.config = config
        self.translation_service = TranslationService(config)

    @staticmethod
    def remove_accents(text: str) -> str:
        """Remove acentos dos caracteres de forma eficiente."""
        normalized_text = unicodedata.normalize('NFD', text)
        return "".join(c for c in normalized_text if unicodedata.category(c) != 'Mn')

    @staticmethod
    def _compress_word(word: str, compression_ratio: float) -> str:
        """
        Comprime uma palavra removendo letras de forma inteligente.
        Mantém a primeira e a última letra e prioriza consoantes.
        """
        if len(word) <= 3 or not (0.0 < compression_ratio < 1.0):
            return word

        keep_chars_count = max(2, int(len(word) * compression_ratio))
        if keep_chars_count >= len(word):
            return word

        first_char, last_char = word[0], word[-1]
        middle_chars = list(word[1:-1])

        # Prioriza manter consoantes sobre vogais
        vowels = "aeiouáéíóúàèìòùâêîôûãõ"
        middle_chars.sort(key=lambda char: char.lower() in vowels)

        # Mantém os caracteres mais importantes do meio
        kept_middle = "".join(middle_chars[:keep_chars_count - 2])
        
        return first_char + kept_middle + last_char

    @staticmethod
    def remove_excessive_whitespace(text: str) -> str:
        """Remove espaços, tabulações e quebras de linha excessivas."""
        return re.sub(r'\s+', ' ', text).strip()

    @staticmethod
    def remove_redundant_punctuation(text: str) -> str:
        """Remove sequências de pontuação repetida."""
        # Ex: "!!!" -> "!", "..." -> "."
        text = re.sub(r'([.!?,\-;:"])\1+', r'\1', text)
        # Remove pontuação desnecessária no final da string
        return re.sub(r'[.,;:]+\s*$', '', text)

    def remove_stop_words(self, text: str, language: str, removal_ratio: float) -> str:
        """Remove uma proporção de stop words do texto."""
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
        """
        Orquestra o processo de otimização do prompt com base nas configurações.
        """
        original_length = len(text)
        
        # Pega as configurações ou usa valores padrão seguros
        should_translate = config_options.get('translate_to_english', False)
        language = config_options.get('language', 'pt')
        stop_word_ratio = config_options.get('stop_word_removal', 0.0)
        should_remove_accents = config_options.get('remove_accents', False)
        word_compression_ratio = config_options.get('word_compression', 1.0)
        should_remove_punctuation = config_options.get('remove_punctuation', False)

        processed_text = text

        # A ordem das operações é importante para o resultado final
        if should_translate:
            processed_text = self.translation_service.translate_to_english(processed_text)
            language = 'en'
        
        processed_text = self.remove_excessive_whitespace(processed_text)
        processed_text = self.remove_redundant_punctuation(processed_text)

        if stop_word_ratio > 0:
            processed_text = self.remove_stop_words(processed_text, language, stop_word_ratio)

        if should_remove_accents:
            processed_text = self.remove_accents(processed_text)

        if word_compression_ratio < 1.0:
            words = processed_text.split(' ')
            # Usa a função de compressão em cada palavra
            compressed_words = [self._compress_word(w, word_compression_ratio) for w in words]
            processed_text = ' '.join(compressed_words)

        if should_remove_punctuation:
            # Cria um padrão regex para remover todos os caracteres de pontuação
            punct_regex = f'[{re.escape("".join(self.config.REMOVABLE_CHARS))}]'
            processed_text = re.sub(punct_regex, '', processed_text)
        
        # Limpeza final de espaços que podem ter sido criados
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
