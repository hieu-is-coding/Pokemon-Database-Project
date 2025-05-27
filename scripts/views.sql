USE pokemon_db;

CREATE VIEW v_pokemon_details AS
SELECT 
    p.id, 
    p.name AS pokemon_name, 
    p.hp, 
    p.attack, 
    p.defense, 
    t.trainer_id, 
    t.trainer_name, 
    t.trainer_level, 
    r.region_id, 
    r.region_name
FROM 
    Pokemon p
LEFT JOIN 
    Trainer t ON p.trainer_id = t.trainer_id
LEFT JOIN 
    Region r ON t.region_id = r.region_id;

-- View for Pokemon with their abilities
CREATE VIEW v_pokemon_abilities AS
SELECT 
    p.id, 
    p.name AS pokemon_name, 
    GROUP_CONCAT(a.ability_name SEPARATOR ', ') AS abilities
FROM 
    Pokemon p
LEFT JOIN 
    Pokemon_Ability pa ON p.id = pa.pokemon_id
LEFT JOIN 
    Ability a ON pa.ability_id = a.ability_id
GROUP BY 
    p.id, p.name;

-- View for Battle details
CREATE VIEW v_battle_details AS
SELECT 
    b.battle_id, 
    b.battle_time, 
    p1.name AS pokemon1_name, 
    p2.name AS pokemon2_name, 
    pw.name AS winner_name, 
    r.region_name,
    t1.trainer_name AS trainer1_name,
    t2.trainer_name AS trainer2_name
FROM 
    Battle b
JOIN 
    Pokemon p1 ON b.trainer1_id = p1.id
JOIN 
    Pokemon p2 ON b.trainer2_id = p2.id
JOIN 
    Pokemon pw ON b.winner_id = pw.id
LEFT JOIN 
    Region r ON b.region_id = r.region_id
LEFT JOIN 
    Trainer t1 ON p1.trainer_id = t1.trainer_id
LEFT JOIN 
    Trainer t2 ON p2.trainer_id = t2.trainer_id;

-- View for Region statistics
CREATE VIEW v_region_stats AS
SELECT 
    r.region_id, 
    r.region_name, 
    COUNT(DISTINCT t.trainer_id) AS trainer_count, 
    COUNT(DISTINCT p.id) AS pokemon_count, 
    COUNT(DISTINCT b.battle_id) AS battle_count
FROM 
    Region r
LEFT JOIN 
    Trainer t ON r.region_id = t.region_id
LEFT JOIN 
    Pokemon p ON t.trainer_id = p.trainer_id
LEFT JOIN 
    Battle b ON r.region_id = b.region_id
GROUP BY 
    r.region_id, r.region_name;