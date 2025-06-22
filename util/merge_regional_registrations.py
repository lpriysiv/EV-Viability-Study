import pandas as pd
import os

def run():
    print("Merging regional registrations data...")
    # Read the regional registrations data
    csv_dir = "./util/Statewise_EV_Reg_Data"
    selected_columns = ["State", "Registration Date", "Vehicle Make", "Vehicle Model", "Vehicle Model Year", "Drivetrain Type"]
    regional_df = pd.concat([pd.read_csv(os.path.join(csv_dir, f)) for f in os.listdir(csv_dir) if f.endswith(".csv")])
    regional_df = regional_df[selected_columns]
    # Convert 'Registration Date' to datetime
    regional_df['Registration Date'] = pd.to_datetime(regional_df['Registration Date'], errors='coerce')
    # Drop rows with NaT in 'Registration Date'
    regional_df.drop_duplicates(inplace=True)
    regional_df.dropna(subset=['Registration Date'], inplace=True)
    # Coerce 'Vehicle Model Year' to numeric, handling errors
    regional_df['Vehicle Model Year'] = regional_df['Vehicle Model Year'].apply(pd.to_numeric, errors='coerce').astype('Int64')
    # Coerce 'Vehicle Make' and 'Vehicle Model' to string
    regional_df['Vehicle Make'] = regional_df['Vehicle Make'].astype(str)
    regional_df['Vehicle Model'] = regional_df['Vehicle Model'].astype(str)
    # Load climate region data abnd merge with regional_df
    climate_region_df = pd.read_csv("./util/us_climate_regions.csv")
    # Ensure 'state_code' column is in the same format for merging
    climate_region_df['state_code'] = climate_region_df['state_code'].str.strip().str.upper()
    regional_df['State'] = regional_df['State'].str.strip().str.upper()
    # Merge regional_df with climate_region_df to add the 'Climate Region' column based on 'State' and 'state_code'
    # This assumes 'State' in regional_df matches 'state_code' in climate_region_df
    regional_df = regional_df.merge(climate_region_df[['state_code', 'climate_regions']], left_on='State', right_on='state_code', how='left')
    # Save the merged data to a CSV file
    regional_df.to_csv("input/ev_registrations_by_region.csv", index=False)
    print("Merged regional registrations data saved to 'input/ev_registrations_by_region.csv'.")
    return
