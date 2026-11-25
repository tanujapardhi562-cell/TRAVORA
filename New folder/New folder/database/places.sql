USE travora_db;

CREATE TABLE places (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    city VARCHAR(100),
    category VARCHAR(100),
    description TEXT,
    latitude DECIMAL(10,7),
    longitude DECIMAL(10,7)
);