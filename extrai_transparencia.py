import pandas as pd
import numpy as np
import requests
import os

def extrair_dados_servidores():
    """Extrai dados de servidores do Portal da Transparência"""
    
    # URL da API do Portal da Transparência (amostra limitada para não sobrecarregar a API)
    url = "http://api.portaldatransparencia.gov.br/api-de-dados/servidores"
    
    # Parâmetros para a consulta
    params = {
        "pagina": 1,
        "tamanhoPagina": 100  # Limitando a 100 registros para exemplo
    }
    
    # Headers necessários (substitua pela sua chave de API se necessário)
    headers = {
        "accept": "*/*",
        "chave-api-dados": "sua-chave-aqui"  # Você precisa se registrar no portal para obter uma chave
    }
    
    try:
        response = requests.get(url, params=params, headers=headers)
        
        if response.status_code == 200:
            data = response.json()
            df = pd.DataFrame(data)
            df.to_csv('servidores_federais.csv', index=False)
            print(f"Dados salvos em 'servidores_federais.csv'")
            return df
        else:
            print(f"Erro ao acessar a API: {response.status_code}")
            # Como alternativa, vamos criar dados sintéticos para exemplo
            return criar_dados_servidores_exemplo()
    except Exception as e:
        print(f"Erro ao acessar a API: {e}")
        # Como alternativa, vamos criar dados sintéticos para exemplo
        return criar_dados_servidores_exemplo()

def criar_dados_servidores_exemplo():
    """Cria dados sintéticos como exemplo de servidores"""
    import numpy as np
    
    # Criar dataset de exemplo com 1000 servidores
    np.random.seed(42)
    n = 1000
    
    # Dados sintéticos
    df = pd.DataFrame({
        'id': range(1, n+1),
        'nome': [f'Servidor {i}' for i in range(1, n+1)],
        'orgao': np.random.choice(['Ministério da Educação', 'Ministério da Saúde', 
                                  'Ministério da Economia', 'Ministério da Defesa', 
                                  'Outros'], n),
        'cargo': np.random.choice(['Analista', 'Técnico', 'Especialista', 
                                  'Assistente', 'Coordenador'], n),
        'salario': np.random.normal(8000, 3000, n),
        'data_ingresso': pd.date_range(start='2000-01-01', periods=n, freq='W')
    })
    
    df.to_csv('servidores_federais_exemplo.csv', index=False)
    print(f"Dados de exemplo salvos em 'servidores_federais_exemplo.csv'")
    return df 