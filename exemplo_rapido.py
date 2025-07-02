"""
🚀 Exemplo Rápido de Análise Meteorológica
Demonstra as principais funcionalidades do sistema
"""

from analise_temporal import AnaliseMeteorolgicaRS

def exemplo_rapido():
    """Executa um exemplo rápido das principais funcionalidades"""
    
    print("🌤️" + "="*60)
    print("  EXEMPLO RÁPIDO - ANÁLISE METEOROLÓGICA")
    print("="*63)
    
    # Criar instância da análise
    print("🚀 Inicializando sistema de análise...")
    analise = AnaliseMeteorolgicaRS()
    
    try:
        # Carregar dados
        print("📂 Carregando dados meteorológicos...")
        analise.carregar_dados_multiplos_anos()
        
        if analise.dados_combinados is not None and len(analise.dados_combinados) > 0:
            print(f"✅ Dados carregados: {len(analise.dados_combinados)} registros")
            
            # Estatísticas básicas
            print("\n📊 Gerando estatísticas descritivas...")
            analise.estatisticas_descritivas()
            
            # Comparação entre cidades
            print("\n🔄 Comparando cidades estatisticamente...")
            analise.comparacao_cidades()
            
            # Análise sazonal
            print("\n🌿 Analisando padrões sazonais...")
            analise.analise_sazonalidade()
            
            # Modelo de previsão
            print("\n🤖 Treinando modelo de previsão...")
            modelo = analise.modelo_previsao_temperatura()
            
            # Insights finais
            print("\n🔍 Gerando insights finais...")
            analise.gerar_insights_finais()
            
            print("\n✅ Exemplo executado com sucesso!")
            print("💡 Para visualizações, execute: analise.visualizacoes_comparativas_avancadas()")
            
            return analise, modelo
            
        else:
            print("❌ Nenhum dado foi carregado.")
            print("💡 Verifique se os arquivos CSV estão nas pastas corretas.")
            return None, None
            
    except Exception as e:
        print(f"❌ Erro durante a execução: {e}")
        print("💡 Verifique se as dependências estão instaladas: pip install -r requirements.txt")
        return None, None

def exemplo_visualizacoes(analise):
    """Executa apenas as visualizações se os dados estão carregados"""
    
    if analise is None or analise.dados_combinados is None:
        print("❌ Dados não carregados. Execute exemplo_rapido() primeiro.")
        return
    
    print("\n🎨 Criando visualizações...")
    
    try:
        # Visualizações interativas
        print("📈 Gerando gráficos interativos (Plotly)...")
        analise.visualizacoes_comparativas_avancadas()
        
        # Visualizações estáticas
        try:
            from visualizacoes_matplotlib import criar_visualizacoes_completas
            print("🎨 Gerando dashboard estático (Matplotlib)...")
            criar_visualizacoes_completas(analise.dados_combinados)
        except ImportError:
            print("⚠️ Visualizações matplotlib não disponíveis")
        
        print("✅ Visualizações criadas com sucesso!")
        
    except Exception as e:
        print(f"❌ Erro nas visualizações: {e}")

if __name__ == "__main__":
    print("🌤️ Executando exemplo rápido da análise meteorológica...\n")
    
    # Executar exemplo
    analise, modelo = exemplo_rapido()
    
    # Perguntar sobre visualizações
    if analise is not None:
        resposta = input("\n❓ Deseja ver as visualizações? (s/n): ").lower()
        if resposta == 's':
            exemplo_visualizacoes(analise)
    
    print("\n👋 Exemplo concluído! Obrigado por usar o sistema.")
