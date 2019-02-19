-- create users postgres
CREATE TABLE users
(
  id         SERIAL PRIMARY KEY,
  email      VARCHAR UNIQUE,
  hashstring VARCHAR
);

-- sqlite
CREATE TABLE users
(
  id         INTEGER PRIMARY KEY AUTOINCREMENT,
  email      VARCHAR UNIQUE,
  hashstring VARCHAR NOT NULL
);


-- sqlite categories
CREATE TABLE categories
(
  id   INTEGER PRIMARY KEY AUTOINCREMENT,
  name VARCHAR UNIQUE NOT NULL
);

-- postgtres categories
CREATE TABLE categories
(
  id   SERIAL PRIMARY KEY,
  name VARCHAR UNIQUE NOT NULL
);

-- sqlite init categories
INSERT INTO categories (name)
VALUES ('Nutrition'),
       ('Domestic'),
       ('Transport'),
       ('Accounts'),
       ('Education'),
       ('Medicines'),
       ('Pets'),
       ('Misc');


-- sqlite expenditures
CREATE TABLE expenditures
(
  id            INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id       INTEGER NOT NULL,
  categories_id INTEGER NOT NULL,
  date          TEXT    NOT NULL,
  name          VARCHAR NOT NULL,
  price         INTEGER DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (categories_id) REFERENCES categories (id)
);


-- postgres expenditures
CREATE TABLE expenditures
(
  id            SERIAL PRIMARY KEY,
  user_id       INTEGER NOT NULL,
  categories_id INTEGER NOT NULL,
  date          DATE    NOT NULL,
  name          VARCHAR NOT NULL,
  price         FLOAT DEFAULT 0,
  FOREIGN KEY (user_id) REFERENCES users (id),
  FOREIGN KEY (categories_id) REFERENCES categories (id)
);


-- sqlite income
CREATE TABLE income
(
  id      INTEGER PRIMARY KEY AUTOINCREMENT,
  user_id INTEGER NOT NULL,
  date    TEXT,
  type    VARCHAR NOT NULL,
  value   INTEGER NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);

-- postgres income
CREATE TABLE income
(
  id      SERIAL PRIMARY KEY,
  user_id INTEGER NOT NULL,
  date    DATE NOT NULL ,
  type    VARCHAR NOT NULL,
  value   FLOAT NOT NULL,
  FOREIGN KEY (user_id) REFERENCES users (id)
);
