import pandas as pd
import numpy as np
import requests
import os

def extrair_dados_covid():
    """Extrai dados de COVID-19 do Brasil.io (baseado em dados do Ministério da Saúde)"""
    
    # URL para download dos dados (fonte alternativa já que a API direta requer autenticação)
    url = "https://data.brasil.io/dataset/covid19/caso.csv.gz"
    
    try:
        # Criar diretório temporário se não existir
        temp_dir = 'temp'
        if not os.path.exists(temp_dir):
            os.makedirs(temp_dir)
            
        # Baixar o arquivo
        file_path = os.path.join(temp_dir, 'covid19_data.csv.gz')
        response = requests.get(url, stream=True)
        
        if response.status_code == 200:
            with open(file_path, 'wb') as f:
                f.write(response.content)
            
            # Ler arquivo comprimido
            df = pd.read_csv(file_path, compression='gzip')
            
            # Filtrar apenas os últimos 6 meses para reduzir tamanho
            if 'date' in df.columns:
                df['date'] = pd.to_datetime(df['date'])
                latest_date = df['date'].max()
                six_months_ago = latest_date - pd.Timedelta(days=180)
                df = df[df['date'] >= six_months_ago]
            
            # Salvar versão processada
            df.to_csv('covid19_brasil.csv', index=False)
            print(f"Dados de COVID-19 salvos em 'covid19_brasil.csv'")
            return df
        else:
            print(f"Erro ao baixar dados: {response.status_code}")
            return criar_dados_covid_exemplo()
    except Exception as e:
        print(f"Erro ao processar dados de COVID-19: {e}")
        return criar_dados_covid_exemplo()

def criar_dados_covid_exemplo():
    """Cria dados sintéticos de COVID-19 como exemplo"""
    import numpy as np
    
    # Criar dataset de exemplo
    np.random.seed(42)
    
    # Lista de estados
    estados = ['AC', 'AL', 'AM', 'AP', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MG', 'MS', 'MT',
               'PA', 'PB', 'PE', 'PI', 'PR', 'RJ', 'RN', 'RO', 'RR', 'RS', 'SC', 'SE', 'SP', 'TO']
    
    # Criar datas para 6 meses
    dates = pd.date_range(start='2023-06-01', end='2023-12-31')
    
    # Criar dataframe
    data = []
    for state in estados:
        for date in dates:
            # Valores fictícios com alguma correlação
            cases_base = np.random.randint(100, 5000)
            deaths_base = int(cases_base * np.random.uniform(0.01, 0.05))
            
            data.append({
                'estado': state,
                'data': date,
                'casos': cases_base,
                'obitos': deaths_base,
                'populacao': np.random.randint(500000, 20000000)
            })
    
    df = pd.DataFrame(data)
    df.to_csv('covid19_brasil_exemplo.csv', index=False)
    print(f"Dados de exemplo de COVID-19 salvos em 'covid19_brasil_exemplo.csv'")
    return df 