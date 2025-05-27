USE pokemon_db;

DROP TABLE IF EXISTS User_Role;
DROP TABLE IF EXISTS User;

CREATE TABLE User_Role (
    role_id INT PRIMARY KEY AUTO_INCREMENT,
    role_name VARCHAR(50) UNIQUE NOT NULL,
    description TEXT
);

CREATE TABLE User (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    role_id INT NOT NULL,
    is_active BOOLEAN DEFAULT TRUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (role_id) REFERENCES User_Role(role_id)
);

INSERT INTO User_Role (role_name, description) VALUES 
('admin', 'Administrator with full access'),
('editor', 'Can create and edit data'),
('viewer', 'Read-only access');
