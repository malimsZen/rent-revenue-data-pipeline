import random
import psycopg2
from sqlalchemy import create_engine
import pandas as pd

# Connect to the PostgreSQL database
engine = create_engine('postgresql://malims:gn0m3t%40mu@localhost:5432/postgres')

# select the property_id and tenant_id from the staging table and create two separate dataframes
property_tenant_df = pd.read_sql("SELECT property_id, tenant_id FROM staging", engine)

# create a list of unique property_ids
property_ids = property_tenant_df['property_id'].unique().tolist()

# create a list of unique tenant_ids
tenant_ids = property_tenant_df['tenant_id'].unique().tolist()

# create a tenant dataframe with the columns tenant_id, tenant_name, tenant_email, tenant_phone.
# The tenant_name, tenant_email, and tenant_phone are randomly generated
tenant_df = pd.DataFrame(columns=['tenant_id', 'tenant_name', 'tenant_email', 'tenant_phone_number'])
for tenant_id in tenant_ids:
    tenant_name = 'tenant_' + str(tenant_id)
    tenant_email = 'tenant_' + str(tenant_id) + '@gmail.com'
    tenant_phone = random.randint(1000000000, 9999999999)
    tenant_df = pd.concat([tenant_df, pd.DataFrame({'tenant_id': tenant_id, 'tenant_name': tenant_name, 'tenant_email': tenant_email, 'tenant_phone_number': tenant_phone}, index=[0])], ignore_index=True)

# create a property dataframe with the columns property_id, property_name, property_address, property_type, number_of_units
# The property_name, property_address, property_type, and number_of_units are randomly generated
property_df = pd.DataFrame(columns=['property_id', 'property_name', 'property_address', 'property_type', 'number_of_units'])
for property_id in property_ids:
    property_name = 'property_' + str(property_id)
    property_address = 'address_' + str(property_id)
    property_type = random.choice(['apartment', 'condo', 'townhouse', 'single_family'])
    number_of_units = random.randint(1, 10)
    property_df = pd.concat([property_df, pd.DataFrame({'property_id': property_id, 'property_name': property_name, 'property_address': property_address, 'property_type': property_type, 'number_of_units': number_of_units}, index=[0])], ignore_index=True)

# load the property and tenant dataframes into the property and tenant tables in the database
property_df.to_sql('property_lookup', engine, if_exists='append', index=False)
tenant_df.to_sql('tenant_lookup', engine, if_exists='append', index=False)

