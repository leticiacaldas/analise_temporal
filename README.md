# 🌤️ Análise Meteorológica Comparativa - Rio Grande vs Capão do Leão

Sistema de análise de dados meteorológicos que compara as condições climáticas entre Rio Grande e Capão do Leão (RS) usando dados do INMET.

## 🚀 Funcionalidades

- **Análise Estatística**: Estatísticas descritivas e comparações entre cidades
- **Machine Learning**: Modelo Random Forest para previsão de temperatura
- **Visualizações**: Gráficos interativos (Plotly) e estáticos (Matplotlib)
- **Análise Temporal**: Padrões sazonais e tendências de 2023-2025
- **Interface Amigável**: Menu interativo para execução seletiva

## 📊 Tecnologias

- **Python**: Pandas, NumPy, Scikit-learn
- **Visualização**: Plotly, Matplotlib
- **Dados**: CSV do INMET (Instituto Nacional de Meteorologia)
- **ML**: Random Forest para previsão meteorológica

## 🛠️ Instalação

```bash
# Clone o repositório
git clone https://github.com/SEU_USUARIO/analise-meteorologica-rs.git
cd analise-meteorologica-rs

# Instale as dependências
pip install -r requirements.txt

# Execute o sistema
python executar_analise.py
```

## 📁 Estrutura do Projeto

```
analise-meteorologica-rs/
├── analise_temporal.py           # Módulo principal de análise
├── executar_analise.py          # Interface de menu interativo
├── visualizacoes_matplotlib.py  # Visualizações avançadas
├── requirements.txt             # Dependências do projeto
├── README.md                    # Documentação
├── 2023/                        # Dados de 2023 (arquivos CSV)
├── 2024/                        # Dados de 2024 (arquivos CSV)
└── 2025/                        # Dados de 2025 (arquivos CSV)
```

## 📈 Como Usar

### Execução Rápida
```bash
python executar_analise.py
```

### Análise Completa Automática
```python
from analise_temporal import AnaliseMeteorolgicaRS

analise = AnaliseMeteorolgicaRS()
modelo = analise.relatorio_completo()
```

## 🎯 Resultados Gerados

- **Comparações estatísticas** entre microclimas
- **Modelos preditivos** para planejamento agrícola
- **Insights climáticos** para tomada de decisão
- **Visualizações profissionais** para apresentações

## 📊 Exemplos de Análises

- Diferenças de temperatura entre as cidades
- Padrões de precipitação sazonal
- Correlações entre variáveis meteorológicas
- Previsões de temperatura baseadas em ML

