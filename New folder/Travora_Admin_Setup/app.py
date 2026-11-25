from flask import Flask, render_template, request, redirect, session, url_for, jsonify
import os
import mysql.connector
from mysql.connector import Error, IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.environ.get("TRAVORA_SECRET_KEY", "travora_secret_key_change_me")

DB_CONFIG = {
    "host": os.environ.get("TRAVORA_DB_HOST", "localhost"),
    "user": os.environ.get("TRAVORA_DB_USER", "root"),
    "password": os.environ.get("TRAVORA_DB_PASSWORD", "Tanuja@1106"),
    "database": os.environ.get("TRAVORA_DB_NAME", "travora_db"),
}


def get_db_connection():
    if DB_CONFIG["password"] == "YOUR_MYSQL_PASSWORD":
        raise RuntimeError("MySQL password is not configured. Set TRAVORA_DB_PASSWORD or replace YOUR_MYSQL_PASSWORD in app.py.")
    return mysql.connector.connect(**DB_CONFIG)


def login_required():
    return "user_id" in session


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html")

    name = request.form.get("name", "").strip()
    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not name or not email or not password:
        return render_template("register.html", error="Please fill all fields."), 400
    if len(password) < 6:
        return render_template("register.html", error="Password must contain at least 6 characters."), 400

    db = cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO users (name, email, password) VALUES (%s, %s, %s)",
            (name, email, generate_password_hash(password)),
        )
        db.commit()
    except IntegrityError:
        return render_template("register.html", error="This email is already registered."), 409
    except Error as exc:
        return render_template("register.html", error=f"Database error: {exc}"), 500
    except RuntimeError as exc:
        return render_template("register.html", error=str(exc)), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return redirect(url_for("login"))


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")

    if not email or not password:
        return render_template("login.html", error="Please enter email and password."), 400

    db = cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()
    except (Error, RuntimeError) as exc:
        return render_template("login.html", error=f"Database error: {exc}"), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    if not user or not check_password_hash(user["password"], password):
        return render_template("login.html", error="Invalid email or password."), 401

    session["user_id"] = user["id"]
    session["user_name"] = user["name"]
    session["user_email"] = user["email"]
    return redirect(url_for("dashboard"))


@app.route("/dashboard")
def dashboard():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("user-dashboard.html")


@app.route("/profile")
def profile():
    if not login_required():
        return redirect(url_for("login"))
    return render_template("profile.html", user={"name": session.get("user_name"), "email": session.get("user_email")})


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/places")
def places():
    return render_template("places.html")


