# Load the data from the staging table into the data warehouse table entities; property, tenant, time and rent_transaction

import psycopg2
from datetime import date

def transform_and_load_data():
    # Connect to the Postgres database
    conn = psycopg2.connect(database="postgres", user="malims", password="gn0m3t@mu", host="localhost", port="5432")
    cursor = conn.cursor()
    
    try:
        # Transform and load data into the time table
        cursor.execute("""
            INSERT INTO time (payment_date, year, quarter, month, day, day_of_week, day_of_year, week_of_year, month_name, quarter_name, year_month, year_quarter)
            SELECT
                payment_date,
                EXTRACT(YEAR FROM payment_date) AS year,
                EXTRACT(QUARTER FROM payment_date) AS quarter,
                EXTRACT(MONTH FROM payment_date) AS month,
                EXTRACT(DAY FROM payment_date) AS day,
                EXTRACT(DOW FROM payment_date) AS day_of_week,
                EXTRACT(DOY FROM payment_date) AS day_of_year,
                EXTRACT(WEEK FROM payment_date) AS week_of_year,
                TO_CHAR(payment_date, 'Month') AS month_name,
                CONCAT(EXTRACT(YEAR FROM payment_date), '-', EXTRACT(QUARTER FROM payment_date)) AS quarter_name,
                TO_CHAR(payment_date, 'YYYY-MM') AS year_month,
                CONCAT(EXTRACT(YEAR FROM payment_date), '-', EXTRACT(QUARTER FROM payment_date)) AS year_quarter
            FROM staging;
        """)
        
        # Load data into the tenant table
        cursor.execute("""
            INSERT INTO tenant (tenant_id, tenant_name, tenant_email, tenant_phone_number)
            SELECT tenant_id, tenant_name, tenant_email, tenant_phone_number
            FROM staging;
        """)
        
        # Load data into the property table
        cursor.execute("""
            INSERT INTO property (property_id, property_name, property_address, property_type, number_of_units)
            SELECT property_id, property_name, property_address, property_type, number_of_units
            FROM staging;
        """)
        
        # Load data into the rent_transaction table
        cursor.execute("""
            INSERT INTO rent_transaction (rent_transaction_id, property_id, tenant_id, payment_amount, payment_date, payment_method, rent_period_start_date, rent_period_end_date)
            SELECT
                staging.staging_id,
                staging.property_id,
                staging.tenant_id,
                staging.payment_amount,
                staging.payment_date,
                staging.payment_method,
                staging.rent_period_start_date,
                staging.rent_period_end_date
            FROM staging
            INNER JOIN tenant ON staging.tenant_id = tenant.tenant_id
            INNER JOIN property ON staging.property_id = property.property_id;
        """)
        
        # Commit the transaction and close the connection
        conn.commit()
        conn.close()
        
        print("Data transformation and loading completed successfully.")
        
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: ", error)
        conn.rollback()
        conn.close()

# Call the function to perform the data transformation and loading
transform_and_load_data()
