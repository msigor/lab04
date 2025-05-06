import pandas as pd
import numpy as np
import requests
import json
import os
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    """Script principal para executar todo o processo de extração e caracterização"""
    print("Iniciando processo de extração e caracterização de dados governamentais")
    
    # 1. Criar pasta de saída
    output_dir = 'output'
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    
    # 2. Selecionar e extrair um dataset (escolha um dos métodos abaixo)
    print("\n** Selecionando dataset para extração **")
    print("1. Dados demográficos (IBGE)")
    print("2. PIB Municipal (IBGE)")
    print("3. Dados de Servidores (Portal da Transparência)")
    print("4. Taxa Selic (Banco Central)")
    print("5. Dados de COVID-19")
    
    try:
        choice = int(input("Escolha uma opção (1-5): "))
    except:
        # Para este exemplo, vamos escolher o PIB Municipal como padrão
        choice = 2
        print(f"Opção selecionada (padrão): {choice}")
    
    # Extrair o dataset escolhido
    df = None
    dataset_name = ""
    
    if choice == 1:
        df = extrair_dados_ibge_demograficos()
        dataset_name = "demografia"
    elif choice == 2:
        df = extrair_pib_municipios()
        dataset_name = "pib_municipios"
    elif choice == 3:
        df = extrair_dados_servidores()
        dataset_name = "servidores"
    elif choice == 4:
        df = extrair_dados_bcb()
        dataset_name = "taxa_selic"
    elif choice == 5:
        df = extrair_dados_covid()
        dataset_name = "covid19"
    else:
        print("Opção inválida! Usando PIB Municipal como padrão.")
        df = extrair_pib_municipios()
        dataset_name = "pib_municipios"
    
    # 3. Caracterizar o dataset
    if df is not None:
        print(f"\nCaracterizando dataset: {dataset_name}")
        info = caracterizar_dataset(df, dataset_name, pasta_output=output_dir)
        
        # 4. Criar modelo de dashboard
        print("\nCriando modelo de dashboard para Power BI")
        modelo = criar_modelo_power_bi(pasta_input=output_dir, nome_dataset=dataset_name)
        
        print("\nProcesso completo!")
        print(f"Arquivos gerados na pasta: {output_dir}")
        print("Agora você pode importar esses arquivos no Power BI, Tableau ou Google Data Studio")
        
        print("\nPara criar o dashboard no Power BI:")
        print("1. Abra o Power BI Desktop")
        print("2. Clique em 'Obter Dados' > 'Arquivo' > 'Excel' ou 'CSV'")
        print(f"3. Navegue até a pasta {output_dir} e selecione o arquivo {dataset_name}_para_bi.xlsx ou {dataset_name}_para_bi.csv")
        print("4. Carregue os dados no Power BI")
        print("5. Crie as visualizações conforme o modelo sugerido")
    else:
        print("Erro: Não foi possível extrair o dataset selecionado.")

if __name__ == "__main__":
    # Importar as funções definidas anteriormente
    from extrai_dados_ibge import extrair_dados_ibge_demograficos, extrair_pib_municipios
    from extrai_transparencia import extrair_dados_servidores
    from extrai_bcb import extrair_dados_bcb
    from extrai_covid import extrair_dados_covid
    from caracteriza_dataset import caracterizar_dataset
    from cria_dashboard import criar_modelo_power_bi
    
    # Executar script principal
    main() 