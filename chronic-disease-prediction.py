### Libraries
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import mean_squared_error
from math import sqrt
import warnings
import os
import io
from azure.storage.blob import BlobServiceClient
import requests
import time

warnings.filterwarnings('ignore')

pd.set_option('display.max_columns', 6)

### Downloading Data from Data Lake in Microsoft Azure
connection_string = "secret_connection_string"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "data-lake"
blob_name = "chronic-disease-indicators.csv"
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
download_stream = blob_client.download_blob()
file_content = download_stream.readall()
data = pd.read_csv(io.StringIO(file_content.decode('utf-8')))

### Data Cleaning/Processing
data = (data[data['datavalue'].isna()==False]).reset_index(drop = True)
data = data[data["yearstart"] != 2001]

mortality = data[data["question"].apply(lambda x: "mortality" in x.lower())]
hospitalization = data[data["question"].apply(lambda x: "hospital" in x.lower())]

hospitalization_number = hospitalization.query("datavaluetype == 'Number' and topic != 'Older Adults'")
hospitalization_number = hospitalization_number[(hospitalization_number['question']).apply(lambda x: "rate" not in x)]
hospitalization_number = hospitalization_number[["yearend", 
                                                 "locationdesc", 
                                                 "topic", 
                                                 "question",
                                                 "stratificationcategory1",
                                                 "stratification1",
                                                 "datavalue"]]
hospitalization_number["datavalue"] = hospitalization_number["datavalue"].apply(int)

mortality_number = mortality.query("datavaluetype == 'Number'")
mortality_number = mortality_number[(mortality_number['question']).apply(lambda x: "rate" not in x)]
mortality_number = mortality_number[["yearend", 
                                     "locationdesc", 
                                     "topic", 
                                     "question", 
                                     "stratificationcategory1",
                                     "stratification1",
                                     "datavalue"]]
mortality_number["datavalue"] = mortality_number["datavalue"].apply(int)

hospitalization_number = hospitalization_number.rename(columns={"yearend": "Year", 
                                                                "locationdesc": "State", 
                                                                "topic": "ChronicDiseaseCategory", 
                                                                "question": "ChronicDiseaseExplanation", 
                                                                "stratificationcategory1": "StratificationCategory",
                                                                "stratification1": "Stratification",
                                                                "datavalue": "HospitalizationCount"}).reset_index(drop=True)

mortality_number = mortality_number.rename(columns={"yearend": "Year", 
                                                    "locationdesc": "State", 
                                                    "topic": "ChronicDiseaseCategory", 
                                                    "question": "ChronicDiseaseExplanation", 
                                                    "stratificationcategory1": "StratificationCategory",
                                                    "stratification1": "Stratification",
                                                    "datavalue": "MortalityCount"}).reset_index(drop=True)

hospitalization_number_stats = hospitalization_number[["Year", "State", "HospitalizationCount"]].groupby(["Year", "State"]).sum().reset_index()
mortality_number_stats = mortality_number[["Year", "State", "MortalityCount"]].groupby(["Year", "State"]).sum().reset_index()

