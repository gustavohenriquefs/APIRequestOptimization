# API de Redução de Custo para LLM

Esta API foi desenvolvida para otimizar prompts e textos, reduzindo o número de caracteres e, consequentemente, os custos de uso com modelos de linguagem grandes (LLMs).

## Estrutura do Projeto

```
ApiReduceCostLLM/
├── src/
│   ├── config/
│   │   ├── __init__.py
│   │   └── settings.py          # Configurações da aplicação
│   ├── models/
│   │   ├── __init__.py
│   │   └── optimization.py      # Modelos de dados
│   ├── services/
│   │   ├── __init__.py
│   │   ├── translation_service.py    # Serviço de tradução
│   │   └── optimization_service.py   # Lógica de otimização
│   ├── controllers/
│   │   ├── __init__.py
│   │   └── optimization_controller.py # Controladores da API
│   ├── utils/
│   │   ├── __init__.py
│   │   ├── validators.py        # Validações de dados
│   │   └── presets.py          # Configurações pré-definidas
│   ├── __init__.py
│   └── app.py                  # Aplicação Flask principal
├── tests/
│   ├── __init__.py
│   ├── test_optimization_service.py      # Testes unitários do serviço
│   ├── test_components_integration.py    # Testes de integração dos componentes
│   └── test_flask_integration.py         # Testes de integração da API Flask
├── venv/                       # Ambiente virtual Python
├── requirements.txt
├── main.py                     # Ponto de entrada
└── README.md
```

## Instalação

1. **Clone o repositório e navegue para o diretório:**
   ```bash
   cd ApiReduceCostLLM
   ```

2. **Ative o ambiente virtual:**
   ```bash
   # Windows
   .\venv\Scripts\activate
   
   # Linux/Mac
   source venv/bin/activate
   ```

3. **Instale as dependências:**
   ```bash
   pip install -r requirements.txt
   ```

## Executando a Aplicação

### 🚀 API com Documentação Automática
```bash
# Windows
./start

# Linux/Mac  
python main.py
```

**URLs da API:**
- **API Base**: `http://localhost:5000/api/v1/`
- **Documentação Swagger**: `http://localhost:5000/docs/`
- **Health Check**: `http://localhost:5000/api/v1/system/health`
- **Presets**: `http://localhost:5000/api/v1/config/presets`
export FLASK_ENV=development
flask run
```

### Usando Gunicorn (Produção)
```bash
gunicorn -w 4 -b 0.0.0.0:5000 "src.app:create_app()"
```

## Endpoints da API

### POST /optimize
Otimiza um texto de acordo com as configurações fornecidas.

**Corpo da requisição:**
```json
{
    "text": "Texto a ser otimizado",
    "config": {
        "translate_to_english": true,
        "remove_accents": true,
        "word_compression": 0.8,
        "min_word_length": 2,
        "stop_word_removal": 0.3,
        "remove_punctuation": false,
        "language": "pt"
    }
}
```

**Resposta:**
```json
{
    "original_text": "Texto original",
    "optimized_text": "Texto otimizado",
    "stats": {
        "original_length": 100,
        "optimized_length": 75,
        "compression_ratio_percent": 25.0,
        "characters_saved": 25
    },
    "config_used": {...}
}
```

### GET /presets
Retorna configurações pré-definidas para diferentes níveis de otimização.

**Resposta:**
```json
{
    "conservative": {
        "description": "Otimização leve...",
        "config": {...}
    },
    "moderate": {...},
    "aggressive": {...},
    "translation_only": {...}
}
```

### GET /health
Endpoint de verificação de saúde da API.

**Resposta:**
```json
{
    "status": "healthy",
    "version": "2.0.0"
}
```

## Configurações Disponíveis

- `translate_to_english`: Traduz o texto para inglês
- `remove_accents`: Remove acentos dos caracteres
- `word_compression`: Comprime palavras (0.0 a 1.0) - porcentagem de caracteres a manter
- `min_word_length`: Tamanho mínimo das palavras após compressão (padrão: 2)
- `stop_word_removal`: Remove palavras comuns (0.0 a 1.0)
- `remove_punctuation`: Remove pontuação
- `language`: Idioma do texto ('pt' ou 'en')

### Exemplo de Compressão com Tamanho Mínimo

```json
{
    "text": "Esta funcionalidade permite controlar melhor a compressão das palavras",
    "config": {
        "word_compression": 0.6,
        "min_word_length": 3,
        "remove_accents": true
    }
}
```

**Resultado:**
- `word_compression: 0.6` = mantém 60% dos caracteres de cada palavra
- `min_word_length: 3` = garante que nenhuma palavra fique com menos de 3 caracteres
- "funcionalidade" → "fncnldde" (respeitando o tamanho mínimo)

## Presets Disponíveis

- **Conservative**: Otimização leve
- **Moderate**: Balanceio entre economia e legibilidade
- **Aggressive**: Otimização máxima
- **Translation Only**: Apenas tradução para inglês

## Executando Testes

### Todos os testes:
```bash
pytest tests/ -v
```

### Testes específicos:
```bash
# Testes unitários do serviço de otimização
pytest tests/test_optimization_service.py -v

# Testes de integração dos componentes
pytest tests/test_components_integration.py -v

# Testes de integração da API Flask
pytest tests/test_flask_integration.py -v
```

### Estrutura de Testes:
- `test_optimization_service.py`: Testes unitários das funções core
- `test_components_integration.py`: Testes de integração entre componentes
- `test_flask_integration.py`: Testes da API usando Flask test client

## Variáveis de Ambiente

- `FLASK_ENV`: Ambiente da aplicação (development, production, testing)
- `FLASK_APP`: Módulo da aplicação Flask

## Arquitetura

O projeto segue uma arquitetura em camadas:

- **Config**: Configurações da aplicação
- **Models**: Modelos de dados
- **Services**: Lógica de negócio
- **Controllers**: Controladores da API
- **Utils**: Utilitários e helpers
