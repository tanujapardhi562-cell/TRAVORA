import getpass
import mysql.connector
from werkzeug.security import generate_password_hash

name = input("Admin name: ").strip()
email = input("Admin email: ").strip().lower()
password = getpass.getpass("Admin password (minimum 8 characters): ")
if not name or not email or len(password) < 8:
    raise SystemExit("Enter a name, valid email, and password with at least 8 characters.")

db = mysql.connector.connect(host="localhost", user="root", password="Tanuja@1106", database="travora_db")
cur = db.cursor()
cur.execute("INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)", (name, email, generate_password_hash(password)))
db.commit()
cur.close()
db.close()
print("Admin account created successfully. You can now use /admin/login.")
