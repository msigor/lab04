# Extração e Caracterização de Dados Governamentais

Este projeto realiza a extração, processamento e caracterização de dados de diversas fontes governamentais brasileiras e prepara os dados para visualização em ferramentas de Business Intelligence como Power BI.

## Fontes de Dados

- Dados demográficos (IBGE)
- PIB Municipal (IBGE)
- Dados de Servidores (Portal da Transparência)
- Taxa Selic (Banco Central)
- Dados de COVID-19

## Instalação

1. Clone este repositório
2. Instale as dependências:

```
pip install -r requirements.txt
```

## Uso

1. Execute o script principal:

```
python Executa
```

2. Selecione uma das opções de dados para extrair
3. O script extrairá os dados, realizará a caracterização e preparará os arquivos para importação no Power BI

## Arquivos de Saída

Os arquivos serão salvos na pasta `output` e incluem:

- Dados brutos em formato CSV
- Estatísticas descritivas
- Visualizações estáticas (PNG)
- Arquivos prontos para importação no Power BI (CSV e Excel)
- Modelo de dashboard em formato JSON

## Criando um Dashboard no Power BI

1. Abra o Power BI Desktop
2. Clique em "Obter Dados" > "Arquivo" > "Excel" ou "CSV"
3. Navegue até a pasta `output` e selecione o arquivo `[dataset]_para_bi.xlsx` ou `[dataset]_para_bi.csv`
4. Carregue os dados no Power BI
5. Crie as visualizações conforme sugerido pelo modelo:

### Página 1: Visão Geral
- Adicione um título "Caracterização do Dataset"
- Adicione um cartão com o número total de registros
- Adicione um cartão com o número de colunas
- Adicione uma visualização de mapa de calor para mostrar a completude dos dados
- Adicione um gráfico de barras para mostrar a distribuição temporal dos dados

### Página 2: Análise Detalhada
- Adicione uma tabela com as estatísticas descritivas
- Adicione histogramas para as principais variáveis numéricas
- Adicione gráficos de barras para as principais variáveis categóricas

### Página 3: Análise de Correlações
- Adicione uma matriz de correlação visual
- Adicione gráficos de dispersão para pares de variáveis com alta correlação 