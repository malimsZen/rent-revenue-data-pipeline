# import the data_source_module and load the csv file into staging table in the database(postgres)

# Path: data_staging_module.py
import data_source_module as dsm
import psycopg2
import csv

# connect to the database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="malims",
    password="gn0pipm3t@mu",
    port = 5432
)

# create a cursor
cur = conn.cursor()

# store the payment data into the staging table
with open('payment_data.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader) # Skip the header row.
    for row in reader:
        cur.execute("INSERT INTO staging(property_id, tenant_id, payment_amount, payment_date, payment_method, rent_period_start_date, rent_period_end_date) VALUES (%s, %s, %s, %s, %s, %s, %s)", row)

# commit the changes
conn.commit()

# close the connection
conn.close()


