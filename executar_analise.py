"""
🌤️ Script de Execução Rápida - Análise Meteorológica
Executa análises específicas conforme necessidade do usuário
"""

from analise_temporal import AnaliseMeteorolgicaRS
import sys
import os

def menu_principal():
    """Menu interativo para escolher análises"""
    print("🌤️" + "="*50)
    print("  ANÁLISE METEOROLÓGICA - MENU PRINCIPAL")
    print("="*53)
    print("1. 🚀 Análise Completa (tudo)")
    print("2. 📊 Apenas Estatísticas Descritivas")
    print("3. 🔄 Apenas Comparação entre Cidades")
    print("4. 🌿 Apenas Análise de Sazonalidade")
    print("5. 📈 Apenas Visualizações Interativas")
    print("6. 🎨 Apenas Visualizações Estáticas")
    print("7. 🤖 Apenas Modelo de Previsão")
    print("8. 🔍 Apenas Insights Finais")
    print("0. ❌ Sair")
    print("="*53)
    
    return input("Escolha uma opção (0-8): ").strip()

def executar_analise_escolhida(opcao):
    """Executa a análise baseada na escolha do usuário"""
    
    # Inicializar análise
    analise = AnaliseMeteorolgicaRS()
    
    try:
        if opcao == "1":
            print("\n🚀 Executando Análise Completa...")
            modelo = analise.relatorio_completo()
            return modelo
            
        elif opcao == "2":
            print("\n📊 Carregando dados e gerando estatísticas...")
            analise.carregar_dados_multiplos_anos()
            analise.estatisticas_descritivas()
            
        elif opcao == "3":
            print("\n🔄 Carregando dados e comparando cidades...")
            analise.carregar_dados_multiplos_anos()
            analise.comparacao_cidades()
            
        elif opcao == "4":
            print("\n🌿 Carregando dados e analisando sazonalidade...")
            analise.carregar_dados_multiplos_anos()
            analise.analise_sazonalidade()
            
        elif opcao == "5":
            print("\n📈 Carregando dados e criando visualizações interativas...")
            analise.carregar_dados_multiplos_anos()
            analise.visualizacoes_comparativas_avancadas()
            
        elif opcao == "6":
            print("\n🎨 Carregando dados e criando visualizações estáticas...")
            analise.carregar_dados_multiplos_anos()
            try:
                from visualizacoes_matplotlib import criar_visualizacoes_completas
                criar_visualizacoes_completas(analise.dados_combinados)
            except ImportError:
                print("❌ Módulo de visualizações matplotlib não encontrado!")
                
        elif opcao == "7":
            print("\n🤖 Carregando dados e treinando modelo...")
            analise.carregar_dados_multiplos_anos()
            modelo = analise.modelo_previsao_temperatura()
            return modelo
            
        elif opcao == "8":
            print("\n🔍 Carregando dados e gerando insights...")
            analise.carregar_dados_multiplos_anos()
            analise.gerar_insights_finais()
            
        elif opcao == "0":
            print("👋 Saindo... Até logo!")
            return None
            
        else:
            print("❌ Opção inválida! Tente novamente.")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        print("💡 Verifique se os arquivos de dados estão no local correto.")
        return False
    
    print("✅ Operação concluída com sucesso!")
    return True

def verificar_estrutura_arquivos():
    """Verifica se a estrutura de arquivos está correta"""
    print("🔍 Verificando estrutura de arquivos...")
    
    anos = ['2023', '2024', '2025']
    arquivos_encontrados = []
    arquivos_faltando = []
    
    for ano in anos:
        # Verificar Rio Grande
        arquivo_rg = f"{ano}/INMET_S_RS_A802_RIO GRANDE_01-01-{ano}_A_*.CSV"
        if os.path.exists(ano) and any(f.startswith("INMET_S_RS_A802_RIO GRANDE") for f in os.listdir(ano)):
            arquivos_encontrados.append(f"✅ Rio Grande {ano}")
        else:
            arquivos_faltando.append(f"❌ Rio Grande {ano}")
        
        # Verificar Capão do Leão
        arquivo_cl = f"{ano}/INMET_S_RS_A887_CAPAO DO LEAO"
        if os.path.exists(ano) and any(f.startswith("INMET_S_RS_A887_CAPAO DO LEAO") for f in os.listdir(ano)):
            arquivos_encontrados.append(f"✅ Capão do Leão {ano}")
        else:
            arquivos_faltando.append(f"❌ Capão do Leão {ano}")
    
    print("\n📁 Status dos arquivos:")
    for arquivo in arquivos_encontrados:
        print(f"   {arquivo}")
    
    if arquivos_faltando:
        print("\n⚠️  Arquivos não encontrados:")
        for arquivo in arquivos_faltando:
            print(f"   {arquivo}")
        print("\n💡 Certifique-se de que os arquivos CSV estão nas pastas corretas.")
        return False
    
    print("\n✅ Todos os arquivos encontrados!")
    return True

def main():
    """Função principal"""
    print("🌤️ Bem-vindo ao Sistema de Análise Meteorológica!")
    print("   Comparação entre Rio Grande e Capão do Leão - RS")
    
    # Verificar arquivos
    if not verificar_estrutura_arquivos():
        resposta = input("\n❓ Deseja continuar mesmo assim? (s/n): ").lower()
        if resposta != 's':
            print("👋 Saindo...")
            return
    
    # Loop principal
    while True:
        opcao = menu_principal()
        
        if opcao == "0":
            print("👋 Obrigado por usar o sistema! Até logo!")
            break
            
        resultado = executar_analise_escolhida(opcao)
        
        if resultado is False:
            continue
        elif resultado is None:
            break
        
        # Perguntar se quer continuar
        print("\n" + "-"*50)
        continuar = input("❓ Deseja executar outra análise? (s/n): ").lower()
        if continuar != 's':
            print("👋 Obrigado por usar o sistema! Até logo!")
            break

if __name__ == "__main__":
    main()
