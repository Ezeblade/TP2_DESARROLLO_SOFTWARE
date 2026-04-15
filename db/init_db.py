import mysql.connector
from prode.constants import DB_HOST, DB_USER, DB_PASSWORD

with open("init_db.sql") as f:
    sql = f.read()

conn = mysql.connector.connect(
    host=DB_HOST,
    user=DB_USER,
    password=DB_PASSWORD
)

cursor = conn.cursor()
for statement in sql.split(";"):
    if statement.strip():
        print(statement)
        cursor.execute(statement)
        conn.commit()
        print("Statement executed")

cursor.close()
conn.close()