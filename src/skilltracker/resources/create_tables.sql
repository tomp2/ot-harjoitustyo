CREATE TABLE IF NOT EXISTS users
(
    id       INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL CHECK (LENGTH(username) >= 3),
    password TEXT        NOT NULL CHECK (LENGTH(password) >= 3)
)