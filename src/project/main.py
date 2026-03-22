import requests
import pandas as pd

def fetch_ine_data():
    url = "https://servicios.ine.es/wstempus/js/ES/DATOS_TABLA/50904"  
    
    response = requests.get(url)
    response.raise_for_status()

    return response.json()


def build_dataframe(data):
    records = []

    for item in data:
        row = {
            "region": item.get("Nombre"),
            "period": item.get("Periodo"),
            "value": item.get("Valor")
        }
        records.append(row)

    df = pd.DataFrame(records)
    return df


def main():
    data = fetch_ine_data()
    df = build_dataframe(data)
    print(df.head())

main()