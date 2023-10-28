import mariadb
import os
from dotenv import load_dotenv
from pathlib import Path

base_dir = Path(__file__).parents[1]

load_dotenv(f"{base_dir}/.secret/gitapi.env")

def insert_data(user_name, commit_num, percent):
    conn = mariadb.connect(
            user= os.environ.get("MARIADB_USER"),
            password=os.environ.get("MARIADB_PASSWORD"),
            host="database",
            port=3306,
            database="user_data"
        )
    
    cur = conn.cursor()

    cur.execute(f"INSERT INTO user_list (user_name, commit_num, percent) VALUES (?, ?, ?)",
                (user_name, commit_num, percent))

    cur.close()

    conn.commit()

    conn.close()