@echo off
echo === Iniciando API de Otimizacao de Prompts ===
echo.

REM Ativa o ambiente virtual
call venv\Scripts\activate

REM Verifica se o ambiente foi ativado corretamente
if "%VIRTUAL_ENV%"=="" (
    echo Erro: Nao foi possivel ativar o ambiente virtual
    pause
    exit /b 1
)

echo Ambiente virtual ativado: %VIRTUAL_ENV%
echo.

REM Executa a aplicação
echo Iniciando servidor Flask...
python main.py

pause
