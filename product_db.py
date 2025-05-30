import psycopg2
import logging
import json

# Log fayl sozlamalari
logging.basicConfig(
    filename='product_db.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)


class ProductDB:
    def __init__(self, db_name, user, password, host='localhost', port=5432):
        self.conn = psycopg2.connect(
            dbname="postgres",
            user="postgres",
            password="123",
            host="192.168.100.11",
            port="5432"
        )
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        query = """
        CREATE TABLE IF NOT EXISTS products (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            price NUMERIC(10, 2) NOT NULL,
            quantity INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        );
        """
        self.cursor.execute(query)
        self.conn.commit()
        logging.info("Table 'products' ensured.")

    def add_product(self, name, price, quantity):
        query = """
        INSERT INTO products (name, price, quantity)
        VALUES (%s, %s, %s);
        """
        self.cursor.execute(query, (name, price, quantity))
        self.conn.commit()
        logging.info(f"Added product: {name}, Price: {price}, Quantity: {quantity}")

    def get_all_products(self):
        self.cursor.execute("SELECT * FROM products;")
        return self.cursor.fetchall()

    def get_product_by_id(self, product_id):
        self.cursor.execute("SELECT * FROM products WHERE id = %s;", (product_id,))
        return self.cursor.fetchone()

    def update_product(self, product_id, name=None, price=None, quantity=None):
        fields = []
        values = []

        if name is not None:
            fields.append("name = %s")
            values.append(name)
        if price is not None:
            fields.append("price = %s")
            values.append(price)
        if quantity is not None:
            fields.append("quantity = %s")
            values.append(quantity)

        if fields:
            values.append(product_id)
            query = f"UPDATE products SET {', '.join(fields)} WHERE id = %s;"
            self.cursor.execute(query, tuple(values))
            self.conn.commit()
            logging.info(f"Updated product ID {product_id} with {fields}")

    def delete_product(self, product_id):
        self.cursor.execute("DELETE FROM products WHERE id = %s;", (product_id,))
        self.conn.commit()
        logging.info(f"Deleted product ID {product_id}")

    def search_by_name(self, name_query):
        self.cursor.execute(
            "SELECT * FROM products WHERE name ILIKE %s;",
            (f"%{name_query}%",)
        )
        return self.cursor.fetchall()

    def filter_by_price(self, min_price, max_price):
        self.cursor.execute(
            "SELECT * FROM products WHERE price BETWEEN %s AND %s;",
            (min_price, max_price)
        )
        return self.cursor.fetchall()

    def export_to_json(self, filename='products.json'):
        products = self.get_all_products()
        keys = ['id', 'name', 'price', 'quantity', 'created_at']

        with open(filename, 'w', encoding='utf-8') as f:
            json.dump([dict(zip(keys, row)) for row in products], f, indent=4, default=str)

        logging.info(f"Exported products to JSON: {filename}")

    def close(self):
        self.cursor.close()
        self.conn.close()
        logging.info("Database connection closed.")



