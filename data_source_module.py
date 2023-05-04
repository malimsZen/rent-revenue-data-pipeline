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
            "payment_date": fake.date_between(start_date='-1000d', end_date='today'),
            "payment_method": random.choice(banks),
            "rent_period_start_date": fake.date_between(start_date='-30d', end_date='today'),
            "rent_period_end_date": fake.date_between(start_date='today', end_date='+30d')
        })
    return payment_data

payment_data = generate_payment_data()

# store the payment data inta csv file
import csv
with open('payment_data.csv', 'w', newline='') as csvfile:
    fieldnames = ['property_id', 'tenant_id', 'payment_amount', 'payment_date', 'payment_method', 'rent_period_start_date', 'rent_period_end_date']
    writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
    writer.writeheader()
    for payment in payment_data:
        writer.writerow(payment)






