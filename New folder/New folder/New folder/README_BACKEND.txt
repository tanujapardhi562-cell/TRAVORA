# Travora – Flask + MySQL Backend

Architecture:
Browser (HTML/CSS/JS) -> Flask -> MySQL (travora_db)

Implemented:
- User registration with hashed passwords
- User login/logout with Flask sessions
- Protected dashboard/profile/booking/itinerary pages
- Places API: /api/places
- Hotels loaded from MySQL
- Booking creation + booking list per user
- Itinerary creation + saved trip list per user
- MySQL schema + seed data in database/travora_database.sql

Run:
pip install -r requirements.txt
python app.py

Then open http://127.0.0.1:5000/
