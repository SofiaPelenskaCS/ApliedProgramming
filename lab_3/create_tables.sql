CREATE TABLE banks (
    id INTEGER NOT NULL PRIMARY KEY,
    per_cent INTEGER,
    all_money INTEGER
);
CREATE TABLE users (
    id INTEGER NOT NULL PRIMARY KEY, 
    passport VARCHAR,
    adress VARCHAR,
    email VARCHAR, 
    telephone_number VARCHAR, 
    money_amount INTEGER,
    password BYTEA
    -- PRIMARY KEY(id)
);

CREATE TABLE credits (
    id INTEGER NOT NULL PRIMARY KEY, 
    "start_date" date, 
    end_date date, 
    start_sum INTEGER,
    current_sum INTEGER,
    "user_id" INTEGER REFERENCES users(id),
    bank_id INTEGER REFERENCES banks(id)
    -- PRIMARY KEY(id), 
    -- FOREIGN KEY(user) REFERENCES Users(id),
    -- FOREIGN KEY(bank) REFERENCES Banks(id)
);

CREATE TABLE transactions (
    id INTEGER NOT NULL, 
    date date,
    "sum" BIGINT, 
    credit_id INTEGER REFERENCES credits(id),
    PRIMARY KEY(id) 
);

-- CREATE TABLE users (
--     uid SERIAL NOT NULL, 
--     email VARCHAR, 
--     password BYTEA,
--     first_name VARCHAR, 
--     last_name VARCHAR, 
--     PRIMARY KEY (uid)
-- );

-- CREATE TABLE wallets (
--     uid SERIAL NOT NULL, 
--     name VARCHAR, 
--     funds BIGINT, 
--     owner_uid INTEGER, 
--     PRIMARY KEY (uid), 
--     FOREIGN KEY(owner_uid) REFERENCES users (uid)
-- );

-- CREATE TABLE transactions (
--     uid SERIAL NOT NULL, 
--     from_wallet_uid INTEGER, 
--     to_wallet_uid INTEGER, 
--     amount BIGINT, 
--     datetime TIMESTAMP WITHOUT TIME ZONE DEFAULT now(), 
--     PRIMARY KEY (uid), 
--     FOREIGN KEY(from_wallet_uid) REFERENCES wallets (uid), 
--     FOREIGN KEY(to_wallet_uid) REFERENCES wallets (uid)
-- );
