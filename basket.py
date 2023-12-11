# basket.py

@app.route('/basket', methods=['GET'])
def view_basket():
    conn = sqlite3.connect('shopping.db')
    cursor = conn.cursor()

    # Execute SQL query to get items from the shopping basket
    cursor.execute("SELECT * FROM shopping_basket")
    items = cursor.fetchall()

    # Convert the items into a JSON response
    response = []
    for item in items:
        response.append({
            'name': item[0],
            'price': item[1]
        })

    conn.close()

    return flask.jsonify(response)
