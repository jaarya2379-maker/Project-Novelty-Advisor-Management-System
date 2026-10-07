# Project Novelty Detector - Backend Documentation

## Overview

This is the complete backend system for the Project Novelty Detector application. It includes:

1. **Novelty Analysis Engine** (`novelty_engine.py`) - Core intelligence module
2. **Flask Backend Server** (`backend.py`) - REST API endpoints
3. **Database Integration** - MySQL database management
4. **Complete Testing Suite** - Workflow testing and validation

---

## Architecture

```
Frontend (Streamlit)
        ↓
REST API Endpoints (Flask Backend)
        ↓
Novelty Analysis Engine
        ↓
MySQL Database
```

### Components

#### 1. Novelty Analysis Engine (`novelty_engine.py`)

**Purpose:** Performs complete novelty analysis for research projects

**Classes:**
- `ProjectAttributeExtractor` - Extract and normalize project attributes
- `SimilarityAnalyzer` - Calculate similarity between projects
- `ComponentAnalyzer` - Analyze common/overused components
- `LimitationAnalyzer` - Extract limitations of similar projects
- `GapAnalyzer` - Identify improvement opportunities
- `NoveltyIdeasGenerator` - Generate novelty suggestions
- `NoveltyAnalysisEngine` - Main orchestrating engine

**Main Function:**
```python
def analyze_project(project_data: Dict, previous_projects: List[Dict]) -> AnalysisResult
```

**Input:**
```python
project_data = {
    "title": str,
    "problem_statement": str,
    "domain": str,
    "dataset": str,
    "method": str,
    "technologies": List[str],
    "additional_info": str (optional)
}

previous_projects = [
    {similar_structure},
    ...
]
```

**Output:**
```python
AnalysisResult(
    project_title: str,
    similar_projects: List[Dict],          # Top 5 similar projects with similarity %
    common_technologies: List[Dict],        # Technologies with usage percentage
    common_datasets: List[Dict],            # Datasets with usage percentage
    common_methods: List[Dict],             # Methods with usage percentage
    existing_limitations: List[str],        # Common limitations found
    possible_gaps: List[str],               # Improvement opportunities
    novelty_suggestions: List[Dict],        # 5 specific novelty ideas
    timestamp: str                          # ISO format timestamp
)
```

**Similarity Calculation Method:**

The engine uses a weighted multi-metric approach:
- **Domain Similarity (25%):** Case-insensitive string comparison
- **Method Similarity (25%):** Algorithm/technique matching
- **Dataset Similarity (20%):** Dataset name comparison
- **Technologies (15%):** Jaccard similarity on technology stacks
- **Keywords (15%):** Semantic similarity on project keywords

Each metric returns a score 0-1, weighted scores are summed to get 0-100% similarity.

#### 2. Flask Backend Server (`backend.py`)

**Purpose:** REST API for frontend-backend communication

**Key Features:**
- Student authentication (register/login)
- Project submission and retrieval
- Analysis orchestration
- Result storage
- Novelty selection management

**Database Configuration:**
```python
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'  # Change this
app.config['MYSQL_DB'] = 'project_novelty_detector'
```

---

## Installation & Setup

### Prerequisites
- Python 3.8+
- MySQL Server 5.7+
- pip (Python package manager)

### Step 1: Install Dependencies

```bash
cd project-novelty-detector

# Frontend dependencies
pip install -r requirements.txt

# Backend dependencies
pip install -r backend_requirements.txt
```

### Step 2: Setup MySQL Database

```bash
# Start MySQL server (if not running)
# On Windows:
mysql --version  # Verify installation

# On Mac:
brew services start mysql

# On Linux:
sudo systemctl start mysql
```

### Step 3: Initialize Database

```bash
python setup_database.py
```

This script will:
- Create the database `project_novelty_detector`
- Create all necessary tables
- Insert sample data for testing

