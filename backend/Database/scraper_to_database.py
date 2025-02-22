import psycopg2
import re
import datetime
from dunnes import dunnes
from supervalu import supervalu
from tesco import tesco

#Connect to SQL database
conn = psycopg2.connect(
    dbname="smartcartsql",
    user="postgres",
    password="BananaPeel",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

#Makes a table based on the current date
today_date = datetime.date.today().strftime('%Y_%m_%d')
daily_table = f"products_{today_date}"

#This is the permanent table
all_products_table = "all_products"

#Creates a table to store all product data
def create_all_products_table():
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {all_products_table} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            price NUMERIC(10,2),
            store VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            quantity NUMERIC(10,2),
            availability VARCHAR(20),
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

#Creates new table if one doesnt exist already
def create_daily_table():
    cur.execute(f"""
        CREATE TABLE IF NOT EXISTS {daily_table} (
            id SERIAL PRIMARY KEY,
            name VARCHAR(255) UNIQUE NOT NULL,
            price NUMERIC(10,2),
            store VARCHAR(100) NOT NULL,
            category VARCHAR(100) NOT NULL,
            quantity NUMERIC(10,2),
            availability VARCHAR(20),
            inserted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
    """)
    conn.commit()

def extract_quantity(product_name):
    match = re.search(r'(\d+)(kg|g)', product_name, re.IGNORECASE)
    if match:
        weight, unit = match.groups()
        weight = float(weight)
        if unit.lower() == "g":

            #Convert from grams to KG
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

        cur.execute(f"""
            INSERT INTO {daily_table} (name, price, store, category, quantity, availability)
            VALUES (%s, %s, %s, 'Potatoes', %s, %s)
            ON CONFLICT (name) DO UPDATE 
            SET price = EXCLUDED.price, quantity = EXCLUDED.quantity, availability = EXCLUDED.availability;
        """, (name, price_value, store_name, quantity, availability))

        cur.execute(f"""
            INSERT INTO {all_products_table} (name, price, store, category, quantity, availability)
            VALUES (%s, %s, %s, 'Potatoes', %s, %s)
            ON CONFLICT (name) DO UPDATE 
            SET price = EXCLUDED.price, quantity = EXCLUDED.quantity, availability = EXCLUDED.availability;
        """, (name, price_value, store_name, quantity, availability))

create_all_products_table()
create_daily_table()

insert_products(dunnes("potatoes"), "Dunnes")
insert_products(supervalu("potatoes"), "SuperValu")
insert_products(tesco("potatoes"), "Tesco")

conn.commit()
cur.close()
conn.close()

print(f"Data inserted into {daily_table} and {all_products_table}")