@app.route("/place-details.html")
def place_details():
    place = request.args.get("place", "").strip()
    key = place.lower().replace("’", "'").strip()
    details = {
        "tiger point": {"title":"Tiger Point","location":"Lonavala","category":"Viewpoint","description":"A popular viewpoint near Lonavala known for wide views of the surrounding Sahyadri hills and valleys.","highlights":["Scenic valley views","Photography and sightseeing","Best experienced in clear weather"]},
        "lion's point": {"title":"Lion's Point","location":"Lonavala","category":"Viewpoint","description":"A scenic viewpoint around Lonavala, especially popular for mountain landscapes, clouds and sunset views.","highlights":["Mountain views","Sunset sightseeing","Photography"]},
        "bhushi dam": {"title":"Bhushi Dam","location":"Lonavala","category":"Water Attraction","description":"A well-known monsoon attraction near Lonavala surrounded by greenery and flowing water during the rainy season.","highlights":["Monsoon scenery","Nature visit","Nearby Lonavala attractions"]},
        "rajmachi fort": {"title":"Rajmachi Fort","location":"Near Lonavala","category":"Fort","description":"A historic fort destination in the Sahyadri mountains and a popular trekking destination near Lonavala.","highlights":["Trekking","Historic fort","Sahyadri views"]},
        "lohagad fort": {"title":"Lohagad Fort","location":"Near Lonavala","category":"Fort","description":"A historic hill fort near Lonavala that is popular for trekking, views and heritage exploration.","highlights":["Trekking","History","Mountain views"]},
        "pawna lake": {"title":"Pawna Lake","location":"Maval, Pune","category":"Lake","description":"A scenic lake surrounded by hills, known for camping, photography and peaceful nature experiences.","highlights":["Camping","Lake views","Photography"]},
        "alibag beach": {"title":"Alibag Beach","location":"Alibaug, Raigad","category":"Beach","description":"A popular coastal destination offering sea views, beach walks and a relaxed weekend experience.","highlights":["Beach walk","Sea views","Photography"]},
        "kashid beach": {"title":"Kashid Beach","location":"Raigad","category":"Beach","description":"A scenic Konkan beach known for its coastal landscape and relaxing seaside atmosphere.","highlights":["Beach scenery","Coastal views","Relaxation"]},
        "kolaba fort": {"title":"Kolaba Fort","location":"Alibaug, Raigad","category":"Fort","description":"A historic sea fort near Alibaug and an important heritage attraction of the Konkan coast.","highlights":["Sea fort","History","Coastal sightseeing"]},
        "korlai fort": {"title":"Korlai Fort","location":"Raigad","category":"Fort","description":"A historic coastal fort near the Konkan coast offering heritage interest and scenic surroundings.","highlights":["Fort exploration","Coastal views","History"]},
        "nagaon beach": {"title":"Nagaon Beach","location":"Alibaug, Raigad","category":"Beach","description":"A popular beach near Alibaug suitable for a relaxed coastal outing and sightseeing.","highlights":["Beach visit","Sea views","Weekend trip"]},
        "varsoli beach": {"title":"Varsoli Beach","location":"Alibaug, Raigad","category":"Beach","description":"A quieter coastal destination near Alibaug known for its sandy shoreline and peaceful atmosphere.","highlights":["Beach walk","Peaceful surroundings","Photography"]},
        "ajanta cave 1": {"title":"Ajanta Cave 1","location":"Ajanta Caves","category":"Heritage Cave","description":"One of the important caves in the Ajanta complex, known for its ancient Buddhist art and paintings.","highlights":["Ancient art","Buddhist heritage","Cave architecture"]},
        "ancient paintings": {"title":"Ancient Paintings","location":"Ajanta Caves","category":"Art & Heritage","description":"The Ajanta complex is renowned for its ancient paintings and artistic heritage preserved inside the rock-cut caves.","highlights":["Ancient paintings","Art history","Cultural heritage"]},
        "buddhist sculptures": {"title":"Buddhist Sculptures","location":"Ajanta Caves","category":"Heritage","description":"The caves contain important Buddhist sculptures and artistic representations that reflect the history of the site.","highlights":["Buddhist art","Sculptures","Heritage exploration"]},
        "cave architecture": {"title":"Cave Architecture","location":"Ajanta Caves","category":"Architecture","description":"The rock-cut architecture of Ajanta demonstrates the craftsmanship and planning used to create the historic cave complex.","highlights":["Rock-cut architecture","History","Photography"]},
        "historical heritage": {"title":"Historical Heritage","location":"Ajanta Caves","category":"Heritage","description":"Ajanta is an important heritage destination where visitors can explore ancient art, architecture and cultural history.","highlights":["Heritage","Ancient culture","Educational visit"]},
        "waghora valley": {"title":"Waghora Valley","location":"Ajanta Caves","category":"Nature & Heritage","description":"The Ajanta caves are set around the Waghora valley, adding a scenic natural setting to the heritage experience.","highlights":["Valley views","Nature","Heritage"]},
        "arthur's seat": {"title":"Arthur's Seat","location":"Mahabaleshwar","category":"Viewpoint","description":"A famous Mahabaleshwar viewpoint offering broad views of valleys and surrounding hills.","highlights":["Valley views","Sightseeing","Photography"]},
        "lingmala waterfall": {"title":"Lingmala Waterfall","location":"Mahabaleshwar","category":"Waterfall","description":"A well-known waterfall attraction in Mahabaleshwar, especially scenic during the monsoon season.","highlights":["Waterfall views","Monsoon scenery","Nature"]},
        "mapro garden": {"title":"Mapro Garden","location":"Mahabaleshwar","category":"Food & Garden","description":"A popular visitor attraction associated with strawberries, food products and a garden-style travel experience.","highlights":["Strawberry products","Food experience","Family visit"]},
        "pratapgad fort": {"title":"Pratapgad Fort","location":"Near Mahabaleshwar","category":"Fort","description":"A historic hill fort near Mahabaleshwar and an important destination for exploring Maratha-era heritage.","highlights":["Fort history","Mountain views","Heritage"]},
        "venna lake": {"title":"Venna Lake","location":"Mahabaleshwar","category":"Lake","description":"A popular lake destination in Mahabaleshwar surrounded by greenery and commonly visited for leisure activities.","highlights":["Lake views","Boating area","Leisure visit"]},
        "wilson point": {"title":"Wilson Point","location":"Mahabaleshwar","category":"Viewpoint","description":"A well-known viewpoint in Mahabaleshwar associated with sunrise and panoramic hill scenery.","highlights":["Sunrise views","Panoramic scenery","Photography"]},
    }
    item = details.get(key)
    if not item:
        return redirect(url_for("places"))
    return render_template("place-details.html", place=item)


