import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from datetime import datetime
import warnings

warnings.filterwarnings("ignore")

class VisualizacoesMeteorlogicas:
    def __init__(self, dados_combinados):
        self.dados = dados_combinados
        # Configurar estilo
        plt.style.use('seaborn-v0_8')
        sns.set_palette("husl")
        
    def configurar_matplotlib(self):
        """Configura matplotlib para melhor visualização"""
        plt.rcParams['figure.figsize'] = (15, 10)
        plt.rcParams['font.size'] = 12
        plt.rcParams['axes.titlesize'] = 14
        plt.rcParams['axes.labelsize'] = 12
        plt.rcParams['xtick.labelsize'] = 10
        plt.rcParams['ytick.labelsize'] = 10
        plt.rcParams['legend.fontsize'] = 11
    
    def dashboard_completo(self):
        """Cria um dashboard completo com matplotlib"""
        self.configurar_matplotlib()
        
        # Criar figura principal
        fig = plt.figure(figsize=(20, 16))
        fig.suptitle('🌤️ Dashboard Meteorológico - Rio Grande vs Capão do Leão', 
                     fontsize=20, fontweight='bold', y=0.98)
        
        # 1. Série temporal de temperaturas
        ax1 = plt.subplot(3, 3, 1)
        self._plot_serie_temporal_temperatura(ax1)
        
        # 2. Box plot comparativo de temperaturas
        ax2 = plt.subplot(3, 3, 2)
        self._plot_boxplot_temperatura(ax2)
        
        # 3. Distribuição de precipitação
        ax3 = plt.subplot(3, 3, 3)
        self._plot_distribuicao_precipitacao(ax3)
        
        # 4. Correlação entre variáveis
        ax4 = plt.subplot(3, 3, 4)
        self._plot_correlacao_variaveis(ax4)
        
        # 5. Padrão diário de temperatura
        ax5 = plt.subplot(3, 3, 5)
        self._plot_padrao_diario(ax5)
        
        # 6. Umidade vs Temperatura
        ax6 = plt.subplot(3, 3, 6)
        self._plot_umidade_temperatura(ax6)
        
        # 7. Rosa dos ventos
        ax7 = plt.subplot(3, 3, 7, projection='polar')
        self._plot_rosa_ventos(ax7)
        
        # 8. Pressão atmosférica
        ax8 = plt.subplot(3, 3, 8)
        self._plot_pressao_atmosferica(ax8)
        
        # 9. Heatmap mensal
        ax9 = plt.subplot(3, 3, 9)
        self._plot_heatmap_mensal(ax9)
        
        plt.tight_layout()
        plt.subplots_adjust(top=0.93)
        plt.show()
    
    def _plot_serie_temporal_temperatura(self, ax):
        """Série temporal de temperaturas"""
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = self.dados[self.dados['cidade'] == cidade]
            
            # Agrupar por dia para reduzir pontos
            temp_diaria = dados_cidade.groupby(dados_cidade['datetime'].dt.date)[
                'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].mean()
            
            ax.plot(temp_diaria.index, temp_diaria.values, 
                   label=cidade, linewidth=1.5, alpha=0.8)
        
        ax.set_title('Série Temporal de Temperaturas')
        ax.set_xlabel('Data')
        ax.set_ylabel('Temperatura (°C)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # Rotacionar labels do eixo x
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _plot_boxplot_temperatura(self, ax):
        """Box plot comparativo de temperaturas"""
        dados_temp = []
        cidades = []
        
        for cidade in ['Rio Grande', 'Capão do Leão']:
            temp_data = self.dados[
                (self.dados['cidade'] == cidade) & 
                (self.dados['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].notna())
            ]['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)']
            
            dados_temp.extend(temp_data.tolist())
            cidades.extend([cidade] * len(temp_data))
        
        df_boxplot = pd.DataFrame({'Temperatura': dados_temp, 'Cidade': cidades})
        
        sns.boxplot(data=df_boxplot, x='Cidade', y='Temperatura', ax=ax)
        ax.set_title('Distribuição de Temperaturas por Cidade')
        ax.set_ylabel('Temperatura (°C)')
    
    def _plot_distribuicao_precipitacao(self, ax):
        """Distribuição de precipitação"""
        for cidade in ['Rio Grande', 'Capão do Leão']:
            precip_data = self.dados[
                (self.dados['cidade'] == cidade) & 
                (self.dados['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'] > 0) &
                (self.dados['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].notna())
            ]['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)']
            
            if len(precip_data) > 0:
                ax.hist(precip_data, bins=30, alpha=0.6, label=cidade, density=True)
        
        ax.set_title('Distribuição de Precipitação (> 0mm)')
        ax.set_xlabel('Precipitação (mm)')
        ax.set_ylabel('Densidade')
        ax.legend()
        ax.set_xlim(0, 20)  # Focar em valores até 20mm
    
    def _plot_correlacao_variaveis(self, ax):
        """Heatmap de correlação entre variáveis"""
        # Selecionar apenas dados de uma cidade para correlação
        dados_rg = self.dados[self.dados['cidade'] == 'Rio Grande']
        
        colunas_numericas = [
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)',
            'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)',
            'UMIDADE RELATIVA DO AR, HORARIA (%)',
            'VENTO, VELOCIDADE HORARIA (m/s)',
            'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)'
        ]
        
        # Filtrar colunas que existem
        colunas_existentes = [col for col in colunas_numericas if col in dados_rg.columns]
        
        if colunas_existentes:
            corr_matrix = dados_rg[colunas_existentes].corr()
            
            # Criar labels mais curtos
            labels_curtos = ['Temp', 'Precip', 'Umid', 'Vento', 'Pressão'][:len(colunas_existentes)]
            
            sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0,
                       square=True, ax=ax, xticklabels=labels_curtos, 
                       yticklabels=labels_curtos, fmt='.2f')
            ax.set_title('Correlação entre Variáveis (Rio Grande)')
    
    def _plot_padrao_diario(self, ax):
        """Padrão diário médio de temperatura"""
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = self.dados[self.dados['cidade'] == cidade]
            dados_cidade['hora'] = dados_cidade['datetime'].dt.hour
            
            temp_por_hora = dados_cidade.groupby('hora')[
                'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].mean()
            
            ax.plot(temp_por_hora.index, temp_por_hora.values, 
                   marker='o', label=cidade, linewidth=2)
        
        ax.set_title('Padrão Diário Médio de Temperatura')
        ax.set_xlabel('Hora do Dia')
        ax.set_ylabel('Temperatura Média (°C)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        ax.set_xticks(range(0, 24, 3))
    
    def _plot_umidade_temperatura(self, ax):
        """Scatter plot umidade vs temperatura"""
        cores = {'Rio Grande': 'blue', 'Capão do Leão': 'orange'}
        
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_scatter = self.dados[
                (self.dados['cidade'] == cidade) &
                (self.dados['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].notna()) &
                (self.dados['UMIDADE RELATIVA DO AR, HORARIA (%)'].notna())
            ].sample(n=min(500, len(self.dados[self.dados['cidade'] == cidade])))
            
            ax.scatter(
                dados_scatter['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'],
                dados_scatter['UMIDADE RELATIVA DO AR, HORARIA (%)'],
                alpha=0.5, label=cidade, color=cores[cidade], s=20
            )
        
        ax.set_title('Relação Umidade vs Temperatura')
        ax.set_xlabel('Temperatura (°C)')
        ax.set_ylabel('Umidade (%)')
        ax.legend()
        ax.grid(True, alpha=0.3)
    
    def _plot_rosa_ventos(self, ax):
        """Rosa dos ventos simplificada"""
        # Usar dados de Rio Grande
        dados_vento = self.dados[
            (self.dados['cidade'] == 'Rio Grande') &
            (self.dados['VENTO, DIREÇÃO HORARIA (gr) (° (gr))'].notna()) &
            (self.dados['VENTO, VELOCIDADE HORARIA (m/s)'].notna())
        ]
        
        if len(dados_vento) > 0:
            # Converter direção para radianos
            direcoes = np.radians(dados_vento['VENTO, DIREÇÃO HORARIA (gr) (° (gr))'])
            velocidades = dados_vento['VENTO, VELOCIDADE HORARIA (m/s)']
            
            # Criar bins para direções
            n_bins = 16
            bins = np.linspace(0, 2*np.pi, n_bins+1)
            
            # Calcular frequência por direção
            freq, _ = np.histogram(direcoes, bins=bins)
            
            # Ângulos para o plot
            theta = np.linspace(0, 2*np.pi, n_bins, endpoint=False)
            
            # Plot de barras polares
            bars = ax.bar(theta, freq, width=2*np.pi/n_bins, alpha=0.7)
            
            ax.set_title('Rosa dos Ventos (Rio Grande)', pad=20)
            ax.set_theta_zero_location('N')
            ax.set_theta_direction(-1)
    
    def _plot_pressao_atmosferica(self, ax):
        """Série temporal de pressão atmosférica"""
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = self.dados[self.dados['cidade'] == cidade]
            
            # Agrupar por dia
            pressao_diaria = dados_cidade.groupby(dados_cidade['datetime'].dt.date)[
                'PRESSAO ATMOSFERICA AO NIVEL DA ESTACAO, HORARIA (mB)'].mean()
            
            if len(pressao_diaria) > 0:
                ax.plot(pressao_diaria.index, pressao_diaria.values, 
                       label=cidade, linewidth=1.5, alpha=0.8)
        
        ax.set_title('Pressão Atmosférica ao Longo do Tempo')
        ax.set_xlabel('Data')
        ax.set_ylabel('Pressão (mB)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _plot_heatmap_mensal(self, ax):
        """Heatmap de temperatura média mensal"""
        # Preparar dados
        dados_temp = self.dados[self.dados['TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].notna()].copy()
        dados_temp['mes'] = dados_temp['datetime'].dt.month
        dados_temp['ano'] = dados_temp['datetime'].dt.year
        
        # Calcular temperatura média por mês e cidade
        temp_mensal = dados_temp.groupby(['cidade', 'ano', 'mes'])[
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].mean().reset_index()
        
        # Pivot para heatmap
        pivot_rg = temp_mensal[temp_mensal['cidade'] == 'Rio Grande'].pivot(
            index='ano', columns='mes', values='TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)')
        
        if not pivot_rg.empty:
            sns.heatmap(pivot_rg, annot=True, fmt='.1f', cmap='RdYlBu_r',
                       ax=ax, cbar_kws={'label': 'Temperatura (°C)'})
            ax.set_title('Temperatura Média Mensal (Rio Grande)')
            ax.set_xlabel('Mês')
            ax.set_ylabel('Ano')
    
    def graficos_especificos(self):
        """Cria gráficos específicos adicionais"""
        
        # 1. Comparação mensal de precipitação
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('Análises Específicas Complementares', fontsize=16, fontweight='bold')
        
        # Precipitação mensal acumulada
        self._plot_precipitacao_mensal(axes[0, 0])
        
        # Velocidade do vento por estação
        self._plot_vento_estacional(axes[0, 1])
        
        # Amplitude térmica diária
        self._plot_amplitude_termica(axes[1, 0])
        
        # Dias com precipitação
        self._plot_dias_precipitacao(axes[1, 1])
        
        plt.tight_layout()
        plt.show()
    
    def _plot_precipitacao_mensal(self, ax):
        """Precipitação acumulada mensal"""
        dados_precip = self.dados.copy()
        dados_precip['mes'] = dados_precip['datetime'].dt.month
        dados_precip['ano'] = dados_precip['datetime'].dt.year
        
        precip_mensal = dados_precip.groupby(['cidade', 'ano', 'mes'])[
            'PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].sum().reset_index()
        
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = precip_mensal[precip_mensal['cidade'] == cidade]
            precip_por_mes = dados_cidade.groupby('mes')['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'].mean()
            
            ax.bar([meses[i-1] for i in precip_por_mes.index], precip_por_mes.values,
                  alpha=0.7, label=cidade)
        
        ax.set_title('Precipitação Média Mensal')
        ax.set_ylabel('Precipitação (mm)')
        ax.legend()
        ax.tick_params(axis='x', rotation=45)
    
    def _plot_vento_estacional(self, ax):
        """Velocidade do vento por estação"""
        dados_vento = self.dados.copy()
        dados_vento['mes'] = dados_vento['datetime'].dt.month
        
        def definir_estacao(mes):
            if mes in [12, 1, 2]: return 'Verão'
            elif mes in [3, 4, 5]: return 'Outono'
            elif mes in [6, 7, 8]: return 'Inverno'
            else: return 'Primavera'
        
        dados_vento['estacao'] = dados_vento['mes'].apply(definir_estacao)
        
        vento_estacional = dados_vento.groupby(['cidade', 'estacao'])[
            'VENTO, VELOCIDADE HORARIA (m/s)'].mean().unstack()
        
        vento_estacional.plot(kind='bar', ax=ax, width=0.8)
        ax.set_title('Velocidade Média do Vento por Estação')
        ax.set_ylabel('Velocidade (m/s)')
        ax.legend(title='Estação')
        ax.tick_params(axis='x', rotation=45)
    
    def _plot_amplitude_termica(self, ax):
        """Amplitude térmica diária"""
        dados_temp = self.dados.copy()
        dados_temp['data'] = dados_temp['datetime'].dt.date
        
        amplitude_diaria = dados_temp.groupby(['cidade', 'data'])[
            'TEMPERATURA DO AR - BULBO SECO, HORARIA (°C)'].agg(['min', 'max']).reset_index()
        amplitude_diaria['amplitude'] = amplitude_diaria['max'] - amplitude_diaria['min']
        
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = amplitude_diaria[amplitude_diaria['cidade'] == cidade]
            
            # Mostrar apenas uma amostra para clareza
            sample_data = dados_cidade.sample(n=min(100, len(dados_cidade)))
            ax.scatter(sample_data['data'], sample_data['amplitude'], 
                      alpha=0.6, label=cidade, s=30)
        
        ax.set_title('Amplitude Térmica Diária')
        ax.set_xlabel('Data')
        ax.set_ylabel('Amplitude (°C)')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
    
    def _plot_dias_precipitacao(self, ax):
        """Número de dias com precipitação por mês"""
        dados_precip = self.dados[self.dados['PRECIPITAÇÃO TOTAL, HORÁRIO (mm)'] > 0].copy()
        dados_precip['data'] = dados_precip['datetime'].dt.date
        dados_precip['mes'] = dados_precip['datetime'].dt.month
        
        dias_chuva = dados_precip.groupby(['cidade', 'mes', 'data']).size().reset_index()
        dias_por_mes = dias_chuva.groupby(['cidade', 'mes']).size().reset_index(name='dias_chuva')
        
        meses = ['Jan', 'Fev', 'Mar', 'Abr', 'Mai', 'Jun',
                'Jul', 'Ago', 'Set', 'Out', 'Nov', 'Dez']
        
        for cidade in ['Rio Grande', 'Capão do Leão']:
            dados_cidade = dias_por_mes[dias_por_mes['cidade'] == cidade]
            dias_mes = dados_cidade.set_index('mes')['dias_chuva'].reindex(range(1, 13), fill_value=0)
            
            ax.plot([meses[i-1] for i in dias_mes.index], dias_mes.values,
                   marker='o', label=cidade, linewidth=2)
        
        ax.set_title('Dias com Precipitação por Mês')
        ax.set_ylabel('Número de Dias')
        ax.legend()
        ax.grid(True, alpha=0.3)
        plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)


# Função para usar as visualizações
def criar_visualizacoes_completas(dados_combinados):
    """Cria todas as visualizações"""
    viz = VisualizacoesMeteorlogicas(dados_combinados)
    
    print("🎨 Criando dashboard principal...")
    viz.dashboard_completo()
    
    print("📊 Criando gráficos específicos...")
    viz.graficos_especificos()
    
    print("✅ Visualizações criadas com sucesso!")
    
    return viz
