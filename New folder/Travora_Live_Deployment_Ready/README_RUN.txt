TRAVORA – Flask + MySQL RUN GUIDE

1) Install Python 3.
2) Open this folder in VS Code.
3) Open Terminal and run:
   pip install -r requirements.txt

4) Open MySQL Workbench.
5) Open database/travora_database.sql and execute the complete script.
6) Confirm with:
   USE travora_db;
   SHOW TABLES;

7) Configure the MySQL password.
   Option A (simple): in app.py replace YOUR_MYSQL_PASSWORD with your MySQL root password.
   Option B (recommended): set Windows environment variable:
      set TRAVORA_DB_PASSWORD=YOUR_PASSWORD
   Do NOT share your real password in chat or in public GitHub repositories.

8) Start Flask:
   python app.py

9) Open in browser:
   http://127.0.0.1:5000/

IMPORTANT:
- Do NOT open templates/index.html directly with file:///.
- Do NOT use Live Server for the Flask version.
- Login/Register now use Flask + MySQL.
- Hotels, bookings and itinerary are database-backed.
