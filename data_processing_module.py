# validation checks

import psycopg2

def validate_staging_data():
    conn = psycopg2.connect(
        database="postgres", 
        user="malims", 
        password="gn0m3t@mu", 
        host="localhost", 
        port="5432")
    cursor = conn.cursor()

    # Execute a SELECT query to fetch data from the staging table
    cursor.execute("SELECT * FROM staging")
    data = cursor.fetchall()

    errors = []

    for row in data:
        staging_id, property_id, tenant_id, payment_amount, payment_date, payment_method, rent_period_start_date, rent_period_end_date = row

        
        # Check for missing values
        if staging_id is None:
            errors.append("Missing value for staging_id")
        if property_id is None:
            errors.append("Missing value for property_id")
        if tenant_id is None:
            errors.append("Missing value for tenant_id")
        if payment_amount is None:
            errors.append("Missing value for payment_amount")
        if payment_date is None:
            errors.append("Missing value for payment_date")
        if payment_method is None:
            errors.append("Missing value for payment_method")
        if rent_period_start_date is None:
            errors.append("Missing value for rent_period_start_date")
        if rent_period_end_date is None:
            errors.append("Missing value for rent_period_end_date")
            
            
        # Check data types
        if not isinstance(staging_id, int):
            errors.append(f"Invalid data type for staging_id: {staging_id}")
        if not isinstance(property_id, int):
            errors.append(f"Invalid data type for property_id: {property_id}")
        if not isinstance(tenant_id, int):
            errors.append(f"Invalid data type for tenant_id: {tenant_id}")
        if not isinstance(payment_amount, float) and not isinstance(payment_amount, int):
            errors.append(f"Invalid data type for payment_amount: {payment_amount}")
        if not isinstance(payment_date, datetime.date):
            errors.append(f"Invalid data type for payment_date: {payment_date}")
        if not isinstance(payment_method, str):
            errors.append(f"Invalid data type for payment_method: {payment_method}")
        if not isinstance(rent_period_start_date, datetime.date):
            errors.append(f"Invalid data type for rent_period_start_date: {rent_period_start_date}")
        if not isinstance(rent_period_end_date, datetime.date):
            errors.append(f"Invalid data type for rent_period_end_date: {rent_period_end_date}")

        # Check payment amount is positive
        if payment_amount < 0:
            errors.append(f"Payment amount cannot be negative: {payment_amount}")

        #check payment date is not in the future
        if payment_date > datetime.date.today():
            errors.append(f"Payment date cannot be in the future: {payment_date}")
            
        #check data consistency in payment method
        if payment_method not in ['cash', 'cheque', 'bank_transfer']:
            errors.append(f"Invalid payment method: {payment_method}")
            
        #check data range for payment amount & rent period start date & rent period end date
        if payment_amount < 0 or payment_amount > 1000000:
            errors.append(f"Invalid payment amount: {payment_amount}")
        if rent_period_start_date < datetime.date(2000, 1, 1) or rent_period_start_date > datetime.date(2020, 12, 31):
            errors.append(f"Invalid rent period start date: {rent_period_start_date}")
            
        #check rent period end date is not before rent period start date
        if rent_period_end_date < rent_period_start_date:
            errors.append(f"Rent period end date cannot be before rent period start date: {rent_period_end_date}")
            
        
    conn.close()

    return errors
