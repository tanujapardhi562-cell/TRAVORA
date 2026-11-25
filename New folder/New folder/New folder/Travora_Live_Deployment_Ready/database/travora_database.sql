CREATE DATABASE IF NOT EXISTS travora_db;
USE travora_db;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);



CREATE TABLE IF NOT EXISTS admins (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    category VARCHAR(100),
    description TEXT,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7)
);

CREATE TABLE IF NOT EXISTS hotels (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(150) NOT NULL,
    location VARCHAR(100),
    price DECIMAL(10,2),
    rating DECIMAL(2,1),
    description TEXT
);

CREATE TABLE IF NOT EXISTS bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    hotel_id INT NOT NULL,
    booking_date DATE NOT NULL,
    travellers INT NOT NULL DEFAULT 1,
    status VARCHAR(50) DEFAULT 'Pending',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (hotel_id) REFERENCES hotels(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS itinerary (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT NOT NULL,
    place_id INT NOT NULL,
    visit_date DATE NULL,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (place_id) REFERENCES places(id) ON DELETE CASCADE
);

INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Lonavala','Pune','Hill Station','Beautiful hill station near Pune and Mumbai.',18.7546,73.4062) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Lonavala');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Khandala','Pune','Hill Station','Scenic hill station near Lonavala.',18.7580,73.3760) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Khandala');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Karla Caves','Lonavala','Historical','Ancient rock-cut caves near Lonavala.',18.7897,73.4789) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Karla Caves');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Pawna Lake','Maval, Pune','Lake','Beautiful lake surrounded by mountains.',18.6380,73.4880) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Pawna Lake');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Rajmachi Fort','Lonavala','Fort','Historic fort surrounded by Sahyadri mountains.',18.8326,73.3945) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Rajmachi Fort');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Gateway of India','Mumbai','Historical','Historic waterfront landmark in Mumbai.',18.9220,72.8347) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Gateway of India');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Alibaug','Raigad','Beach','Popular coastal destination in Maharashtra.',18.6414,72.8722) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Alibaug');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Sinhagad Fort','Pune','Fort','Historic fort near Pune.',18.3663,73.7559) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Sinhagad Fort');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Mahabaleshwar','Satara','Hill Station','Famous hill station known for viewpoints and strawberries.',17.9307,73.6477) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Mahabaleshwar');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Ajanta Caves','Chhatrapati Sambhajinagar','Historical','Ancient Buddhist rock-cut caves.',20.5519,75.7033) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Ajanta Caves');
INSERT INTO places (name, city, category, description, latitude, longitude)
SELECT * FROM (SELECT 'Ellora Caves','Chhatrapati Sambhajinagar','Historical','Famous ancient rock-cut caves.',20.0268,75.1793) AS x
WHERE NOT EXISTS (SELECT 1 FROM places WHERE name='Ellora Caves');

INSERT INTO hotels (name, location, price, rating, description)
SELECT * FROM (SELECT 'Valley View Resort','Lonavala',2500.00,4.5,'Comfortable resort with beautiful valley views.') AS x
WHERE NOT EXISTS (SELECT 1 FROM hotels WHERE name='Valley View Resort');
INSERT INTO hotels (name, location, price, rating, description)
SELECT * FROM (SELECT 'Hilltop Stay','Mahabaleshwar',3200.00,4.3,'Peaceful stay near popular tourist attractions.') AS x
WHERE NOT EXISTS (SELECT 1 FROM hotels WHERE name='Hilltop Stay');
INSERT INTO hotels (name, location, price, rating, description)
SELECT * FROM (SELECT 'Coastal Retreat','Alibaug',2800.00,4.4,'Relaxing hotel near the beach.') AS x
WHERE NOT EXISTS (SELECT 1 FROM hotels WHERE name='Coastal Retreat');

-- Check after running:
-- SHOW TABLES;
-- SELECT * FROM users;
-- SELECT * FROM places;
-- SELECT * FROM hotels;
-- SELECT * FROM bookings;
-- SELECT * FROM itinerary;
