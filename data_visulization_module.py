# connect to postgresql database(postgres) and print out the tables(property, tenant, time, rent_transaction)into csv files using dataframes

import psycopg2
import pandas as pd

def export_data_warehouse():
    # Connect to the PostgreSQL database
    conn = psycopg2.connect(
        host="localhost",
        database="postgres",
        user="malims",
        password="gn0m3t@mu"
    )

    # Create a cursor object to execute SQL queries
    cur = conn.cursor()

    try:
        # Export property_dimension table
        property_df = pd.read_sql_query("SELECT * FROM property", conn)
        property_df.to_csv('property.csv', index=False)

        # Export tenant_dimension table
        tenant_df = pd.read_sql_query("SELECT * FROM tenant", conn)
        tenant_df.to_csv('tenant.csv', index=False)

        # Export time_dimension table
        time_df = pd.read_sql_query("SELECT * FROM time", conn)
        time_df.to_csv('time.csv', index=False)

        # Export rent_transaction_fact table
        rent_transaction_df = pd.read_sql_query("SELECT * FROM rent_transaction", conn)
        rent_transaction_df.to_csv('rent_transaction.csv', index=False)

        # Commit the changes and close the connection
        conn.commit()
        print("Data warehouse exported successfully.")
        
    except Exception as e:
        print("Error occurred while exporting data warehouse:", str(e))
    finally:
        cur.close()
        conn.close()
        
        
export_data_warehouse()