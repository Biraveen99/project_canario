from flask import Flask, jsonify
import mysql.connector

# Initialize the Flask application
app = Flask(__name__)

# Database switch variable (change this to 0 or 1 to switch databases)
db_switch = 0


# Initialize the database connection
def connect_to_db():
    if db_switch == 1:
        db_name = 'canariodb'
    else:
        db_name = 'canariodb2'

    try:
        conn = mysql.connector.connect(user='root', password='ProBook1', host='localhost', database=db_name)
        return conn
    except mysql.connector.Error as err:
        print(f"Error: {err}")
        return None


# Create a connection using the above function
conn = connect_to_db()


@app.route('/api/featureStatus', methods=['GET'])  #this is were the link is after IP-adress
def get_feature_status():
    if conn is None:
        return jsonify({"error": "Database connection has not been established"}), 500

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT status FROM FeatureToggles WHERE feature_name='BlackFridayDeal'")
        result = cursor.fetchone()

        if result:
            status = result[0]
        else:
            status = 'OFF'
    except Exception as err:
        return jsonify({"error": f"Database operation failed: {err}"}), 500

    return jsonify({"BlackFridayDeal": status})


if __name__ == '__main__':
    app.run(debug=True)



# http://127.0.0.1:5000/api/featureStatus <-- the site: ive chosen to put it here as its easier to find it if i ever "lose" it :D
