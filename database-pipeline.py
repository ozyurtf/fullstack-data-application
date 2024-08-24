import psycopg2
import csv
from psycopg2 import sql

# Download Chronic Disaese Indicators data from http://cdc.gov
# Upload that data into the data lake in Microsoft Azure
with open('download-data.py') as file:
    exec(file.read())

# Download the Chronic Disease Indicators data from Microsoft Azure 
# Preprocess/clean it, use it as an input to the time series forecasting model 
# Obtain the forecasts and store it in the data folder as a .csv file (ChronicDiseaseForecast.csv).
with open('chronic-disease-prediction.py') as file:
    exec(file.read())

# Database connection parameters
db_params = {
    "host": "localhost",
    "database": "postgres",
    "user": "postgres",
    "password": "secret_password"
}
# CSV file path
csv_file_path = 'data/ChronicDiseaseForecast.csv'

def get_column_names(cursor, table_name):
    cursor.execute(f"SELECT * FROM {table_name} LIMIT 0")
    return [desc[0] for desc in cursor.description]

try:
    # Connect to the database
    conn = psycopg2.connect(**db_params)
    cur = conn.cursor()

    # 1. Empty the ChronicDiseaseForecast table
    cur.execute("TRUNCATE TABLE ChronicDiseaseForecast;")

    # Get column names from the table
    columns = get_column_names(cur, 'ChronicDiseaseForecast')

    # 2. Fill the table with CSV data
    with open(csv_file_path, 'r') as f:
        csv_reader = csv.reader(f)
        header = next(csv_reader)  # Read the header row
        
        # Create the INSERT query dynamically
        insert_query = sql.SQL("INSERT INTO ChronicDiseaseForecast ({}) VALUES ({})").format(
            sql.SQL(', ').join(map(sql.Identifier, columns)),
            sql.SQL(', ').join(sql.Placeholder() * len(columns))
        )
        
        for row in csv_reader:
            # Ensure the row has the correct number of elements
            if len(row) != len(columns):
                print(f"Skipping row {csv_reader.line_num}: incorrect number of fields")
                continue
            
            try:
                cur.execute(insert_query, row)
            except psycopg2.Error as e:
                print(f"Error inserting row {csv_reader.line_num}: {e}")

    # 3. Refresh materialized view LastInvoiceDetailsPerCustomer
    cur.execute("REFRESH MATERIALIZED VIEW LastInvoiceDetailsPerCustomer;")

    # 4. Refresh materialized view CustomerContract
    cur.execute("REFRESH MATERIALIZED VIEW CustomerContract;")

    # Commit the changes
    conn.commit()

    print("All operations completed successfully.")

except (Exception, psycopg2.Error) as error:
    print("Error while connecting to PostgreSQL or executing operations:", error)

finally:
    if conn:
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")