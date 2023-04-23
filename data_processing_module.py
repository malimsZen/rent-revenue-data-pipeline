# import the data source module and run the validate_payment_data function

# Path: data_processing_module.py
import data_source_module as dsm

# validate the data

# Path: data_processing_module.py
#create a processing function that fixes the data that raises an error from the validate_payment_data function

# Path: data_processing_module.py
def process_payment_data(payment_data):
    processed_data = []
    for payment in payment_data:
        processed_data.append({
            "property_id": payment["property_id"],
            "tenant_id": payment["tenant_id"],
            "payment_amount": payment["payment_amount"],
            "payment_date": payment["payment_date"],
            "payment_method": payment["payment_method"],
            "rent_period_start_date": payment["rent_period_start_date"],
            "rent_period_end_date": payment["rent_period_end_date"]
        })
    return processed_data

# print the processed data
print(process_payment_data(dsm.generate_payment_data()))

# validate the processed data
print(dsm.validate_payment_data(process_payment_data(dsm.generate_payment_data())))


