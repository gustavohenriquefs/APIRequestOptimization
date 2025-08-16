"""
Serviço responsável pela tradução de textos.
"""
import json
import logging
from typing import Optional

import requests
from requests.exceptions import RequestException

from src.config.settings import Config


class TranslationService:
    """Serviço para tradução de textos usando APIs externas."""

    def __init__(self, config: Config):
        self.config = config
        self.http_session = requests.Session()

    def _make_translation_request(self, url: str, method: str, **kwargs) -> Optional[str]:
        """
        Função auxiliar para fazer requisições de tradução com tratamento de erro.
        """
        try:
            if method.upper() == 'GET':
                response = self.http_session.get(
                    url, 
                    params=kwargs.get('params'), 
                    timeout=self.config.REQUESTS_TIMEOUT
                )
            elif method.upper() == 'POST':
                response = self.http_session.post(
                    url, 
                    json=kwargs.get('json'), 
                    timeout=self.config.REQUESTS_TIMEOUT
                )
            else:
                raise ValueError("Método HTTP não suportado.")

            response.raise_for_status()
            data = response.json()

            # Extrai o texto traduzido dependendo da API
            if "mymemory" in url and data.get('responseStatus') == 200:
                return data['responseData']['translatedText']
            if "libretranslate" in url and "translatedText" in data:
                return data["translatedText"]

            logging.warning(f"Resposta inesperada da API de tradução {url}: {data}")
            return None

        except RequestException as e:
            logging.error(f"Erro de comunicação com a API de tradução {url}: {e}")
            return None
        except (KeyError, json.JSONDecodeError) as e:
            logging.error(f"Erro ao processar a resposta da API de tradução {url}: {e}")
            return None

    def translate_to_english(self, text: str) -> str:
        """
        Traduz texto para inglês, com fallback para outra API.
        Retorna o texto original em caso de falha.
        """
        text_to_translate = text[:self.config.TRANSLATION_CHAR_LIMIT]

        # 1. Tenta a API MyMemory
        params = {'q': text_to_translate, 'langpair': 'pt|en'}
        translated_text = self._make_translation_request(
            self.config.MYMEMORY_API_URL, 'GET', params=params
        )
        if translated_text:
            return translated_text

        # 2. Fallback para a API LibreTranslate
        logging.info("Falha na API MyMemory, tentando fallback com LibreTranslate.")
        json_data = {"q": text_to_translate, "source": "pt", "target": "en"}
        translated_text = self._make_translation_request(
            self.config.LIBRETRANSLATE_API_URL, 'POST', json=json_data
        )
        if translated_text:
            return translated_text

        logging.error("Ambas as APIs de tradução falharam. Retornando texto original.")
        return text
