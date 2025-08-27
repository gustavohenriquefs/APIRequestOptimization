# 🧪 **Estrutura de Testes - ApiReduceCostLLM**

## 📁 **Organização**

```
tests/
├── conftest.py              # Fixtures compartilhadas
├── fixtures/                # Dados de teste (vazio por enquanto)
│
├── unit/                    # Testes unitários
│   ├── test_optimization_core.py      # Funcionalidades principais
│   ├── test_specialized_services.py   # Serviços especializados  
│   └── test_edge_cases.py             # Casos específicos e edge cases
│
└── integration/             # Testes de integração
    ├── test_flask_api.py              # API Flask endpoints
    └── test_performance.py            # Performance e benchmarks
```

## 🎯 **Tipos de Testes**

### **Unit Tests (Testes Unitários)**
- **test_optimization_core.py**: Funcionalidades principais do `OptimizationService`
- **test_specialized_services.py**: `AbbreviationService` e `EntityPreservationService`
- **test_edge_cases.py**: Casos específicos como variações de localização, preservação de números, compressão de palavras

### **Integration Tests (Testes de Integração)**
- **test_flask_api.py**: Endpoints da API, validação, cenários complexos
- **test_performance.py**: Performance, benchmarks, qualidade da otimização

## 🚀 **Como Executar**

### **Todos os testes**
```bash
pytest tests/
```

### **Apenas testes unitários**
```bash
pytest tests/unit/
```

### **Apenas testes de integração**
```bash
pytest tests/integration/
```

### **Teste específico**
```bash
pytest tests/unit/test_optimization_core.py::TestOptimizationServiceCore::test_compress_word_preserves_order
```

### **Com relatório de cobertura**
```bash
pytest tests/ --cov=src --cov-report=html
```

## 📊 **Cobertura Atual**

Os testes cobrem:

### **✅ Funcionalidades Principais**
- ✅ Remoção de acentos e espaços excessivos
- ✅ Compressão de palavras com preservação da ordem
- ✅ Otimização básica e avançada de texto
- ✅ Configurações de presets vs manuais

### **✅ Serviços Especializados**
- ✅ Abreviações de tecnologia, localização, animais, medidas
- ✅ Preservação de entidades (números, locais, tecnologias, animais)
- ✅ Níveis de preservação (Never, Low, Medium, High)

### **✅ Casos Edge**
- ✅ Variações de capitalização em localizações (Ceará/ceara/Ceara)
- ✅ Preservação de números importantes vs não importantes
- ✅ Compressão mantendo legibilidade (viralata → virlta, não vrltia)
- ✅ Palavras curtas não comprimidas
- ✅ Precedência de configurações manuais sobre presets

### **✅ API Flask**
- ✅ Health check endpoint
- ✅ Presets endpoint
- ✅ Optimization endpoint com validação
- ✅ Documentação Swagger
- ✅ Cenários complexos com múltiplas funcionalidades

### **✅ Performance**
- ✅ Tempo de processamento aceitável
- ✅ Consistência de resultados
- ✅ Eficiência por nível de compressão
- ✅ Qualidade e precisão da otimização

## 📋 **Fixtures Disponíveis**

- **app**: Aplicação Flask para testes
- **client**: Cliente de teste Flask
- **config**: Configuração de teste
- **optimization_service**: Instância do OptimizationService
- **sample_texts**: Textos de exemplo para diferentes cenários
- **preset_configs**: Configurações de presets para testes

## 🐛 **Bugs Cobertos**

### **Bug #1**: Preset overriding manual configs
- **Problema**: `gato` com `min_word_length=3` virava `ca`
- **Solução**: Precedência de configurações manuais
- **Teste**: `test_manual_config_overrides_preset`

### **Bug #2**: Word compression breaking letter order
- **Problema**: `viralata` virava `vrltia` (ordem quebrada)
- **Solução**: Algoritmo preserva ordem natural
- **Teste**: `test_compress_word_preserves_order`

## 📈 **Métricas de Qualidade**

- **22 testes passando** ✅
- **Cobertura**: Funcionalidades principais, serviços especializados, API
- **Performance**: < 5s para textos grandes
- **Qualidade**: Mantém legibilidade e preserva entidades importantes

## 🔮 **Próximos Passos**

1. **Vector Database Tests**: Quando implementar semantic optimization
2. **Load Tests**: Para avaliar comportamento sob carga
3. **Error Handling Tests**: Cenários de erro e recuperação
4. **Mock Tests**: Para isolamento de dependências externas
