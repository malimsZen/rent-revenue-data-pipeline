from faker import Faker
import psycopg2

fake = Faker()

# Connect to the PostgreSQL database
conn = psycopg2.connect(
    host="localhost",
    database="postgres",
    user="malims",
    password="gn0m3t@mu",
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

# Generate and insert data into the tenant_lookup table
cur.execute("""
    INSERT INTO tenant_lookup (tenant_id, tenant_name, tenant_email, tenant_phone_number)
    SELECT DISTINCT tenant_id, 
           'Unknown' AS tenant_name, 
           'Unknown' AS tenant_email, 
           'Unknown' AS tenant_phone_number
    FROM staging;
""")

# Update the property_lookup table with generated fake data for missing attributes
cur.execute("""
    UPDATE property_lookup
    SET property_name = %(property_name)s,
        property_address = %(property_address)s,
        property_type = %(property_type)s,
        number_of_units = %(number_of_units)s
    FROM (
        SELECT DISTINCT property_id, 
               %(property_name)s AS property_name, 
               %(property_address)s AS property_address, 
               %(property_type)s AS property_type, 
               %(number_of_units)s AS number_of_units
        FROM staging
    ) AS data
    WHERE property_lookup.property_id = data.property_id;
""",
{
    "property_name": fake.name(),
    "property_address": fake.address().replace('\n', ', '),
    "property_type": fake.random_element(elements=('Residential', 'Commercial', 'Industrial')),
    "number_of_units": fake.random_int(min=1, max=10)
})

# Update the tenant_lookup table with generated fake data for missing attributes
cur.execute("""
    SELECT DISTINCT tenant_id
    FROM staging;
""")
tenant_ids = cur.fetchall()

for tenant_id in tenant_ids:
    tenant_name = fake.unique.name()
    tenant_email = fake.email()
    tenant_phone_number = fake.phone_number()

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
