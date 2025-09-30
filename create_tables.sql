PRAGMA foreign_keys = ON;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    profile TEXT DEFAULT 'moderado'
);

CREATE TABLE categories (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    type TEXT DEFAULT 'gasto',
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id)
);

CREATE TABLE investments (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT NOT NULL,
    monthly_rate REAL NOT NULL,
    risk TEXT
);

CREATE TABLE transactions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    amount REAL NOT NULL,
    type TEXT NOT NULL,
    category_id INTEGER,
    date TEXT,
    description TEXT,
    reversed INTEGER DEFAULT 0,
    is_reversal INTEGER DEFAULT 0,
    reversal_of_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (category_id) REFERENCES categories (id),
    FOREIGN KEY (reversal_of_id) REFERENCES transactions (id)
);

CREATE TABLE metas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    user_id INTEGER NOT NULL,
    description TEXT NOT NULL,
    target_amount REAL NOT NULL,
    deadline TEXT,
    current_amount REAL DEFAULT 0,
    kind TEXT DEFAULT 'caixinha',
    investment_id INTEGER,
    months_applied INTEGER DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users (id),
    FOREIGN KEY (investment_id) REFERENCES investments (id)
);