### Time Series Forecasting
def process_dataframe(df, name):
    folder_name = f"{name.lower()}-forecast"
    os.makedirs(folder_name, exist_ok=True)
    
    df['Year'] = pd.to_datetime(df['Year'].astype(str) + '-01-01')
    last_year = df['Year'].dt.year.max()
    forecast_year = last_year + 1

    def forecast_state(state_data):
        if len(state_data) < 2:
            return np.nan
        try:
            model = ARIMA(state_data['{}Count'.format(name)], order=(1,1,1))
            results = model.fit()
            forecast = results.forecast(steps=1)
            return forecast.values[0]
        except Exception as e:
            print(f"Error forecasting for state: {state_data['State'].iloc[0]} in {name}. Error: {str(e)}")
            return np.nan
    
    forecasts = {}
    last_year_data = {}
    for state in df['State'].unique():
        state_data = df[df['State'] == state].sort_values('Year')
        forecasts[state] = forecast_state(state_data)
        last_year_data[state] = state_data[state_data['Year'].dt.year == last_year]['{}Count'.format(name)].values[0]
    
    forecast_df = pd.DataFrame({
        'State': list(forecasts.keys()),
        f'{name}CountCurrentYear': list(last_year_data.values()),
        f'{name}CountNextYear': list(forecasts.values())
    })
    forecast_df = forecast_df.sort_values('State').reset_index(drop=True)
    forecast_df[f'{name}CountNextYear'] = forecast_df[f'{name}CountNextYear'].apply(lambda x: int(x) if pd.notna(x) else x)
    
    def plot_state_forecast(state_data, state, name):
        plt.figure(figsize=(10, 6))
        plt.plot(state_data['Year'], state_data['{}Count'.format(name)], label='Historical Data')
        plt.scatter(state_data['Year'], state_data['{}Count'.format(name)], color='blue')
        
        last_year_value = state_data[state_data['Year'].dt.year == last_year]['{}Count'.format(name)].values[0]
        forecast_value = forecast_df[forecast_df['State'] == state][f'{name}CountNextYear'].values[0]
        
        if pd.notna(forecast_value):
            plt.scatter(pd.to_datetime(f"{last_year}-01-01"), last_year_value, color='blue', s=100, zorder=5)
            plt.scatter(pd.to_datetime(f"{forecast_year}-01-01"), forecast_value, color='red', s=100, zorder=5)
            plt.plot([pd.to_datetime(f"{last_year}-01-01"), pd.to_datetime(f"{forecast_year}-01-01")], 
                     [last_year_value, forecast_value], 
                     color='red', linestyle='--', label='Forecast')
        
        plt.title(f'{name} Data and Forecast for {state}')
        plt.xlabel('Year')
        plt.ylabel(f'{name} Number')
        plt.legend()
        plt.grid(True, linestyle='--', alpha=0.7)
        plt.tight_layout()
        plt.savefig(os.path.join(folder_name, f'{state}_forecast.png'))
        plt.close()
    
    for state in df['State'].unique():
        state_data = df[df['State'] == state].sort_values('Year')
        plot_state_forecast(state_data, state, name)
    
    return forecast_df

mortality_forecasts = process_dataframe(mortality_number_stats, "Mortality")
hospitalization_forecasts = process_dataframe(hospitalization_number_stats, "Hospitalization")

combined_forecasts = mortality_forecasts.merge(hospitalization_forecasts, on='State')

column_order = ['State', 'MortalityCountCurrentYear', 'MortalityCountNextYear', 'HospitalizationCountCurrentYear', 'HospitalizationCountNextYear']
combined_forecasts = combined_forecasts[column_order]

combined_forecasts['MortalityChange'] = ((combined_forecasts['MortalityCountNextYear'] - combined_forecasts['MortalityCountCurrentYear']) / combined_forecasts['MortalityCountCurrentYear'])
combined_forecasts['HospitalizationChange'] = ((combined_forecasts['HospitalizationCountNextYear'] - combined_forecasts['HospitalizationCountCurrentYear']) / combined_forecasts['HospitalizationCountCurrentYear'])

def scale_to_range(series, new_min=0.05, new_max=0.30):
    min_val = series.min()
    max_val = series.max()
    scaled = (series - min_val) / (max_val - min_val)
    
    return scaled * (new_max - new_min) + new_min


combined_forecasts["PremiumAmountIncreaseRate"] = scale_to_range(combined_forecasts["HospitalizationChange"]*0.75 + 
                                                                 combined_forecasts["MortalityChange"]*0.25)

combined_forecasts['MortalityChange'] = combined_forecasts['MortalityChange'].round(2)
combined_forecasts['HospitalizationChange'] = combined_forecasts['HospitalizationChange'].round(2)
combined_forecasts['PremiumAmountIncreaseRate'] = combined_forecasts['PremiumAmountIncreaseRate'].round(2)

combined_forecasts.to_csv('data/ChronicDiseaseForecast.csv', index=False)

### Uploading Data to Data Lake in Microsoft Azure
blob_name = "ChronicDiseaseForecast.csv"
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
csv_content = combined_forecasts.to_csv(index=False)
blob_client.upload_blob(csv_content, blob_type="BlockBlob", overwrite=True)