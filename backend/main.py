import psycopg2
import re

conn = psycopg2.connect(
    dbname="smartcartsql",
    user="postgres",
    password="Lobotomite9",
    host="localhost",
    port="5432"
)

cur = conn.cursor()

carrot_prices = {
    'Tesco Family Pack Carrots 1Kg': '€1.25', 
}

for name, price in carrot_prices.items():
    price_value = float(re.sub(r'[€]', '', price))
    

    cur.execute("""
        INSERT INTO products (name, price, store, category)
        VALUES (%s, %s, 'Tesco', 'Carrots')
        ON CONFLICT DO NOTHING;
    """, (name, price_value))


conn.commit()
cur.close()
conn.close()

print("Data inserted successfully!")