**Expected Output:**
```
✓ Database 'project_novelty_detector' created successfully
✓ Table 'students' created
✓ Table 'projects' created
✓ Table 'analysis_results' created
✓ Table 'selected_novelties' created
✓ All tables created successfully!
✓ Sample data inserted successfully!
```

### Step 4: Update Database Credentials

Edit `backend.py` and `setup_database.py` with your MySQL credentials:

```python
# Line ~35 in backend.py
app.config['MYSQL_PASSWORD'] = 'your_mysql_password'
```

---

## Running the Application

### Terminal 1: Start Backend Server

```bash
python backend.py
```

**Expected Output:**
```
================================================================================
Project Novelty Detector - Backend Server
================================================================================
Starting Flask server on http://localhost:5000
API Documentation available at http://localhost:5000/docs
================================================================================
```

### Terminal 2: Start Frontend Application

```bash
python -m streamlit run app_single_file.py
```

**Expected Output:**
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
Network URL: http://192.168.1.7:8501
```

---

## API Endpoints

### Authentication Endpoints

#### 1. Register Student
```
POST /api/auth/register
Content-Type: application/json

{
    "username": "john_doe",
    "email": "john@university.edu",
    "password": "securepassword123",
    "name": "John Doe"
}

Response:
{
    "success": true,
    "message": "Registration successful",
    "data": {
        "student_id": 1,
        "username": "john_doe",
        "email": "john@university.edu"
    }
}
```

#### 2. Login Student
```
POST /api/auth/login
Content-Type: application/json

{
    "username": "john_doe",
    "password": "securepassword123"
}

Response:
{
    "success": true,
    "message": "Login successful",
    "data": {
        "student_id": 1,
        "username": "john_doe",
        "email": "john@university.edu",
        "name": "John Doe"
    }
}
```

### Project Endpoints

#### 3. Submit Project
```
POST /api/projects/submit
Content-Type: application/json

{
    "student_id": 1,
    "title": "AI-Powered Disease Detection",
    "problem_statement": "Develop ML model to detect diseases from medical images",
    "domain": "Medical AI",
    "dataset": "Medical Image Dataset",
    "method": "Convolutional Neural Networks",
    "technologies": ["Python", "TensorFlow", "OpenCV"],
    "additional_info": "Using attention mechanisms for better accuracy"
}

Response:
{
    "success": true,
    "message": "Project submitted successfully",
    "data": {
        "project_id": 1,
        "status": "submitted"
    }
}
```

#### 4. Get Project Details
```
GET /api/projects/1

Response:
{
    "success": true,
    "message": "Project retrieved successfully",
    "data": {
        "project_id": 1,
        "student_id": 1,
        "title": "AI-Powered Disease Detection",
        "domain": "Medical AI",
        "technologies": ["Python", "TensorFlow", "OpenCV"],
        "status": "submitted",
        "created_at": "2026-09-13 10:30:00"
    }
}
```

#### 5. Get User's Projects
```
GET /api/projects/user/1

Response:
{
    "success": true,
    "message": "Projects retrieved successfully",
    "data": [
        {project1_data},
        {project2_data},
        ...
    ]
}
```

### Analysis Endpoints

#### 6. Run Analysis
```
POST /api/analyze/1

Response:
{
    "success": true,
    "message": "Analysis completed successfully",
    "data": {
        "analysis_id": 1,
        "project_id": 1,
        "similar_projects": [
            {
                "title": "Medical Image Classification",
                "domain": "Medical AI",
                "similarity": 85,
                ...
            }
        ],
        "common_technologies": [
            {"name": "Python", "usage_percent": 95},
            {"name": "TensorFlow", "usage_percent": 78}
        ],
        "novelty_suggestions": [
            {
                "id": "novelty_001",
                "title": "Implement Federated Learning",
                "impact": "High",
                "feasibility": "Medium"
            }
        ]
    }
}
```

#### 7. Get Analysis Results
```
GET /api/analysis/1

