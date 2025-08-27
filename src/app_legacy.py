"""
Arquivo principal da aplicação Flask.
"""
import logging
import os

from flask import Flask

from src.config.settings import config_by_name
from src.services.optimization_service import OptimizationService
from src.controllers.optimization_controller import OptimizationController


def create_app(config_name: str = None) -> Flask:
    """Factory function para criar a aplicação Flask."""
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    
    # Configuração do logging
    logging.basicConfig(
        level=logging.INFO, 
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Instancia os serviços e controladores
    config_instance = config_by_name[config_name]()
    optimization_service = OptimizationService(config_instance)
    optimization_controller = OptimizationController(optimization_service)
    
    # Registra as rotas
    register_routes(app, optimization_controller)
    
    return app


def register_routes(app: Flask, optimization_controller: OptimizationController):
    """Registra todas as rotas da aplicação."""
    
    @app.route('/optimize', methods=['POST'])
    def optimize():
        return optimization_controller.optimize()
    
    @app.route('/presets', methods=['GET'])
    def presets():
        return optimization_controller.get_presets()
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return optimization_controller.health_check()


if __name__ == '__main__':
    app = create_app()
    
    # Usar o logger do Flask para mensagens de inicialização
    app.logger.info("=== API de Otimização de Prompts v2.0 ===")
    app.logger.info("Endpoints disponíveis:")
    app.logger.info("  POST /optimize  - Otimiza um prompt")
    app.logger.info("  GET  /presets   - Lista configurações predefinidas")
    app.logger.info("  GET  /health    - Verificação de saúde")
    app.logger.info("Servidor rodando em http://0.0.0.0:5000")
    
    # host='0.0.0.0' torna o servidor acessível na rede local
    # debug=True é ótimo para desenvolvimento, mas deve ser False em produção
    app.run(host='0.0.0.0', port=5000, debug=True)
