# API.py

import flask
import sqlite3

app = flask.Flask(__name__)

# Connect to the SQL server
conn = sqlite3.connect('webshop.db')

# Create a cursor object
cursor = conn.cursor()

# Define API routes
@app.route('/products', methods=['GET'])
def get_products():
    # Execute SQL query to get products from the database
    cursor.execute("SELECT * FROM products")
    products = cursor.fetchall()
    
    # Convert the products into a JSON response
    response = []
    for product in products:
        response.append({
            'id': product[0],
            'name': product[1],
            'price': product[2]
        })
    
    return flask.jsonify(response)

@app.route('/add_product', methods=['POST'])
def add_product():
    # Get the product details from the request body
    product = flask.request.json
    
    # Insert the product into the database
    cursor.execute("INSERT INTO products (name, price) VALUES (?, ?)", (product['name'], product['price']))
    conn.commit()
    
    return 'Product added successfully'

if __name__ == '__main__':
    app.run(debug=True)
