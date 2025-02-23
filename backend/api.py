from flask import Flask, request, jsonify
from flask_cors import CORS
from scraping import tesco, supervalu, dunnes, aldi
from ai_integration import best_deal_from_each_store
import psycopg2
import json
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
        port="5432",
    )


def fetch_cheapest_products_from_db(item):
    conn = get_db_connection()
    cur = conn.cursor()
    today_date = datetime.date.today().strftime("%Y_%m_%d")
    daily_table = f"products_{today_date}"

    print(f"🔍 Searching for '{item}' in table {daily_table}")

    cur.execute(
        f"""
        SELECT name, price, store, category, quantity, availability
        FROM {daily_table}
        WHERE LOWER(name) LIKE %s
        ORDER BY price ASC;
    """,
        (f"%{item}%",),
    )

    rows = cur.fetchall()
    print(f"Found {len(rows)} results for '{item}' in the database.")

    store_cheapest = {}
    for row in rows:
        store = row[2]  # Store name
        if store not in store_cheapest:
            store_cheapest[store] = {
                "title": row[0],
                "price": float(row[1]) if isinstance(row[1], Decimal) else row[1],
                "store": row[2],
                "category": row[3],
                "quantity": float(row[4]) if isinstance(row[4], Decimal) else row[4],
                "availability": row[5],
            }

    cur.close()
    conn.close()
    return list(store_cheapest.values())


def insert_products_into_db(products, store_name):
    conn = get_db_connection()
    cur = conn.cursor()
    today_date = datetime.date.today().strftime("%Y_%m_%d")
    daily_table = f"products_{today_date}"

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
        match = re.search(r"(\d+)(kg|g)", product_name, re.IGNORECASE)
        if match:
            weight, unit = match.groups()
            weight = float(weight)
            if unit.lower() == "g":
                weight /= 1000
            return weight
        return 1

    for product in products:
        name = product["title"]
        price_text = product["price"]
        price_value = (
            float(re.sub(r"[€]", "", price_text)) if "€" in price_text else None
        )
        availability = "Unavailable" if price_value is None else "Available"
        quantity = extract_quantity(name)

        cur.execute(
            f"""
            INSERT INTO {daily_table} (name, price, store, category, quantity, availability)
            VALUES (%s, %s, %s, 'General', %s, %s)
            ON CONFLICT (name) DO UPDATE 
            SET price = EXCLUDED.price, quantity = EXCLUDED.quantity, availability = EXCLUDED.availability;
        """,
            (name, price_value, store_name, quantity, availability),
        )

    conn.commit()
    cur.close()
    conn.close()


@app.route("/api/shopping-list")
def search_shopping_list_no_db():
    global id_counter
    shopping_list = request.args.getlist("items")

    results = {}
    for item in shopping_list:
        tesco_products = tesco(item)
        for product in tesco_products:
            product["store"] = "Tesco"
            product["ID"] = id_counter
            id_counter += 1

        dunnes_products = dunnes(item)
        for product in dunnes_products:
            product["store"] = "Dunnes"
            product["ID"] = id_counter
            id_counter += 1

        supervalu_products = supervalu(item)
        for product in supervalu_products:
            product["store"] = "SuperValu"
            product["ID"] = id_counter
            id_counter += 1

        aldi_products = aldi(item)
        for product in aldi_products:
            product["store"] = "Aldi"
            product["ID"] = id_counter
            id_counter += 1

        all_products = (
            tesco_products + supervalu_products + dunnes_products + aldi_products
        )
        all_products_short = all_products.copy()
        # remove images from all products
        for product in all_products_short:
            product.pop("image", None)

        response = dict(
            best_deal_from_each_store(str(json.dumps(all_products_short)), item)
        )
        best_deal_products = response["best_deal_products"]

        results[item] = [p for p in all_products if p["title"] in best_deal_products]

    return jsonify(results)


def search_shopping_list():
    global id_counter
    shopping_list = request.args.getlist("items")

    results = {}
    for item in shopping_list:
        products_from_db = fetch_cheapest_products_from_db(item.lower())
        if not products_from_db:
            tesco_products = tesco(item)
            for product in tesco_products:
                product["store"] = "Tesco"
                product["ID"] = id_counter
                id_counter += 1
            insert_products_into_db(tesco_products, "Tesco")

            dunnes_products = dunnes(item)
            for product in dunnes_products:
                product["store"] = "Dunnes"
                product["ID"] = id_counter
                id_counter += 1
            insert_products_into_db(dunnes_products, "Dunnes")

            supervalu_products = supervalu(item)
            for product in supervalu_products:
                product["store"] = "SuperValu"
                product["ID"] = id_counter
                id_counter += 1
            insert_products_into_db(supervalu_products, "SuperValu")

            aldi_products = aldi(item)
            for product in aldi_products:
                product["store"] = "Aldi"
                product["ID"] = id_counter
                id_counter += 1
            insert_products_into_db(aldi_products, "Aldi")

            all_products = (
                tesco_products + supervalu_products + dunnes_products + aldi_products
            )
        else:
            all_products = products_from_db

        results[item] = all_products

    return jsonify(results)


@app.route("/api/products")
def search_products():
    global id_counter
    query = request.args.get("q", "").lower()
    print("QUERY:   ", query)

    tesco_products = tesco(query)
    for product in tesco_products:
        product["store"] = "Tesco"
        product["ID"] = id_counter
        id_counter += 1

    dunnes_products = dunnes(query)
    for product in dunnes_products:
        product["store"] = "Dunnes"
        product["ID"] = id_counter
        id_counter += 1

    supervalu_products = supervalu(query)
    for product in supervalu_products:
        product["store"] = "SuperValu"
        product["ID"] = id_counter
        id_counter += 1

    aldi_products = aldi(query)
    for product in aldi_products:
        product["store"] = "Aldi"
        product["ID"] = id_counter
        id_counter += 1

    all_products = tesco_products + supervalu_products + dunnes_products + aldi_products
    all_products_short = all_products.copy()
    # remove images from all products
    for product in all_products_short:
        product.pop("image", None)

    response = dict(
        best_deal_from_each_store(str(json.dumps(all_products_short)), query)
    )
    best_deal_products = response["best_deal_products"]

    result = [p for p in all_products if p["title"] in best_deal_products]
    return jsonify(result)

# CORS(app)

if __name__ == "__main__":
    app.run(debug=True)
