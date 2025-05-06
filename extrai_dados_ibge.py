import pandas as pd
import numpy as np
import requests
import os

def extrair_dados_ibge_demograficos():
    """Extrai dados demográficos do IBGE"""
    
    # URL da API do IBGE para dados populacionais
    url = "https://servicodados.ibge.gov.br/api/v1/projecoes/populacao"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Criar dataframe com dados de projeção populacional
        df_projecao = pd.DataFrame({
            'data': [item['data'] for item in data['projecao']],
            'populacao': [item['populacao'] for item in data['projecao']],
            'periodo': [item['periodo'] for item in data['projecao']]
        })
        
        # Salvar dados
        df_projecao.to_csv('dados_populacionais_brasil.csv', index=False)
        print(f"Dados salvos em 'dados_populacionais_brasil.csv'")
        return df_projecao
    else:
        print(f"Erro ao acessar a API: {response.status_code}")
        print("Criando dados demográficos de exemplo...")
        return criar_dados_demograficos_exemplo()

def extrair_pib_municipios():
    """Extrai dados do PIB dos municípios do IBGE"""
    
    # URL da API do IBGE para PIB dos municípios
    url = "https://servicodados.ibge.gov.br/api/v1/pesquisas/indicadores/47001/resultados"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        
        # Transformando em dataframe
        pib_data = []
        for item in data:
            indicador = item['indicador']
            for resultado in item['resultados']:
                for localidade in resultado['localidades']:
                    for serie in localidade['series']:
                        for data_point in serie['serie'].items():
                            if data_point[1] is not None:  # Verificar se o valor não é nulo
                                pib_data.append({
                                    'indicador': indicador,
                                    'localidade_id': localidade['id'],
                                    'localidade_nome': localidade['nome'],
                                    'ano': data_point[0],
                                    'valor': data_point[1]
                                })
        
        # Criando dataframe
        df = pd.DataFrame(pib_data)
        
        # Salvar para importar na ferramenta de BI
        df.to_csv('pib_municipios.csv', index=False)
        print(f"Dados salvos em 'pib_municipios.csv'")
        return df
    else:
        print(f"Erro ao acessar a API: {response.status_code}")
        print("Criando dados de PIB municipal de exemplo...")
        return criar_dados_pib_exemplo()

def criar_dados_demograficos_exemplo():
    """Cria dados demográficos de exemplo"""
    import numpy as np
    
    # Criar dataset de exemplo
    np.random.seed(42)
    
    # Criar datas para 10 anos
    anos = range(2010, 2024)
    
    # Criar dataframe
    data = []
    populacao_base = 200000000  # População base em 2010
    
    for ano in anos:
        # Crescimento populacional com alguma variação
        crescimento = 1 + np.random.uniform(0.005, 0.015)  # Entre 0.5% e 1.5% de crescimento
        populacao_base *= crescimento
        
        data.append({
            'data': f'{ano}-07-01',
            'populacao': int(populacao_base),
            'periodo': f'{ano}'
        })
    
    df = pd.DataFrame(data)
    df.to_csv('dados_populacionais_brasil_exemplo.csv', index=False)
    print(f"Dados demográficos de exemplo salvos em 'dados_populacionais_brasil_exemplo.csv'")
    return df

def criar_dados_pib_exemplo():
    """Cria dados de PIB municipal de exemplo"""
    import numpy as np
    
    # Criar dataset de exemplo
    np.random.seed(42)
    
    # Lista de municípios (alguns exemplos)
    municipios = [
        {'id': '3550308', 'nome': 'São Paulo'},
        {'id': '3304557', 'nome': 'Rio de Janeiro'},
        {'id': '5300108', 'nome': 'Brasília'},
        {'id': '2927408', 'nome': 'Salvador'},
        {'id': '3106200', 'nome': 'Belo Horizonte'},
        {'id': '2304400', 'nome': 'Fortaleza'},
        {'id': '1302603', 'nome': 'Manaus'},
        {'id': '2611606', 'nome': 'Recife'},
        {'id': '5103403', 'nome': 'Cuiabá'},
        {'id': '4106902', 'nome': 'Curitiba'}
    ]
    
    # Anos
    anos = range(2010, 2021)
    
    # Criar dataframe
    data = []
    
    for municipio in municipios:
        pib_base = np.random.randint(1000000, 100000000)  # PIB base inicial
        
        for ano in anos:
            # Crescimento do PIB com alguma variação
            crescimento = 1 + np.random.normal(0.03, 0.02)  # Média de 3% com desvio de 2%
            pib_base *= crescimento
            
            data.append({
                'indicador': 'PIB Municipal',
                'localidade_id': municipio['id'],
                'localidade_nome': municipio['nome'],
                'ano': str(ano),
                'valor': round(pib_base, 2)
            })
    
    df = pd.DataFrame(data)
    df.to_csv('pib_municipios_exemplo.csv', index=False)
    print(f"Dados de PIB municipal de exemplo salvos em 'pib_municipios_exemplo.csv'")
    return df 