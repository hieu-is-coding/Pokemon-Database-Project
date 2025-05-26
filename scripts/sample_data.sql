-- Clear existing data 
SET FOREIGN_KEY_CHECKS = 0;
TRUNCATE TABLE battle;
TRUNCATE TABLE pokemon_ability;
TRUNCATE TABLE pokemon;
TRUNCATE TABLE ability;
TRUNCATE TABLE trainer;
TRUNCATE TABLE region;
SET FOREIGN_KEY_CHECKS = 1;

-- Insert regions
INSERT INTO region (region_name) VALUES 
('Kanto'), ('Johto'), ('Hoenn'), ('Sinnoh'), 
('Unova'), ('Kalos'), ('Alola'), ('Galar');

-- Insert abilities
INSERT INTO ability (ability_name, description) VALUES
('Overgrow', 'Powers up Grass-type moves when the Pokémon is in trouble.'),
('Blaze', 'Powers up Fire-type moves when the Pokémon is in trouble.'),
('Torrent', 'Powers up Water-type moves when the Pokémon is in trouble.');

-- Insert trainers
INSERT INTO trainer (trainer_name, trainer_level, region_id) VALUES
('Ash Ketchum', 30, 1),
('Misty', 28, 1),
('Brock', 32, 1),
('Gary Oak', 35, 1),
('Lance', 45, 2);

-- Insert pokemon
INSERT INTO pokemon (name, hp, attack, defense, trainer_id) VALUES
('Pikachu', 35, 55, 40, 1),
('Charizard', 78, 84, 78, 1),
('Staryu', 30, 45, 55, 2),
('Onix', 35, 45, 160, 3),
('Blastoise', 79, 83, 100, 4);

-- Insert pokemon_ability relationships
INSERT INTO pokemon_ability (pokemon_id, ability_id) VALUES
(1, 3), -- Pikachu has Torrent
(2, 2), -- Charizard has Blaze
(3, 3), -- Staryu has Torrent
(4, 1), -- Onix has Overgrow
(5, 3); -- Blastoise has Torrent

-- Insert battles
INSERT INTO battle (battle_time, trainer1_id, trainer2_id, winner_id, region_id) VALUES
(NOW() - INTERVAL 10 DAY, 1, 2, 1, 1),
(NOW() - INTERVAL 20 DAY, 1, 3, 3, 2),
(NOW() - INTERVAL 30 DAY, 2, 4, 4, 1);
