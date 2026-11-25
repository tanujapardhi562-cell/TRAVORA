import getpass
from werkzeug.security import generate_password_hash
from app import get_db_connection

print("Create or update the Travora administrator account")
name = input("Admin name: ").strip()
email = input("Admin email: ").strip().lower()
password = getpass.getpass("Admin password (minimum 8 characters): ")

if not name or not email or len(password) < 8:
    raise SystemExit("Please enter a name, email, and password with at least 8 characters.")

# Uses the same MySQL connection settings as app.py.
db = cursor = None
try:
    db = get_db_connection()
    cursor = db.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS admins (
            id INT AUTO_INCREMENT PRIMARY KEY,
            name VARCHAR(100) NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password VARCHAR(255) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    cursor.execute("SELECT id FROM admins WHERE email = %s", (email,))
    existing_admin = cursor.fetchone()
    password_hash = generate_password_hash(password)

    if existing_admin:
        cursor.execute(
            "UPDATE admins SET name = %s, password = %s WHERE email = %s",
            (name, password_hash, email),
        )
        print("Existing admin account updated successfully.")
    else:
        cursor.execute(
            "INSERT INTO admins (name, email, password) VALUES (%s, %s, %s)",
            (name, email, password_hash),
        )
        print("Admin account created successfully.")
    db.commit()
    print("Now open http://127.0.0.1:5000/admin/login")
finally:
    if cursor:
        cursor.close()
    if db:
        db.close()
