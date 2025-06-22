import pandas as pd
import numpy as np
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth
import matplotlib.pyplot as plt

def autopct_func(pct):
    total = sum(sizes)
    idx = int(round(pct/100.*(len(itemset_labels)-1)))
    if pct > 0 and idx < len(itemset_labels):
        return itemset_labels.iloc[idx]
    return ''

def run():
    # Load the merged EV registrations data
    local_file_path = "input/ev_registrations_by_region.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(local_file_path, low_memory=False)
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    # Keep only the columns with Drivetrain Type BEV
    df = df[df['Drivetrain Type'] == 'BEV']  
    df['Vehicle'] = df['Vehicle Make'] + ' ' + df['Vehicle Model']
    

    # Group by State and Vehicle, sum the counts
    table = df.groupby(['Vehicle']).size().reset_index(name='Count')

    # Sort by Count descending and take the top 10
    top_10 = table.sort_values(by='Count', ascending=False).head(10)

    # Print the table
    print("Top 10 EVs across all states:")
    print(top_10.to_string(index=False))

    # Save the table as an image
    _, ax = plt.subplots(figsize=(12, 2 + 0.3 * len(top_10)))
    plt.subplots_adjust(top=0.5)
    ax.axis('off')
    tbl = ax.table(cellText=top_10.values, colLabels=top_10.columns, loc='center', cellLoc='center', colColours=['#4F81BD']*len(top_10.columns))

    # Style header
    for (row, _), cell in tbl.get_celld().items():
        if row == 0:
            cell.set_text_props(weight='bold', color='white')
            cell.set_facecolor('#4F81BD')
        elif row % 2 == 0:
            cell.set_facecolor('#DCE6F1')
        else:
            cell.set_facecolor('white')
        cell.set_edgecolor('#4F81BD')
        cell.set_fontsize(10)

    tbl.auto_set_font_size(False)
    tbl.set_fontsize(8)
    tbl.auto_set_column_width(col=list(range(len(top_10.columns))))
    plt.savefig('output/top_10_evs_across_states.png', bbox_inches='tight', dpi=200)
    plt.close()

    # For fp analysis reduce columns
    selected_columns = ['Vehicle']
    df = df[selected_columns]
    list_of_lists = df.values.tolist()

    # Get frquent itemsets using fpgrowth
    # Prepare transaction encoder
    te = TransactionEncoder()
    te_transform = te.fit(list_of_lists).transform(list_of_lists)
    fp_df = pd.DataFrame(te_transform, columns=te.columns_)
    # Run fp growth on this fp_df and save output for display
    frequent_registrations = fpgrowth(fp_df, min_support=0.015, use_colnames=True).sort_values(by='support', ascending=False)
    print(frequent_registrations)

    # Display the top 10 as a bar chart
    labels = frequent_registrations['itemsets'].apply(lambda x: next(iter(x)) if isinstance(x, frozenset) and len(x) == 1 else str(x))
    sizes = frequent_registrations['support']


    fig, ax1 = plt.subplots(figsize=(12, 6))

    ax1.bar(labels, sizes, color='C5')
    ax1.set_ylabel('Support')
    ax1.set_xlabel('Vehicle')
    ax1.set_title('Frequent EV Registrations')
    ax1.tick_params(axis='x', rotation=65)

    plt.tight_layout()
    plt.show()
    #plt.savefig('output/freq_registrations.png')
    plt.close()