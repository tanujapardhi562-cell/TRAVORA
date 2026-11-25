TRAVORA LIVE DEPLOYMENT (FLASK + MYSQL)
=======================================
Recommended stack: Railway for Flask + MySQL in one project.

1) Test locally:
   python -m pip install -r requirements.txt
   python app.py
   Open http://127.0.0.1:5000/

2) GitHub:
   Create a repository named travora.
   Upload the CONTENTS of this folder (app.py, templates, static, maps, database, etc.).
   Do NOT upload passwords or .env files.

3) Railway:
   Create a new project.
   Add a MySQL database service.
   Deploy the GitHub repository as a service.
   Railway provides MYSQLHOST, MYSQLPORT, MYSQLUSER, MYSQLPASSWORD and MYSQLDATABASE.
   This version of app.py reads those variables automatically.

4) Database:
   Open the Railway MySQL service and import database/travora_database.sql.
   If the database name provided by Railway is not travora_db, the app automatically uses MYSQLDATABASE.

5) Service settings:
   Start command: gunicorn app:app --bind 0.0.0.0:$PORT
   Health check: /health

6) Generate a public domain from Railway service Networking.

IMPORTANT:
- Never commit your MySQL password.
- Local MySQL and Railway MySQL are separate databases.
- Import your schema/data into the cloud database.