@app.route("/api/places")
def api_places():
    db = cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, city, category, description, latitude, longitude FROM places ORDER BY name")
        rows = cursor.fetchall()
        return jsonify(rows)
    except (Error, RuntimeError) as exc:
        return jsonify({"error": str(exc)}), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
@app.route("/hotels")
def hotels():
    db = cursor = None
    hotels_data = []
    error = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, location, price, rating, description FROM hotels ORDER BY name")
        hotels_data = cursor.fetchall()
    except (Error, RuntimeError) as exc:
        error = str(exc)
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    return render_template("hotels.html", hotels=hotels_data, error=error)


@app.route("/booking", methods=["GET", "POST"])
def booking():
    if not login_required():
        return redirect(url_for("login"))

    db = cursor = None
    message = None
    error = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, location, price FROM hotels ORDER BY name")
        hotels_data = cursor.fetchall()

        if request.method == "POST":
            hotel_id = request.form.get("hotel_id")
            booking_date = request.form.get("booking_date")
            travellers = request.form.get("travellers", "1")
            if not hotel_id or not booking_date or not travellers:
                error = "Please fill all booking fields."
            elif int(travellers) < 1:
                error = "Travellers must be at least 1."
            else:
                cursor.execute(
                    "INSERT INTO bookings (user_id, hotel_id, booking_date, travellers, status) VALUES (%s, %s, %s, %s, 'Pending')",
                    (session["user_id"], int(hotel_id), booking_date, int(travellers)),
                )
                db.commit()
                message = "Booking request saved successfully."

        cursor.execute(
            """SELECT b.id, h.name AS hotel_name, h.location, b.booking_date, b.travellers, b.status
               FROM bookings b JOIN hotels h ON h.id = b.hotel_id
               WHERE b.user_id = %s ORDER BY b.id DESC""",
            (session["user_id"],),
        )
        bookings = cursor.fetchall()
    except (Error, RuntimeError, ValueError) as exc:
        if db:
            db.rollback()
        error = f"Booking error: {exc}"
        bookings = []
        hotels_data = locals().get("hotels_data", [])
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return render_template("booking.html", hotels=hotels_data, bookings=bookings, message=message, error=error)


@app.route("/itinerary", methods=["GET", "POST"])
def itinerary():
    if not login_required():
        return redirect(url_for("login"))

    db = cursor = None
    message = None
    error = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, city FROM places ORDER BY name")
        places_data = cursor.fetchall()

        if request.method == "POST":
            place_id = request.form.get("place_id")
            visit_date = request.form.get("visit_date") or None
            notes = request.form.get("notes", "").strip()
            if not place_id:
                error = "Please select a place."
            else:
                cursor.execute(
                    "INSERT INTO itinerary (user_id, place_id, visit_date, notes) VALUES (%s, %s, %s, %s)",
                    (session["user_id"], int(place_id), visit_date, notes),
                )
                db.commit()
                message = "Place added to your trip."

        cursor.execute(
            """SELECT i.id, p.name, p.city, p.category, i.visit_date, i.notes
               FROM itinerary i JOIN places p ON p.id = i.place_id
               WHERE i.user_id = %s ORDER BY i.visit_date IS NULL, i.visit_date, i.id""",
            (session["user_id"],),
        )
        itinerary_data = cursor.fetchall()
    except (Error, RuntimeError, ValueError) as exc:
        if db:
            db.rollback()
        error = f"Trip planner error: {exc}"
        places_data = locals().get("places_data", [])
        itinerary_data = []
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    return render_template("itinerary.html", places=places_data, itinerary=itinerary_data, message=message, error=error)



