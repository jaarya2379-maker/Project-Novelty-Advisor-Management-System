"""
Test and Demo Script - Complete Workflow Testing

This script demonstrates the entire flow of the project novelty detector:
1. Novelty engine analysis
2. Backend API testing
3. Database operations
4. Result validation
"""

import json
from novelty_engine import NoveltyAnalysisEngine, test_novelty_engine
from datetime import datetime


def test_novelty_engine_complete():
    """Complete test of the novelty analysis engine."""
    
    print("\n" + "="*80)
    print("NOVELTY ANALYSIS ENGINE - COMPLETE TEST")
    print("="*80)
    
    # Run the test
    result = test_novelty_engine()
    
    # Display results
    print(f"\n✓ Project analyzed: {result.project_title}")
    print(f"✓ Analysis completed at: {result.timestamp}")
    
    print("\n--- SIMILAR PROJECTS ANALYSIS ---")
    print(f"Found {len(result.similar_projects)} similar projects:")
    for i, proj in enumerate(result.similar_projects, 1):
        print(f"\n  {i}. {proj['title']}")
        print(f"     Domain: {proj['domain']}")
        print(f"     Method: {proj['method']}")
        print(f"     Similarity Score: {proj['similarity']}%")
    
    print("\n--- COMPONENT ANALYSIS ---")
    print("\nCommon Technologies:")
    for tech in result.common_technologies[:5]:
        print(f"  • {tech['name']}: {tech['usage_percent']}% usage ({tech['count']} projects)")
    
    print("\nCommon Methods:")
    for method in result.common_methods[:5]:
        print(f"  • {method['name']}: {method['usage_percent']}% usage")
    
    print("\nCommon Datasets:")
    for dataset in result.common_datasets[:3]:
        print(f"  • {dataset['name']}: {dataset['usage_percent']}% usage")
    
    print("\n--- LIMITATIONS ANALYSIS ---")
    for i, limit in enumerate(result.existing_limitations, 1):
        print(f"  {i}. {limit}")
    
    print("\n--- GAPS & OPPORTUNITIES ---")
    for i, gap in enumerate(result.possible_gaps, 1):
        print(f"  {i}. {gap}")
    
    print("\n--- NOVELTY SUGGESTIONS ---")
    for sugg in result.novelty_suggestions:
        print(f"\n  ID: {sugg['id']}")
        print(f"  Title: {sugg['title']}")
        print(f"  Description: {sugg['description']}")
        print(f"  Impact: {sugg['impact']} | Feasibility: {sugg['feasibility']}")
        print(f"  Reason: {sugg['reason']}")
    
    print("\n" + "="*80)
    
    return result


def test_api_endpoints():
    """Test backend API endpoints (requires backend running)."""
    
    print("\n" + "="*80)
    print("BACKEND API ENDPOINT TESTS")
    print("="*80)
    
    print("\nNote: These tests require the backend server to be running.")
    print("Start the backend with: python backend.py\n")
    
    try:
        import requests
        
        BASE_URL = "http://localhost:5000/api"
        
        # Test 1: Health check
        print("Test 1: Health Check")
        response = requests.get(f"{BASE_URL}/health")
        if response.status_code == 200:
            print("  ✓ Server is running")
            print(f"  Response: {response.json()['message']}")
        else:
            print("  ✗ Server not responding")
            return
        
        # Test 2: Register student
        print("\nTest 2: Student Registration")
        student_data = {
            "username": f"test_user_{datetime.now().timestamp()}",
            "email": f"test_{datetime.now().timestamp()}@university.edu",
            "password": "test_password123",
            "name": "Test User"
        }
        response = requests.post(f"{BASE_URL}/auth/register", json=student_data)
        if response.status_code == 201:
            student = response.json()['data']
            student_id = student['student_id']
            print(f"  ✓ Student registered successfully")
            print(f"  Student ID: {student_id}")
        else:
            print(f"  ✗ Registration failed: {response.json()['message']}")
            return
        
        # Test 3: Submit project
        print("\nTest 3: Project Submission")
        project_data = {
            "student_id": student_id,
            "title": "Advanced NLP Model Analysis",
            "problem_statement": "Analyze text classification techniques",
            "domain": "Natural Language Processing",
            "dataset": "Custom Dataset",
            "method": "BERT with Attention",
            "technologies": ["Python", "PyTorch", "Transformers"],
            "additional_info": "Research on domain-specific fine-tuning"
        }
        response = requests.post(f"{BASE_URL}/projects/submit", json=project_data)
        if response.status_code == 201:
            project = response.json()['data']
            project_id = project['project_id']
            print(f"  ✓ Project submitted successfully")
            print(f"  Project ID: {project_id}")
        else:
            print(f"  ✗ Submission failed: {response.json()['message']}")
            return
        
        # Test 4: Run analysis
        print("\nTest 4: Project Analysis")
        response = requests.post(f"{BASE_URL}/analyze/{project_id}")
        if response.status_code == 200:
            analysis = response.json()['data']
            print(f"  ✓ Analysis completed successfully")
            print(f"  Similar projects found: {len(analysis['similar_projects'])}")
            print(f"  Novelty suggestions: {len(analysis['novelty_suggestions'])}")
        else:
            print(f"  ✗ Analysis failed: {response.json()['message']}")
            return
        
        # Test 5: Get analysis results
        print("\nTest 5: Retrieve Analysis Results")
        response = requests.get(f"{BASE_URL}/analysis/{project_id}")
        if response.status_code == 200:
            print(f"  ✓ Analysis results retrieved successfully")
        else:
            print(f"  ✗ Failed to retrieve results")
        
        # Test 6: Select novelty
        print("\nTest 6: Select Novelty Idea")
        novelty_data = {
            "project_id": project_id,
            "novelty_title": "Federated Learning Implementation",
            "novelty_description": "Implement federated learning for privacy",
            "novelty_impact": "High",
            "novelty_feasibility": "Medium",
            "notes": "Great opportunity to explore privacy-preserving ML"
        }
        response = requests.post(f"{BASE_URL}/novelty/select", json=novelty_data)
        if response.status_code == 201:
            print(f"  ✓ Novelty idea saved successfully")
        else:
            print(f"  ✗ Failed to save novelty: {response.json()['message']}")
        
        print("\n" + "="*80)
        print("All API tests completed successfully!")
        print("="*80)
    
    except ImportError:
        print("  Note: 'requests' library not installed")
        print("  Install with: pip install requests")
    except Exception as e:
        print(f"  Error during testing: {e}")


