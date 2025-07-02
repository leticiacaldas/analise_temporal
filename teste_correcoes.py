#!/usr/bin/env python3
"""
Teste das correções no arquivo analise_temporal.py
"""

def teste_imports():
    """Testa se todos os imports funcionam"""
    print("🔍 Testando imports...")
    
    try:
        from analise_temporal import AnaliseMeteorolgicaRS
        print("✅ Import da classe principal: OK")
    except ImportError as e:
        print(f"❌ Erro no import da classe: {e}")
        return False
    
    try:
        # Testar criação da instância
        analise = AnaliseMeteorolgicaRS()
        print("✅ Criação da instância: OK")
    except Exception as e:
        print(f"❌ Erro na criação da instância: {e}")
        return False
    
    return True

def teste_verificacao_bibliotecas():
    """Testa se as verificações de bibliotecas funcionam"""
    print("\n🔍 Testando verificações de bibliotecas...")
    
    try:
        from analise_temporal import SKLEARN_DISPONIVEL, PLOTLY_DISPONIVEL, SCIPY_DISPONIVEL
        print(f"✅ Scikit-learn disponível: {SKLEARN_DISPONIVEL}")
        print(f"✅ Plotly disponível: {PLOTLY_DISPONIVEL}")
        print(f"✅ SciPy disponível: {SCIPY_DISPONIVEL}")
    except ImportError as e:
        print(f"❌ Erro nas verificações: {e}")
        return False
    
    return True

def teste_metodos_basicos():
    """Testa métodos básicos sem necessidade de dados"""
    print("\n🔍 Testando métodos básicos...")
    
    try:
        from analise_temporal import AnaliseMeteorolgicaRS
        analise = AnaliseMeteorolgicaRS()
        
        # Testar métodos que devem funcionar mesmo sem dados
        print("Testando estatísticas_descritivas...")
        analise.estatisticas_descritivas()
        
        print("✅ Métodos básicos: OK")
    except Exception as e:
        print(f"❌ Erro nos métodos básicos: {e}")
        return False
    
    return True

def main():
    """Executa todos os testes"""
    print("🚀 Iniciando testes de correções...")
    print("=" * 50)
    
    todos_ok = True
    
    # Teste 1: Imports
    if not teste_imports():
        todos_ok = False
    
    # Teste 2: Verificações de bibliotecas
    if not teste_verificacao_bibliotecas():
        todos_ok = False
    
    # Teste 3: Métodos básicos
    if not teste_metodos_basicos():
        todos_ok = False
    
    print("\n" + "=" * 50)
    if todos_ok:
        print("🎉 TODOS OS TESTES PASSARAM!")
        print("✅ O arquivo analise_temporal.py está funcionando corretamente.")
    else:
        print("❌ ALGUNS TESTES FALHARAM!")
        print("⚠️ Verifique os erros acima.")

if __name__ == "__main__":
    main()
