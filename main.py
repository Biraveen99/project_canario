#### database

import mysql.connector

db = mysql.connector.connect(
  host="localhost:3306",
  user="root",
  password="########",
  database="(Local instance 3306"
)

cursor = db.cursor()

cursor.execute("CREATE TABLE FeatureToggles (feature_name VARCHAR(255), status VARCHAR(10))")
