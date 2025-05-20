CREATE DATABASE IF NOT EXISTS pokemon_db;
USE pokemon_db;

-- Drop tables if they exist
DROP TABLE IF EXISTS Battle;
DROP TABLE IF EXISTS Pokemon_Ability;
DROP TABLE IF EXISTS Pokemon;
DROP TABLE IF EXISTS Ability;
DROP TABLE IF EXISTS Trainer;
DROP TABLE IF EXISTS Region;


-- Initialize tables
CREATE TABLE Region (
    region_id INT PRIMARY KEY AUTO_INCREMENT,
    region_name VARCHAR(100) UNIQUE NOT NULL
);

CREATE TABLE Trainer (
    trainer_id INT PRIMARY KEY AUTO_INCREMENT,
    trainer_name VARCHAR(100) NOT NULL,
    trainer_level INT NOT NULL,
    region_id INT,
    FOREIGN KEY (region_id) REFERENCES Region(region_id)
);

CREATE TABLE Ability (
    ability_id INT PRIMARY KEY AUTO_INCREMENT,
    ability_name VARCHAR(100) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE Pokemon (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100) NOT NULL UNIQUE,
    hp INT NOT NULL,
    attack INT NOT NULL,
    defense INT NOT NULL,
    trainer_id INT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (trainer_id) REFERENCES Trainer(trainer_id)
);

CREATE TABLE Pokemon_Ability (
    pokemon_id INT,
    ability_id INT,
    PRIMARY KEY (pokemon_id, ability_id),
    FOREIGN KEY (pokemon_id) REFERENCES Pokemon(id),
    FOREIGN KEY (ability_id) REFERENCES Ability(ability_id)
);

CREATE TABLE Battle (
    battle_id INT PRIMARY KEY AUTO_INCREMENT,
    battle_time TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    trainer1_id INT NOT NULL,
    trainer2_id INT NOT NULL,
    winner_id INT NOT NULL,
    region_id INT,
    FOREIGN KEY (trainer1_id) REFERENCES Pokemon(id),
    FOREIGN KEY (trainer2_id) REFERENCES Pokemon(id),
    FOREIGN KEY (winner_id) REFERENCES Pokemon(id),
    FOREIGN KEY (region_id) REFERENCES Region(region_id)
);
