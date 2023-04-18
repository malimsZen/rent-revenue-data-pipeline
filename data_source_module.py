# Data source module for the data pipeline
#using faker library to generate fake data and random library to generate random numbers

import random
from faker import Faker
fake = Faker()

def generate_payment_data():
    payment_data = []
    banks = ["ABSA", "KCB", "StanChart", "National Bank"]
    for i in range(1000):
        payment_data.append({
            "property_id": fake.random_int(min=1, max=100),
            "tenant_id": fake.random_int(min=1, max=1000),
            "payment_amount": round(random.uniform(1000, 10000), 2),
            "payment_date": fake.date_between(start_date='-30d', end_date='today'),
            "payment_method": random.choice(banks),
            "rent_period_start_date": fake.date_between(start_date='-30d', end_date='today'),
            "rent_period_end_date": fake.date_between(start_date='today', end_date='+30d')
        })
    return payment_data


# create a function to validate the data whether its in the right format and raise an error if not
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





# print the data
print(generate_payment_data())

# validate the data
print(validate_payment_data(generate_payment_data()))

