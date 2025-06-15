import pandas as pd

def run(df):
    df_clean = df.dropna(subset=["name"])
    df_clean.to_csv("data/processed/clean_data.csv", index=False)
    return df_clean