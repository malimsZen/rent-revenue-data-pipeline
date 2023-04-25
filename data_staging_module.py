# import the data_source_module and load the csv file into staging table in the database(postgres)

# Path: data_staging_module.py
import data_source_module as dsm
import psycopg2
import csv

# connect to the database
conn = psycopg2.connect(
    host="2.tcp.ngrok.io",
    database="postgres",
    user="malims",
    password="gn0m3t@mu",
    port = "16745"
)

# create a cursor
cur = conn.cursor()

# store the payment data into the staging table in the database, generate unique id for each record using the uuid library and store the id in the stage_id column in the staging table
import uuid
with open('payment_data.csv', newline='') as csvfile:
    reader = csv.DictReader(csvfile)
    for row in reader:
        stage_id = uuid.uuid4()
        cur.execute("INSERT INTO staging (staging_id, property_id, tenant_id, payment_amount, payment_date, payment_method, rent_period_start_date, rent_period_end_date) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (str(stage_id), row['property_id'], row['tenant_id'], row['payment_amount'], row['payment_date'], row['payment_method'], row['rent_period_start_date'], row['rent_period_end_date']))

# commit the changes
conn.commit()

# close the connection
conn.close()







