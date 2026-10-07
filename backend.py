"""
Project Novelty Detector - Backend Server

Flask-based REST API for the Project Novelty Detection system.
Integrates with MySQL database and the Novelty Analysis Engine.

API Endpoints:
- POST /api/auth/register - Register a new student
- POST /api/auth/login - Login student
- POST /api/projects/submit - Submit a new project
- GET /api/projects/<project_id> - Get project details
- GET /api/projects/user/<user_id> - Get all projects for a user
- POST /api/analyze/<project_id> - Run analysis on a project
- GET /api/analysis/<project_id> - Get analysis results
- POST /api/novelty/select - Save selected novelty idea
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_mysqldb import MySQL
import MySQLdb.cursors
import json
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime
from functools import wraps
from typing import Dict, Any, Tuple
import traceback

# Import the novelty engine
from novelty_engine import NoveltyAnalysisEngine

# ============================================================================
# FLASK APP CONFIGURATION
# ============================================================================

app = Flask(__name__)
CORS(app)

# MySQL Configuration
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'  # Change this to your MySQL password
app.config['MYSQL_DB'] = 'project_novelty_detector'

mysql = MySQL(app)

# Initialize novelty engine
novelty_engine = NoveltyAnalysisEngine()

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def initialize_database():
    """Initialize database tables if they don't exist."""
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    # Create students table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS students (
            student_id INT AUTO_INCREMENT PRIMARY KEY,
            username VARCHAR(100) UNIQUE NOT NULL,
            email VARCHAR(100) UNIQUE NOT NULL,
            password_hash VARCHAR(255) NOT NULL,
            name VARCHAR(100) NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    
    # Create projects table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id INT AUTO_INCREMENT PRIMARY KEY,
            student_id INT NOT NULL,
            title VARCHAR(255) NOT NULL,
            problem_statement TEXT NOT NULL,
            domain VARCHAR(100),
            dataset VARCHAR(255),
            method VARCHAR(255),
            technologies JSON,
            additional_info TEXT,
            status VARCHAR(50) DEFAULT 'submitted',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
            FOREIGN KEY (student_id) REFERENCES students(student_id)
        )
    """)
    
    # Create analysis_results table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS analysis_results (
            analysis_id INT AUTO_INCREMENT PRIMARY KEY,
            project_id INT NOT NULL,
            similar_projects JSON,
            common_technologies JSON,
            common_datasets JSON,
            common_methods JSON,
            existing_limitations JSON,
            possible_gaps JSON,
            novelty_suggestions JSON,
            analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(project_id)
        )
    """)
    
    # Create selected_novelties table
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS selected_novelties (
            novelty_id INT AUTO_INCREMENT PRIMARY KEY,
            project_id INT NOT NULL,
            novelty_title VARCHAR(255),
            novelty_description TEXT,
            novelty_impact VARCHAR(50),
            novelty_feasibility VARCHAR(50),
            notes TEXT,
            selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (project_id) REFERENCES projects(project_id)
        )
    """)
    
    mysql.connection.commit()
    cursor.close()
    
    print("✓ Database initialized successfully")


# ============================================================================
# UTILITY FUNCTIONS
# ============================================================================

def hash_password(password: str) -> str:
    """Hash password using Werkzeug's salted PBKDF2 hasher.

    Each call produces a different hash (and includes the salt + method
    inside the string), so two users with the same password end up with
    different stored hashes -- unlike a bare SHA256 digest, this is not
    vulnerable to rainbow-table lookups.
    """
    return generate_password_hash(password)

def verify_password(password: str, password_hash: str) -> bool:
    """Verify a plaintext password against a Werkzeug-generated hash."""
    return check_password_hash(password_hash, password)

def success_response(data: Any = None, message: str = "Success", status_code: int = 200) -> Tuple[Dict, int]:
    """Return standardized success response."""
    return {
        "success": True,
        "message": message,
        "data": data
    }, status_code

def error_response(message: str, status_code: int = 400, error_details: str = None) -> Tuple[Dict, int]:
    """Return standardized error response."""
    response = {
        "success": False,
        "message": message,
        "error": error_details
    }
    return response, status_code

def validate_required_fields(data: Dict, required_fields: list) -> Tuple[bool, str]:
    """Validate that required fields are present."""
    for field in required_fields:
        if field not in data or not data[field]:
            return False, f"Missing required field: {field}"
    return True, ""

# ============================================================================
# AUTHENTICATION ENDPOINTS
# ============================================================================

@app.route('/api/auth/register', methods=['POST'])
def register():
    """Register a new student account."""
    try:
        data = request.get_json()
        
        # Validate required fields
        valid, error_msg = validate_required_fields(data, ['username', 'email', 'password', 'name'])
        if not valid:
            return error_response(error_msg, 400)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Check if user already exists
        cursor.execute("SELECT * FROM students WHERE email = %s OR username = %s", 
                      (data['email'], data['username']))
        
        if cursor.fetchone():
            return error_response("User already exists with this email or username", 409)
        
        # Hash password and insert
        password_hash = hash_password(data['password'])
        cursor.execute(
            "INSERT INTO students (username, email, password_hash, name) VALUES (%s, %s, %s, %s)",
            (data['username'], data['email'], password_hash, data['name'])
        )
        mysql.connection.commit()
        
        student_id = cursor.lastrowid
        cursor.close()
        
        return success_response(
            {"student_id": student_id, "username": data['username'], "email": data['email']},
            "Registration successful",
            201
        )
    
    except Exception as e:
        return error_response("Registration failed", 500, str(e))


@app.route('/api/auth/login', methods=['POST'])
def login():
    """Authenticate student login."""
    try:
        data = request.get_json()
        
        valid, error_msg = validate_required_fields(data, ['username', 'password'])
        if not valid:
            return error_response(error_msg, 400)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM students WHERE username = %s OR email = %s", 
                      (data['username'], data['username']))
        
        student = cursor.fetchone()
        cursor.close()
        
        if not student or not verify_password(data['password'], student['password_hash']):
            return error_response("Invalid username/email or password", 401)
        
        return success_response(
            {
                "student_id": student['student_id'],
                "username": student['username'],
                "email": student['email'],
                "name": student['name']
            },
            "Login successful",
            200
        )
    
    except Exception as e:
        return error_response("Login failed", 500, str(e))


# ============================================================================
# PROJECT SUBMISSION ENDPOINTS
# ============================================================================

@app.route('/api/projects/submit', methods=['POST'])
def submit_project():
    """Submit a new project for analysis."""
    try:
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['student_id', 'title', 'problem_statement', 'domain', 
                         'dataset', 'method', 'technologies']
        valid, error_msg = validate_required_fields(data, required_fields)
        if not valid:
            return error_response(error_msg, 400)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Verify student exists
        cursor.execute("SELECT * FROM students WHERE student_id = %s", (data['student_id'],))
        if not cursor.fetchone():
            return error_response("Student not found", 404)
        
        # Insert project
        technologies_json = json.dumps(data['technologies'])
        cursor.execute("""
            INSERT INTO projects 
            (student_id, title, problem_statement, domain, dataset, method, technologies, additional_info, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            data['student_id'],
            data['title'],
            data['problem_statement'],
            data['domain'],
            data['dataset'],
            data['method'],
            technologies_json,
            data.get('additional_info', ''),
            'submitted'
        ))
        mysql.connection.commit()
        
        project_id = cursor.lastrowid
        cursor.close()
        
        return success_response(
            {"project_id": project_id, "status": "submitted"},
            "Project submitted successfully",
            201
        )
    
    except Exception as e:
        return error_response("Project submission failed", 500, str(e))


