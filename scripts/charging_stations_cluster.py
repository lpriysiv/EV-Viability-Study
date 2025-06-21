import os
import requests
import pandas as pd
import numpy as np
import folium
from folium.plugins import MarkerCluster
from sklearn.cluster import DBSCAN
from sklearn.metrics import silhouette_score
from sklearn.metrics import davies_bouldin_score

def evaluate_clustering(coordinates, labels):
    if len(set(labels)) > 1:  # Ensure there is more than one cluster
        silhouette_avg = silhouette_score(coordinates, labels, metric="haversine")
        db_score = davies_bouldin_score(coordinates, labels)
        return silhouette_avg, db_score
    else:           
        return None, None
    
def run():
    #Fetch the charging stations data from NREL API
    key=os.getenv("NREL_API_KEY")
    response = requests.get(f"https://developer.nrel.gov/api/alt-fuel-stations/v1?api_key={key}&format=csv&status=E&fuel_type=ELEC&access=public&country=US&ev_connector_type=J1772,J1772COMBO")
    local_file_path = "input/fuel_stations.csv"
    with open(local_file_path, 'wb') as f:
         for chunk in response.iter_content(chunk_size=8192):
             f.write(chunk)

    print(f"File '{local_file_path}' downloaded successfully.")
    # Read the CSV file into a DataFrame
    df = pd.read_csv(local_file_path, low_memory=False)
    
    # Clean and preprocess the data
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    # Remove rows with missing values in the 'Latitude' column
    df.dropna(subset=["Latitude"], inplace=True)
    # Remove rows with missing values in the 'Longitude' column
    df.dropna(subset=["Longitude"], inplace=True)
    # Select only the relevant columns
    df_subset = df[["Station Name", "Street Address", "City", "State", "EV Connector Types", "Latitude", "Longitude"]]
    df_subset.to_csv("input/clean_fuel_stations_data.csv", index=False)

    # Perform clustering
    # Get coordinates for clustering with DBSCAN
    coordinates = df_subset[["Latitude", "Longitude"]].values
    # Perform clustering with DBSCAN with epsilon of 200 miles and that has best silhouette score
    earth_radius = 3959  # in miles
    clustering = DBSCAN(eps=250/earth_radius, min_samples=5, metric="haversine", algorithm="ball_tree").fit(np.radians(coordinates))
    df_subset.loc[:, "Cluster"] = clustering.labels_

   
    # Visualize the clusters
    # Create a folium map
    m = folium.Map(location=[df_subset["Latitude"].mean(), df_subset["Longitude"].mean()], width=1024, height=768, zoom_start=5)
    marker_cluster = MarkerCluster().add_to(m)

    # Add markers to the map
    for _, row in df_subset.iterrows():
        folium.Marker(
            location=[row["Latitude"], row["Longitude"]],
            popup=row["Station Name"],
        ).add_to(marker_cluster)

    # Write as html for streamlit to display
    m.save("./output/map.html")
