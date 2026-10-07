"""
Database Setup Script for Project Novelty Detector

Run this script to initialize the MySQL database.
Requirements: MySQL server running on localhost
"""

import MySQLdb
from MySQLdb.cursors import DictCursor
from werkzeug.security import generate_password_hash

# Database connection parameters
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'password',  # Change this to your MySQL root password
}

def create_database():
    """Create the main database."""
    try:
        conn = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password']
        )
        cursor = conn.cursor()
        
        # Create database
        cursor.execute("CREATE DATABASE IF NOT EXISTS project_novelty_detector")
        print("✓ Database 'project_novelty_detector' created successfully")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        return True
    
    except MySQLdb.Error as e:
        print(f"✗ Database creation failed: {e}")
        print("\nMake sure:")
        print("  1. MySQL server is running")
        print("  2. The password in DB_CONFIG is correct")
        return False


def create_tables():
    """Create all required tables."""
    try:
        conn = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            db='project_novelty_detector'
        )
        cursor = conn.cursor()
        
        # Students table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS students (
                student_id INT AUTO_INCREMENT PRIMARY KEY,
                username VARCHAR(100) UNIQUE NOT NULL,
                email VARCHAR(100) UNIQUE NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                name VARCHAR(100) NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("✓ Table 'students' created")
        
        # Projects table
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
                FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,
                INDEX idx_student_id (student_id),
                INDEX idx_status (status),
                FULLTEXT INDEX ft_title (title),
                FULLTEXT INDEX ft_problem (problem_statement)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("✓ Table 'projects' created")
        
        # Analysis results table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS analysis_results (
                analysis_id INT AUTO_INCREMENT PRIMARY KEY,
                project_id INT NOT NULL UNIQUE,
                similar_projects JSON,
                common_technologies JSON,
                common_datasets JSON,
                common_methods JSON,
                existing_limitations JSON,
                possible_gaps JSON,
                novelty_suggestions JSON,
                analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
                INDEX idx_project_id (project_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("✓ Table 'analysis_results' created")
        
        # Selected novelties table
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
                FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,
                INDEX idx_project_id (project_id)
            ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4
        """)
        print("✓ Table 'selected_novelties' created")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("\n✓ All tables created successfully!")
        return True
    
    except MySQLdb.Error as e:
        print(f"✗ Table creation failed: {e}")
        return False


def insert_sample_data():
    """Insert sample previous projects for testing."""
    try:
        conn = MySQLdb.connect(
            host=DB_CONFIG['host'],
            user=DB_CONFIG['user'],
            passwd=DB_CONFIG['password'],
            db='project_novelty_detector'
        )
        cursor = conn.cursor()
        
        # Create a test student
        # The password hash is generated here (rather than hardcoded) so it
        # always matches whatever hashing scheme backend.py currently uses
        # (werkzeug.security.generate_password_hash, salted PBKDF2).
        cursor.execute("""
            INSERT IGNORE INTO students (username, email, password_hash, name)
            VALUES (%s, %s, %s, %s)
        """, (
            'test_student',
            'test@university.edu',
            generate_password_hash('password'),
            'Test Student'
        ))
        
        # Get the student ID
        cursor.execute("SELECT student_id FROM students WHERE username = 'test_student'")
        student_id = cursor.fetchone()[0]
        
        # Insert sample projects
        sample_projects = [
            (
                student_id,
                'Sentiment Analysis using BERT',
                'Classify social media posts for sentiment using BERT model',
                'Natural Language Processing',
                'Twitter Dataset',
                'BERT Transfer Learning',
                '["Python", "PyTorch", "Transformers", "Pandas"]',
                'Real-time sentiment classification',
                'analyzed'
            ),
            (
                student_id,
                'Image Classification with CNN',
                'Classify medical images for disease detection',
                'Computer Vision',
                'Medical Image Dataset',
                'Convolutional Neural Networks',
                '["Python", "TensorFlow", "OpenCV", "NumPy"]',
                'Multi-class classification with attention',
                'analyzed'
            ),
            (
                student_id,
                'Time Series Forecasting',
                'Predict stock prices using LSTM',
                'Time Series Analysis',
                'Stock Market Data',
                'LSTM Networks',
                '["Python", "TensorFlow", "Pandas", "Scikit-learn"]',
                'Multi-step ahead forecasting',
                'analyzed'
            ),
            (
                student_id,
                'NLP Text Generation',
                'Generate human-like text using transformer models',
                'Natural Language Processing',
                'Wikipedia Corpus',
                'GPT-based Transfer Learning',
                '["Python", "PyTorch", "Transformers", "NumPy"]',
                'Language model fine-tuning',
                'analyzed'
            ),
            (
                student_id,
                'Object Detection using YOLO',
                'Real-time object detection in video streams',
                'Computer Vision',
                'COCO Dataset',
                'YOLOv8 Detection',
                '["Python", "PyTorch", "OpenCV", "Pandas"]',
                'Real-time video processing',
                'analyzed'
            )
        ]
        
        cursor.executemany("""
            INSERT IGNORE INTO projects 
            (student_id, title, problem_statement, domain, dataset, method, technologies, additional_info, status)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, sample_projects)
        
        conn.commit()
        print("✓ Sample data inserted successfully!")
        print(f"  - Test student created: username='test_student', password='password'")
        print(f"  - 5 sample projects created for analysis comparison")
        
        cursor.close()
        conn.close()
        return True
    
    except MySQLdb.Error as e:
        print(f"Note: Sample data insertion (non-critical): {e}")
        return True


def main():
    """Main setup function."""
    print("\n" + "="*80)
    print("Project Novelty Detector - Database Setup")
    print("="*80 + "\n")
    
    print("Step 1: Creating database...")
    if not create_database():
        return False
    
    print("\nStep 2: Creating tables...")
    if not create_tables():
        return False
    
    print("\nStep 3: Inserting sample data...")
    insert_sample_data()
    
    print("\n" + "="*80)
    print("Database setup completed successfully!")
    print("="*80)
    print("\nNext steps:")
    print("  1. Update backend.py with your MySQL password if needed")
    print("  2. Run: python backend.py")
    print("  3. Run: python -m streamlit run app_single_file.py")
    print("="*80 + "\n")
    
    return True


if __name__ == '__main__':
    main()
