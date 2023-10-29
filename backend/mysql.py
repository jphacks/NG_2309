import mysql.connector
from dotenv import load_dotenv
import os

load_dotenv("../.secret/db.env")

connection = mysql.connector.connect(
    host='database:3308',
    user=os.environ.get("MARIADB_USER"),
    password=os.environ.get("MARIADB_PASSWORD"),
    database=os.environ.get("MARIADB_DATABASE")
)

cursor = connection.cursor()

query = "SELECT user_name, commit_num, stress_revel from database"
cursor.execute(query)


results = cursor.fetchall()

cursor.close()
connection.close()