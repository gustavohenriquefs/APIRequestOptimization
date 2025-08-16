@echo off
echo === Executando Testes da API ===
echo.

REM Ativa o ambiente virtual
call venv\Scripts\activate.bat

REM Executa os testes
echo Executando testes unitarios...
python -m pytest tests/ -v

echo.
echo Executando teste da API (servidor deve estar rodando)...
python test_api.py

pause
