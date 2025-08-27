"""
Ponto de entrada principal da aplicação com documentação automática.
"""
import os
import sys

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from src.app import create_api_app


if __name__ == '__main__':
    app = create_api_app()
    
    print("=" * 60)
    print("🚀 API DE OTIMIZAÇÃO DE PROMPTS v2.0")
    print("=" * 60)
    print(f"📚 Documentação Swagger: http://localhost:5000/docs/")
    print(f"🔗 API Base URL:         http://localhost:5000/api/v1/")
    print(f"💚 Health Check:        http://localhost:5000/api/v1/system/health")
    print(f"⚙️  Presets:             http://localhost:5000/api/v1/config/presets")
    print(f"🎯 Endpoint Principal:   http://localhost:5000/api/v1/optimization/optimize")
    print("=" * 60)
    print("🏃 Iniciando servidor...")
    
    app.run(host='0.0.0.0', port=5000, debug=True)
