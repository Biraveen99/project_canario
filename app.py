from flask import Flask, jsonify
import mysql.connector

# Initialize the Flask application
app = Flask(__name__)

# Initialize the database connection
try:
    conn = mysql.connector.connect(user='root', password='ProBook1', host='localhost', database='canariodb') #this is for making the connection
except mysql.connector.Error as err:
    print(f"Error: {err}") #this prints the error message in terminal
    conn = None  # Set to None so you can check later before using it (lowkey just have it there as a error handling because im sick of seeing an error in the terminal

@app.route('/api/featureStatus', methods=['GET']) #this one chekcs the tabel(in mysqlworkbench) and returns the table values
def get_feature_status():
    if conn is None: #so if the connection to the database dosent happen this message will me shown in localhost webpage
        return jsonify({"error": "Database connection has not been established"}), 500

    try:
        # Usees  the already established connection
        cursor = conn.cursor() #create a new mysql "cursour" object using the existing database connection. A cursour object is used to execute SQL queries and fetch results
        cursor.execute("SELECT status FROM FeatureToggles WHERE feature_name='BlackFridayDeal'") # executes a SQL query to fetch the status(in my case its blackfriday deals from the table named FeatureToggles.
        result = cursor.fetchone() #the "fetchone()" method is used to retrive the next row of a query result set and reutnr a single sequence(in our case its a tuple), if there isnt any more rows its will return "None"

        if result: #if the "fetchone()" returned a results( as in a row was found that mathced the query) this part of code will execute.
            status = result[0] #the result that was found, the first element of the result tuple is assigned to the variable "status" (the latest in the table"
        else: #this is errorhandling this part will only execute if "fetchone()" returned "None" eg: nothing
            status = 'OFF'  # Default to 'OFF' if the feature flag is not found in the database
    except Exception as err:
        return jsonify({"error": f"Database operation failed: {err}"}), 500

    return jsonify({"BlackFridayDeal": status}) #here it returns the "status"

# Start the Flask app (this must alwasy be at the bottom of the project
if __name__ == '__main__':
    app.run(debug=True)


# http://127.0.0.1:5000/api/featureStatus <-- the site: ive chosen to put it here as its easier to find it if i ever "lose" it :D
