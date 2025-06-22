import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt


def run():
    # Load the merged EV registrations data
    local_file_path = "input/ev_registrations_by_region.csv"

    # Read the CSV file into a DataFrame
    df = pd.read_csv(local_file_path, low_memory=False)
    df.rename(columns={'climate_regions': 'Climate Region'}, inplace=True)
    df['Vehicle Model Year'] = df['Vehicle Model Year'].apply(pd.to_numeric, errors='coerce').astype('Int64')
    # Keep only the columns with Drivetrain Type BEV
    df = df[df['Drivetrain Type'] == 'BEV']
    # Get the top 10 most registered electric vehicle model, make and model year by climate region
    top_10_evs = df.groupby(['Climate Region', 'Vehicle Make', 'Vehicle Model', 'Vehicle Model Year','State']).size().reset_index(name='Count')
    top_10_evs = top_10_evs.sort_values(by=['Climate Region', 'Count'], ascending=[True, False])
    top_10_evs = top_10_evs.groupby('Climate Region').head(10).reset_index(drop=True)   
    # Save the top 10 electric vehicles by climate region to a CSV file
    output_file_path = "input/top_10_evs_by_region.csv"
    top_10_evs.to_csv(output_file_path, index=False)
    print(f"Top 10 electric vehicles by climate region saved to '{output_file_path}'.")

    # Create a color map for climate regions
    climate_regions = top_10_evs['Climate Region'].unique()
    colors = plt.cm.get_cmap('tab10', len(climate_regions))
    climate_region_color_map = {region: colors(i) for i, region in enumerate(climate_regions)}
    # Combine manufacturer and model and year for labeling
    top_10_evs['ModelLabel'] = top_10_evs['Vehicle Make'] + ' ' + top_10_evs['Vehicle Model'] + ' ' + top_10_evs['Vehicle Model Year'].astype(str)
    # Ensure unique labels for each vehicle model by appending the state
    top_10_evs['ModelLabel'] = top_10_evs['ModelLabel'] + ' (' + top_10_evs['State'] + ')'
    # Create the figure and axes. 
    # Subplots should be two columns in each row, one for each climate region
    # and each cell should represent a climate region with the top 10 electric vehicles.

    regions = sorted(top_10_evs['Climate Region'].unique(), reverse=True)
    n_regions = len(regions)
    # Set up subplots in two columns
    n_cols = 2
    n_rows = int(np.ceil(n_regions / n_cols))
    fig, axes = plt.subplots(n_rows, n_cols, figsize=(12, 3.2 * n_rows), squeeze=False)
    plt.subplots_adjust(top=0.90, hspace=0.4, wspace=1.0)  # More space between columns

    for idx, region in enumerate(regions):
        row = idx // n_cols
        col = idx % n_cols
        region_data = top_10_evs[top_10_evs['Climate Region'] == region]
        axes[row, col].barh(region_data['ModelLabel'], region_data['Count'], color=[climate_region_color_map[region]] * len(region_data), height=0.22)
        axes[row, col].set_title(f'Climate Region: {region}', fontsize=8)
        axes[row, col].set_xlabel('Number of Registrations', fontsize=6)
        axes[row, col].set_ylabel('Vehicle Model', fontsize=6)
        axes[row, col].invert_yaxis()
        # Reduce font size of ModelLabel (y-tick labels)
        axes[row, col].set_yticklabels(region_data['ModelLabel'], fontsize=6)
        # Add value labels to the bars
        for j, value in enumerate(region_data['Count']):
            axes[row, col].text(value, j, str(value), va='center', fontsize=6)
    # Hide any unused subplots
    for idx in range(n_regions, n_rows * n_cols):
        row = idx // n_cols
        col = idx % n_cols
        fig.delaxes(axes[row, col])
    # Adjust layout
    plt.subplots_adjust()
    # Save the plot
    plt.savefig("output/top_10_evs_by_region.png", bbox_inches='tight')
    print("Top 10 electric vehicles by climate region plot saved to 'output/top_10_evs_by_region.png'.")
    plt.close()  # Close the plot to free up memory
    # Save the DataFrame to a CSV file for further analysis
    top_10_evs.to_csv("output/top_10_evs_by_region_detailed.csv", index=False)
    print("Detailed top 10 electric vehicles by climate region saved to 'output/top_10_evs_by_region_detailed.csv'.")
    return