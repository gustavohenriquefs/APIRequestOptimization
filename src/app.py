"""
Aplicação Flask com documentação automática Swagger/OpenAPI.
Implementa as melhores práticas para APIs REST com documentação.
"""
from flask import Flask
from flask_restx import Api, Resource, fields, Namespace
from werkzeug.middleware.proxy_fix import ProxyFix

from src.config.settings import Config
from src.services.optimization_service import OptimizationService
from src.utils.validators import validate_request_data
from src.utils.presets import get_presets_dict


def create_api_app(config_class=None):
    app = Flask(__name__)
    
    if config_class:
        app.config.from_object(config_class)
    
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1, x_host=1, x_prefix=1)
    
    api = Api(
        app,
        version='2.0.0',
        title='API de Otimização de Prompts',
        description='''
        API REST para otimização de prompts e textos para IA.
        
        Esta API oferece várias técnicas de otimização:
        - **Tradução automática** para inglês (mais eficiente para LLMs)
        - **Compressão inteligente** de palavras mantendo legibilidade  
        - **Remoção de stop words** (palavras vazias)
        - **Remoção de acentos** e pontuação redundante
        - **Presets predefinidos** para diferentes níveis de otimização
        
        Todas as operações mantêm o significado original do texto.
        ''',
        doc='/docs/', 
        prefix='/api/v1',
        validate=True,
        contact='Gustavo Henrique',
        contact_email='gustavohenriquefs@exemplo.com',
        license='MIT',
        authorizations={
            'apikey': {
                'type': 'apiKey',
                'in': 'header',
                'name': 'X-API-KEY'
            }
        }
    )
    
    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Origin', '*')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
        return response
    
    config = Config()
    optimizer = OptimizationService(config)
    
    
    optimization_config = api.model('OptimizationConfig', {
        'translate_to_english': fields.Boolean(
            description='Traduzir texto para inglês (mais eficiente para LLMs)',
            default=False,
            example=True
        ),
        'language': fields.String(
            description='Idioma do texto original',
            default='pt',
            enum=['pt', 'en', 'es', 'fr'],
            example='pt'
        ),
        'stop_word_removal': fields.Float(
            description='Proporção de stop words a remover (0.0 = nenhuma, 1.0 = todas)',
            default=0.0,
            min=0.0,
            max=1.0,
            example=0.3
        ),
        'remove_accents': fields.Boolean(
            description='Remover acentos e caracteres especiais',
            default=False,
            example=True
        ),
        'word_compression': fields.Float(
            description='Proporção de caracteres a manter por palavra (0.1 = 10% dos chars)',
            default=1.0,
            min=0.1,
            max=1.0,
            example=0.7
        ),
        'min_word_length': fields.Integer(
            description='Tamanho mínimo das palavras após compressão',
            default=2,
            min=1,
            max=10,
            example=3
        ),
        'remove_punctuation': fields.Boolean(
            description='Remover pontuação desnecessária',
            default=False,
            example=False
        )
    })
    
    optimization_request = api.model('OptimizationRequest', {
        'text': fields.String(
            required=True,
            description='Texto a ser otimizado',
            example='Este é um exemplo de texto que será otimizado para reduzir tokens.'
        ),
        'preset': fields.String(
            description='Preset predefinido (ignora config se especificado)',
            enum=['conservative', 'moderate', 'aggressive', 'translation_only'],
            example='moderate'
        ),
        **optimization_config
    })
    
    optimization_stats = api.model('OptimizationStats', {
        'original_length': fields.Integer(
            description='Número de caracteres do texto original',
            example=85
        ),
        'optimized_length': fields.Integer(
            description='Número de caracteres do texto otimizado',
            example=52
        ),
        'compression_ratio_percent': fields.Float(
            description='Percentual de redução de caracteres',
            example=38.82
        ),
        'characters_saved': fields.Integer(
            description='Número de caracteres economizados',
            example=33
        )
    })
    
    optimization_response = api.model('OptimizationResponse', {
        'original_text': fields.String(
            description='Texto original fornecido',
            example='Este é um exemplo de texto que será otimizado para reduzir tokens.'
        ),
        'optimized_text': fields.String(
            description='Texto após otimização',
            example='This is example text optimized to reduce tokens'
        ),
        'stats': fields.Nested(
            optimization_stats,
            description='Estatísticas da otimização'
        ),
        'config_used': fields.Nested(
            optimization_config,
            description='Configuração que foi aplicada'
        )
    })
    
    preset_config = api.model('PresetConfig', {
        'description': fields.String(
            description='Descrição do preset',
            example='Otimização moderada com tradução'
        ),
        'config': fields.Nested(
            optimization_config,
            description='Configurações do preset'
        )
    })
    
    error_response = api.model('ErrorResponse', {
        'error': fields.String(
            description='Mensagem de erro',
            example='Texto é obrigatório'
        ),
        'code': fields.String(
            description='Código do erro',
            example='VALIDATION_ERROR'
        )
    })
    
    health_response = api.model('HealthResponse', {
        'status': fields.String(
            description='Status da aplicação',
            example='healthy'
        ),
        'version': fields.String(
            description='Versão da API',
            example='2.0.0'
        ),
        'timestamp': fields.String(
            description='Timestamp da verificação',
            example='2025-08-27T10:30:00Z'
        )
    })
    
    
    optimization_ns = Namespace(
        'optimization',
        description='Operações de otimização de texto',
        path='/optimization'
    )
    
    config_ns = Namespace(
        'config',
        description='Configurações e presets',
        path='/config'
    )
    
    system_ns = Namespace(
        'system',
        description='Operações do sistema',
        path='/system'
    )
    
    
    @optimization_ns.route('/optimize')
    class OptimizeResource(Resource):
        @optimization_ns.doc('optimize_text')
        @optimization_ns.expect(optimization_request, validate=True)
        @optimization_ns.response(200, 'Sucesso', optimization_response)
        @optimization_ns.response(400, 'Erro de validação', error_response)
        @optimization_ns.response(500, 'Erro interno do servidor', error_response)
        def post(self):
            try:
                data = api.payload
                
                error_message = validate_request_data(data)
                if error_message:
                    return {'error': error_message, 'code': 'VALIDATION_ERROR'}, 400
                
                text = data['text']
                
                manual_config = {k: v for k, v in data.items() if k not in ['text', 'preset']}
                
                if 'preset' in data:
                    presets = get_presets_dict()
                    if data['preset'] not in presets:
                        return {
                            'error': f"Preset '{data['preset']}' não encontrado",
                            'code': 'INVALID_PRESET'
                        }, 400
                    
                    config_options = presets[data['preset']]['config'].copy()
                    config_options.update(manual_config) 
                else:
                    config_options = manual_config
                
                result = optimizer.optimize(text, config_options)
                
                return {
                    'original_text': result.original_text,
                    'optimized_text': result.optimized_text,
                    'stats': {
                        'original_length': result.stats.original_length,
                        'optimized_length': result.stats.optimized_length,
                        'compression_ratio_percent': result.stats.compression_ratio_percent,
                        'characters_saved': result.stats.characters_saved
                    },
                    'config_used': result.config_used
                }, 200
                
            except Exception as e:
                return {
                    'error': 'Erro interno no processamento',
                    'code': 'INTERNAL_ERROR'
                }, 500
    
    @config_ns.route('/presets')
    class PresetsResource(Resource):
        @config_ns.doc('get_presets')
        @config_ns.response(200, 'Sucesso', fields.Raw)
        def get(self):
            return get_presets_dict(), 200
    
    @config_ns.route('/presets/<string:preset_name>')
    class PresetResource(Resource):
        @config_ns.doc('get_preset')
        @config_ns.response(200, 'Sucesso', preset_config)
        @config_ns.response(404, 'Preset não encontrado', error_response)
        def get(self, preset_name):
            presets = get_presets_dict()
            if preset_name not in presets:
                return {
                    'error': f"Preset '{preset_name}' não encontrado",
                    'code': 'PRESET_NOT_FOUND'
                }, 404
            
            return presets[preset_name], 200
    
    @system_ns.route('/health')
    class HealthResource(Resource):
        @system_ns.doc('health_check')
        @system_ns.response(200, 'Sistema saudável', health_response)
        def get(self):
            from datetime import datetime, timezone
            return {
                'status': 'healthy',
                'version': '2.0.0',
                'timestamp': datetime.now(timezone.utc).isoformat()
            }, 200
    
    api.add_namespace(optimization_ns)
    api.add_namespace(config_ns)  
    api.add_namespace(system_ns)
    
    
    from werkzeug.exceptions import BadRequest
    from jsonschema.exceptions import ValidationError
    
    @api.errorhandler(BadRequest)
    def handle_bad_request(error):
        return {'error': 'Dados de entrada inválidos', 'code': 'INVALID_REQUEST'}, 400
    
    @api.errorhandler(ValidationError)
    def handle_validation_error(error):
        return {'error': f'Erro de validação: {error.message}', 'code': 'VALIDATION_ERROR'}, 400
    
    @api.errorhandler(ValueError)
    def handle_value_error(error):
        return {'error': str(error), 'code': 'VALUE_ERROR'}, 400
    
    @api.errorhandler(KeyError)
    def handle_key_error(error):
        return {'error': f'Campo obrigatório: {error}', 'code': 'MISSING_FIELD'}, 400
    
    @api.errorhandler(Exception)
    def handle_generic_error(error):
        return {'error': 'Erro interno do servidor', 'code': 'INTERNAL_ERROR'}, 500
    
    return app


if __name__ == '__main__':
    app = create_api_app()
    print("🚀 API de Otimização v2.0 com Documentação")
    print("📚 Documentação: http://localhost:5000/docs/")
    print("🔗 API Base: http://localhost:5000/api/v1/")
    print("💚 Health: http://localhost:5000/api/v1/system/health")
    app.run(host='0.0.0.0', port=5000, debug=True)
