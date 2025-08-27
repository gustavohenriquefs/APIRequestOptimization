"""
Serviço principal para otimização de prompts.
Versão melhorada com preservação de entidades e abreviações inteligentes.
"""
import re
import string
import unicodedata
from typing import Dict, Any, List, Tuple

from src.config.settings import Config
from src.models.optimization import OptimizationResponse, OptimizationStats
from src.services.translation_service import TranslationService
from src.services.optimization import AbbreviationService, EntityPreservationService

class OptimizationService:
    """Encapsula toda a lógica para otimização de texto com preservação inteligente."""

    def __init__(self, config: Config):
        self.config = config
        self.translation_service = TranslationService(config)
        self.abbreviation_service = AbbreviationService()
        self.entity_service = EntityPreservationService()

    @staticmethod
    def remove_accents(text: str) -> str:
        """Remove acentos dos caracteres de forma eficiente."""
        normalized_text = unicodedata.normalize('NFD', text)
        return "".join(c for c in normalized_text if unicodedata.category(c) != 'Mn')

    @staticmethod
    def _compress_word(word: str, compression_ratio: float, min_word_length: int = 2) -> str:
        """
        Comprime uma palavra removendo letras de forma inteligente.
        
        Args:
            word: Palavra a ser comprimida
            compression_ratio: Porcentagem de caracteres a manter (0.0 a 1.0)
            min_word_length: Tamanho mínimo que a palavra deve ter após compressão
            
        Returns:
            Palavra comprimida respeitando o tamanho mínimo
        """
        # Só comprimir palavras que tenham mais caracteres que o mínimo desejado
        # Assim, palavras já no tamanho mínimo ou menores ficam intocadas
        if len(word) <= min_word_length or not (0.0 < compression_ratio < 1.0):
            return word

        # Calcula a porcentagem mínima necessária para atingir min_word_length
        min_ratio_for_min_length = min_word_length / len(word)
        
        # Usa a maior porcentagem entre a solicitada e a mínima necessária
        # Isso garante que o resultado nunca seja menor que min_word_length
        effective_ratio = max(compression_ratio, min_ratio_for_min_length)
        
        # Calcula quantos caracteres manter baseado na porcentagem efetiva
        target_length = int(len(word) * effective_ratio)
        
        # Garante que não seja menor que o mínimo (proteção adicional)
        target_length = max(min_word_length, target_length)
        
        # Se o tamanho alvo já é igual ou maior que a palavra original
        if target_length >= len(word):
            return word

        # Para palavras pequenas (3 caracteres ou menos), aplica corte simples
        if len(word) <= 3:
            return word[:target_length]

        # Para palavras maiores, usa estratégia inteligente mantendo primeiro e último caractere
        if target_length <= 2:
            # Se só podemos manter 2 caracteres, mantém primeiro e último
            return word[0] + word[-1]
        
        first_char = word[0]
        last_char = word[-1]
        middle_chars = list(word[1:-1])

        # Calcula quantos caracteres do meio manter (target_length - 2 para primeiro e último)
        middle_chars_to_keep = target_length - 2
        
        # Garante que não tentamos manter mais caracteres do que temos
        middle_chars_to_keep = min(middle_chars_to_keep, len(middle_chars))
        
        if middle_chars_to_keep <= 0:
            compressed = first_char + last_char
        else:
            # Nova estratégia: preservar ordem natural e privilegiar consoantes importantes
            # Mas sem quebrar completamente a sequência
            
            if middle_chars_to_keep >= len(middle_chars):
                # Se vamos manter todos, mantém a ordem original
                kept_middle = "".join(middle_chars)
            else:
                # Estratégia melhorada: remove vogais duplas primeiro, depois distribui uniformemente
                vowels = "aeiouáéíóúàèìòùâêîôûãõAEIOUÁÉÍÓÚÀÈÌÒÙÂÊÎÔÛÃÕ"
                
                # Identificar vogais duplicadas para remoção prioritária
                chars_with_priority = []
                for i, char in enumerate(middle_chars):
                    is_vowel = char.lower() in vowels
                    is_duplicate_vowel = (is_vowel and i > 0 and 
                                        middle_chars[i-1].lower() in vowels and 
                                        middle_chars[i-1].lower() == char.lower())
                    
                    priority = 2 if is_duplicate_vowel else (1 if is_vowel else 0)
                    chars_with_priority.append((char, i, priority))
                
                # Ordenar por prioridade (0=consoante, 1=vogal, 2=vogal duplicada)
                # Em caso de empate, manter ordem original (índice)
                chars_with_priority.sort(key=lambda x: (x[2], x[1]))
                
                # Pegar os caracteres com menor prioridade (consoantes primeiro)
                selected_chars = chars_with_priority[:middle_chars_to_keep]
                
                # Reordenar pelos índices originais para preservar sequência
                selected_chars.sort(key=lambda x: x[1])
                
                kept_middle = "".join([char for char, _, _ in selected_chars])
            
            compressed = first_char + kept_middle + last_char
            
        return compressed

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
        Versão melhorada com preservação de entidades e abreviações inteligentes.
        """
        original_length = len(text)
        
        # Pega as configurações ou usa valores padrão seguros
        should_translate = config_options.get('translate_to_english', False)
        language = config_options.get('language', 'pt')
        stop_word_ratio = config_options.get('stop_word_removal', 0.0)
        should_remove_accents = config_options.get('remove_accents', False)
        word_compression_ratio = config_options.get('word_compression', 1.0)
        min_word_length = config_options.get('min_word_length', 2)
        should_remove_punctuation = config_options.get('remove_punctuation', False)
        
        # Novas configurações para funcionalidades melhoradas
        abbreviation_level = config_options.get('abbreviation_level', 0.5)
        preserve_entities = config_options.get('preserve_entities', True)

        processed_text = text

        # 1. PRESERVAÇÃO DE ENTIDADES (primeiro para identificar o que proteger)
        entities = []
        if preserve_entities:
            entities = self.entity_service.extract_entities(processed_text)

        # 2. APLICAÇÃO DE ABREVIAÇÕES INTELIGENTES (antes da tradução)
        if abbreviation_level > 0:
            processed_text, replacements = self.abbreviation_service.apply_abbreviations(
                processed_text, 
                aggressiveness=abbreviation_level,
                preserve_context=True
            )

        # 3. TRADUÇÃO (se solicitada)
        if should_translate:
            processed_text = self.translation_service.translate_to_english(processed_text)
            language = 'en'
        
        # 4. LIMPEZAS BÁSICAS
        processed_text = self.remove_excessive_whitespace(processed_text)
        processed_text = self.remove_redundant_punctuation(processed_text)

        # 5. REMOÇÃO DE STOP WORDS
        if stop_word_ratio > 0:
            processed_text = self.remove_stop_words(processed_text, language, stop_word_ratio)

        # 6. REMOÇÃO DE ACENTOS
        if should_remove_accents:
            processed_text = self.remove_accents(processed_text)

        # 7. REMOÇÃO DE PONTUAÇÃO (antes da compressão)
        if should_remove_punctuation:
            # Cria um padrão regex para remover todos os caracteres de pontuação
            punct_regex = f'[{re.escape("".join(self.config.REMOVABLE_CHARS))}]'
            processed_text = re.sub(punct_regex, '', processed_text)

        # 8. COMPRESSÃO DE PALAVRAS COM PRESERVAÇÃO DE ENTIDADES
        if word_compression_ratio < 1.0:
            processed_text = self._compress_words_with_preservation(
                processed_text, 
                word_compression_ratio, 
                min_word_length,
                entities
            )
        
        # 9. LIMPEZA FINAL
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
        """Comprime palavras respeitando entidades preservadas e números importantes."""
        words = text.split(' ')
        compressed_words = []
        
        for word in words:
            if not word.strip():
                continue
            
            # Verifica se é um número importante que deve ser preservado
            is_important, _ = self.abbreviation_service.number_service.is_important_number(word)
            if is_important:
                compressed_words.append(word)  # Preserva números importantes
                continue
                
            # Encontrar posição aproximada da palavra no texto original
            # (simplificado - poderia ser mais preciso)
            word_position = text.find(word)
            
            # Verificar se a palavra deve ser preservada por ser uma entidade
            should_preserve, compression_limit = self.entity_service.should_preserve_word(
                word, word_position, entities
            )
            
            if should_preserve and compression_limit:
                # Usar limite de compressão da entidade
                effective_ratio = max(compression_ratio, compression_limit)
            else:
                effective_ratio = compression_ratio
            
            compressed_word = self._compress_word(word, effective_ratio, min_word_length)
            compressed_words.append(compressed_word)
        
        return ' '.join(compressed_words)
