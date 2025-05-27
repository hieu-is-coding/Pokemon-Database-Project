import os
import sys
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Get database connection details from environment
DB_USERNAME = os.getenv('DB_USERNAME', 'root')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'password')
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_PORT = os.getenv('DB_PORT', '3306')
DB_NAME = os.getenv('DB_NAME', 'pokemon_db')

# Create database URL
db_url = f"mysql+pymysql://{DB_USERNAME}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Create engine
engine = create_engine(db_url)

def execute_sql_file(file_path):
    print(f"Executing {file_path}...")
    
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return
    
    with open(file_path, 'r') as f:
        sql = f.read()
    
    # Handle DELIMITER statements for triggers
    if 'DELIMITER' in sql:
        # Split by DELIMITER statements
        parts = sql.split('DELIMITER')
        
        for part in parts:
            if not part.strip():
                continue
                
            # Get the delimiter
            lines = part.strip().split('\n')
            if not lines:
                continue
                
            delimiter = lines[0].strip()
            # Join the rest of the lines
            statements = '\n'.join(lines[1:])
            
            # Split by the delimiter
            for statement in statements.split(delimiter):
                if statement.strip():
                    try:
                        with engine.connect() as conn:
                            conn.execute(text(statement))
                            conn.commit()
                    except Exception as e:
                        print(f"Error executing statement: {str(e)}")
    else:
        # Regular SQL file without DELIMITER statements
        statements = sql.split(';')
        for statement in statements:
            if statement.strip():
                try:
                    with engine.connect() as conn:
                        conn.execute(text(statement))
                        conn.commit()
                except Exception as e:
                    print(f"Error executing statement: {str(e)}")
    
    print(f"Finished executing {file_path}")

def main():
    # Directory containing SQL files
    sql_dir = os.path.join(os.path.dirname(__file__), 'scripts')
    
    # Files to execute in order
    files = [
        'schema.sql',
        'indexes.sql',
        'views.sql',
        'triggers.sql',
        'partitioning.sql'
    ]
    
    for file in files:
        execute_sql_file(os.path.join(sql_dir, file))
    
    print("All SQL files executed successfully!")

if __name__ == "__main__":
    main()
