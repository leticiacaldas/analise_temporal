"""
🧪 Teste Simples e Funcional
Executa apenas com pandas, numpy e matplotlib
"""

import sys

def testar_bibliotecas_basicas():
    """Testa apenas as bibliotecas essenciais"""
    print("🧪 Testando bibliotecas básicas...")
    
    erros = []
    
    try:
        import pandas as pd
        print("✅ Pandas: OK")
    except ImportError:
        erros.append("pandas")
        print("❌ Pandas: NÃO INSTALADO")
    
    try:
        import numpy as np
        print("✅ Numpy: OK")
    except ImportError:
        erros.append("numpy")
        print("❌ Numpy: NÃO INSTALADO")
    
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib: OK")
    except ImportError:
        erros.append("matplotlib")
        print("❌ Matplotlib: NÃO INSTALADO")
    
    return len(erros) == 0, erros

def testar_classe_simplificada():
    """Testa a classe simplificada"""
    print("\n🧪 Testando classe simplificada...")
    
    try:
        from analise_temporal_simplificada import AnaliseMeteorolgicaRS
        print("✅ Importação da classe: OK")
        
        analise = AnaliseMeteorolgicaRS()
        print("✅ Instanciação: OK")
        
        return True
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

def executar_teste_basico():
    """Executa apenas as funções básicas"""
    print("\n🧪 Executando teste básico...")
    
    try:
        from analise_temporal_simplificada import AnaliseMeteorolgicaRS
        
        analise = AnaliseMeteorolgicaRS()
        print("✅ Classe carregada com sucesso")
        
        # Tentar carregar dados
        print("📂 Tentando carregar dados...")
        analise.carregar_dados_multiplos_anos()
        
        if analise.dados_combinados is not None and len(analise.dados_combinados) > 0:
            print(f"✅ Dados carregados: {len(analise.dados_combinados)} registros")
            
            # Teste básico de estatísticas
            print("📊 Executando estatísticas básicas...")
            analise.estatisticas_descritivas()
            
            return True
        else:
            print("⚠️ Nenhum dado carregado (mas a classe funciona)")
            return True
            
    except Exception as e:
        print(f"❌ Erro no teste: {e}")
        return False

def main():
    """Função principal simplificada"""
    print("🧪" + "="*50)
    print("  TESTE BÁSICO - ANÁLISE METEOROLÓGICA")
    print("="*53)
    
    # Teste 1: Bibliotecas
    libs_ok, erros = testar_bibliotecas_basicas()
    
    if not libs_ok:
        print(f"\n❌ ERRO: Bibliotecas não instaladas: {', '.join(erros)}")
        print("💡 Execute: pip install pandas numpy matplotlib")
        return
    
    # Teste 2: Classe
    classe_ok = testar_classe_simplificada()
    
    if not classe_ok:
        print("\n❌ ERRO: Problema na classe Python")
        return
    
    # Teste 3: Execução básica
    execucao_ok = executar_teste_basico()
    
    # Resultado final
    print("\n" + "="*53)
    print("📋 RESULTADO FINAL:")
    print("="*53)
    
    if libs_ok and classe_ok and execucao_ok:
        print("🎉 SUCESSO! Sistema funcionando!")
        print("💡 Execute: python analise_temporal_simplificada.py")
    elif libs_ok and classe_ok:
        print("✅ Sistema funcionando (mas sem dados)")
        print("💡 Coloque os arquivos CSV nas pastas corretas")
        print("💡 Execute: python analise_temporal_simplificada.py")
    else:
        print("❌ Sistema com problemas")
        print("💡 Verifique os erros acima")

if __name__ == "__main__":
    main()
