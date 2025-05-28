# 📌 Project Title  
**Simple Pokemon Database Project**

## 📄 Brief Description  
This project is a part of COMP3030 where we focus in Database managment. The system aims to manage a simplified dataset of Pokemon, providing a web-based, user-friendly interface for performing basic Create, Read, Update, and Delete (CRUD) operations (Entities Management) on Pokemon records stored exclusively in a MySQL database.  

It solves the problem of needing a straightforward tool to view, add, modify, and remove Pokemon entries without directly interacting with the database via complex queries, while adhering to database design and implementation best practices.

---

## 🖥️ Setup Instructions

*Prefer cmd on Windows, zsh on Mac, anything is fine on Linux*

1. Clone the repository:
```
git clone https://github.com/hieu-is-coding/Pokemon-Database-Project
cd Pokemon-Database-Project
```

2. Create and activate a virtual environment:
```
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```
pip install -r requirements.txt
```

4. Create new user for access (optional):
```
mysql -u root -p

CREATE USER 'your_mysql_username'@'localhost' IDENTIFIED BY 'your_mysql_password';
```

5. Grant full acess to *your_mysql_username*
```
mysql -u root -p

CREATE DATABASE IF NOT EXISTS pokemon_db;
GRANT ALL PRIVILEGES ON pokemon_db.* TO 'your_mysql_username'@'localhost';
FLUSH PRIVILEGES;
exit
```

6. Create a `.env` file in the project root with the following content:
```
DB_USERNAME=your_mysql_username
DB_PASSWORD=your_mysql_password
DB_HOST=localhost
DB_PORT=3306
DB_NAME=pokemon_db

# This is for password encryption (please change for your safety)
SECRET_KEY=8f42a73054b1749f8f58848be5e6502c8f42a73054b1749f8f58848be5e6502c
```

7. Create the database and add indexes, views, striggers, partitioning:
```
python3 setup.py
```

8. Set up admin for security enhancement (you should remember this login detail)
```
python3 src/create_admin.py admin admin@example.com your_password
```

9. Data sample loading (optional):
```
mysql -u your_mysql_username -p pokemon_db < scripts/sample_data.sql
```

10. Run the application:
```
python3 main.py
```

11. Access the application at http://localhost:5000

---
## 💿 Schema
![Entity relationship diagram](Document/Pokemon_ERD.png)
---

## 🎯 Functional & Non-functional Requirements  

### **Functional Requirements**

#### Entities Management (CRUD)
- **Create**: Add new entity entries (Region, Trainer, Ability, Pokemon, Battle) via a validated web form.  
- **Read**: View all entities in a sortable/filterable table.  
- **Update**: Edit entity details through the interface.  
- **Delete**: Remove entity records with confirmation.  
- **Search**: Simple search for name of entity.

#### Analytics and Reporting (Basic)
- At least one **VIEW** to show aggregated/specific data (e.g., Pokemon above a certain attack threshold, total count).
- Basic statistics tracking includes number of users and entities. 
- Log views access for admin 

#### Database Features
- **two STORED PROCEDURES** 
- **one TRIGGER**

### **Non-functional Requirements**

- **Usability**: Clean, intuitive, user-friendly interface.  
- **Performance**: Fast operations; use of **INDEXING** for optimization.  
- **Reliability**: Graceful error handling, data integrity via constraints.  
- **Maintainability**: Well-structured and commented code with version control (Git/GitHub).  
- **Security**:
  - Input validation (client + server).
  - Use **prepared statements** to prevent SQL injection.
  - _(Course Req)_ Define MySQL user roles (e.g., `app_user`, `admin_user`) with least privilege.  
  - If authentication is added: encrypt sensitive data.

- **Database Standards**: Use MySQL-specific features (SPs, Triggers).  
- **Normalization**: Aim for **Third Normal Form (3NF)**.  
- **Reproducibility**: Clear documentation for easy setup and testing.

---

## ⚙️ Technology

- **Database**: MySQL (Workbench/CLI)  
- **Backend**: Python + Flask  
- **DB Connector**: SQLAlchemy
- **Frontend**: HTML, CSS, JavaScript 
- **Runtime**: Python 3.x  
- **Version Control**: Git / GitHub  

---

## 👥 Team Members and Roles

### **Member 1: Pham Minh Hieu** — Backend & Database Developer  
- Database design (ERD, normalization, DDL)  
- MySQL implementation (tables, views, SPs, triggers, indexing)  
- Flask API, server-side validation, security, DB connections  

### **Member 2: Cao Lam Huy** — Frontend Developer & Tester  
- HTML/CSS/JS development, Tailwind styling  
- Form handling, API calls, client-side validation  
- Reporting/visualization, documentation, testing  

---

## 📅 Timeline

### **Week 1 (May 6–13)**
- Git repo setup, environment setup  
- Finalize topic, list requirements  
- Create initial ERD (≥4 entities), plan normalization  
- Draft design doc, peer review by May 13

### **Week 2 (May 13–20)**
- Finalize schema & DDL, create DB  
- Build Flask DB connection, implement Read API  
- Basic frontend (HTML structure, table layout)  
- Deliverable: Design Document by May 20

### **Week 3 (May 20–27)**
- Implement Create/Update/Delete APIs (with validation)  
- Create Views, Stored Procedures, Triggers  
- JS for data fetch/add form submission

### **Week 4 (May 20–27)**
- Implement Edit/Delete frontend features  
- Connect reporting view to frontend  
- Add user roles, apply indexing, test query speed  
- Refine UI/UX, add feedback messages

### **Week 5 (May 27)**
- End-to-end testing, validation, constraint checks  
- Finalize documentation and README  
- Prepare slides, rehearse demo  
- Deliverables: Final code (GitHub), report PDF, slides PDF for presentation

---

## 🗃️ Database Implementation Details

- **Views**: e.g., `v_high_attack_pokemon`  
- **Stored Procedures**: `sp_add_pokemon`, `sp_update_pokemon_stats`  
- **Triggers**: e.g., `trg_pokemon_before_update`  
- **Indexing**: On `pokemon.name`, foreign keys, etc.

---

## 🧪 Testing Strategy

- **Integration Testing**: Ensure frontend triggers backend/database correctly  
- **End-to-End Testing**: Manual test of CRUD, validation, error handling  
- **Security Testing**: Ensure SQL injection attempts fail

---

## 📦 Deliverables

- **Source Code**: Fully functional & documented (Flask + HTML/CSS/JS + SQL) in GitHub  
- **Design Document**: ERD, DDL, task division (check our document folder)  
- **Final Report**: Architecture, decisions, testing, challenges (PDF)  
- **Presentation Slides**: Summary of the project (PDF)  
- **In-Class Presentation**: 10–15 min demo + Q&A  