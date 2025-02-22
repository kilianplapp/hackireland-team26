import psycopg2
import re
import datetime
import pandas as pd
import matplotlib.pyplot as plt
from dunnes import dunnes
from supervalu import supervalu
from tesco import tesco

def price_tracker(product_name):
    """Runs the full price tracking workflow for the given product."""
    
    #Connect to SQL database
    conn = psycopg2.connect(
        dbname="smartcartsql",
        user="postgres",
        password="BananaPeel",
        host="localhost",
        port="5432"
    )
    cur = conn.cursor()

    #Generate today's table name
    today_date = datetime.date.today().strftime('%Y_%m_%d')
    daily_table = f"products_{today_date}"
    all_products_table = "all_products"

    #Create all_products table if it doesn't exist
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

    #Create daily table if it doesn't exist
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

    #Extract weight from product name
    def extract_quantity(product_name):
        match = re.search(r'(\d+)(kg|g)', product_name, re.IGNORECASE)
        if match:
            weight, unit = match.groups()
            weight = float(weight)
            if unit.lower() == "g":
                weight /= 1000  # Convert grams to kg
            return weight
        return 1  # Default to 1kg if no weight is found

    #Insert product data into daily & all_products tables
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
                INSERT INTO {all_products_table} (name, price, store, category, quantity, availability, inserted_at)
                VALUES (%s, %s, %s, 'Potatoes', %s, %s, CURRENT_TIMESTAMP)
                ON CONFLICT (name) DO UPDATE 
                SET price = EXCLUDED.price, quantity = EXCLUDED.quantity, availability = EXCLUDED.availability;
            """, (name, price_value, store_name, quantity, availability))

    #Function to compare a products price over time
    def price_comparison(product_name):
        print(f"\n🔍 Comparing price history for: {product_name}\n")

        #Fetch historical prices from all_products
        query = f"""
            SELECT name, price, inserted_at FROM {all_products_table}
            WHERE name = %s AND price IS NOT NULL
            ORDER BY inserted_at;
        """
        df_historical = pd.read_sql(query, conn, params=[product_name])

        if df_historical.empty:
            print(f"No historical data found for '{product_name}'.")
            return

        df_historical['inserted_at'] = pd.to_datetime(df_historical['inserted_at'])

        #Fetch daily prices from all dated tables
        query = """
            SELECT table_name FROM information_schema.tables
            WHERE table_name LIKE 'products_%'
            ORDER BY table_name;
        """
        cur.execute(query)
        daily_tables = [row[0] for row in cur.fetchall()]

        all_daily_data = []
        
        for table in daily_tables:
            query = f"""
                SELECT name, price, '{table}' AS date FROM {table}
                WHERE name = %s AND price IS NOT NULL;
            """
            df_daily = pd.read_sql(query, conn, params=[product_name])
            if not df_daily.empty:
                df_daily['date'] = pd.to_datetime(df_daily['date'].str.replace("products_", "", regex=True), format='%Y_%m_%d')
                all_daily_data.append(df_daily)

        if not all_daily_data:
            print(f"No daily data found for '{product_name}'.\n")
            return

        df_daily_combined = pd.concat(all_daily_data)

        #Plot price trends
        plt.figure(figsize=(12, 6))

        #Daily Prices
        plt.plot(df_daily_combined['date'], df_daily_combined['price'], marker='o', linestyle='-', label="Daily Price Trend", color='blue')

        #Historical Prices
        plt.plot(df_historical['inserted_at'], df_historical['price'], marker='s', linestyle='--', label="Historical Price Trend", color='red', alpha=0.7)

        plt.xlabel("Date")
        plt.ylabel("Price (€)")
        plt.title(f"Price Comparison for {product_name}")
        plt.legend()
        plt.xticks(rotation=45)
        plt.grid(True)

        plt.savefig(f"price_comparison_{product_name}.png")
        plt.show()

        print(f"Price comparison chart saved as 'price_comparison_{product_name}.png'\n")

    #Create tables if they dont exist
    create_all_products_table()
    create_daily_table()

    #Insert new product data
    insert_products(dunnes(product_name), "Dunnes")
    insert_products(supervalu(product_name), "SuperValu")
    insert_products(tesco(product_name), "Tesco")

    conn.commit()

    #Run price comparison
    price_comparison(product_name)

    #Close database connection
    cur.close()
    conn.close()

    print(f"Data inserted into {daily_table} and {all_products_table}")


#This is an example. 
#Function will look for price of potatoes
price_tracker("potatoes")
