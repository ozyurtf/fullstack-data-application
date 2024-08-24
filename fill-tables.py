### Libraries
import pandas as pd
import csv
from collections import OrderedDict
import os
import psycopg2

### Inserting Data into Tables
db_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "secret_password"
}

csv_files = [
    {
        "file_path": "data/PostalCode.csv",
        "table_name": "postalcode",
        "primary_key_columns": ["Zip"]
    },
    
    {
        "file_path": "data/Prospect.csv",
        "table_name": "prospect",
        "primary_key_columns": ["ProspectID"]
    },

    {
        "file_path": "data/Customer.csv",
        "table_name": "customer",
        "primary_key_columns": ["CustomerSSN"]
    },  

    {
        "file_path": "data/ParticipantClaimant.csv",
        "table_name": "participantclaimant",
        "primary_key_columns": ["ParticipantSSN"]
    },      


    {
        "file_path": "data/Policy.csv",
        "table_name": "policy",
        "primary_key_columns": ["PolicyID"]
    },    
    

    {
        "file_path": "data/Contract.csv",
        "table_name": "contract",
        "primary_key_columns": ["ContractNumber"]
    },  

    {
        "file_path": "data/CoveredConditions.csv",
        "table_name": "coveredconditions",
        "primary_key_columns": ["PolicyID", "CoveredCondition"]
    },      


    {
        "file_path": "data/InNetworkProviders.csv",
        "table_name": "innetworkproviders",
        "primary_key_columns": ["PolicyID"]
    },      


    {
        "file_path": "data/CoveredBy.csv",
        "table_name": "coveredby",
        "primary_key_columns": ["ParticipantSSN", "ContractNumber"]
    },     

    {
        "file_path": "data/Claim.csv",
        "table_name": "claim",
        "primary_key_columns": ["ClaimNumber", "DateOfClaim"]
    },    


    {
        "file_path": "data/Account.csv",
        "table_name": "account",
        "primary_key_columns": ["AcctNumber", "AccountEstablishedDate"]
    },  


    {
        "file_path": "data/Operation.csv",
        "table_name": "operation",
        "primary_key_columns": ["GeoCode"]
    },  


    {
        "file_path": "data/BillingAccount.csv",
        "table_name": "billingaccount",
        "primary_key_columns": ["BAcctNumber"]
    },    


    {
        "file_path": "data/ChronicDiseaseForecast.csv",
        "table_name": "chronicdiseaseforecast",
        "primary_key_columns": ["State"]
    },       


    {
        "file_path": "data/ContractPremium.csv",
        "table_name": "contractpremium",
        "primary_key_columns": ["PremiumCode", "ContractNumber"]
    },   


    {
        "file_path": "data/Invoice.csv",
        "table_name": "invoice",
        "primary_key_columns": ["InvoiceNumber", "InvoiceDate"]
    }, 


    {
        "file_path": "data/InvoiceDetail.csv",
        "table_name": "invoicedetail",
        "primary_key_columns": ["InvoiceNumber", "LineNumber"]
    },        
]

def remove_duplicates(csv_file, pk_columns):
    unique_rows = OrderedDict()
    with open(csv_file, 'r') as f:
        csv_reader = csv.DictReader(f)
        for row in csv_reader:
            key = tuple(row[col] for col in pk_columns)
            unique_rows[key] = row
    return list(unique_rows.values())

def process_csv_file(cursor, file_info):
    csv_file_path = file_info["file_path"]
    table_name = file_info["table_name"]
    primary_key_columns = file_info["primary_key_columns"]

    print(f"Processing file: {csv_file_path}")

    unique_data = remove_duplicates(csv_file_path, primary_key_columns)

    if not unique_data:
        print(f"No data to insert after removing duplicates for {csv_file_path}")
        return

    headers = list(unique_data[0].keys())

    insert_query = f"INSERT INTO {table_name} ({', '.join(headers)}) VALUES ({', '.join(['%s' for _ in headers])})"

    for row in unique_data:
        # Replace empty strings with None (which will be converted to NULL in SQL)
        values = [None if row[header] == '' else row[header] for header in headers]
        cursor.execute(insert_query, values)

    print(f"Inserted {len(unique_data)} unique rows into {table_name}")
    print()

conn = psycopg2.connect(**db_params)
cursor = conn.cursor()

try:
    for file_info in csv_files:
        if not os.path.exists(file_info["file_path"]):
            print(f"File not found: {file_info['file_path']}")
            continue
        
        process_csv_file(cursor, file_info)

    conn.commit()
    print("All files processed successfully!")

except Exception as e:
    conn.rollback()
    print(f"An error occurred: {e}")

finally:
    cursor.close()
    conn.close()


    


