"""
🧪 Teste Básico do Sistema
Verifica se o código está funcionando corretamente
"""

import sys
import os

def testar_importacoes():
    """Testa se todas as bibliotecas necessárias estão disponíveis"""
    print("🧪 Testando importações...")
    
    try:
        import pandas as pd
        print("✅ Pandas: OK")
    except ImportError as e:
        print(f"❌ Pandas: {e}")
        return False
    
    try:
        import numpy as np
        print("✅ Numpy: OK")
    except ImportError as e:
        print(f"❌ Numpy: {e}")
        return False
    
    try:
        import matplotlib.pyplot as plt
        print("✅ Matplotlib: OK")
    except ImportError as e:
        print(f"❌ Matplotlib: {e}")
        return False
    
    try:
        import seaborn as sns
        print("✅ Seaborn: OK")
    except ImportError as e:
        print(f"❌ Seaborn: {e}")
        return False
    
    try:
        import plotly.express as px
        print("✅ Plotly: OK")
    except ImportError as e:
        print(f"❌ Plotly: {e}")
        return False
    
    try:
        from sklearn.ensemble import RandomForestRegressor
        print("✅ Scikit-learn: OK")
    except ImportError as e:
        print(f"❌ Scikit-learn: {e}")
        return False
    
    try:
        from scipy import stats
        print("✅ Scipy: OK")
    except ImportError as e:
        print(f"❌ Scipy: {e}")
        return False
    
    return True

def testar_carregamento_classe():
    """Testa se a classe principal pode ser carregada"""
    print("\n🧪 Testando carregamento da classe...")
    
    try:
        from analise_temporal import AnaliseMeteorolgicaRS
        print("✅ Classe AnaliseMeteorolgicaRS: OK")
        
        # Tentar instanciar
        analise = AnaliseMeteorolgicaRS()
        print("✅ Instanciação da classe: OK")
        return True
        
    except Exception as e:
        print(f"❌ Erro ao carregar classe: {e}")
        return False

def testar_estrutura_arquivos():
    """Testa se a estrutura de arquivos está presente"""
    print("\n🧪 Testando estrutura de arquivos...")
    
    anos = ['2023', '2024', '2025']
    arquivos_encontrados = 0
    total_arquivos = 0
    
    for ano in anos:
        total_arquivos += 2  # Rio Grande + Capão do Leão
        
        if os.path.exists(ano):
            arquivos = os.listdir(ano)
            
            # Verificar Rio Grande
            if any('RIO GRANDE' in f for f in arquivos):
                print(f"✅ Rio Grande {ano}: Encontrado")
                arquivos_encontrados += 1
            else:
                print(f"❌ Rio Grande {ano}: Não encontrado")
            
            # Verificar Capão do Leão
            if any('CAPAO DO LEAO' in f for f in arquivos):
                print(f"✅ Capão do Leão {ano}: Encontrado")
                arquivos_encontrados += 1
            else:
                print(f"❌ Capão do Leão {ano}: Não encontrado")
        else:
            print(f"❌ Pasta {ano}: Não encontrada")
    
    print(f"\n📊 Arquivos encontrados: {arquivos_encontrados}/{total_arquivos}")
    return arquivos_encontrados > 0

def main():
    """Função principal de teste"""
    print("🧪" + "="*50)
    print("  TESTE DO SISTEMA DE ANÁLISE METEOROLÓGICA")
    print("="*53)
    
    # Testes
    print("Executando bateria de testes...\n")
    
    teste1 = testar_importacoes()
    teste2 = testar_carregamento_classe()
    teste3 = testar_estrutura_arquivos()
    
    # Resumo
    print("\n" + "="*53)
    print("📋 RESUMO DOS TESTES:")
    print("="*53)
    
    if teste1:
        print("✅ Bibliotecas: Todas instaladas corretamente")
    else:
        print("❌ Bibliotecas: Algumas não estão instaladas")
        print("💡 Execute: pip install -r requirements.txt")
    
    if teste2:
        print("✅ Código: Carregamento da classe funcionando")
    else:
        print("❌ Código: Problema no carregamento da classe")
    
    if teste3:
        print("✅ Dados: Arquivos CSV encontrados")
    else:
        print("❌ Dados: Arquivos CSV não encontrados")
        print("💡 Certifique-se de que os arquivos estão nas pastas corretas")
    
    # Conclusão
    if teste1 and teste2:
        print("\n🎉 Sistema pronto para uso!")
        if teste3:
            print("   Execute: python executar_analise.py")
        else:
            print("   ⚠️ Mas você precisa dos arquivos CSV para análise completa")
    else:
        print("\n⚠️ Sistema com problemas. Resolva os erros acima.")

if __name__ == "__main__":
    main()
