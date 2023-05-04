import random
import psycopg2
import pandas as pd

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="malims",
    password="gn0m3t@mu",
    port='5432'
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# create a lookup table for property using a dataframe (property_id, property_name, property_address,property_type,num_of_units). 
# Use property_id from staging table as primary key and randomize the rest of the columns
#select the    property_id from the staging table
cur.execute("SELECT property_id FROM staging")
property_id = cur.fetchall()


property_id = [i for i in range(property_id)]
property_name = [f"property_{i}" for i in range(1, 1001)]
property_address = [f"address_{i}" for i in range(1, 1001)]
property_type = [random.choice(['apartment', 'condo', 'house']) for i in range(1, 1001)]
num_of_units = [random.randint(1, 10) for i in range(1, 1001)]

property_df = pd.DataFrame({
    'property_id': property_id,
    'property_name': property_name,
    'property_address': property_address,
    'property_type': property_type,
    'num_of_units': num_of_units
})

# Export property lookup table
property_df.to_csv('property.csv', index=False)

# create a lookup table for tenant using a dataframe (tenant_id, tenant_name, tenant_phone,tenant_email,tenant_address).
# Use tenant_id from staging table as primary key and randomize the rest of the columns respecting column data types
#select the    tenant_id from the staging table
cur.execute("SELECT tenant_id FROM staging")
tenant_id = cur.fetchall()

tenant_id = [i for i in range(tenant_id)]
tenant_name = [f"tenant_{i}" for i in range(1, 1001)]
tenant_phone = [random.randint(1000000000, 9999999999) for i in range(1, 1001)]
