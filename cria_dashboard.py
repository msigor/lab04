import json

def criar_modelo_power_bi(pasta_input='output', nome_dataset='pib_municipios'):
    """
    Cria um modelo conceitual de como seria o dashboard no Power BI
    """
    modelo = {
        "dashboardTitle": f"Caracterização do Dataset - {nome_dataset}",
        "pages": [
            {
                "name": "Visão Geral",
                "visualizations": [
                    {
                        "title": "Número Total de Registros",
                        "type": "card",
                        "position": {"x": 0, "y": 0, "width": 8, "height": 4},
                        "data": {
                            "source": f"{nome_dataset}_para_bi.csv",
                            "measure": "COUNT()"
                        }
                    },
                    {
                        "title": "Completude dos Dados",
                        "type": "heatmap",
                        "position": {"x": 8, "y": 0, "width": 16, "height": 12},
                        "data": {
                            "source": f"{nome_dataset}_valores_ausentes.png"
                        }
                    },
                    {
                        "title": "Distribuição Temporal",
                        "type": "column_chart",
                        "position": {"x": 0, "y": 12, "width": 24, "height": 12},
                        "data": {
                            "source": f"{nome_dataset}_contagem_por_ano.csv",
                            "xAxis": "ano",
                            "yAxis": "contagem"
                        }
                    }
                ]
            },
            {
                "name": "Análise Detalhada",
                "visualizations": [
                    {
                        "title": "Estatísticas Principais",
                        "type": "table",
                        "position": {"x": 0, "y": 0, "width": 24, "height": 8},
                        "data": {
                            "source": f"{nome_dataset}_estatisticas.csv"
                        }
                    },
                    {
                        "title": "Distribuições",
                        "type": "image",
                        "position": {"x": 0, "y": 8, "width": 12, "height": 12},
                        "data": {
                            "source": f"{nome_dataset}_histograma_valor.png"
                        }
                    },
                    {
                        "title": "Correlações",
                        "type": "image",
                        "position": {"x": 12, "y": 8, "width": 12, "height": 12},
                        "data": {
                            "source": f"{nome_dataset}_correlacao.png"
                        }
                    }
                ]
            }
        ]
    }
    
    # Salvar o modelo como um JSON
    with open(f'modelo_dashboard_{nome_dataset}.json', 'w') as f:
        json.dump(modelo, f, indent=4)
    
    print(f"Modelo de dashboard para {nome_dataset} criado.")
    print("Para criar o dashboard real:")
    print("1. Abra o Power BI Desktop")
    print(f"2. Importe os arquivos da pasta {pasta_input}")
    print("3. Crie as visualizações conforme o modelo")
    
    return modelo 