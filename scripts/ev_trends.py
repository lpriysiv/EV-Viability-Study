import os
import requests
import pandas as pd
import numpy as np
from datetime import datetime
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_absolute_error, mean_squared_error

def run():
    local_file_path = "input/ev_list.csv"
    #Fetch the ev data from NREL API only if it doesn't exist
    if not os.path.exists(local_file_path):
        print("Downloading EV data from NREL API...")
        key=os.getenv("NREL_API_KEY")
        response = requests.get(f"https://developer.nrel.gov/api/vehicles/v1/light_duty_automobiles.csv?api_key={key}&fuel_id=41")
        with open(local_file_path, 'wb') as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)
        print(f"File '{local_file_path}' downloaded successfully.")        
    else:
        print("EV data already exists, skipping download.")


    # Read the CSV file into a DataFrame
    df = pd.read_csv(local_file_path, low_memory=False)
    
    # Clean and preprocess the data
    # Remove duplicates
    df.drop_duplicates(inplace=True)
    df.dropna(subset=["Category"], inplace=True)  # Remove rows with missing values in the 'Category' column
    # Remove rows with missing values in the 'Model Year' column
    df.dropna(subset=["Model Year"], inplace=True)
   
    # Prepare the data for graphing linear trend for each category to provide insight into how many models are available in each category over the years
    df['Model Year'] = pd.to_datetime(df['Model Year'], format='%Y').dt.year
     # Only keep rows for the last 5 years
    current_year = datetime.now().year
    df = df[df['Model Year'] >= (current_year - 5)]

    # Convert 'Category' to string and add a count column for aggregation
    df['Category'] = df['Category'].astype(str)  
    df['Count'] = 1  # Add a count column for aggregation

    # Group by 'Model Year' and 'Category' and count the number of models
    category_trends = df.groupby(['Model Year', 'Category']).size().reset_index(name='Count')
    # Pivot the DataFrame to have 'Model Year' as index and 'Category' as columns
    category_trends_pivot = category_trends.pivot(index='Model Year', columns='Category', values='Count').fillna(0)
    # Reset index to have 'Model Year' as a column
    category_trends_pivot.reset_index(inplace=True)
    # Save the trends data to a CSV file
    output_file_path = "input/ev_category_trends.csv"
    category_trends_pivot.to_csv(output_file_path, index=False)
    print(f"EV category trends data saved to '{output_file_path}'.")
    # Plot the trends and show a marker for each year and display the number on hover
    plt.figure(figsize=(12, 6))
    for category in category_trends_pivot.columns[1:]:  # Skip the 'Model Year' column
        plt.plot(category_trends_pivot['Model Year'], category_trends_pivot[category], label=category)
        # Add the linear regression line for each category
         # Prepare the data for linear regression
        X = category_trends_pivot['Model Year'].values.reshape(-1, 1)
        y = category_trends_pivot[category].values
        
        # Fit the linear regression model
        model = LinearRegression()
        model.fit(X, y)        
        # Predict values for the trend line
        trend_line = model.predict(X)       
        # Evaluate the model's performance
        # Print the model's r2 and mean absolute error
        print(f"Category: {category}, R^2 Score: {r2_score(y, trend_line)}, Mean Absolute Error: {mean_absolute_error(y, trend_line)}, Root Mean Squared Error: {mean_squared_error(y, trend_line)}")

        # Plot the regression line and match the color of the actual value line
        plt.plot(category_trends_pivot['Model Year'], trend_line, linestyle='--', color=plt.gca().lines[-1].get_color(), label=f'{category} Regression Line')
 
        #Show markers with value for each category for each year
        for i, value in enumerate(category_trends_pivot[category]):
            plt.text(category_trends_pivot['Model Year'][i], value, str(int(value)), ha='center', va='bottom')
    plt.title('Electric Vehicle Model Trends by Category with Linear Regression')
    plt.xlabel('Model Year')
    plt.ylabel('Number of Models')
    plt.xticks(category_trends_pivot['Model Year'], rotation=45)
    plt.legend(title='Category')
    plt.tight_layout()
    plt.savefig("output/ev_category_trends_linear.png")
    print("EV category trends linear regression plot saved as 'output/ev_category_trends_linear.png'.")
    plt.close()
    print("EV trends analysis completed successfully.")

    # Repeat the analysis with linear regression by year and seating capacity
    print("Starting EV seating capacity trends analysis...")
    # Clean the data for the seating capacity analysis
    # Remove rows with missing values in the 'Seating Capacity' column
    df.dropna(subset=["Seating Capacity"], inplace=True)
    # Convert seating capacity of 5,6 or 7 to 5-7
    df['Seating Capacity'] = df['Seating Capacity'].astype(str)  # Convert 'Seating Capacity' to string
    df['Seating Capacity'] = df['Seating Capacity'].replace({'5': '5-7', '6': '5-7', '7': '5-7'})
    
    # Group by 'Model Year' and 'Seating Capacity' and count the number of models
    seating_capacity_trends = df.groupby(['Model Year', 'Seating Capacity']).size().reset_index(name='Count')
    # Pivot the DataFrame to have 'Model Year' as index and 'Seating Capacity' as columns
    seating_capacity_trends_pivot = seating_capacity_trends.pivot(index='Model Year', columns='Seating Capacity', values='Count').fillna(0)
    # Reset index to have 'Model Year' as a column
    seating_capacity_trends_pivot.reset_index(inplace=True)
    # Save the trends data to a CSV file
    output_file_path = "input/ev_seating_capacity_trends.csv"
    seating_capacity_trends_pivot.to_csv(output_file_path, index=False)
    print(f"EV seating capacity trends data saved to '{output_file_path}'.")
   
    # Plot the trends and show a marker for each year and display the number on hover
    plt.figure(figsize=(12, 6))     
    for seating_capacity in seating_capacity_trends_pivot.columns[1:]:  # Skip the 'Model Year' column
        plt.plot(seating_capacity_trends_pivot['Model Year'], seating_capacity_trends_pivot[seating_capacity], label=seating_capacity)
        # Add the linear regression line for each seating capacity
         # Prepare the data for linear regression
        X = seating_capacity_trends_pivot['Model Year'].values.reshape(-1, 1)
        y = seating_capacity_trends_pivot[seating_capacity].values
        
        # Fit the linear regression model
        model = LinearRegression()
        model.fit(X, y)        
        # Predict values for the trend line
        trend_line = model.predict(X)        
        # Evaluate the model's performance
        # Print the model's score
        print(f"Seating Capacity: {seating_capacity}, R^2 Score: {r2_score(y, trend_line)}, Mean Absolute Error: {mean_absolute_error(y, trend_line)}, Root Mean Squared Error: {mean_squared_error(y, trend_line)}")
        # Plot the regression line and match the color of the actual value line
        plt.plot(seating_capacity_trends_pivot['Model Year'], trend_line, linestyle='--', color=plt.gca().lines[-1].get_color(), label=f'{seating_capacity} Regression Line')
        #Show markers with value for each category for each year
        for i, value in enumerate(seating_capacity_trends_pivot[seating_capacity]):
            plt.text(seating_capacity_trends_pivot['Model Year'][i], value, str(int(value)), ha='center', va='bottom')
    plt.title('Electric Vehicle Model Trends by Seating Capacity with Linear Regression')
    plt.xlabel('Model Year')
    plt.ylabel('Number of Models')
    plt.xticks(seating_capacity_trends_pivot['Model Year'], rotation=45)
    plt.legend(title='Seating Capacity')
    plt.tight_layout()
    plt.savefig("output/ev_seating_capacity_trends_linear.png")
    print("EV seating capacity trends linear regression plot saved as 'output/ev_seating_capacity_trends_linear.png'.")
    plt.close()
    print("EV seating capacity trends analysis completed successfully.")