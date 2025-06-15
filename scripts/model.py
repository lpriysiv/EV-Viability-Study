def run(df):
    summary = df.describe(include='all')
    summary.to_csv("outputs/summary.csv")
    return summary