def display_sample_analysis_json():
    """Display sample analysis output in JSON format."""
    
    print("\n" + "="*80)
    print("SAMPLE ANALYSIS OUTPUT (JSON FORMAT)")
    print("="*80)
    
    result = test_novelty_engine()
    
    output = {
        "project_title": result.project_title,
        "timestamp": result.timestamp,
        "similar_projects": result.similar_projects,
        "common_components": {
            "technologies": result.common_technologies[:5],
            "methods": result.common_methods[:5],
            "datasets": result.common_datasets[:3]
        },
        "limitations": result.existing_limitations[:5],
        "gaps": result.possible_gaps[:5],
        "novelty_suggestions": [
            {
                "id": s["id"],
                "title": s["title"],
                "impact": s["impact"],
                "feasibility": s["feasibility"],
                "reason": s["reason"]
            }
            for s in result.novelty_suggestions
        ]
    }
    
    print(json.dumps(output, indent=2))
    print("\n" + "="*80)


def display_api_documentation():
    """Display API endpoint documentation."""
    
    print("\n" + "="*80)
    print("BACKEND API DOCUMENTATION")
    print("="*80)
    
    endpoints = [
        {
            "method": "POST",
            "endpoint": "/api/auth/register",
            "description": "Register a new student",
            "payload": {
                "username": "string",
                "email": "string",
                "password": "string",
                "name": "string"
            }
        },
        {
            "method": "POST",
            "endpoint": "/api/auth/login",
            "description": "Login a student",
            "payload": {
                "username": "string (email or username)",
                "password": "string"
            }
        },
        {
            "method": "POST",
            "endpoint": "/api/projects/submit",
            "description": "Submit a new project",
            "payload": {
                "student_id": "integer",
                "title": "string",
                "problem_statement": "string",
                "domain": "string",
                "dataset": "string",
                "method": "string",
                "technologies": ["array of strings"],
                "additional_info": "string (optional)"
            }
        },
        {
            "method": "GET",
            "endpoint": "/api/projects/<project_id>",
            "description": "Get project details"
        },
        {
            "method": "GET",
            "endpoint": "/api/projects/user/<user_id>",
            "description": "Get all projects for a user"
        },
        {
            "method": "POST",
            "endpoint": "/api/analyze/<project_id>",
            "description": "Run novelty analysis on a project"
        },
        {
            "method": "GET",
            "endpoint": "/api/analysis/<project_id>",
            "description": "Get analysis results for a project"
        },
        {
            "method": "POST",
            "endpoint": "/api/novelty/select",
            "description": "Save selected novelty idea",
            "payload": {
                "project_id": "integer",
                "novelty_title": "string",
                "novelty_description": "string",
                "novelty_impact": "string",
                "novelty_feasibility": "string",
                "notes": "string (optional)"
            }
        },
        {
            "method": "GET",
            "endpoint": "/api/novelty/<project_id>",
            "description": "Get selected novelty for a project"
        },
        {
            "method": "GET",
            "endpoint": "/api/health",
            "description": "Health check - verify server is running"
        }
    ]
    
    for ep in endpoints:
        print(f"\n{ep['method']} {ep['endpoint']}")
        print(f"  Description: {ep['description']}")
        if 'payload' in ep:
            print(f"  Payload: {json.dumps(ep['payload'], indent=2)}")
    
    print("\n" + "="*80)


def main():
    """Main test execution."""
    
    print("\n" + "="*100)
    print(" "*30 + "PROJECT NOVELTY DETECTOR - TESTING SUITE")
    print("="*100)
    
    # Run tests
    test_1 = input("\n1. Test Novelty Analysis Engine? (y/n): ").lower() == 'y'
    if test_1:
        test_novelty_engine_complete()
    
    test_2 = input("\n2. Display Sample Analysis Output (JSON)? (y/n): ").lower() == 'y'
    if test_2:
        display_sample_analysis_json()
    
    test_3 = input("\n3. Display API Documentation? (y/n): ").lower() == 'y'
    if test_3:
        display_api_documentation()
    
    test_4 = input("\n4. Test Backend API Endpoints? (y/n): ").lower() == 'y'
    if test_4:
        test_api_endpoints()
    
    print("\n" + "="*100)
    print(" "*35 + "TESTING COMPLETE")
    print("="*100 + "\n")


if __name__ == '__main__':
    main()