# =========================
# ADMIN LOGIN AND MANAGEMENT
# =========================

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "GET":
        return render_template("admin-login.html")

    email = request.form.get("email", "").strip().lower()
    password = request.form.get("password", "")
    db = cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, password FROM admins WHERE email = %s", (email,))
        admin = cursor.fetchone()
    except (Error, RuntimeError) as exc:
        return render_template("admin-login.html", error=f"Database error: {exc}"), 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()

    if not admin or not check_password_hash(admin["password"], password):
        return render_template("admin-login.html", error="Invalid admin email or password."), 401

    session.clear()
    session["admin_id"] = admin["id"]
    session["admin_name"] = admin["name"]
    return redirect(url_for("admin_dashboard"))


@app.route("/admin/dashboard")
def admin_dashboard():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))

    db = cursor = None
    counts = {"users": 0, "bookings": 0}
    try:
        db = get_db_connection()
        cursor = db.cursor()
        cursor.execute("SELECT COUNT(*) FROM users")
        counts["users"] = cursor.fetchone()[0]
        cursor.execute("SELECT COUNT(*) FROM bookings")
        counts["bookings"] = cursor.fetchone()[0]
    except (Error, RuntimeError) as exc:
        return f"Database error: {exc}", 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    return render_template("admin-dashboard.html", counts=counts)


@app.route("/admin/users")
def admin_users():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))
    db = cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("SELECT id, name, email, created_at FROM users ORDER BY id DESC")
        users = cursor.fetchall()
    except (Error, RuntimeError) as exc:
        return f"Database error: {exc}", 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    return render_template("admin-users.html", users=users)


@app.route("/admin/bookings")
def admin_bookings():
    if "admin_id" not in session:
        return redirect(url_for("admin_login"))
    db = cursor = None
    try:
        db = get_db_connection()
        cursor = db.cursor(dictionary=True)
        cursor.execute("""
            SELECT b.id, u.name AS user_name, u.email, h.name AS hotel_name,
                   b.booking_date, b.travellers, b.status, b.created_at
            FROM bookings b
            JOIN users u ON u.id = b.user_id
            JOIN hotels h ON h.id = b.hotel_id
            ORDER BY b.id DESC
        """)
        bookings = cursor.fetchall()
    except (Error, RuntimeError) as exc:
        return f"Database error: {exc}", 500
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()
    return render_template("admin-bookings.html", bookings=bookings)


@app.route("/admin/logout")
def admin_logout():
    session.pop("admin_id", None)
    session.pop("admin_name", None)
    return redirect(url_for("admin_login"))

# Existing frontend compatibility routes
PAGE_ROUTES = {
    "index.html", "login.html", "register.html", "user-dashboard.html", "profile.html",
    "places.html", "hotels.html", "booking.html", "itinerary.html", "packages.html",
    "place.html", "map.html", "offline-map.html", "travora-offline-map.html",
    "lonavlainfo.html", "lonavlainfo_2.html", "alibag.html", "ajanta.html",
    "mahabaleshwer.html"
}


@app.route("/<page>.html")
def html_page(page):
    filename = page + ".html"
    if filename in PAGE_ROUTES and os.path.exists(os.path.join(app.template_folder, filename)):
        return render_template(filename)
    return ("Page not found", 404)


@app.route("/css/<path:filename>")
def css_file(filename):
    return app.send_static_file("css/" + filename)


@app.route("/js/<path:filename>")
def js_file(filename):
    return app.send_static_file("js/" + filename)


@app.route("/images/<path:filename>")
def image_file(filename):
    return app.send_static_file("images/" + filename)


@app.route("/style.css")
def style_root():
    return app.send_static_file("css/style.css")


@app.route("/map.css")
def map_css_root():
    return app.send_static_file("css/map.css")


@app.route("/destination.css")
def destination_css_root():
    return app.send_static_file("css/destination.css")


@app.route("/lonavla.css")
def lonavla_css_root():
    return app.send_static_file("css/lonavla.css")


if __name__ == "__main__":
    app.run(debug=True)
