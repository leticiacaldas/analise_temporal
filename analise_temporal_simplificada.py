import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt
import warnings
import glob

warnings.filterwarnings("ignore")

# Imports condicionais para bibliotecas que podem não estar instaladas
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    SKLEARN_DISPONIVEL = True
except ImportError:
    SKLEARN_DISPONIVEL = False
    print("⚠️ Scikit-learn não instalado. Funcionalidades de ML desabilitadas.")

try:
    import plotly.express as px
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_DISPONIVEL = True
except ImportError:
    PLOTLY_DISPONIVEL = False
    print("⚠️ Plotly não instalado. Visualizações interativas desabilitadas.")

try:
    from scipy import stats
    SCIPY_DISPONIVEL = True
except ImportError:
    SCIPY_DISPONIVEL = False
    stats = None
    print("⚠️ Scipy não instalado. Testes estatísticos desabilitados.")

# Importar visualizações matplotlib
try:
    from visualizacoes_matplotlib import criar_visualizacoes_completas
    MATPLOTLIB_VIZ_DISPONIVEL = True
except ImportError:
    MATPLOTLIB_VIZ_DISPONIVEL = False
    print("⚠️ Módulo de visualizações matplotlib não encontrado.")

class AnaliseMeteorolgicaRS:
    def __init__(self):
        self.dados_rio_grande = []
        self.dados_capao_leao = []
        self.dados_combinados = None
        
    def carregar_dados_multiplos_anos(self):
        """Carrega dados de todos os anos disponíveis (2023, 2024, 2025)"""
        anos = ['2023', '2024', '2025']
        
        for ano in anos:
            # Rio Grande
            arquivo_rg = f"{ano}/INMET_S_RS_A802_RIO GRANDE_01-01-{ano}_A_*.CSV"
            arquivos_rg = glob.glob(arquivo_rg)
            
            if arquivos_rg:
                df_rg = self._processar_arquivo(arquivos_rg[0])
                if df_rg is not None:
                    df_rg['cidade'] = 'Rio Grande'
                    df_rg['ano'] = int(ano)
                    self.dados_rio_grande.append(df_rg)
            
            # Capão do Leão
            arquivo_cl = f"{ano}/INMET_S_RS_A887_CAPAO DO LEAO (PELOTAS)_01-01-{ano}_A_*.CSV"
            arquivos_cl = glob.glob(arquivo_cl)
            
            if arquivos_cl:
                df_cl = self._processar_arquivo(arquivos_cl[0])
                if df_cl is not None:
                    df_cl['cidade'] = 'Capão do Leão'
                    df_cl['ano'] = int(ano)
                    self.dados_capao_leao.append(df_cl)
        
        # Combinar todos os dados
        self._combinar_dados()
        print("✅ Dados carregados com sucesso!")
        print(f"   📊 Rio Grande: {len(self.dados_rio_grande)} arquivos")
        print(f"   📊 Capão do Leão: {len(self.dados_capao_leao)} arquivos")
    
    def _processar_arquivo(self, arquivo):
        """Processa um arquivo CSV individual"""
        try:
            # Ler arquivo pulando as linhas de metadados
            df = pd.read_csv(arquivo, sep=';', skiprows=8, encoding='latin-1')
            
            # Limpar nomes das colunas
            df.columns = df.columns.str.strip()
            
            # Criar datetime combinando data e hora
            df['datetime'] = pd.to_datetime(df['Data'] + ' ' + df['Hora UTC'], 
                                         format='%Y/%m/%d %H%M UTC', errors='coerce')
            
            # Selecionar e renomear colunas importantes
            colunas_importantes = [
                'Data', 'Hora UTC', 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
                'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)',
                'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
                'TEMPERATURA DO PONTO DE ORVALHO (°C)',
                'UMIDADE RELATIVA DO AR, HORARIA (%)',
                'VENTO, VELOCIDADE HORARIA (m/s)',
                'VENTO, DIREÇÃO HORARIA (gr) (° (gr))',
                'RADIACAO GLOBAL (Kj/m²)'
            ]
            
            # Verificar quais colunas existem
            colunas_existentes = [col for col in colunas_importantes if col in df.columns]
            df_processado = df[['datetime'] + colunas_existentes].copy()
            
            # Converter colunas numéricas
            for col in colunas_existentes:
                if col not in ['Data', 'Hora UTC']:
                    df_processado[col] = pd.to_numeric(df_processado[col], errors='coerce')
            
            # Remover linhas com datetime inválido
            df_processado = df_processado[df_processado['datetime'].notna()]
            
            return df_processado
            
        except (FileNotFoundError, pd.errors.EmptyDataError, UnicodeDecodeError) as e:
            print(f"Erro ao processar arquivo {arquivo}: {e}")
            return None
    
    def _combinar_dados(self):
        """Combina todos os dados em um único DataFrame"""
        if self.dados_rio_grande and self.dados_capao_leao:
            # Concatenar dados de Rio Grande
            df_rg_completo = pd.concat(self.dados_rio_grande, ignore_index=True)
            
            # Concatenar dados de Capão do Leão
            df_cl_completo = pd.concat(self.dados_capao_leao, ignore_index=True)
            
            # Combinar ambas as cidades
            self.dados_combinados = pd.concat([df_rg_completo, df_cl_completo], ignore_index=True)
            
            # Ordenar por datetime
            self.dados_combinados = self.dados_combinados.sort_values('datetime').reset_index(drop=True)
    
    def estatisticas_descritivas(self):
        """Gera estatísticas descritivas completas"""
        if self.dados_combinados is None:
            print("❌ Dados não carregados. Execute carregar_dados_multiplos_anos() primeiro.")
            return
        
        print("=" * 60)
        print("📊 ESTATÍSTICAS DESCRITIVAS METEOROLÓGICAS")
        print("=" * 60)
        
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = self.dados_combinados[self.dados_combinados['cidade'] == cidade]
            
            print(f"\n🏙️  {cidade.upper()}")
            print("-" * 40)
            
            # Temperatura
            if 'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)' in dados_cidade.columns:
                temp = dados_cidade['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].dropna()
                print("🌡️  Temperatura:")
                print(f"   Média: {temp.mean():.1f}°C")
                print(f"   Máxima: {temp.max():.1f}°C")
                print(f"   Mínima: {temp.min():.1f}°C")
                print(f"   Desvio Padrão: {temp.std():.1f}°C")
            
            # Precipitação
            if 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)' in dados_cidade.columns:
                precip = dados_cidade['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].dropna()
                print("🌧️  Precipitação:")
                print(f"   Total: {precip.sum():.1f}mm")
                print(f"   Média horária: {precip.mean():.2f}mm")
                print(f"   Máxima horária: {precip.max():.1f}mm")
            
            # Umidade
            if 'UMIDADE RELATIVA DO AR, HORARIA (%)' in dados_cidade.columns:
                umid = dados_cidade['UMIDADE RELATIVA DO AR, HORARIA (%)'].dropna()
                print("💧 Umidade:")
                print(f"   Média: {umid.mean():.1f}%")
                print(f"   Máxima: {umid.max():.1f}%")
                print(f"   Mínima: {umid.min():.1f}%")
            
            # Vento
            if 'VENTO, VELOCIDADE HORARIA (m/s)' in dados_cidade.columns:
                vento = dados_cidade['VENTO, VELOCIDADE HORARIA (m/s)'].dropna()
                print("💨 Vento:")
                print(f"   Velocidade média: {vento.mean():.1f}m/s")
                print(f"   Rajada máxima: {vento.max():.1f}m/s")
    
    def comparacao_cidades(self):
        """Compara estatisticamente as duas cidades"""
        if self.dados_combinados is None:
            print("❌ Dados não carregados.")
            return
        
        print("\n" + "=" * 60)
        print("🔄 COMPARAÇÃO ESTATÍSTICA ENTRE CIDADES")
        print("=" * 60)
        
        # Preparar dados para comparação
        rg_data = self.dados_combinados[self.dados_combinados['cidade'] == 'Rio Grande']
        cl_data = self.dados_combinados[self.dados_combinados['cidade'] == 'Capão do Leão']
        
        variaveis = [
            ('TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)', '🌡️ Temperatura'),
            ('PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', '🌧️ Precipitação'),
            ('UMIDADE RELATIVA DO AR, HORARIA (%)', '💧 Umidade'),
            ('VENTO, VELOCIDADE HORARIA (m/s)', '💨 Velocidade do Vento'),
            ('PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)', '📊 Pressão')
        ]
        
        for var_col, var_nome in variaveis:
            if var_col in self.dados_combinados.columns:
                rg_var = rg_data[var_col].dropna()
                cl_var = cl_data[var_col].dropna()
                
                if len(rg_var) > 0 and len(cl_var) > 0:
                    print(f"\n{var_nome}:")
                    print(f"   Rio Grande - Média: {rg_var.mean():.2f}")
                    print(f"   Capão do Leão - Média: {cl_var.mean():.2f}")
                    print(f"   Diferença: {rg_var.mean() - cl_var.mean():.2f}")
                    
                    # Comparação simples entre médias
                    diferenca = abs(rg_var.mean() - cl_var.mean())
                    if diferenca > rg_var.std() * 0.1:  # Diferença maior que 10% do desvio padrão
                        print("   ✅ Diferença considerável entre as cidades")
                    else:
                        print("   ❌ Diferença pequena entre as cidades")
                    
                    if SCIPY_DISPONIVEL:
                        print("   📊 Teste estatístico disponível (scipy instalado)")
                    else:
                        print("   ⚠️ Teste estatístico não disponível (scipy não instalado)")
    
    def analise_sazonalidade(self):
        """Analisa padrões sazonais"""
        if self.dados_combinados is None:
            print("❌ Dados não carregados.")
            return
        
        print("\n" + "=" * 60)
        print("🌿 ANÁLISE DE SAZONALIDADE")
        print("=" * 60)
        
        # Adicionar informações de estação
        self.dados_combinados['mes'] = self.dados_combinados['datetime'].dt.month
        
        def definir_estacao(mes):
            if mes in [12, 1, 2]:
                return 'Verão'
            elif mes in [3, 4, 5]:
                return 'Outono'
            elif mes in [6, 7, 8]:
                return 'Inverno'
            else:
                return 'Primavera'
        
        self.dados_combinados['estacao'] = self.dados_combinados['mes'].apply(definir_estacao)
        
        # Análise por estação
        for cidade in ['Rio Grande', 'Capão do Leão']:
            print(f"\n🏙️ {cidade}:")
            dados_cidade = self.dados_combinados[self.dados_combinados['cidade'] == cidade]
            
            colunas_analise = []
            if 'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)' in dados_cidade.columns:
                colunas_analise.append(('TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)', 'mean'))
            if 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)' in dados_cidade.columns:
                colunas_analise.append(('PRECIPITAÇÃO TOTAL, HORÁRIO (mm)', 'sum'))
            if 'UMIDADE RELATIVA DO AR, HORARIA (%)' in dados_cidade.columns:
                colunas_analise.append(('UMIDADE RELATIVA DO AR, HORARIA (%)', 'mean'))
            
            if colunas_analise:
                for coluna, func in colunas_analise:
                    print(f"   {coluna}:")
                    for estacao in ['Verão', 'Outono', 'Inverno', 'Primavera']:
                        dados_estacao = dados_cidade[dados_cidade['estacao'] == estacao][coluna].dropna()
                        if len(dados_estacao) > 0:
                            if func == 'mean':
                                valor = dados_estacao.mean()
                            else:
                                valor = dados_estacao.sum()
                            print(f"     {estacao}: {valor:.2f}")
    
    def visualizacoes_basicas_matplotlib(self):
        """Cria visualizações básicas usando apenas matplotlib"""
        if self.dados_combinados is None:
            print("❌ Dados não carregados.")
            return
        
        print("\n🎨 Criando visualizações básicas...")
        
        # Configurar matplotlib
        plt.style.use('default')
        
        # Criar figura com subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 10))
        fig.suptitle('Análise Meteorológica - Rio Grande vs Capão do Leão', fontsize=16)
        
        # 1. Comparação de temperaturas médias
        if 'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)' in self.dados_combinados.columns:
            cidades = ['Rio Grande', 'Capão do Leão']
            temps_medias = []
            for cidade in cidades:
                temp_media = self.dados_combinados[
                    self.dados_combinados['cidade'] == cidade
                ]['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].mean()
                temps_medias.append(temp_media)
            
            axes[0, 0].bar(cidades, temps_medias, color=['blue', 'orange'], alpha=0.7)
            axes[0, 0].set_title('Temperatura Média por Cidade')
            axes[0, 0].set_ylabel('Temperatura (°C)')
        
        # 2. Precipitação total
        if 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)' in self.dados_combinados.columns:
            precips_total = []
            for cidade in cidades:
                precip_total = self.dados_combinados[
                    self.dados_combinados['cidade'] == cidade
                ]['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].sum()
                precips_total.append(precip_total)
            
            axes[0, 1].bar(cidades, precips_total, color=['blue', 'orange'], alpha=0.7)
            axes[0, 1].set_title('Precipitação Total por Cidade')
            axes[0, 1].set_ylabel('Precipitação (mm)')
        
        # 3. Umidade média
        if 'UMIDADE RELATIVA DO AR, HORARIA (%)' in self.dados_combinados.columns:
            umids_medias = []
            for cidade in cidades:
                umid_media = self.dados_combinados[
                    self.dados_combinados['cidade'] == cidade
                ]['UMIDADE RELATIVA DO AR, HORARIA (%)'].mean()
                umids_medias.append(umid_media)
            
            axes[1, 0].bar(cidades, umids_medias, color=['blue', 'orange'], alpha=0.7)
            axes[1, 0].set_title('Umidade Média por Cidade')
            axes[1, 0].set_ylabel('Umidade (%)')
        
        # 4. Velocidade do vento média
        if 'VENTO, VELOCIDADE HORARIA (m/s)' in self.dados_combinados.columns:
            ventos_medios = []
            for cidade in cidades:
                vento_medio = self.dados_combinados[
                    self.dados_combinados['cidade'] == cidade
                ]['VENTO, VELOCIDADE HORARIA (m/s)'].mean()
                ventos_medios.append(vento_medio)
            
            axes[1, 1].bar(cidades, ventos_medios, color=['blue', 'orange'], alpha=0.7)
            axes[1, 1].set_title('Velocidade Média do Vento por Cidade')
            axes[1, 1].set_ylabel('Velocidade (m/s)')
        
        plt.tight_layout()
        plt.show()
        
        print("✅ Visualizações básicas criadas!")
    
    def modelo_previsao_temperatura(self):
        """Cria modelo de previsão de temperatura (se sklearn disponível)"""
        if not SKLEARN_DISPONIVEL:
            print("❌ Scikit-learn não disponível. Modelo de ML não pode ser criado.")
            return None
            
        if self.dados_combinados is None:
            print("❌ Dados não carregados.")
            return None
        
        print("\n" + "=" * 60)
        print("🤖 MODELO DE PREVISÃO DE TEMPERATURA")
        print("=" * 60)
        
        try:
            # Preparar dados para modelagem
            dados_modelo = self.dados_combinados.dropna(subset=[
                'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
                'UMIDADE RELATIVA DO AR, HORARIA (%)',
                'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)',
                'VENTO, VELOCIDADE HORARIA (m/s)'
            ]).copy()
            
            # Features
            features = [
                'UMIDADE RELATIVA DO AR, HORARIA (%)',
                'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)',
                'VENTO, VELOCIDADE HORARIA (m/s)'
            ]
            
            # Adicionar features temporais
            dados_modelo['hora'] = dados_modelo['datetime'].dt.hour
            dados_modelo['dia_ano'] = dados_modelo['datetime'].dt.dayofyear
            dados_modelo['mes'] = dados_modelo['datetime'].dt.month
            features.extend(['hora', 'dia_ano', 'mes'])
            
            # Encoding para cidade
            dados_modelo['cidade_encoded'] = dados_modelo['cidade'].map({'Rio Grande': 0, 'Capão do Leão': 1})
            features.append('cidade_encoded')
            
            X = dados_modelo[features]
            y = dados_modelo['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)']
            
            # Dividir dados
            X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
            
            # Treinar modelo
            rf_modelo = RandomForestRegressor(n_estimators=100, random_state=42)
            rf_modelo.fit(X_train, y_train)
            
            # Previsões
            y_pred = rf_modelo.predict(X_test)
            
            # Métricas
            mse = mean_squared_error(y_test, y_pred)
            rmse = np.sqrt(mse)
            
            print("📊 Métricas do Modelo:")
            print(f"   RMSE: {rmse:.2f}°C")
            print(f"   R²: {rf_modelo.score(X_test, y_test):.3f}")
            
            # Importância das features
            importancias = pd.DataFrame({
                'feature': features,
                'importancia': rf_modelo.feature_importances_
            }).sort_values('importancia', ascending=False)
            
            print("\n🎯 Importância das Variáveis:")
            for _, row in importancias.iterrows():
                print(f"   {row['feature']}: {row['importancia']:.3f}")
            
            return rf_modelo
            
        except (ValueError, KeyError, AttributeError) as e:
            print(f"❌ Erro ao criar modelo: {e}")
            return None
    
    def gerar_insights_finais(self):
        """Gera insights finais da análise"""
        if self.dados_combinados is None:
            return
        
        print("\n" + "=" * 60)
        print("🔍 INSIGHTS PRINCIPAIS")
        print("=" * 60)
        
        # Calcular diferenças médias
        rg_data = self.dados_combinados[self.dados_combinados['cidade'] == 'Rio Grande']
        cl_data = self.dados_combinados[self.dados_combinados['cidade'] == 'Capão do Leão']
        
        # Temperatura
        if 'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)' in self.dados_combinados.columns:
            temp_rg = rg_data['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].mean()
            temp_cl = cl_data['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].mean()
            
            if temp_rg > temp_cl:
                print(f"🌡️ Rio Grande é em média {temp_rg - temp_cl:.1f}°C mais quente que Capão do Leão")
            else:
                print(f"🌡️ Capão do Leão é em média {temp_cl - temp_rg:.1f}°C mais quente que Rio Grande")
        
        # Precipitação
        if 'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)' in self.dados_combinados.columns:
            precip_rg = rg_data['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].sum()
            precip_cl = cl_data['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].sum()
            
            if precip_rg > precip_cl:
                print(f"🌧️ Rio Grande teve {precip_rg - precip_cl:.0f}mm a mais de chuva no período")
            else:
                print(f"🌧️ Capão do Leão teve {precip_cl - precip_rg:.0f}mm a mais de chuva no período")
        
        # Umidade
        if 'UMIDADE RELATIVA DO AR, HORARIA (%)' in self.dados_combinados.columns:
            umid_rg = rg_data['UMIDADE RELATIVA DO AR, HORARIA (%)'].mean()
            umid_cl = cl_data['UMIDADE RELATIVA DO AR, HORARIA (%)'].mean()
            
            if umid_rg > umid_cl:
                print(f"💧 Rio Grande é {umid_rg - umid_cl:.1f}% mais úmido em média")
            else:
                print(f"💧 Capão do Leão é {umid_cl - umid_rg:.1f}% mais úmido em média")
        
        # Vento
        if 'VENTO, VELOCIDADE HORARIA (m/s)' in self.dados_combinados.columns:
            vento_rg = rg_data['VENTO, VELOCIDADE HORARIA (m/s)'].mean()
            vento_cl = cl_data['VENTO, VELOCIDADE HORARIA (m/s)'].mean()
            
            if vento_rg > vento_cl:
                print(f"💨 Rio Grande tem ventos {vento_rg - vento_cl:.1f}m/s mais fortes em média")
            else:
                print(f"💨 Capão do Leão tem ventos {vento_cl - vento_rg:.1f}m/s mais fortes em média")
        
        print("\n📋 Recomendações:")
        print("   • Use os modelos de previsão para planejamento agrícola")
        print("   • Monitore padrões sazonais para atividades ao ar livre")
        print("   • Considere as diferenças climáticas para cultivos específicos")
        print("   • Utilize os gráficos para comunicar resultados a stakeholders")
    
    def relatorio_completo(self):
        """Gera relatório completo da análise"""
        print("🚀 Executando Análise Meteorológica Completa...")
        print("=" * 60)
        
        # Carregar dados
        self.carregar_dados_multiplos_anos()
        
        # Estatísticas
        self.estatisticas_descritivas()
        
        # Comparação
        self.comparacao_cidades()
        
        # Sazonalidade
        self.analise_sazonalidade()
        
        # Visualizações básicas
        try:
            self.visualizacoes_basicas_matplotlib()
        except (ValueError, KeyError) as e:
            print(f"⚠️ Erro nas visualizações básicas: {e}")
        
        # Visualizações avançadas matplotlib
        if MATPLOTLIB_VIZ_DISPONIVEL and self.dados_combinados is not None:
            print("\n🎨 Criando visualizações avançadas (Matplotlib)...")
            try:
                criar_visualizacoes_completas(self.dados_combinados)
            except (ImportError, AttributeError) as e:
                print(f"⚠️ Erro nas visualizações avançadas: {e}")
        
        # Modelo
        trained_model = self.modelo_previsao_temperatura()
        
        # Insights finais
        self.gerar_insights_finais()
        
        print("\n" + "=" * 60)
        print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
        # Status das funcionalidades
        print("\n📊 STATUS DAS FUNCIONALIDADES:")
        print("   Análise básica: ✅ Disponível")
        print("   Visualizações básicas: ✅ Disponível")
        print(f"   Testes estatísticos: {'✅' if SCIPY_DISPONIVEL else '❌'} {'Disponível' if SCIPY_DISPONIVEL else 'Scipy não instalado'}")
        print(f"   Machine Learning: {'✅' if SKLEARN_DISPONIVEL else '❌'} {'Disponível' if SKLEARN_DISPONIVEL else 'Scikit-learn não instalado'}")
        print(f"   Visualizações interativas: {'✅' if PLOTLY_DISPONIVEL else '❌'} {'Disponível' if PLOTLY_DISPONIVEL else 'Plotly não instalado'}")
        print(f"   Visualizações avançadas: {'✅' if MATPLOTLIB_VIZ_DISPONIVEL else '❌'} {'Disponível' if MATPLOTLIB_VIZ_DISPONIVEL else 'Módulo não encontrado'}")
        
        return trained_model


# Executar análise completa
if __name__ == "__main__":
    analise = AnaliseMeteorolgicaRS()
    trained_model = analise.relatorio_completo()
