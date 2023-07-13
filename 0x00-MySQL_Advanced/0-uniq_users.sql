-- Creates a table with unique users.
DROP TABLE IF EXISTS users;
CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTO_INCREMENT NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255)
);
