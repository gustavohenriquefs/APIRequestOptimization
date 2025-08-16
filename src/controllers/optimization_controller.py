"""
Controladores da API Flask.
"""
import logging
from dataclasses import asdict

from flask import jsonify, request

from src.services.optimization_service import OptimizationService
from src.utils.validators import validate_request_data
from src.utils.presets import get_presets_dict


class OptimizationController:
    """Controlador para endpoints de otimização."""

    def __init__(self, optimization_service: OptimizationService):
        self.optimization_service = optimization_service

    def optimize(self):
        """Endpoint principal para otimização de prompts."""
        data = request.get_json()
        
        error_message = validate_request_data(data)
        if error_message:
            logging.warning(f"Requisição inválida para /optimize: {error_message}")
            return jsonify({'error': error_message}), 400
            
        try:
            text = data['text']
            config = data.get('config', {})
            result = self.optimization_service.optimize(text, config)
            
            # Converte o dataclass para dicionário para serialização JSON
            response_dict = {
                'original_text': result.original_text,
                'optimized_text': result.optimized_text,
                'stats': asdict(result.stats),
                'config_used': result.config_used
            }
            
            return jsonify(response_dict), 200
        except Exception as e:
            logging.critical(f"Erro inesperado em /optimize: {e}", exc_info=True)
            return jsonify({'error': 'Ocorreu um erro interno no servidor.'}), 500

    @staticmethod
    def get_presets():
        """Retorna configurações predefinidas para diferentes níveis de otimização."""
        return jsonify(get_presets_dict())

    @staticmethod
    def health_check():
        """Endpoint de verificação de saúde (health check) da API."""
        return jsonify({'status': 'healthy', 'version': '2.0.0'})
