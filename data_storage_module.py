# Load the data from the staging table into the data warehouse table entities; property, tenant, time and rent_transaction

import psycopg2
from faker import Faker

fake = Faker()

def transform_load_data():
    # Connect to the database
    conn = psycopg2.connect(host='localhost', dbname='postgres', user='malims', password='gn0m3t@mu', port='5432')
    cursor = conn.cursor()

    # Define the SQL queries for transforming and loading data
    transform_query = """
        ALTER TABLE property ADD CONSTRAINT property_pk PRIMARY KEY (property_id);
        ALTER TABLE time ADD CONSTRAINT time_pk PRIMARY KEY (time_id);
        
        INSERT INTO time (payment_date, year, quarter, month, day, day_of_week, day_of_year, week_of_year, month_name, quarter_name, year_month, year_quarter)
        SELECT payment_date, EXTRACT(YEAR FROM payment_date), EXTRACT(QUARTER FROM payment_date), EXTRACT(MONTH FROM payment_date), 
               EXTRACT(DAY FROM payment_date), EXTRACT(DOW FROM payment_date), EXTRACT(DOY FROM payment_date), 
               EXTRACT(WEEK FROM payment_date), TO_CHAR(payment_date, 'Month'), 
               CONCAT('Q', EXTRACT(QUARTER FROM payment_date), ' ', EXTRACT(YEAR FROM payment_date)), 
               TO_CHAR(payment_date, 'YYYY-MM'), 
               CONCAT(EXTRACT(YEAR FROM payment_date), ' Q', EXTRACT(QUARTER FROM payment_date))
        FROM staging
        ON CONFLICT (payment_date) DO NOTHING;
        
        INSERT INTO tenant (tenant_id, tenant_name, tenant_email, tenant_phone_number)
        SELECT DISTINCT tenant_id, COALESCE(s.tenant_name, fake.name()), COALESCE(s.tenant_email, fake.email()), COALESCE(s.tenant_phone_number, fake.phone_number())
        FROM staging s
        LEFT JOIN tenant t ON s.tenant_id = t.tenant_id
        ON CONFLICT (tenant_id) DO NOTHING;
        
        INSERT INTO property (property_id, property_name, property_address, property_type, number_of_units)
        SELECT DISTINCT property_id, COALESCE(s.property_name, fake.company()), COALESCE(s.property_address, fake.address()), COALESCE(s.property_type, fake.word()), 
               COALESCE(s.number_of_units, fake.random_int(min=1, max=10))
        FROM staging s
        LEFT JOIN property p ON s.property_id = p.property_id
        ON CONFLICT (property_id) DO NOTHING;
    """

    # Execute the transformation and loading queries
    cursor.execute(transform_query)
    conn.commit()

    # Close the database connection
    cursor.close()
    conn.close()

# Call the function to execute the transformation and loading
transform_load_data()

