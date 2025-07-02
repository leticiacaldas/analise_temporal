"""
🔧 Instalador Automático de Dependências
Instala todas as bibliotecas necessárias para o projeto
"""

import subprocess
import sys
import os

def instalar_biblioteca(nome_biblioteca):
    """Instala uma biblioteca usando pip"""
    try:
        print(f"📦 Instalando {nome_biblioteca}...")
        resultado = subprocess.run([
            sys.executable, "-m", "pip", "install", nome_biblioteca
        ], capture_output=True, text=True, check=True)
        
        print(f"✅ {nome_biblioteca} instalado com sucesso!")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar {nome_biblioteca}: {e}")
        print(f"   Saída do erro: {e.stderr}")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado ao instalar {nome_biblioteca}: {e}")
        return False

def verificar_biblioteca(nome_biblioteca, nome_import=None):
    """Verifica se uma biblioteca está instalada"""
    if nome_import is None:
        nome_import = nome_biblioteca
    
    try:
        __import__(nome_import)
        print(f"✅ {nome_biblioteca}: Já instalado")
        return True
    except ImportError:
        print(f"❌ {nome_biblioteca}: Não encontrado")
        return False

def main():
    """Função principal"""
    print("🔧" + "="*50)
    print("  INSTALADOR DE DEPENDÊNCIAS METEOROLÓGICAS")
    print("="*53)
    
    # Lista de bibliotecas necessárias
    bibliotecas = [
        ("pandas", "pandas"),
        ("numpy", "numpy"),
        ("matplotlib", "matplotlib"),
        ("seaborn", "seaborn"),
        ("scikit-learn", "sklearn"),
        ("plotly", "plotly"),
        ("scipy", "scipy")
    ]
    
    print("\n🔍 Verificando bibliotecas existentes...")
    print("-" * 40)
    
    bibliotecas_faltantes = []
    
    for nome_pip, nome_import in bibliotecas:
        if not verificar_biblioteca(nome_pip, nome_import):
            bibliotecas_faltantes.append(nome_pip)
    
    if not bibliotecas_faltantes:
        print("\n🎉 Todas as bibliotecas já estão instaladas!")
        print("   Você pode executar: python analise_temporal.py")
        return
    
    print(f"\n📦 Encontradas {len(bibliotecas_faltantes)} bibliotecas para instalar:")
    for lib in bibliotecas_faltantes:
        print(f"   • {lib}")
    
    resposta = input("\n❓ Deseja instalar automaticamente? (s/n): ").lower()
    
    if resposta != 's':
        print("❌ Instalação cancelada pelo usuário.")
        print("💡 Para instalar manualmente:")
        for lib in bibliotecas_faltantes:
            print(f"   pip install {lib}")
        return
    
    print("\n🚀 Iniciando instalação...")
    print("=" * 40)
    
    sucessos = 0
    falhas = 0
    
    for biblioteca in bibliotecas_faltantes:
        if instalar_biblioteca(biblioteca):
            sucessos += 1
        else:
            falhas += 1
        print()  # Linha em branco para separar
    
    # Resumo final
    print("=" * 40)
    print("📋 RESUMO DA INSTALAÇÃO:")
    print("=" * 40)
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    
    if falhas == 0:
        print("\n🎉 Todas as bibliotecas foram instaladas com sucesso!")
        print("   Agora você pode executar:")
        print("   • python analise_temporal.py")
        print("   • python exemplo_rapido.py")
        print("   • python teste_sistema.py")
    else:
        print(f"\n⚠️ {falhas} biblioteca(s) falharam na instalação.")
        print("💡 Tente instalar manualmente as que falharam:")
        print("   pip install <nome_da_biblioteca>")
    
    print("\n🔄 Executando verificação final...")
    subprocess.run([sys.executable, "teste_sistema.py"])

if __name__ == "__main__":
    main()