@app.route('/api/projects/<int:project_id>', methods=['GET'])
def get_project(project_id):
    """Retrieve project details."""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
        
        project = cursor.fetchone()
        cursor.close()
        
        if not project:
            return error_response("Project not found", 404)
        
        # Parse JSON fields
        project['technologies'] = json.loads(project['technologies'])
        
        return success_response(project, "Project retrieved successfully")
    
    except Exception as e:
        return error_response("Failed to retrieve project", 500, str(e))


@app.route('/api/projects/user/<int:user_id>', methods=['GET'])
def get_user_projects(user_id):
    """Retrieve all projects for a student."""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT p.*, s.name as student_name
            FROM projects p
            JOIN students s ON p.student_id = s.student_id
            WHERE p.student_id = %s
            ORDER BY p.created_at DESC
        """, (user_id,))
        
        projects = cursor.fetchall()
        cursor.close()
        
        # Parse JSON fields
        for project in projects:
            project['technologies'] = json.loads(project['technologies'])
        
        return success_response(projects, "Projects retrieved successfully")
    
    except Exception as e:
        return error_response("Failed to retrieve projects", 500, str(e))


# ============================================================================
# ANALYSIS ENDPOINTS
# ============================================================================

@app.route('/api/analyze/<int:project_id>', methods=['POST'])
def analyze_project(project_id):
    """Run novelty analysis on a submitted project."""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Get the project
        cursor.execute("SELECT * FROM projects WHERE project_id = %s", (project_id,))
        project = cursor.fetchone()
        
        if not project:
            return error_response("Project not found", 404)
        
        # Get all previous projects for comparison
        cursor.execute("""
            SELECT * FROM projects 
            WHERE student_id != %s AND status != 'submitted'
            ORDER BY created_at DESC
            LIMIT 20
        """, (project['student_id'],))
        
        previous_projects = cursor.fetchall()
        cursor.close()
        
        # Parse JSON fields
        project['technologies'] = json.loads(project['technologies'])
        for prev_proj in previous_projects:
            prev_proj['technologies'] = json.loads(prev_proj['technologies'])
        
        # Run analysis
        analysis_result = novelty_engine.analyze_project(project, previous_projects)
        
        # Store analysis results in database
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            INSERT INTO analysis_results
            (project_id, similar_projects, common_technologies, common_datasets, 
             common_methods, existing_limitations, possible_gaps, novelty_suggestions)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (
            project_id,
            json.dumps(analysis_result.similar_projects),
            json.dumps(analysis_result.common_technologies),
            json.dumps(analysis_result.common_datasets),
            json.dumps(analysis_result.common_methods),
            json.dumps(analysis_result.existing_limitations),
            json.dumps(analysis_result.possible_gaps),
            json.dumps(analysis_result.novelty_suggestions)
        ))
        
        # Update project status
        cursor.execute(
            "UPDATE projects SET status = %s WHERE project_id = %s",
            ('analyzed', project_id)
        )
        mysql.connection.commit()
        
        analysis_id = cursor.lastrowid
        cursor.close()
        
        return success_response(
            {
                "analysis_id": analysis_id,
                "project_id": project_id,
                "similar_projects": analysis_result.similar_projects,
                "common_technologies": analysis_result.common_technologies,
                "common_datasets": analysis_result.common_datasets,
                "common_methods": analysis_result.common_methods,
                "existing_limitations": analysis_result.existing_limitations,
                "possible_gaps": analysis_result.possible_gaps,
                "novelty_suggestions": analysis_result.novelty_suggestions
            },
            "Analysis completed successfully",
            200
        )
    
    except Exception as e:
        return error_response("Analysis failed", 500, str(e) + "\n" + traceback.format_exc())


@app.route('/api/analysis/<int:project_id>', methods=['GET'])
def get_analysis_results(project_id):
    """Retrieve analysis results for a project."""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT * FROM analysis_results 
            WHERE project_id = %s
            ORDER BY analysis_timestamp DESC
            LIMIT 1
        """, (project_id,))
        
        analysis = cursor.fetchone()
        cursor.close()
        
        if not analysis:
            return error_response("Analysis results not found", 404)
        
        # Parse JSON fields
        analysis['similar_projects'] = json.loads(analysis['similar_projects'])
        analysis['common_technologies'] = json.loads(analysis['common_technologies'])
        analysis['common_datasets'] = json.loads(analysis['common_datasets'])
        analysis['common_methods'] = json.loads(analysis['common_methods'])
        analysis['existing_limitations'] = json.loads(analysis['existing_limitations'])
        analysis['possible_gaps'] = json.loads(analysis['possible_gaps'])
        analysis['novelty_suggestions'] = json.loads(analysis['novelty_suggestions'])
        
        return success_response(analysis, "Analysis results retrieved successfully")
    
    except Exception as e:
        return error_response("Failed to retrieve analysis results", 500, str(e))