## 🤝 Contribuições

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch para sua feature (`git checkout -b feature/nova-analise`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova análise'`)
4. Push para a branch (`git push origin feature/nova-analise`)
5. Abra um Pull Request

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para detalhes.

## 📈 Aplicações

Ideal para:
- Pesquisa acadêmica em climatologia
- Planejamento agrícola regional
- Estudos de microclima
- Análise de dados meteorológicos

## ⚠️ Dados

Os dados meteorológicos são obtidos do INMET. Para usar este projeto:
1. Baixe os dados das estações A802 (Rio Grande) e A887 (Capão do Leão)
2. Organize nos diretórios `2023/`, `2024/`, `2025/`
3. Execute o sistema

---
📧 **Contato**: [seu-email@exemplo.com]  
🔗 **LinkedIn**: [seu-linkedin]

## 📊 Funcionalidades

### ✨ Análises Implementadas

1. **Carregamento Automático de Dados**

    - Lê automaticamente arquivos CSV de múltiplos anos (2023, 2024, 2025)
    - Processa dados do INMET com tratamento de encoding
    - Combina dados de ambas as cidades

2. **Estatísticas Descritivas**

    - Temperatura (média, máxima, mínima, desvio padrão)
    - Precipitação (total, média horária, máxima)
    - Umidade relativa
    - Velocidade do vento

3. **Comparação Estatística**

    - Teste t para comparar médias entre cidades
    - Análise de significância estatística
    - Diferenças quantitativas entre as cidades

4. **Análise de Sazonalidade**

    - Padrões por estação do ano
    - Estatísticas sazonais por cidade

5. **Visualizações Interativas (Plotly)**

    - Série temporal de temperaturas
    - Precipitação comparativa
    - Scatter plot umidade vs temperatura
    - Distribuição de temperaturas
    - Análise de velocidade do vento
    - Pressão atmosférica

6. **Visualizações Estáticas (Matplotlib)**

    - Dashboard completo com 9 gráficos
    - Rosa dos ventos
    - Heatmaps mensais
    - Box plots comparativos
    - Análises específicas complementares

7. **Modelo de Machine Learning**

    - Random Forest para previsão de temperatura
    - Análise de importância das variáveis
    - Métricas de performance (RMSE, R²)

8. **Insights Automatizados**
    - Comparações quantitativas automáticas
    - Recomendações baseadas nos dados
    - Relatório final com conclusões

## 🚀 Como Usar

### Pré-requisitos

```bash
pip install pandas numpy matplotlib seaborn scikit-learn plotly scipy
```

### Execução Básica

```python
# Executar análise completa
from analise_temporal import AnaliseMeteorolgicaRS

analise = AnaliseMeteorolgicaRS()
modelo = analise.relatorio_completo()
```

### Execução de Componentes Individuais

```python
# Carregar dados
analise = AnaliseMeteorolgicaRS()
analise.carregar_dados_multiplos_anos()

# Estatísticas específicas
analise.estatisticas_descritivas()
analise.comparacao_cidades()
analise.analise_sazonalidade()

# Visualizações
analise.visualizacoes_comparativas_avancadas()

# Modelo de previsão
modelo = analise.modelo_previsao_temperatura()
```

## 📁 Estrutura de Arquivos Esperada

```
📂 Dados meteorológicos/
├── analise_temporal.py
├── visualizacoes_matplotlib.py
├── 📂 2023/
│   ├── INMET_S_RS_A802_RIO GRANDE_01-01-2023_A_31-12-2023.CSV
│   └── INMET_S_RS_A887_CAPAO DO LEAO (PELOTAS)_01-01-2023_A_31-12-2023.CSV
├── 📂 2024/
│   ├── INMET_S_RS_A802_RIO GRANDE_01-01-2024_A_31-12-2024.CSV
│   └── INMET_S_RS_A887_CAPAO DO LEAO (PELOTAS)_01-01-2024_A_31-12-2024.CSV
└── 📂 2025/
    ├── INMET_S_RS_A802_RIO GRANDE_01-01-2025_A_31-05-2025.CSV
    └── INMET_S_RS_A887_CAPAO DO LEAO (PELOTAS)_01-01-2025_A_31-05-2025.CSV
```

## 📈 Tipos de Gráficos Gerados

### Plotly (Interativos)

-   Série temporal de temperaturas
-   Precipitação por barras
-   Scatter plot multivariado
-   Histogramas comparativos
-   Análise de vento e pressão

### Matplotlib (Estáticos)

-   Dashboard com 9 painéis
-   Rosa dos ventos polar
-   Heatmaps de correlação
-   Box plots de distribuição
-   Padrões diários e sazonais

## 🔍 Insights Principais Extraídos

O sistema automaticamente identifica:

-   **Diferenças de temperatura** entre as cidades
-   **Padrões de precipitação** comparativos
-   **Variações de umidade** relativa
-   **Características do vento** em cada localidade
-   **Correlações** entre variáveis meteorológicas
-   **Padrões sazonais** e diários

## 🤖 Modelo de Machine Learning

-   **Algoritmo**: Random Forest Regressor
-   **Objetivo**: Prever temperatura baseada em outras variáveis
-   **Features**: Umidade, pressão, vento, hora, dia do ano, mês, cidade
-   **Métricas**: RMSE e R² para avaliar performance
-   **Output**: Importância das variáveis para previsão

## 📊 Variáveis Analisadas

-   🌡️ **Temperatura do ar** (bulbo seco)
-   🌧️ **Precipitação total** horária
-   💧 **Umidade relativa** do ar
-   💨 **Velocidade do vento**
-   🎯 **Direção do vento**
-   📊 **Pressão atmosférica**
-   ☀️ **Radiação global** (quando disponível)

## ⚡ Melhorias Implementadas

✅ **Carregamento robusto**: Tratamento de múltiplos anos automaticamente  
✅ **Visualizações avançadas**: Combinação Plotly + Matplotlib  
✅ **Análises estatísticas**: Testes de significância  
✅ **Machine Learning**: Modelo preditivo com feature importance  
✅ **Relatório automatizado**: Insights e recomendações automáticas  
✅ **Tratamento de erros**: Gerenciamento de dados faltantes  
✅ **Documentação completa**: Código bem comentado

## 🎯 Possíveis Extensões Futuras

1. **Análise de extremos climáticos**
2. **Previsão de precipitação**
3. **Análise de mudanças climáticas temporais**
4. **Comparação com outras cidades**
5. **Dashboard web interativo**
6. **Alertas automáticos baseados em padrões**
7. **Integração com APIs meteorológicas**
8. **Análise de impacto agrícola**
