drop database if exists calories_db;
create database calories_db;

use calories_db;

create table if not exists user (
    id INT NOT NULL AUTO_INCREMENT,
    username varchar(255) NOT NULL,
    password varchar(255) NOT NULL,
    calories_daily_limit int NOT NULL,
    price_monthly_limit int,
    PRIMARY KEY (id)
);

create table if not exists food (
    id INT NOT NULL AUTO_INCREMENT,
    name varchar(255) NOT NULL,
    date_eaten DATETIME NOT NULL,
    calories INT NOT NULL,
    price FLOAT,
    user_id INT NOT NULL,
    PRIMARY KEY (id)
);

