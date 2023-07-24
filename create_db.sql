
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS category;
CREATE TABLE category (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    name VARCHAR (32) 
    );

INSERT INTO category (name) VALUES ('ram'); 
INSERT INTO category (name) VALUES ('cpu'); 
INSERT INTO category (name) VALUES ('gpu'); 

DROP TABLE IF EXISTS product;
CREATE TABLE product (
    id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL UNIQUE, 
    name VARCHAR (32), 
    category VARCHAR (256), 
    price FLOAT (6,4), 
    percent TINYINT UNSIGNED,
    FOREIGN KEY (category) REFERENCES category (name)
    );

INSERT INTO product (name, category, price, percent) VALUES ('GTX4090', 'gpu', 1000.00, 0); 
INSERT INTO product (name, category, price, percent) VALUES ('GTX4060', 'gpu', 800.00, 0); 
INSERT INTO product (name, category, price, percent) VALUES ('GTX4050', 'gpu', 500.00, 0); 
INSERT INTO product (name, category, price, percent) VALUES ('core-i9', 'cpu', 900.00, 0); 
INSERT INTO product (name, category, price, percent) VALUES ('core-i7', 'cpu', 600.00, 0); 
INSERT INTO product (name, category, price, percent) VALUES ('core-i5', 'cpu', 200.00, 0); 
INSERT INTO product (name, category, price, percent) VALUES ('kingston 8g', 'ram', 40.00, 0); 
INSERT INTO product (name, category, price, percent) VALUES ('kingston 16g', 'ram', 70.00, 0); 
INSERT INTO product (name, category, price, percent) VALUES ('corsair 32g', 'ram', 110.00, 0); 


COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
