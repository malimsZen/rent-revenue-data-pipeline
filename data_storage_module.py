import psycopg2

# Function to populate the data warehouse
def populate_data_warehouse():
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
        # Populate property_dimension table
        cur.execute("""
            INSERT INTO property (property_id, property_name, property_address, property_type, number_of_units)
            SELECT property_id, property_name, property_address, property_type, number_of_units
            FROM property_lookup
        """)

        # Populate tenant_dimension table
        cur.execute("""
            INSERT INTO tenant (tenant_id, tenant_name, tenant_email, tenant_phone_number)
            SELECT tenant_id, tenant_name, tenant_email, tenant_phone_number
            FROM tenant_lookup
        """)

        # Populate time_dimension table
        cur.execute("""
            INSERT INTO time (payment_date, year, quarter, month, day, day_of_week, day_of_year, week_of_year, month_name, quarter_name, year_month, year_quarter)
            SELECT payment_date, EXTRACT(year FROM payment_date), EXTRACT(quarter FROM payment_date), EXTRACT(month FROM payment_date),
                   EXTRACT(day FROM payment_date), EXTRACT(dow FROM payment_date), EXTRACT(doy FROM payment_date),
                   EXTRACT(week FROM payment_date), TO_CHAR(payment_date, 'Month'), TO_CHAR(payment_date, 'Q'),
                   TO_CHAR(payment_date, 'YYYY-MM'), TO_CHAR(payment_date, 'YYYY-Q')
            FROM staging
        """)

        # Populate rent_transaction_fact table
        cur.execute("""
            INSERT INTO rent_transaction (rent_transaction_id, property_id, tenant_id, payment_amount, payment_date, payment_method, rent_period_start_date, rent_period_end_date)
            SELECT staging_id, property_id, tenant_id, payment_amount, payment_date, payment_method, rent_period_start_date, rent_period_end_date
            FROM staging
        """)

        # Commit the changes and close the connection
        conn.commit()
        print("Data warehouse populated successfully.")
    except Exception as e:
        print("Error occurred while populating data warehouse:", str(e))
    finally:
        cur.close()
        conn.close()

populate_data_warehouse()