# ============================================================================
# NOVELTY SELECTION ENDPOINTS
# ============================================================================

@app.route('/api/novelty/select', methods=['POST'])
def select_novelty():
    """Save the selected novelty idea for a project."""
    try:
        data = request.get_json()
        
        valid, error_msg = validate_required_fields(data, ['project_id', 'novelty_title'])
        if not valid:
            return error_response(error_msg, 400)
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        # Verify project exists
        cursor.execute("SELECT * FROM projects WHERE project_id = %s", (data['project_id'],))
        if not cursor.fetchone():
            return error_response("Project not found", 404)
        
        # Insert selected novelty
        cursor.execute("""
            INSERT INTO selected_novelties
            (project_id, novelty_title, novelty_description, novelty_impact, novelty_feasibility, notes)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (
            data['project_id'],
            data['novelty_title'],
            data.get('novelty_description', ''),
            data.get('novelty_impact', ''),
            data.get('novelty_feasibility', ''),
            data.get('notes', '')
        ))
        
        # Update project status
        cursor.execute(
            "UPDATE projects SET status = %s WHERE project_id = %s",
            ('saved', data['project_id'])
        )
        mysql.connection.commit()
        
        novelty_id = cursor.lastrowid
        cursor.close()
        
        return success_response(
            {"novelty_id": novelty_id, "project_id": data['project_id']},
            "Novelty idea saved successfully",
            201
        )
    
    except Exception as e:
        return error_response("Failed to save novelty idea", 500, str(e))


@app.route('/api/novelty/<int:project_id>', methods=['GET'])
def get_selected_novelty(project_id):
    """Retrieve the selected novelty for a project."""
    try:
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("""
            SELECT * FROM selected_novelties 
            WHERE project_id = %s
            ORDER BY selected_at DESC
            LIMIT 1
        """, (project_id,))
        
        novelty = cursor.fetchone()
        cursor.close()
        
        if not novelty:
            return error_response("No novelty selected for this project", 404)
        
        return success_response(novelty, "Selected novelty retrieved successfully")
    
    except Exception as e:
        return error_response("Failed to retrieve novelty selection", 500, str(e))


# ============================================================================
# HEALTH CHECK ENDPOINT
# ============================================================================

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return success_response(
        {"status": "running", "timestamp": datetime.now().isoformat()},
        "Backend server is running"
    )


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return error_response("Endpoint not found", 404)


@app.errorhandler(500)
def server_error(error):
    """Handle 500 errors."""
    return error_response("Internal server error", 500, str(error))


# ============================================================================
# MAIN EXECUTION
# ============================================================================

if __name__ == '__main__':
    # Initialize database
    with app.app_context():
        try:
            initialize_database()
        except Exception as e:
            print(f"Database initialization error: {e}")
            print("Note: Make sure MySQL is running and credentials are correct in the config")
    
    # Start Flask server
    print("\n" + "="*80)
    print("Project Novelty Detector - Backend Server")
    print("="*80)
    print(f"Starting Flask server on http://localhost:5000")
    print(f"API Documentation available at http://localhost:5000/docs")
    print("="*80 + "\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
