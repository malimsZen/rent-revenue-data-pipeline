import random
import psycopg2
import pandas as pd

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="8.tcp.ngrok.io",
    database="postgres",
    user="malims",
    password="gn0m3t@mu",
    port='19207'
)

# Create a cursor object to execute SQL queries
cur = conn.cursor()

# Generate and insert data into the property_lookup table
cur.execute("""
    INSERT INTO property_lookup (property_id, property_name, property_address, property_type, number_of_units)
    SELECT DISTINCT property_id, 
           'Unknown' AS property_name, 
           'Unknown' AS property_address, 
           'Unknown' AS property_type, 
           0 AS number_of_units
    FROM staging;
""")

# Create a dataframe from the property_lookup table and populate the missing attributes, property_id should be extracted from staging table in the database
df = pd.read_sql_query("""
   SELECT DISTINCT property_id,
         'Unknown' AS property_name,
        'Unknown' AS property_address,
       'Unknown' AS property_type,
      0 AS number_of_units
 FROM staging;
""", conn)
df['property_name'] = random.choice(["Tsavo Divine", "Tsavo Rising", "Tsavo Stanley", "Sunset 2","Royal Suburbs","90 Degrees","Coral Bells"])
df['property_address'] = "Unknown"
df['property_type'] = random.choice(['Residential', 'Commercial', 'Industrial'])
df['number_of_units'] = random.randint(1, 10)
df.to_sql('property_lookup', conn, if_exists='replace', index=False)


# Update the tenant_lookup table with generated fake data for missing attributes
cur.execute("""
    SELECT DISTINCT tenant_id
    FROM staging;
""")
tenant_ids = cur.fetchall()

for tenant_id in tenant_ids:
    tenant_name = "Tenant " + str(tenant_id[0])
    tenant_email = "tenant" + str(tenant_id[0]) + "@example.com"
    tenant_phone_number = "555-555-5555"

    cur.execute("""
        UPDATE tenant_lookup
        SET tenant_name = %(tenant_name)s,
            tenant_email = %(tenant_email)s,
            tenant_phone_number = %(tenant_phone_number)s
        WHERE tenant_id = %(tenant_id)s;
    """,
    {
        "tenant_name": tenant_name,
        "tenant_email": tenant_email,
        "tenant_phone_number": tenant_phone_number,
        "tenant_id": tenant_id
    })

# Commit the changes and close the connection
conn.commit()
cur.close()
conn.close()    