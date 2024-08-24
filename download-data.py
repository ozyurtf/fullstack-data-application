### Libraries
import requests
import json
import pandas as pd
import time
import io
from azure.storage.blob import BlobServiceClient

### Download Data
def fetch_cdi_data(limit=50000, offset=0):
    url = f"https://data.cdc.gov/resource/g4ie-h725.json?$limit={limit}&$offset={offset}"
    response = requests.get(url)
    return response.json()

def download_all_cdi_data():
    all_data = []
    offset = 0
    limit = 50000
    
    while True:
        print(f"Downloading rows {offset} to {offset + limit}")
        data_chunk = fetch_cdi_data(limit, offset)
        
        if not data_chunk:
            break
        
        all_data.extend(data_chunk)
        offset += len(data_chunk)
        
        if len(data_chunk) < limit:
            break
        
        time.sleep(2)  # Increased delay due to larger chunks
    
    print(f"Total rows downloaded: {len(all_data)}")
    return all_data


cdi_data = download_all_cdi_data()

cdi_df = pd.DataFrame(cdi_data)

cdi_df.to_csv("data/chronic-disease-indicators.csv", index=False)

### Uploading Data to Data Lake in Microsoft Azure
csv_content = cdi_df.to_csv(index=False)
connection_string = "secret_connection_string"
blob_service_client = BlobServiceClient.from_connection_string(connection_string)
container_name = "data-lake"
blob_name = "chronic-disease-indicators.csv"
blob_client = blob_service_client.get_blob_client(container=container_name, blob=blob_name)
blob_client.upload_blob(csv_content, blob_type="BlockBlob", overwrite=True)