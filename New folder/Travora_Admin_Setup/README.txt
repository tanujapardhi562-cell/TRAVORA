TRAVORA ADMIN SETUP

Your app.py already contains these admin routes:
- /admin/login
- /admin/dashboard
- /admin/users
- /admin/bookings
- /admin/logout

The missing part was creating an admin record in the MySQL admins table.

STEPS
1. Copy app.py and create_admin.py into your existing Travora project folder (replace app.py with this copy only if it is the same project version).
2. Make sure MySQL is running and the database travora_db already exists.
3. Check the MySQL password in create_admin.py. It currently uses Tanuja@1106, matching the DB_CONFIG in app.py. Change it if your MySQL root password is different.
4. Install required packages if needed:
   pip install flask mysql-connector-python werkzeug
5. Open terminal in the project folder and run:
   python create_admin.py
6. Start the Flask app:
   python app.py
7. Open:
   http://127.0.0.1:5000/admin/login

DEFAULT ADMIN LOGIN
Email: admin@travora.com
Password: Admin@12345

IMPORTANT
- Run create_admin.py once after the travora_db database exists.
- This script creates the admins table and inserts/updates the admin account.
- Password is stored as a secure hash, not plain text.
- Change the default email/password in create_admin.py before running if you prefer your own credentials.
- This does not create the travora_db database or the users/bookings/hotels tables. Those must already exist for the full dashboard and booking lists to work.
