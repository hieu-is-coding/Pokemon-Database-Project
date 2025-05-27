USE pokemon_db;

CREATE TABLE pokemon_audit_log (
    log_id INT AUTO_INCREMENT PRIMARY KEY,
    table_name VARCHAR(50) NOT NULL,
    record_id INT NOT NULL,
    action_type VARCHAR(10) NOT NULL, -- INSERT, UPDATE, DELETE
    changed_by VARCHAR(100) DEFAULT 'system',
    change_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    old_values TEXT,
    new_values TEXT
);

DELIMITER //
CREATE TRIGGER pokemon_after_insert 
AFTER INSERT ON Pokemon
FOR EACH ROW 
BEGIN
    INSERT INTO pokemon_audit_log (
        table_name, 
        record_id, 
        action_type, 
        old_values, 
        new_values
    ) 
    VALUES (
        'Pokemon',
        NEW.id,
        'INSERT',
        NULL,
        JSON_OBJECT(
            'name', NEW.name,
            'hp', NEW.hp,
            'attack', NEW.attack,
            'defense', NEW.defense,
            'trainer_id', NEW.trainer_id
        )
    );
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER pokemon_after_update 
AFTER UPDATE ON Pokemon
FOR EACH ROW 
BEGIN
    INSERT INTO pokemon_audit_log (
        table_name, 
        record_id, 
        action_type, 
        old_values, 
        new_values
    ) 
    VALUES (
        'Pokemon',
        NEW.id,
        'UPDATE',
        JSON_OBJECT(
            'name', OLD.name,
            'hp', OLD.hp,
            'attack', OLD.attack,
            'defense', OLD.defense,
            'trainer_id', OLD.trainer_id
        ),
        JSON_OBJECT(
            'name', NEW.name,
            'hp', NEW.hp,
            'attack', NEW.attack,
            'defense', NEW.defense,
            'trainer_id', NEW.trainer_id
        )
    );
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER pokemon_before_delete 
BEFORE DELETE ON Pokemon
FOR EACH ROW 
BEGIN
    INSERT INTO pokemon_audit_log (
        table_name, 
        record_id, 
        action_type, 
        old_values, 
        new_values
    ) 
    VALUES (
        'Pokemon',
        OLD.id,
        'DELETE',
        JSON_OBJECT(
            'name', OLD.name,
            'hp', OLD.hp,
            'attack', OLD.attack,
            'defense', OLD.defense,
            'trainer_id', OLD.trainer_id
        ),
        NULL
    );
END //
DELIMITER ;

DELIMITER //
CREATE TRIGGER pokemon_before_insert_update 
BEFORE INSERT ON Pokemon
FOR EACH ROW 
BEGIN
    -- Validate HP (must be between 1 and 255)
    IF NEW.hp < 1 OR NEW.hp > 255 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'HP must be between 1 and 255';
    END IF;
    
    -- Validate Attack (must be between 1 and 255)
    IF NEW.attack < 1 OR NEW.attack > 255 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Attack must be between 1 and 255';
    END IF;
    
    -- Validate Defense (must be between 1 and 255)
    IF NEW.defense < 1 OR NEW.defense > 255 THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Defense must be between 1 and 255';
    END IF;
    
    -- Validate name (must not be empty)
    IF NEW.name IS NULL OR TRIM(NEW.name) = '' THEN
        SIGNAL SQLSTATE '45000' 
        SET MESSAGE_TEXT = 'Pokemon name cannot be empty';
    END IF;
END //
DELIMITER ;
