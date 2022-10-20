DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS users;

CREATE TABLE IF NOT EXISTS payments
(
    id             INTEGER PRIMARY KEY,
    eth_address    TEXT,
    solana_address TEXT,
    amount         INTEGER,
    status         INTEGER
);

CREATE TABLE IF NOT EXISTS users
(
    id          INTEGER PRIMARY KEY,
    chat_id     INTEGER,
    eth_address TEXT
);
