import pandas as pd
import numpy as np
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

def caracterizar_dataset(df, nome_dataset, pasta_output='output'):
    """
    Realiza análise exploratória para caracterizar o dataset
    
    Parâmetros:
    df (DataFrame): DataFrame a ser analisado
    nome_dataset (str): Nome do dataset para uso nos arquivos de saída
    pasta_output (str): Pasta onde os arquivos serão salvos
    """
    # Criar pasta de output se não existir
    if not os.path.exists(pasta_output):
        os.makedirs(pasta_output)
    
    # 1. Informações gerais do dataset
    info = {
        'num_registros': len(df),
        'num_colunas': len(df.columns),
        'colunas': list(df.columns),
        'tipos_dados': {col: str(df[col].dtype) for col in df.columns},
        'valores_nulos': {col: int(df[col].isna().sum()) for col in df.columns},
        'percentual_nulos': {col: float(df[col].isna().mean()*100) for col in df.columns}
    }
    
    # Salvar informações em JSON
    with open(f'{pasta_output}/{nome_dataset}_info.json', 'w') as f:
        json.dump(info, f, indent=4)
    
    # 2. Estatísticas descritivas para colunas numéricas
    colunas_numericas = df.select_dtypes(include=['number']).columns
    if len(colunas_numericas) > 0:
        estatisticas = df[colunas_numericas].describe().transpose().reset_index()
        estatisticas.rename(columns={'index': 'coluna'}, inplace=True)
        estatisticas.to_csv(f'{pasta_output}/{nome_dataset}_estatisticas.csv', index=False)
    
    # 3. Distribuição de valores para colunas categóricas
    colunas_categoricas = df.select_dtypes(exclude=['number']).columns
    for col in colunas_categoricas:
        if df[col].nunique() <= 30:  # Limitar para colunas com não muitas categorias
            dist = df[col].value_counts().reset_index()
            dist.columns = [col, 'contagem']
            dist.to_csv(f'{pasta_output}/{nome_dataset}_distribuicao_{col}.csv', index=False)
    
    # 4. Análise temporal (se aplicável)
    colunas_data = [col for col in df.columns if 'data' in col.lower() or 'date' in col.lower() or df[col].dtype == 'datetime64[ns]']
    
    for col_data in colunas_data:
        try:
            # Converter para datetime se ainda não estiver
            if df[col_data].dtype != 'datetime64[ns]':
                df[col_data] = pd.to_datetime(df[col_data], errors='coerce')
            
            # Extrair ano e mês
            df['ano'] = df[col_data].dt.year
            df['mes'] = df[col_data].dt.month
            
            # Contagem por ano
            contagem_ano = df.groupby('ano').size().reset_index(name='contagem')
            contagem_ano.to_csv(f'{pasta_output}/{nome_dataset}_contagem_por_ano.csv', index=False)
            
            # Contagem por mês (último ano)
            ultimo_ano = df['ano'].max()
            contagem_mes = df[df['ano'] == ultimo_ano].groupby('mes').size().reset_index(name='contagem')
            contagem_mes.to_csv(f'{pasta_output}/{nome_dataset}_contagem_por_mes.csv', index=False)
            
            # Remover colunas temporárias
            df.drop(['ano', 'mes'], axis=1, inplace=True, errors='ignore')
            
        except Exception as e:
            print(f"Erro na análise temporal da coluna {col_data}: {e}")
    
    # 5. Gerar visualizações úteis para o dashboard
    try:
        # Configurar estilo
        plt.style.use('seaborn-v0_8-whitegrid')
        
        # a. Completude dos dados (heatmap de valores nulos)
        plt.figure(figsize=(10, 6))
        sns.heatmap(df.isnull(), cbar=False, yticklabels=False, cmap='viridis')
        plt.title('Mapa de Valores Ausentes no Dataset')
        plt.tight_layout()
        plt.savefig(f'{pasta_output}/{nome_dataset}_valores_ausentes.png', dpi=300)
        plt.close()
        
        # b. Histogramas para variáveis numéricas
        for col in colunas_numericas[:5]:  # Limitar a 5 colunas para não gerar muitos gráficos
            plt.figure(figsize=(10, 6))
            sns.histplot(df[col].dropna(), kde=True)
            plt.title(f'Distribuição de {col}')
            plt.tight_layout()
            plt.savefig(f'{pasta_output}/{nome_dataset}_histograma_{col}.png', dpi=300)
            plt.close()
        
        # c. Barplot para variáveis categóricas
        for col in colunas_categoricas:
            if df[col].nunique() <= 10:  # Limitar para colunas com poucas categorias
                plt.figure(figsize=(10, 6))
                top_cats = df[col].value_counts().nlargest(10)
                sns.barplot(x=top_cats.index, y=top_cats.values)
                plt.title(f'Top 10 Categorias em {col}')
                plt.xticks(rotation=45)
                plt.tight_layout()
                plt.savefig(f'{pasta_output}/{nome_dataset}_barplot_{col}.png', dpi=300)
                plt.close()
        
        # d. Correlação entre variáveis numéricas (se tiver mais de uma)
        if len(colunas_numericas) > 1:
            plt.figure(figsize=(12, 10))
            corr = df[colunas_numericas].corr()
            mask = np.triu(np.ones_like(corr, dtype=bool))
            sns.heatmap(corr, mask=mask, annot=True, cmap='coolwarm', linewidths=.5)
            plt.title('Matriz de Correlação das Variáveis Numéricas')
            plt.tight_layout()
            plt.savefig(f'{pasta_output}/{nome_dataset}_correlacao.png', dpi=300)
            plt.close()
        
        # e. Séries temporais (se aplicável)
        for col_data in colunas_data:
            for col_num in colunas_numericas[:3]:  # Limitar a 3 colunas numéricas
                try:
                    plt.figure(figsize=(12, 6))
                    df_temp = df.copy()
                    df_temp[col_data] = pd.to_datetime(df_temp[col_data], errors='coerce')
                    df_temp = df_temp.sort_values(col_data)
                    df_temp = df_temp.set_index(col_data)
                    df_temp[col_num].resample('M').mean().plot()
                    plt.title(f'Série Temporal de {col_num} (Média Mensal)')
                    plt.tight_layout()
                    plt.savefig(f'{pasta_output}/{nome_dataset}_serie_temporal_{col_num}.png', dpi=300)
                    plt.close()
                except Exception as e:
                    print(f"Erro ao criar série temporal para {col_num}: {e}")
    
    except Exception as e:
        print(f"Erro ao gerar visualizações: {e}")
    
    # 6. Preparar arquivo para Power BI ou Tableau
    # Salvar dataset completo em formato adequado para BI
    df.to_csv(f'{pasta_output}/{nome_dataset}_para_bi.csv', index=False)
    
    try:
        df.to_excel(f'{pasta_output}/{nome_dataset}_para_bi.xlsx', index=False)
    except Exception as e:
        print(f"Erro ao salvar em Excel, tente instalar openpyxl: {e}")
    
    print(f"Caracterização do dataset '{nome_dataset}' concluída. Arquivos salvos em '{pasta_output}'")
    return info 