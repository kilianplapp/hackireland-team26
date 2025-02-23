from flask import Flask, request, jsonify
from scraping import tesco, supervalu, dunnes, aldi
from ai_integration import group_and_sort
import json
import psycopg2
import re
import datetime
from decimal import Decimal

app = Flask(__name__)
id_counter = 0

def get_db_connection():
    return psycopg2.connect(
        dbname="smartcartsql",
        user="postgres",
        password="BananaPeel",
        host="localhost",
        port="5432"
    )

def fetch_products_from_db(query):
    conn = get_db_connection()
    cur = conn.cursor()
    today_date = datetime.date.today().strftime('%Y_%m_%d')
    daily_table = f"products_{today_date}"

    cur.execute(f"""
        SELECT name, price, store, category, quantity, availability
        FROM {daily_table}
        WHERE LOWER(name) LIKE %s;
    """, (f"%{query}%",))

    products = []
    for row in cur.fetchall():
        products.append({
            "title": row[0],
            "price": float(row[1]) if isinstance(row[1], Decimal) else row[1],  # Convert Decimal to float
            "store": row[2],
            "category": row[3],
            "quantity": float(row[4]) if isinstance(row[4], Decimal) else row[4],  # Convert Decimal to float
            "availability": row[5]
        })

    cur.close()
    conn.close()
    return products

def insert_products_into_db(products, store_name):
    conn = get_db_connection()
    cur = conn.cursor()
    today_date = datetime.date.today().strftime('%Y_%m_%d')
    daily_table = f"products_{today_date}"
    all_products_table = "all_products"

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
                weight /= 1000
            return weight
        return 1

    for product in products:
        name = product['title']
        price_text = product['price']
        price_value = float(re.sub(r'[€]', '', price_text)) if "€" in price_text else None
        availability = "Unavailable" if price_value is None else "Available"
        quantity = extract_quantity(name)

        cur.execute(f"""
            INSERT INTO {daily_table} (name, price, store, category, quantity, availability)
            VALUES (%s, %s, %s, 'General', %s, %s)
            ON CONFLICT (name) DO UPDATE 
            SET price = EXCLUDED.price, quantity = EXCLUDED.quantity, availability = EXCLUDED.availability;
        """, (name, price_value, store_name, quantity, availability))
    
    conn.commit()
    cur.close()
    conn.close()
    
@app.route("/api/products")
def search_products():
    global id_counter
    query = request.args.get("q", "").lower()

    products_from_db = fetch_products_from_db(query)
    if not products_from_db:
        tesco_products = tesco(query)
        for product in tesco_products:
            product["store"] = "Tesco"
            product["ID"] = id_counter
            id_counter += 1
        insert_products_into_db(tesco_products, "Tesco")

        dunnes_products = dunnes(query)
        for product in dunnes_products:
            product["store"] = "Dunnes"
            product["ID"] = id_counter
            id_counter += 1
        insert_products_into_db(dunnes_products, "Dunnes")

        supervalu_products = supervalu(query)
        for product in supervalu_products:
            product["store"] = "SuperValu"
            product["ID"] = id_counter
            id_counter += 1
        insert_products_into_db(supervalu_products, "SuperValu")

        aldi_products = aldi(query)
        for product in aldi_products:
            product["store"] = "Aldi"
            product["ID"] = id_counter
            id_counter += 1
        insert_products_into_db(aldi_products, "Aldi")

        all_products = tesco_products + supervalu_products + dunnes_products + aldi_products
    else:
        all_products = products_from_db

    all_products_short = all_products.copy()
    for product in all_products_short:
        product.pop("image", None)

    response = group_and_sort(json.dumps(all_products_short), query)
    
    group_names = response.group_names
    groups = response.groups

    result = {group_names[0]: [p for p in all_products if p["title"] in groups[0]]}

    return jsonify(result)

if __name__ == "__main__":
    app.run(debug=True)
