import psycopg2 as psg
import pandas as pd

#connect to postgres database
conn = psg.connect(
    database="postgres",
    user="malims",
    password="gn0m3t@mu",
    host="localhost",
    port="5432"
)

#cursor object
cursor = conn.cursor()

#execute query
cursor.execute("SELECT * FROM staging")

# transform data into pandas dataframe
data = pd.DataFrame(cursor.fetchall())

# load property table of postgres database using data from staging table. Generate values for the columns that are not in the staging table.
# property attributes and data types (property_id INT NOT NULL,property_name VARCHAR(50) NOT NULL,property_address VARCHAR(50) NOT NULL,property_type VARCHAR(50) NOT NULL,number_of_units INT NOT NULL,PRIMARY KEY (property_id))



