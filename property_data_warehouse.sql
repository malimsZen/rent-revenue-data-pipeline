/* Create a normalized data warehouse
the  rent_transaction fact table has the following attributes:
(rent_transaction_id, property_id, tenant_id, payment_amount, payment_date, payment_method, rent_period_start_date,rent_period_end_date)

The property table has the following attributes:
(property_id, property_name, property_address, property_type, number_of_units)

The tenant table has the following attributes:
(tenant_id, tenant_name, tenant_email, tenant_phone_number)

Time dimension table has the following attributes:
(payment_date, year, quarter, month, day, day_of_week, day_of_year, week_of_year, month_name, quarter_name, year_month, year_quarter)
*/ 

CREATE TABLE property (
property_id INT NOT NULL,
property_name VARCHAR(50) NOT NULL,
property_address VARCHAR(50) NOT NULL,
property_type VARCHAR(50) NOT NULL,
number_of_units INT NOT NULL,
PRIMARY KEY (property_id)
);

CREATE TABLE tenant (
tenant_id INT NOT NULL,
tenant_name VARCHAR(50) NOT NULL,
tenant_email VARCHAR(50) NOT NULL,
tenant_phone_number VARCHAR(50) NOT NULL,
PRIMARY KEY (tenant_id)
);

--alter table rent_transaction and change rent_transaction_id to string data type
ALTER TABLE rent_transaction
ALTER COLUMN rent_transaction_id TYPE VARCHAR(50);


CREATE TABLE rent_transaction (
rent_transaction_id INT NOT NULL,
property_id INT NOT NULL,
tenant_id INT NOT NULL,
payment_amount DECIMAL(10,2) NOT NULL,
payment_date DATE NOT NULL,
payment_method VARCHAR(50) NOT NULL,
rent_period_start_date DATE NOT NULL,
rent_period_end_date DATE NOT NULL,
PRIMARY KEY (rent_transaction_id),
FOREIGN KEY (property_id) REFERENCES property(property_id),
FOREIGN KEY (tenant_id) REFERENCES tenant(tenant_id)
);

-- alter table time and create a unique primary key besides the payment_date column
ALTER TABLE time
ADD COLUMN time_id SERIAL PRIMARY KEY;

-- Remove payment_date as the primary key
ALTER TABLE time
DROP CONSTRAINT time_pkey;


CREATE TABLE time (
payment_date DATE NOT NULL,
year INT NOT NULL,
quarter INT NOT NULL,
month INT NOT NULL,
day INT NOT NULL,
day_of_week INT NOT NULL,
day_of_year INT NOT NULL,
week_of_year INT NOT NULL,
month_name VARCHAR(50) NOT NULL,
quarter_name VARCHAR(50) NOT NULL,
year_month VARCHAR(50) NOT NULL,
year_quarter VARCHAR(50) NOT NULL,
PRIMARY KEY (payment_date)
);

/* Create a staging table to load the data from the csv files
the staging table has the following attributes:
(staging_id, property_id, tenant_id, payment_amount, payment_date, payment_method, rent_period_start_date,rent_period_end_date)
*/


CREATE TABLE staging (
staging_id INT NOT NULL,
property_id INT NOT NULL,
tenant_id INT NOT NULL,
payment_amount DECIMAL(10,2) NOT NULL,
payment_date DATE NOT NULL,
payment_method VARCHAR(50) NOT NULL,
rent_period_start_date DATE NOT NULL,/*  */
rent_period_end_date DATE NOT NULL,
PRIMARY KEY (staging_id)
);


/* drop table staging */
DROP TABLE staging;


CREATE TABLE property_lookup (
    property_id INT PRIMARY KEY,
    property_name VARCHAR(50) NOT NULL,
    property_address VARCHAR(50) NOT NULL,
    property_type VARCHAR(50) NOT NULL,
    number_of_units INT NOT NULL
);

CREATE TABLE tenant_lookup (
    tenant_id INT PRIMARY KEY,
    tenant_name VARCHAR(50) NOT NULL,
    tenant_email VARCHAR(50) NOT NULL,
    tenant_phone_number VARCHAR(50) NOT NULL
);


-- Truncate the property_lookup table
TRUNCATE TABLE property_lookup;

-- Truncate the tenant_lookup table
TRUNCATE TABLE tenant_lookup;
