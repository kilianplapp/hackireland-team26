import psycopg2
import re
from dunnes import dunnes
from supervalu import supervalu
from tesco import tesco


conn = psycopg2.connect(
    dbname="smartcartsql",
    user="postgres",
    password="BananaPeel",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


def extract_quantity(product_name):
    match = re.search(r'(\d+)(kg|g)', product_name, re.IGNORECASE)
    if match:
        weight, unit = match.groups()
        weight = float(weight)
        if unit.lower() == "g":
            weight /= 1000
        return weight
    return 1 


def insert_products(products, store_name):
    for product in products:
        name = product['title']
        price_text = product['price']


        price_value = float(re.sub(r'[€]', '', price_text)) if "€" in price_text else None
        availability = "Unavailable" if price_value is None else "Available"

        quantity = extract_quantity(name)

        cur.execute("""
            INSERT INTO products (name, price, store, category, quantity, availability)
            VALUES (%s, %s, %s, 'Carrots', %s, %s)
            ON CONFLICT (name) DO UPDATE 
            SET price = EXCLUDED.price, quantity = EXCLUDED.quantity, availability = EXCLUDED.availability;
        """, (name, price_value, store_name, quantity, availability))


insert_products(dunnes("potatoes"), "Dunnes")
insert_products(supervalu("potatoes"), "SuperValu")
insert_products(tesco("potatoes"), "Tesco")


conn.commit()
cur.close()
conn.close()

print("Data inserted")
