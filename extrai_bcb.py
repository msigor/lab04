import pandas as pd
import requests
import os

def extrair_dados_bcb():
    """Extrai dados econômicos do Banco Central do Brasil"""
    
    # URL da API do BCB para séries temporais (exemplo: taxa Selic - 432)
    url = "https://api.bcb.gov.br/dados/serie/bcdata.sgs.432/dados?formato=json"
    
    try:
        response = requests.get(url)
        
        if response.status_code == 200:
            data = response.json()
            
            # Converter para DataFrame
            df = pd.DataFrame(data)
            
            # Converter tipos de dados
            df['data'] = pd.to_datetime(df['data'], format='%d/%m/%Y')
            df['valor'] = pd.to_numeric(df['valor'], errors='coerce')
            
            # Adicionar coluna de ano para facilitar agregações
            df['ano'] = df['data'].dt.year
            df['mes'] = df['data'].dt.month
            
            # Salvar dados
            df.to_csv('taxa_selic_historica.csv', index=False)
            print(f"Dados da taxa Selic salvos em 'taxa_selic_historica.csv'")
            
            return df
        else:
            print(f"Erro ao acessar a API do BCB: {response.status_code}")
            return None
    except Exception as e:
        print(f"Erro ao processar dados do BCB: {e}")
        return None 