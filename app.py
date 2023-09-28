from flask import Flask, jsonify
import mysql.connector

app = Flask(__name__)


def connect_to_db():
    try:
        conn = mysql.connector.connect(user='root', password='ProBook1', host='localhost', database='canariodb')
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


@app.route('/products', methods=['GET'])
def get_products():
    conn = connect_to_db()
    if conn is None:
        return jsonify({"error": "Database connection has not been established"}), 500

    try:
        cursor = conn.cursor()

        # Check FeatureToggle status
        cursor.execute("SELECT status FROM FeatureToggles WHERE feature_name='BlackFridayDeal'")
        result = cursor.fetchone()

        if result:
            feature_status = result[0]
        else:
            feature_status = 'OFF'

        # Depending on the status, choose which price to display
        if feature_status == 'ON':
            cursor.execute("SELECT Produkt, `BF-pris` as Pris FROM Produkt")
        else:
            cursor.execute("SELECT Produkt, Pris FROM Produkt")

        products = cursor.fetchall()
        product_list = [{"Produkt": product[0], "Pris": product[1]} for product in products]

    except Exception as err:
        return jsonify({"error": f"Database operation failed: {err}"}), 500

    return jsonify(product_list)


if __name__ == '__main__':
    app.run(debug=True)
