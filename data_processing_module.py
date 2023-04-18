# import the data source module and create a validation function
# create processing function to make sure the data is in the right format

# Path: data-processing-module.py
# import the data source module and create a validation function
# create processing function to make sure the data is in the right format

import data_source_module

def validate_payment_data(payment_data):
    for payment in payment_data:
        if not isinstance(payment["property_id"], int):
            raise TypeError("property_id must be an integer")
        if not isinstance(payment["tenant_id"], int):
            raise TypeError("tenant_id must be an integer")
        if not isinstance(payment["payment_amount"], float):
            raise TypeError("payment_amount must be a float")
        if not isinstance(payment["payment_date"], str):
            raise TypeError("payment_date must be a string")
        if not isinstance(payment["payment_method"], str):
            raise TypeError("payment_method must be a string")
        if not isinstance(payment["rent_period_start_date"], str):
            raise TypeError("rent_period_start_date must be a string")
        if not isinstance(payment["rent_period_end_date"], str):
            raise TypeError("rent_period_end_date must be a string")
    return True

# create processing function to make sure the data is in the right format
def process_payment_data(payment_data):
    processed_payment_data = []
    for payment in payment_data:
        processed_payment_data.append({
            "property_id": payment["property_id"],
            "tenant_id": payment["tenant_id"],
            "payment_amount": payment["payment_amount"],
            "payment_date": payment["payment_date"],
            "payment_method": payment["payment_method"],
            "rent_period_start_date": payment["rent_period_start_date"],
            "rent_period_end_date": payment["rent_period_end_date"]
        })
    return processed_payment_data

# print the data
print(data_source_module.generate_payment_data())

# validate the data
print(validate_payment_data(data_source_module.generate_payment_data()))

