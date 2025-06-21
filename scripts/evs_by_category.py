import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt

def get_value_from_range(value):
    if isinstance(value, str) and '-' in value:
        lower, _ = value.split('-')
        return int(lower)
    return int(value)


def run():
    #Fetch the ev data from NREL API
    key=os.getenv("NREL_API_KEY")
    response = requests.get(f"https://developer.nrel.gov/api/vehicles/v1/light_duty_automobiles.csv?api_key={key}&fuel_id=41")
    local_file_path = "input/ev_list.csv"
    with open(local_file_path, 'wb') as f:
        for chunk in response.iter_content(chunk_size=8192):
            f.write(chunk)

    print(f"File '{local_file_path}' downloaded successfully.")
    # Read the CSV file into a DataFrame
    df = pd.read_csv(local_file_path, low_memory=False)
    
    # Clean and preprocess the data
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    # Remove rows with missing values in the 'Electric-Only Range' column
    df.dropna(subset=["Electric-Only Range"], inplace=True)
    # Convert 'Electric-Only Range' to numeric
    df["Electric-Only Range"] =df["Electric-Only Range"].apply(get_value_from_range)
    # Filter for the last 3 years of data
    current_year = datetime.now().year
    df_recent = df[df['Model Year'] >= (current_year - 3)]
    # Get the top 10 electric vehicles by electric-only range for every year in the last 3 years
    top_10_evs = df_recent.groupby('Model Year').apply(lambda x: x.nlargest(10, 'Electric-Only Range'))
    # Select relevant columns
    top_10_evs = top_10_evs[['Model', 'Model Year', 'Manufacturer', 'Electric-Only Range', 'Category']].reset_index(drop=True)
    # Save the top 10 electric vehicles to a CSV file
    output_file_path = "input/top_10_evs.csv"
    top_10_evs.to_csv(output_file_path, index=False)

    # Create a color map for categories
    categories = top_10_evs['Category'].unique()
    colors = plt.cm.get_cmap('tab10', len(categories))
    category_color_map = {cat: colors(i) for i, cat in enumerate(categories)}

    # Combine manufacturer and model for labeling
    top_10_evs['ModelLabel'] = top_10_evs['Manufacturer'] + ' ' + top_10_evs['Model']
    # Ensure unique labels for each bar
    top_10_evs['UniqueLabel'] = top_10_evs['Manufacturer'] + ' ' + top_10_evs['Model'] + ' (' + top_10_evs.index.astype(str) + ')'

    # Prepare legend handles (before plotting)
    handles = [plt.Rectangle((0,0),1,1, color=category_color_map[cat]) for cat in categories]
    # Create the figure and axes
    years = sorted(top_10_evs['Model Year'].unique(), reverse=True)
    n_years = len(years)
    _, axes = plt.subplots(n_years, 1, figsize=(20, 6 * n_years), squeeze=False)
   
  
    for idx, year in enumerate(years):
        year_data = top_10_evs[top_10_evs['Model Year'] == year].copy()
        ax = axes[idx, 0]

        # Assign colors for each bar based on category
        bar_colors = year_data['Category'].map(category_color_map)
        ax.bar(year_data['UniqueLabel'], year_data['Electric-Only Range'], 
               color=bar_colors, edgecolor='black', width=0.2, snap=False)
        ax.set_xlabel('Electric Vehicle (Manufacturer Model and Index)')
        ax.set_ylabel('Electric-Only Range (miles)')
        ax.set_title(f'Top 10 Electric Vehicles by Electric-Only Range - {year}')
        ax.set_xlim(-0.5, len(year_data) - 0.5)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        # Set x-tick labels only
        ax.set_xticklabels(year_data['UniqueLabel'], rotation=45, ha='right', fontsize=10)
        # Only add legend once, and place it inside the plot
        if idx == 0:
            handles = [plt.Rectangle((0,0),1,1, color=category_color_map[cat]) for cat in categories]
            ax.legend(handles, categories, title='Category', loc='upper right', bbox_to_anchor=(0.98, 0.98), frameon=True)
    plt.tight_layout(h_pad=3)
    plt.savefig("output/evs_by_range_combined.png")
    print("Combined bar chart saved to 'output/evs_by_range_combined.png'.")
    plt.show()

