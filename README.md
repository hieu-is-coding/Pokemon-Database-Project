# Pokemon Database Web App - README

## Overview
This is a Flask-based Pokemon database web application with MySQL database support. The application allows users to perform CRUD operations (Create, Read, Update, Delete) on various entities including regions, trainers, abilities, Pokemon, and battles.

## Features
- **Region Management**: Add, view, edit, and delete Pokemon regions
- **Trainer Management**: Add, view, edit, and delete trainers with region assignments
- **Ability Management**: Add, view, edit, and delete Pokemon abilities
- **Pokemon Management**: Add, view, edit, and delete Pokemon with trainer assignments and ability relationships
- **Battle Management**: Record, view, edit, and delete battles between Pokemon
- **Search Functionality**: Search capabilities for all entities

## Technology Stack
- **Backend**: Flask (Python)
- **Database**: MySQL
- **ORM**: SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript, Bootstrap

## Installation and Setup

### Prerequisites
- Python 3.x
- MySQL Server
- pip (Python package manager)

### Setup Instructions

1. Clone the repository:
```
git clone <repository-url>
cd pokemon_db_app
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create a `.env` file in the project root with the following content:
```
DB_USERNAME=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pokemon_db
SECRET_KEY=your_secret_key
```

5. Create the database and tables:
```
mysql -u your_mysql_username -p < schema.sql
```

6. Run the application:
```
python main.py
```

7. Access the application at http://localhost:5000

## Project Structure
```
pokemon_db_app/
├── venv/                      # Virtual environment
├── src/                       # Source code
│   ├── main.py                # Application entry point
│   ├── models/                # Database models
│   │   ├── __init__.py
│   │   ├── region.py          # Region model
│   │   ├── trainer.py         # Trainer model
│   │   ├── ability.py         # Ability model
│   │   ├── pokemon.py         # Pokemon model
│   │   └── battle.py          # Battle model
│   ├── routes/                # API routes
│   │   ├── __init__.py
│   │   ├── region_routes.py   # Region CRUD routes
│   │   ├── trainer_routes.py  # Trainer CRUD routes
│   │   ├── ability_routes.py  # Ability CRUD routes
│   │   ├── pokemon_routes.py  # Pokemon CRUD routes
│   │   └── battle_routes.py   # Battle CRUD routes
│   ├── static/                # Static assets
│   │   ├── css/               # CSS files
│   │   ├── js/                # JavaScript files
│   │   └── img/               # Image files
│   └── templates/             # HTML templates
│       ├── base.html          # Base template
│       ├── index.html         # Home page
│       ├── regions/           # Region templates
│       ├── trainers/          # Trainer templates
│       ├── abilities/         # Ability templates
│       ├── pokemons/          # Pokemon templates
│       └── battles/           # Battle templates
├── main.py                    # Application entry point
├── schema.sql                 # Database schema
└── requirements.txt           # Project dependencies
```

## Entity Relationships

1. **Region**:
   - One-to-many relationship with Trainer (one region can have many trainers)
   - One-to-many relationship with Battle (one region can host many battles)

2. **Trainer**:
   - Many-to-one relationship with Region (many trainers can be from one region)
   - One-to-many relationship with Pokemon (one trainer can own many Pokemon)

3. **Ability**:
   - Many-to-many relationship with Pokemon through Pokemon_Ability junction table

4. **Pokemon**:
   - Many-to-one relationship with Trainer (many Pokemon can be owned by one trainer)
   - Many-to-many relationship with Ability through Pokemon_Ability junction table
   - One-to-many relationship with Battle (one Pokemon can participate in many battles)

5. **Battle**:
   - Many-to-one relationship with Region (many battles can occur in one region)
   - Many-to-one relationship with Pokemon for trainer1_id, trainer2_id, and winner_id

## API Endpoints

### Region Endpoints
- GET /regions - List all regions
- GET /regions/<id> - Get region details
- POST /regions - Create new region
- PUT /regions/<id> - Update region
- DELETE /regions/<id> - Delete region

### Trainer Endpoints
- GET /trainers - List all trainers
- GET /trainers/<id> - Get trainer details
- POST /trainers - Create new trainer
- PUT /trainers/<id> - Update trainer
- DELETE /trainers/<id> - Delete trainer

### Ability Endpoints
- GET /abilities - List all abilities
- GET /abilities/<id> - Get ability details
- POST /abilities - Create new ability
- PUT /abilities/<id> - Update ability
- DELETE /abilities/<id> - Delete ability

### Pokemon Endpoints
- GET /pokemons - List all Pokemon
- GET /pokemons/<id> - Get Pokemon details
- POST /pokemons - Create new Pokemon
- PUT /pokemons/<id> - Update Pokemon
- DELETE /pokemons/<id> - Delete Pokemon
- POST /pokemons/<id>/abilities/<ability_id> - Assign ability to Pokemon
- DELETE /pokemons/<id>/abilities/<ability_id> - Remove ability from Pokemon

### Battle Endpoints
- GET /battles - List all battles
- GET /battles/<id> - Get battle details
- POST /battles - Create new battle
- PUT /battles/<id> - Update battle
- DELETE /battles/<id> - Delete battle

## License
This project is licensed under the MIT License - see the LICENSE file for details.
