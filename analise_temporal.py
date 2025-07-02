import pandas as pd 
import warnings
import glob

# Imports condicionais para bibliotecas que podem não estar disponíveis
try:
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestRegressor
    from sklearn.metrics import mean_squared_error
    SKLEARN_DISPONIVEL = True
except ImportError:
    SKLEARN_DISPONIVEL = False
    print("⚠️ Scikit-learn não encontrado. Algumas funcionalidades serão limitadas.")

try:
    import plotly.graph_objects as go
    from plotly.subplots import make_subplots
    PLOTLY_DISPONIVEL = True
except ImportError:
    PLOTLY_DISPONIVEL = False
    print("⚠️ Plotly não encontrado. Visualizações interativas serão limitadas.")

# Importar visualizações matplotlib
try:
    from visualizacoes_matplotlib import criar_visualizacoes_completas
    MATPLOTLIB_DISPONIVEL = True
except ImportError:
    MATPLOTLIB_DISPONIVEL = False
    print("⚠️ Módulo de visualizações matplotlib não encontrado.")

warnings.filterwarnings("ignore")

class AnaliseMeteorolgicaRS:
    def __init__(self):
        self.dados_rio_grande = []
        self.dados_capao_leao = []
        self.dados_combinados = None
        self.colunas_mapeadas = {
            'Data': 'data',
            'Hora UTC': 'hora',
            'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'precipitacao',
            'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': 'pressao',
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'temperatura',
            'TEMPERATURA DO PONTO DE ORVALHO (°C)': 'temp_orvalho',
            'UMIDADE RELATIVA DO AR, HORARIA (%)': 'umidade',
            'VENTO, VELOCIDADE HORARIA (m/s)': 'vento_velocidade',
            'VENTO, DIREÇÃO HORARIA (gr) (° (gr))': 'vento_direcao',
            'RADIACAO GLOBAL (Kj/m²)': 'radiacao'
        }
    
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
            df_processado = df_processado.dropna(subset=['datetime'])
            
            return df_processado
            
        except (FileNotFoundError, pd.errors.EmptyDataError, ValueError) as e:
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
                    print(f"   Rio Grande - Desvio Padrão: {rg_var.std():.2f}")
                    print(f"   Capão do Leão - Desvio Padrão: {cl_var.std():.2f}")
                    
                    # Análise simples de diferença percentual
                    diff_percentual = abs(rg_var.mean() - cl_var.mean()) / ((rg_var.mean() + cl_var.mean()) / 2) * 100
                    if diff_percentual > 5:
                        print(f"   📊 Diferença considerável ({diff_percentual:.1f}%)")
                    else:
                        print(f"   📊 Diferença pequena ({diff_percentual:.1f}%)")
    
    def visualizacoes_comparativas_avancadas(self):
        """Cria visualizações comparativas avançadas"""
        if self.dados_combinados is None:
            print("❌ Dados não carregados.")
            return
        
        if not PLOTLY_DISPONIVEL:
            print("❌ Plotly não disponível. Visualizações interativas não podem ser criadas.")
            return
        
        # Criar múltiplos gráficos
        fig = make_subplots(
            rows=3, cols=2,
            subplot_titles=[
                'Temperatura por Cidade', 'Precipitação por Cidade',
                'Umidade vs Temperatura', 'Distribuição de Temperaturas',
                'Velocidade do Vento', 'Pressão Atmosférica'
            ],
            specs=[[{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}]]
        )
        
        # Preparar dados mensais
        dados_mensais = self._preparar_dados_mensais()
        
        cores = {'Rio Grande': '#1f77b4', 'Capão do Leão': '#ff7f0e'}
        
        # 1. Temperatura por cidade (série temporal)
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = dados_mensais[dados_mensais['cidade'] == cidade]
            fig.add_trace(
                go.Scatter(
                    x=dados_cidade['data_mes'],
                    y=dados_cidade['temp_media'],
                    mode='lines+markers',
                    name=f'{cidade} - Temp',
                    line=dict(color=cores[cidade]),
                    showlegend=True
                ),
                row=1, col=1
            )
        
        # 2. Precipitação acumulada
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = dados_mensais[dados_mensais['cidade'] == cidade]
            fig.add_trace(
                go.Bar(
                    x=dados_cidade['data_mes'],
                    y=dados_cidade['precip_total'],
                    name=f'{cidade} - Precip',
                    marker_color=cores[cidade],
                    opacity=0.7,
                    showlegend=False
                ),
                row=1, col=2
            )
        
        # 3. Scatter: Umidade vs Temperatura
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_scatter = self.dados_combinados[
                (self.dados_combinados['cidade'] == cidade) &
                (self.dados_combinados['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].notna()) &
                (self.dados_combinados['UMIDADE RELATIVA DO AR, HORARIA (%)'].notna())
            ].sample(n=min(1000, len(self.dados_combinados[self.dados_combinados['cidade'] == cidade])))
            
            fig.add_trace(
                go.Scatter(
                    x=dados_scatter['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'],
                    y=dados_scatter['UMIDADE RELATIVA DO AR, HORARIA (%)'],
                    mode='markers',
                    name=f'{cidade}',
                    marker=dict(color=cores[cidade], size=4, opacity=0.6),
                    showlegend=False
                ),
                row=2, col=1
            )
        
        # 4. Histograma de temperaturas
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_temp = self.dados_combinados[
                (self.dados_combinados['cidade'] == cidade) &
                (self.dados_combinados['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].notna())
            ]['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)']
            
            fig.add_trace(
                go.Histogram(
                    x=dados_temp,
                    name=f'{cidade}',
                    opacity=0.7,
                    marker_color=cores[cidade],
                    showlegend=False,
                    nbinsx=30
                ),
                row=2, col=2
            )
        
        # 5. Velocidade do vento
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = dados_mensais[dados_mensais['cidade'] == cidade]
            fig.add_trace(
                go.Scatter(
                    x=dados_cidade['data_mes'],
                    y=dados_cidade['vento_medio'],
                    mode='lines+markers',
                    name=f'{cidade} - Vento',
                    line=dict(color=cores[cidade]),
                    showlegend=False
                ),
                row=3, col=1
            )
        
        # 6. Pressão atmosférica
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = dados_mensais[dados_mensais['cidade'] == cidade]
            fig.add_trace(
                go.Scatter(
                    x=dados_cidade['data_mes'],
                    y=dados_cidade['pressao_media'],
                    mode='lines+markers',
                    name=f'{cidade} - Pressão',
                    line=dict(color=cores[cidade]),
                    showlegend=False
                ),
                row=3, col=2
            )
        
        # Atualizar layout
        fig.update_layout(
            height=1200,
            title_text="📊 Análise Meteorológica Comparativa: Rio Grande vs Capão do Leão",
            showlegend=True,
            title_font_size=16
        )
        
        # Atualizar eixos
        fig.update_xaxes(title_text="Data", row=1, col=1)
        fig.update_yaxes(title_text="Temperatura (°C)", row=1, col=1)
        
        fig.update_xaxes(title_text="Data", row=1, col=2)
        fig.update_yaxes(title_text="Precipitação (mm)", row=1, col=2)
        
        fig.update_xaxes(title_text="Temperatura (°C)", row=2, col=1)
        fig.update_yaxes(title_text="Umidade (%)", row=2, col=1)
        
        fig.update_xaxes(title_text="Temperatura (°C)", row=2, col=2)
        fig.update_yaxes(title_text="Frequência", row=2, col=2)
        
        fig.update_xaxes(title_text="Data", row=3, col=1)
        fig.update_yaxes(title_text="Velocidade (m/s)", row=3, col=1)
        
        fig.update_xaxes(title_text="Data", row=3, col=2)
        fig.update_yaxes(title_text="Pressão (mB)", row=3, col=2)
        
        fig.show()
    
    def _preparar_dados_mensais(self):
        """Prepara dados agregados mensalmente"""
        if self.dados_combinados is None:
            return pd.DataFrame()
        
        # Adicionar colunas de data
        self.dados_combinados['ano_mes'] = self.dados_combinados['datetime'].dt.to_period('M')
        
        # Agregar por mês e cidade
        dados_mensais = self.dados_combinados.groupby(['cidade', 'ano_mes']).agg({
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': ['mean', 'max', 'min'],
            'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'sum',
            'UMIDADE RELATIVA DO AR, HORARIA (%)': 'mean',
            'VENTO, VELOCIDADE HORARIA (m/s)': 'mean',
            'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)': 'mean'
        }).reset_index()
        
        # Renomear colunas
        dados_mensais.columns = [
            'cidade', 'ano_mes', 'temp_media', 'temp_max', 'temp_min',
            'precip_total', 'umidade_media', 'vento_medio', 'pressao_media'
        ]
        
        # Converter período para datetime
        dados_mensais['data_mes'] = dados_mensais['ano_mes'].dt.to_timestamp()
        
        return dados_mensais
    
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
            
            estacoes_stats = dados_cidade.groupby('estacao').agg({
                'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)': 'mean',
                'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)': 'sum',
                'UMIDADE RELATIVA DO AR, HORARIA (%)': 'mean'
            }).round(2)
            
            print(estacoes_stats)
    
    def modelo_previsao_temperatura(self):
        """Cria modelo de previsão de temperatura"""
        if self.dados_combinados is None:
            print("❌ Dados não carregados.")
            return
        
        if not SKLEARN_DISPONIVEL:
            print("❌ Scikit-learn não disponível. Modelo de previsão não pode ser criado.")
            return
        
        print("\n" + "=" * 60)
        print("🤖 MODELO DE PREVISÃO DE TEMPERATURA")
        print("=" * 60)
        
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
        rmse = mse ** 0.5  # Calcular raiz quadrada de forma mais robusta
        
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
        
        # Visualizações Plotly
        if PLOTLY_DISPONIVEL:
            print("\n🎯 Criando visualizações interativas (Plotly)...")
            self.visualizacoes_comparativas_avancadas()
        else:
            print("\n⚠️ Visualizações Plotly não disponíveis (biblioteca não encontrada)")
        
        # Modelo
        if SKLEARN_DISPONIVEL:
            print("\n🤖 Criando modelo de previsão...")
            modelo_resultado = self.modelo_previsao_temperatura()
        else:
            print("\n⚠️ Modelo de previsão não disponível (Scikit-learn não encontrado)")
            modelo_resultado = None
        
        # Visualizações matplotlib
        if MATPLOTLIB_DISPONIVEL and self.dados_combinados is not None:
            print("\n🎨 Criando visualizações estáticas (Matplotlib)...")
            try:
                criar_visualizacoes_completas(self.dados_combinados)
            except (ImportError, AttributeError) as e:
                print(f"⚠️ Erro nas visualizações matplotlib: {e}")
        
        # Insights finais
        self.gerar_insights_finais()
        
        print("\n" + "=" * 60)
        print("✅ ANÁLISE CONCLUÍDA COM SUCESSO!")
        print("=" * 60)
        
        return modelo_resultado
    
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


# Executar análise completa
if __name__ == "__main__":
    analise = AnaliseMeteorolgicaRS()
    modelo = analise.relatorio_completo()