import sys
import os
from dotenv import load_dotenv

load_dotenv()

current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
sys.path.append(project_root)

from src.main import create_app
from src.models import db
from src.models.user import User, UserRole
from sqlalchemy import text

def create_admin_user(username, email, password):
    app = create_app()
    
    with app.app_context():
        # Check if admin role exists
        admin_role = db.session.execute(text("SELECT role_id FROM User_Role WHERE role_name = 'admin'")).fetchone()
        
        if not admin_role:
            print("Admin role not found. Creating roles...")
            # Create roles
            db.session.execute(text("""
                INSERT INTO User_Role (role_name, description) VALUES 
                ('admin', 'Administrator with full access'),
                ('editor', 'Can create and edit data'),
                ('viewer', 'Read-only access')
            """))
            db.session.commit()
            admin_role = db.session.execute(text("SELECT role_id FROM User_Role WHERE role_name = 'admin'")).fetchone()
        
        # Check if user already exists
        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        
        if existing_user:
            print(f"User {username} or email {email} already exists.")
            return
        
        # Create admin user
        admin_user = User(username=username, email=email, role_id=admin_role[0])
        admin_user.set_password(password)
        
        db.session.add(admin_user)
        db.session.commit()
        
        print(f"Admin user {username} created successfully!")

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python create_admin.py <username> <email> <password>")
        sys.exit(1)
    
    username = sys.argv[1]
    email = sys.argv[2]
    password = sys.argv[3]
    
    create_admin_user(username, email, password)
