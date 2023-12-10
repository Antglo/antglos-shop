from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

@app.route('/')
def landing_page():
    return render_template('landing.html')

@app.route('/add_to_cart', methods=['POST'])
def add_to_cart():
    # Get the shoe details from the request body
    shoe = request.json
    
    # Insert the shoe into the shopping basket table in the database
    conn = sqlite3.connect('shopping.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO shopping_basket (name, price) VALUES (?, ?)", (shoe['name'], shoe['price']))
    conn.commit()
    conn.close()
    
    return 'Shoe added to cart successfully'

if __name__ == '__main__':
    app.run()
