import mariadb
import os
from dotenv import load_dotenv
from pathlib import Path


base_dir = Path(__file__).parents[1]
load_dotenv(f"{base_dir}/.secret/db.env")

def insert_data(user_name, commit_num, percent):

    print(os.environ.get("MARIADB_PASSWORD"))

    conn = mariadb.connect(
            user= os.environ.get("MARIADB_USER"),
            password=os.environ.get("MARIADB_PASSWORD"),
            host="localhost",
            port=3306,
            database="user_data"
        )
    
    cur = conn.cursor()

    cur.execute(f"INSERT INTO user_list (user_name, commit_num, percent) VALUES (?, ?, ?)",
                (user_name, commit_num, percent))

    cur.close()

    conn.commit()

    conn.close()


def get_data(user_name):

    connection = mariadb.connect(
        host='localhost:3306',
        user=os.environ.get("MARIADB_USER"),
        password=os.environ.get("MARIADB_PASSWORD"),
        database=os.environ.get("MARIADB_DATABASE")
    )

    cursor = connection.cursor()

    query = f"SELECT user_name, commit_num, stress_revel from user_list WHERE user_name={user_name}"
    results = cursor.execute(query)


    cursor.close()
    connection.close()

    return results