Response:
{
    "success": true,
    "message": "Analysis results retrieved successfully",
    "data": {
        "analysis_id": 1,
        "project_id": 1,
        "similar_projects": [...],
        "common_technologies": [...],
        "existing_limitations": [...],
        "possible_gaps": [...],
        "novelty_suggestions": [...]
    }
}
```

### Novelty Endpoints

#### 8. Select Novelty Idea
```
POST /api/novelty/select
Content-Type: application/json

{
    "project_id": 1,
    "novelty_title": "Implement Federated Learning",
    "novelty_description": "Add federated learning for privacy",
    "novelty_impact": "High",
    "novelty_feasibility": "Medium",
    "notes": "Great opportunity for privacy-preserving ML"
}

Response:
{
    "success": true,
    "message": "Novelty idea saved successfully",
    "data": {
        "novelty_id": 1,
        "project_id": 1
    }
}
```

#### 9. Get Selected Novelty
```
GET /api/novelty/1

Response:
{
    "success": true,
    "message": "Selected novelty retrieved successfully",
    "data": {
        "novelty_id": 1,
        "project_id": 1,
        "novelty_title": "Implement Federated Learning",
        "novelty_impact": "High",
        "selected_at": "2026-09-13 10:45:00"
    }
}
```

### Health Check

#### 10. Health Check
```
GET /api/health

Response:
{
    "success": true,
    "message": "Backend server is running",
    "data": {
        "status": "running",
        "timestamp": "2026-09-13T10:30:00.123456"
    }
}
```

---

## Database Schema

### students Table
```sql
student_id (INT, PRIMARY KEY)
username (VARCHAR 100, UNIQUE)
email (VARCHAR 100, UNIQUE)
password_hash (VARCHAR 255)
name (VARCHAR 100)
created_at (TIMESTAMP)
```

### projects Table
```sql
project_id (INT, PRIMARY KEY)
student_id (INT, FOREIGN KEY)
title (VARCHAR 255)
problem_statement (TEXT)
domain (VARCHAR 100)
dataset (VARCHAR 255)
method (VARCHAR 255)
technologies (JSON)
additional_info (TEXT)
status (VARCHAR 50)
created_at (TIMESTAMP)
updated_at (TIMESTAMP)
```

### analysis_results Table
```sql
analysis_id (INT, PRIMARY KEY)
project_id (INT, FOREIGN KEY, UNIQUE)
similar_projects (JSON)
common_technologies (JSON)
common_datasets (JSON)
common_methods (JSON)
existing_limitations (JSON)
possible_gaps (JSON)
novelty_suggestions (JSON)
analysis_timestamp (TIMESTAMP)
```

### selected_novelties Table
```sql
novelty_id (INT, PRIMARY KEY)
project_id (INT, FOREIGN KEY)
novelty_title (VARCHAR 255)
novelty_description (TEXT)
novelty_impact (VARCHAR 50)
novelty_feasibility (VARCHAR 50)
notes (TEXT)
selected_at (TIMESTAMP)
```

---

## Testing

### Run Complete Test Suite

```bash
python test_complete_workflow.py
```

This will:
1. Test novelty analysis engine with sample data
2. Display analysis output in JSON format
3. Show API endpoint documentation
4. (Optional) Test backend API endpoints if server is running

### Test Output

```
1. Novelty Analysis Engine Test
   - Analyzes 5 sample projects
   - Compares new project against them
   - Displays similar projects, limitations, gaps, suggestions

2. Sample Analysis Output (JSON)
   - Shows complete analysis structure
   - Useful for understanding API response format

3. API Documentation
   - All 10 endpoints documented
   - Request/response examples

4. API Endpoint Tests
   - Requires: Backend running on localhost:5000
   - Tests: Registration, submission, analysis, selection
