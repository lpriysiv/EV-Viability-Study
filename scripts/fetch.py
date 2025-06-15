import pandas as pd
import requests

def run():
    response = requests.get("https://api.sampleapis.com/futurama/characters")
    data = response.json()
    df = pd.DataFrame(data)
    df.to_csv("data/raw/fetched_data.csv", index=False)
    return df
