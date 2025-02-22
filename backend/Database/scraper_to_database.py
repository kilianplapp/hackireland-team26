import psycopg2
import re

conn = psycopg2.connect(
    dbname="smartcartsql",
    user="postgres",
    password="BananaPeel",
    host="localhost",
    port="5432"
)
cur = conn.cursor()


carrot_prices = {
    'Tesco Family Pack Carrots 1Kg': '€1.25',
    'Tesco Carrots Loose': '€0.13',
    'Tesco Carrot Bag 500G': '€0.79',
    'Tesco Family Pack Carrots 2Kg': '€2.15',
    'Tesco Organic Carrots 700G': '€1.25',
    'Tesco Sliced Carrots Peeled & Cut 1Kg': '€1.55',
    'Gilfresh Carrot Battons 500G': '€1.49',
    "Grower's Harvest Sliced Carrots 300G": '€0.65',
    'Tesco Carrots And Parsnips 750G': '€1.05',
    'Green Isle Baby Carrots 450g': '€2.00',
    'Sunny South Baby Carrots In Jar 340G': '€1.40',
    'Bunched Carrots 500G': '€2.69',
    'Gilfresh Sliced Carrot 300G': '€2.00',
    'Farm Select Snack Carrots 200G': '€0.99',
    'Dole Go Organic Carrots 700g': '€1.39',
    'Sunny South Sliced Carrots 340G': '€1.40',
    'Tesco Baby Carrots In Water 300G': '€1.05',
    'Gilfresh Broccoli Cauliflower And Carrot 350G': '€2.00',
    'Hughes Farming Carrot Bag 750g': '€2.35',
    'Tesco 4 Steam Bag Carrots Broccoli & Sweetcorn 640G': '€1.05',
    'Tesco Sliced Carrots In Water 300G': '€0.75',
    'Tesco Petits Pois & Baby Carrot Water 340G': '€2.99',
    'Test': '€0.00',
}

def extract_quantity(product_name):
    match = re.search(r'(\d+)(kg|g)', product_name, re.IGNORECASE)
    if match:
        weight, unit = match.groups()
        weight = float(weight)
        if unit.lower() == "g":
            weight /= 1000
        return weight
    return 1

for name, price in carrot_prices.items():
    price_value = float(re.sub(r'[€]', '', price))
    quantity = extract_quantity(name)
    availability = "Unavailable" if price_value == 0.00 else "Available"
    price_value = None if price_value == 0.00 else price_value 

    cur.execute("""
        INSERT INTO products (name, price, store, category, quantity, availability)
        VALUES (%s, %s, 'Tesco', 'Carrots', %s, %s)
        ON CONFLICT (name) DO UPDATE 
        SET price = EXCLUDED.price, quantity = EXCLUDED.quantity, availability = EXCLUDED.availability;
    """, (name, price_value, quantity, availability))

conn.commit()
cur.close()
conn.close()

print("Data inserted")


print("Data inserted")
