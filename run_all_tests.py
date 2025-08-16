"""
Script completo de testes da aplicação.
"""
import sys
import subprocess

def run_command(command, description):
    """Executa um comando e mostra o resultado."""
    print(f"\n{'='*60}")
    print(f"Testando: {description}")
    print(f"{'='*60}")
    
    try:
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            cwd="."
        )
        
        if result.returncode == 0:
            print(f"[OK] {description} - PASSOU")
            if result.stdout:
                print(result.stdout)
        else:
            print(f"[ERRO] {description} - FALHOU")
            if result.stderr:
                print(f"Erro: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"[ERRO] Erro ao executar {description}: {e}")
        return False
        
    return True

def main():
    """Executa todos os testes da aplicação."""
    print("EXECUTANDO BATERIA COMPLETA DE TESTES")
    print("="*60)
    
    python_path = "C:/Workspace/Projects/ApiReduceCostLLM/venv/Scripts/python.exe"
    
    tests = [
        (f"{python_path} -m pytest tests/ -v", "Testes Unitarios"),
        (f"{python_path} test_components.py", "Teste dos Componentes"),
        (f"{python_path} test_flask_app.py", "Teste da Aplicacao Flask")
    ]
    
    passed = 0
    total = len(tests)
    
    for command, description in tests:
        if run_command(command, description):
            passed += 1
    
    print(f"\n{'='*60}")
    print(f"RESUMO DOS TESTES")
    print(f"{'='*60}")
    print(f"Total de testes: {total}")
    print(f"Passaram: {passed}")
    print(f"Falharam: {total - passed}")
    
    if passed == total:
        print(f"\nSUCESSO: TODOS OS TESTES PASSARAM! Aplicacao esta funcionando perfeitamente!")
        return 0
    else:
        print(f"\nAVISO: {total - passed} teste(s) falharam. Verifique os erros acima.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
