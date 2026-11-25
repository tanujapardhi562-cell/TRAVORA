"""Create or reset the default Travora administrator account.
Run: python create_admin.py
"""
import os
import mysql.connector
from werkzeug.security import generate_password_hash

DB_CONFIG = {
    "host": os.environ.get("TRAVORA_DB_HOST", "localhost"),
    "user": os.environ.get("TRAVORA_DB_USER", "root"),
    "password": os.environ.get("TRAVORA_DB_PASSWORD", "Tanuja@1106"),
    "database": os.environ.get("TRAVORA_DB_NAME", "travora_db"),
}

# You can change these credentials before running this file.
ADMIN_NAME = "Travora Admin"
ADMIN_EMAIL = "admin@travora.com"
ADMIN_PASSWORD = "Admin@12345"


def create_admin():
    db = mysql.connector.connect(**DB_CONFIG)
    cursor = db.cursor()
    try:
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS admins (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(100) NOT NULL,
                email VARCHAR(150) NOT NULL UNIQUE,
                password VARCHAR(255) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)

        password_hash = generate_password_hash(ADMIN_PASSWORD)
        cursor.execute("""
            INSERT INTO admins (name, email, password)
            VALUES (%s, %s, %s)
            ON DUPLICATE KEY UPDATE
                name = VALUES(name),
                password = VALUES(password)
        """, (ADMIN_NAME, ADMIN_EMAIL, password_hash))
        db.commit()
        print("Admin account created/updated successfully.")
        print("Admin login page: http://127.0.0.1:5000/admin/login")
        print("Email:", ADMIN_EMAIL)
        print("Password:", ADMIN_PASSWORD)
        print("Change ADMIN_EMAIL and ADMIN_PASSWORD in create_admin.py before running if you want different credentials.")
    finally:
        cursor.close()
        db.close()


if __name__ == "__main__":
    try:
        create_admin()
    except mysql.connector.Error as error:
        print("MySQL error:", error)
        print("Check that MySQL is running, travora_db exists, and DB_CONFIG password is correct.")
