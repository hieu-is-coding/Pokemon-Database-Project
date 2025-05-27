USE pokemon_db;

-- Indexes for Region table
CREATE INDEX idx_region_name ON Region(region_name);

-- Indexes for Trainer table
CREATE INDEX idx_trainer_name ON Trainer(trainer_name);
CREATE INDEX idx_trainer_region ON Trainer(region_id);

-- Indexes for Ability table
CREATE INDEX idx_ability_name ON Ability(ability_name);

-- Indexes for Pokemon table
CREATE INDEX idx_pokemon_name ON Pokemon(name);
CREATE INDEX idx_pokemon_trainer ON Pokemon(trainer_id);
CREATE INDEX idx_pokemon_stats ON Pokemon(hp, attack, defense);

-- Indexes for Battle table
CREATE INDEX idx_battle_region ON Battle(region_id);
CREATE INDEX idx_battle_pokemon1 ON Battle(trainer1_id);
CREATE INDEX idx_battle_pokemon2 ON Battle(trainer2_id);
CREATE INDEX idx_battle_winner ON Battle(winner_id);
CREATE INDEX idx_battle_time ON Battle(battle_time);