```

---

## Troubleshooting

### MySQL Connection Error
```
Error: "Can't connect to MySQL server on 'localhost'"
```

**Solution:**
1. Verify MySQL is running: `mysql --version`
2. Check credentials in `backend.py`
3. On Windows: `Services` → Search for MySQL → Start service
4. On Mac: `brew services start mysql`
5. On Linux: `sudo systemctl start mysql`

### Module Import Error
```
Error: "No module named 'MySQLdb'"
```

**Solution:**
```bash
pip install mysqlclient
```
`mysqlclient` needs the MySQL/MariaDB client dev headers and a C compiler
to build -- see the install notes at the bottom of `backend_requirements.txt`
for the platform-specific prerequisite packages. (Note: `PyMySQL` is a
pure-Python alternative but is **not** a drop-in fix here, since
`backend.py` imports `MySQLdb` directly via Flask-MySQLdb.)

### Port Already in Use
```
Error: "Address already in use" for port 5000
```

**Solution:**
```bash
# Kill process using port 5000
lsof -ti:5000 | xargs kill -9  # Mac/Linux
netstat -ano | findstr :5000   # Windows (then taskkill /PID xxx /F)
```

### Database Not Found
```
Error: "Unknown database 'project_novelty_detector'"
```

**Solution:**
```bash
python setup_database.py
# Then verify: mysql -u root -p project_novelty_detector
```

---

## Example Workflow

### 1. Register & Login
```bash
curl -X POST http://localhost:5000/api/auth/register \
  -H "Content-Type: application/json" \
  -d '{
    "username": "alice",
    "email": "alice@uni.edu",
    "password": "pass123",
    "name": "Alice Smith"
  }'
```

### 2. Submit Project
```bash
curl -X POST http://localhost:5000/api/projects/submit \
  -H "Content-Type: application/json" \
  -d '{
    "student_id": 1,
    "title": "NLP Sentiment Analysis",
    "problem_statement": "Analyze sentiment in social media",
    "domain": "Natural Language Processing",
    "dataset": "Twitter Data",
    "method": "BERT Transfer Learning",
    "technologies": ["Python", "PyTorch", "Transformers"]
  }'
```

### 3. Run Analysis
```bash
curl -X POST http://localhost:5000/api/analyze/1
```

### 4. Get Results
```bash
curl -X GET http://localhost:5000/api/analysis/1
```

### 5. Select Novelty
```bash
curl -X POST http://localhost:5000/api/novelty/select \
  -H "Content-Type: application/json" \
  -d '{
    "project_id": 1,
    "novelty_title": "Multi-language Support",
    "novelty_impact": "High",
    "novelty_feasibility": "High"
  }'
```

---

## Performance Notes

*(Expectations based on algorithmic complexity, not a formal benchmark run.)*

- **Similarity Calculation:** O(n) where n = number of previous projects
- **Optimal Database Performance:** Index on `student_id`, `status`, and project title
  (already defined in `setup_database.py`)
- **Recommended Max Projects:** 100-1000 per analysis (memory efficient)
- **Analysis Time:** ~1-2 seconds for a typical dataset of a few dozen projects

---

## Security Considerations

1. **Passwords:** Hashed with Werkzeug's salted PBKDF2 hasher (`werkzeug.security.generate_password_hash`) -- each hash includes its own random salt, so identical passwords do not produce identical stored hashes
2. **Input Validation:** All endpoints validate required fields
3. **SQL Injection:** Using parameterized queries with MySQLdb
4. **CORS:** Enabled for cross-origin requests
5. **Database:** Use strong password for MySQL root user

---

## Future Enhancements

- [ ] JWT token-based authentication
- [ ] Advanced similarity algorithms (embeddings, NLP)
- [ ] Real-time collaboration features
- [ ] Export analysis to PDF/Excel
- [ ] API rate limiting
- [ ] Advanced analytics dashboard
- [ ] Machine learning model training for better suggestions

---

## Support & Questions

For issues or questions:
1. Check troubleshooting section
2. Review test output: `python test_complete_workflow.py`
3. Check MySQL connection: `mysql -u root -p`
4. Review Flask logs for error details

---

## License

This project is for educational purposes. Use as needed.

---

**Version:** 1.1 -- see `CHANGELOG.md` for revision history
