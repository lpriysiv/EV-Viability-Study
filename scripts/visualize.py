import matplotlib.pyplot as plt

def run(df, _):
    plt.figure(figsize=(6, 4))
    df['age'] = df['age'].fillna(0).astype(int)
    df['age'].hist(bins=10)
    plt.title("Age Distribution")
    plt.savefig("outputs/plots.png")
