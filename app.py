"""
Project Novelty Detector - SINGLE FILE APPLICATION
Complete Streamlit frontend for analyzing research project novelty.
All code consolidated into one file for simpler deployment.

Navigation Flow:
Login → Dashboard → Submit Project → Analyze → Novelty Results → Select Novelty → Save → My Projects
"""

import base64
import os
from pathlib import Path

import pymysql
import streamlit as st
import streamlit.components.v1 as components
import textwrap
import time
from datetime import datetime
from dotenv import load_dotenv
from werkzeug.security import check_password_hash

load_dotenv()

# ============================================================================
# CONFIGURATION AND SETUP
# ============================================================================

st.set_page_config(
    page_title="Project Novelty Detector",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded"
)

MYSQL_CONFIG = {
    "host": os.getenv("MYSQL_HOST", "localhost"),
    "user": os.getenv("MYSQL_USER", "root"),
    "password": os.getenv("MYSQL_PASSWORD", "password"),
    "database": os.getenv("MYSQL_DB", "project_novelty_detector"),
    "port": int(os.getenv("MYSQL_PORT", "3306")),
    "connect_timeout": 2,
    "cursorclass": pymysql.cursors.DictCursor,
}

# ============================================================================
# SAMPLE DATA
# ============================================================================

SAMPLE_STUDENTS = {
    "student1": {
        "username": "john_doe",
        "email": "john@university.edu",
        "password": "password123",
        "name": "John Doe"
    },
    "student2": {
        "username": "jane_smith",
        "email": "jane@university.edu",
        "password": "password123",
        "name": "Jane Smith"
    }
}

SAMPLE_PROJECTS = [
    {
        "id": "proj_001",
        "student_id": "student1",
        "title": "AI-Powered Sentiment Analysis for Social Media",
        "problem_statement": "Analyze public sentiment in real-time social media posts",
        "domain": "Natural Language Processing",
        "dataset": "Twitter/X Dataset",
        "method": "BERT-based Transfer Learning",
        "technologies": ["Python", "BERT", "Transformers", "TensorFlow"],
        "status": "analyzed",
        "created_date": "2024-09-01",
        "selected_novelty": "Implement multi-language sentiment detection"
    },
    {
        "id": "proj_002",
        "student_id": "student1",
        "title": "ECG Anomaly Detection using CNN",
        "problem_statement": "Detect cardiac anomalies from ECG signals",
        "domain": "Medical AI",
        "dataset": "MIT-BIH ECG Database",
        "method": "Convolutional Neural Networks",
        "technologies": ["Python", "TensorFlow", "Keras", "Pandas"],
        "status": "saved",
        "created_date": "2024-08-15",
        "selected_novelty": "Add attention mechanism for explainability"
    }
]

SAMPLE_SIMILAR_PROJECTS = [
    {
        "title": "Deep Learning for Stock Price Prediction",
        "authors": "Smith et al.",
        "year": 2023,
        "similarity": 72,
        "domain": "Time Series Analysis",
        "method": "LSTM Networks",
        "technologies": ["Python", "TensorFlow", "NumPy"]
    },
    {
        "title": "Recurrent Neural Networks for Sequence Modeling",
        "authors": "Johnson & Lee",
        "year": 2023,
        "similarity": 68,
        "domain": "Deep Learning",
        "method": "RNN/LSTM",
        "technologies": ["PyTorch", "Python"]
    },
    {
        "title": "Transformer Models for Time Series Forecasting",
        "authors": "Chen et al.",
        "year": 2024,
        "similarity": 65,
        "domain": "Deep Learning",
        "method": "Transformer Architecture",
        "technologies": ["Python", "Transformers", "PyTorch"]
    }
]

COMMON_TECHNOLOGIES = [
    {"name": "Python", "usage_percent": 95},
    {"name": "TensorFlow", "usage_percent": 78},
    {"name": "PyTorch", "usage_percent": 72},
    {"name": "Pandas", "usage_percent": 85},
    {"name": "NumPy", "usage_percent": 88},
    {"name": "Scikit-learn", "usage_percent": 65}
]

COMMON_DATASETS = [
    {"name": "ImageNet", "usage_percent": 70},
    {"name": "MNIST", "usage_percent": 65},
    {"name": "CIFAR-10", "usage_percent": 58},
    {"name": "UCI ML Repository", "usage_percent": 72},
    {"name": "Kaggle Datasets", "usage_percent": 80}
]

COMMON_METHODS = [
    {"name": "CNN (Convolutional Neural Networks)", "usage_percent": 75},
    {"name": "RNN/LSTM", "usage_percent": 68},
    {"name": "Transfer Learning", "usage_percent": 70},
    {"name": "Random Forest", "usage_percent": 55},
    {"name": "Support Vector Machines (SVM)", "usage_percent": 48}
]

NOVELTY_IDEAS = [
    {
        "id": "novelty_001",
        "title": "Implement Federated Learning",
        "description": "Add federated learning capabilities to train the model across distributed devices while maintaining data privacy.",
        "impact": "High",
        "feasibility": "Medium",
        "details": "Distribute model training across multiple devices without centralizing data"
    },
    {
        "id": "novelty_002",
        "title": "Add Explainability with SHAP",
        "description": "Integrate SHAP (SHapley Additive exPlanations) to make model predictions interpretable and trustworthy.",
        "impact": "High",
        "feasibility": "High",
        "details": "Provide feature importance and decision explanations for each prediction"
    },
    {
        "id": "novelty_003",
        "title": "Implement Adversarial Robustness",
        "description": "Add adversarial training and robustness testing to make the model resilient against adversarial attacks.",
        "impact": "Medium",
        "feasibility": "Medium",
        "details": "Train and test against adversarial examples to improve model robustness"
    },
    {
        "id": "novelty_004",
        "title": "Multi-Modal Learning Approach",
        "description": "Combine multiple data modalities (text, images, audio) for improved predictions.",
        "impact": "High",
        "feasibility": "Low",
        "details": "Fuse different data types with ensemble methods"
    },
    {
        "id": "novelty_005",
        "title": "Real-time Inference Optimization",
        "description": "Optimize the model for edge deployment with quantization and pruning techniques.",
        "impact": "Medium",
        "feasibility": "High",
        "details": "Deploy lightweight models for mobile and IoT devices"
    }
]

EXISTING_LIMITATIONS = [
    "Limited to small batch sizes due to memory constraints",
    "Training time exceeds 24 hours for large datasets",
    "Model performance degrades with domain shift",
    "Lack of real-time inference capabilities",
    "High computational requirements for deployment",
    "Limited cross-domain generalization",
    "Absence of uncertainty quantification"
]

POSSIBLE_GAPS = [
    "No standardized benchmarking framework for this domain",
    "Lack of interpretability in model decisions",
    "Limited focus on edge deployment and mobile optimization",
    "Missing privacy-preserving training methods",
    "No comprehensive comparison of recent architectures",
    "Insufficient real-world dataset diversity",
    "Limited multi-modal learning approaches"
]

# ============================================================================
# CUSTOM CSS STYLING
# ============================================================================

def apply_custom_css():
    """Apply custom CSS styling to the application matching the dark chalkboard pill aesthetic."""
    st.markdown("""
    <style>
        /* 1. Global Dark Chalkboard Theme */
        :root {
            --primary-color: #ffffff;
            --secondary-color: #94a3b8;
            --success-color: #4ade80;
            --danger-color: #f87171;
            --warning-color: #fb923c;
            --chalk-bg: #0b0b0f;
            --chalk-card: rgba(26, 26, 34, 0.75);
            --chalk-border: rgba(255, 255, 255, 0.85);
        }

        [data-testid="stAppViewContainer"] {
            background-color: #0b0b0f !important;
            background: radial-gradient(circle at 60% 40%, #161622 0%, #0b0b0f 85%) !important;
            color: #ffffff !important;
            overflow-x: hidden !important;
        }

        [data-testid="stHeader"] {
            background: transparent !important;
            color: #ffffff !important;
        }

        /* 2. Left Sidebar (Matching Mockup) */
        [data-testid="stSidebar"] {
            background-color: #0d0d14 !important;
            background: #0d0d14 !important;
            border-right: 1.5px solid rgba(255, 255, 255, 0.4) !important;
        }

        [data-testid="stSidebar"] * {
            color: #ffffff !important;
        }

        /* Sidebar Brand Pill */
        .sidebar-brand-pill {
            width: 100%;
            border: 1.5px solid rgba(255, 255, 255, 0.85);
            border-radius: 9999px;
            background: rgba(35, 35, 45, 0.65);
            color: #ffffff;
            text-align: center;
            padding: 0.65rem 1rem;
            font-size: 0.95rem;
            font-weight: 500;
            letter-spacing: 0.3px;
            margin-bottom: 0.75rem;
            box-shadow: 0 4px 14px rgba(0, 0, 0, 0.4);
        }

        .sidebar-divider {
            width: 100%;
            height: 1.5px;
            background: rgba(255, 255, 255, 0.85);
            margin: 0.75rem 0 1.25rem 0;
        }

        .sidebar-user-name {
            font-size: 1.15rem;
            color: #ffffff !important;
            font-weight: 400;
            margin-bottom: 1.5rem;
            padding-left: 0.25rem;
        }

        /* Sidebar Pill Navigation Buttons */
        [data-testid="stSidebar"] .stButton > button {
            width: 100% !important;
            border: 1.5px solid rgba(255, 255, 255, 0.85) !important;
            border-radius: 9999px !important;
            background: rgba(85, 85, 95, 0.75) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            padding: 0.65rem 1.2rem !important;
            margin-bottom: 0.75rem !important;
            box-shadow: 0 2px 8px rgba(0, 0, 0, 0.4) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        [data-testid="stSidebar"] .stButton > button:hover {
            background: #ffffff !important;
            color: #0b0b0f !important;
            -webkit-text-fill-color: #0b0b0f !important;
            font-weight: 600 !important;
            box-shadow: 0 0 16px rgba(255, 255, 255, 0.5) !important;
            transform: translateY(-1px) !important;
        }

        /* 3. Main Content Container */
        .main {
            background: transparent !important;
            color: #ffffff !important;
            padding: 1.5rem 2.5rem !important;
        }

        .main .block-container {
            max-width: 1100px !important;
            padding: 1.5rem 1rem !important;
            background: transparent !important;
        }

        /* 4. Dashboard Specific Components (Exact Mockup Match) */
        .dash-hero-wrapper {
            width: 100%;
            max-width: 880px;
            margin: 0 auto 0.75rem auto;
            display: flex;
            justify-content: center;
            align-items: center;
            position: relative;
        }

        .dash-hero-stage {
            position: relative;
            width: 100%;
            max-width: 862px;
            margin: 0 auto;
        }

        .dash-hero-img {
            width: 100%;
            height: auto;
            display: block;
            user-select: none;
            pointer-events: none;
        }

        .dash-hero-overlay {
            position: absolute;
            top: 48%;
            left: 53.4%;
            transform: translate(-50%, -50%);
            width: 65%;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            pointer-events: none;
        }

        .dash-welcome-title {
            font-size: clamp(1.2rem, 2.2vw, 1.8rem);
            font-weight: 400;
            color: #ffffff;
            margin: 0 0 0.35rem 0;
            letter-spacing: 0.3px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.85);
        }

        .dash-welcome-subtitle {
            font-size: clamp(0.78rem, 1.3vw, 1.02rem);
            color: #f1f5f9;
            font-weight: 400;
            letter-spacing: 0.1px;
            margin: 0;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
            text-shadow: 0 2px 8px rgba(0, 0, 0, 0.85);
        }

        /* 3 Stats Pills (Capsules / Ovals) */
        .dash-stat-pill {
            width: 100%;
            height: 52px;
            min-height: 52px;
            border: 1.5px solid rgba(255, 255, 255, 0.95);
            border-radius: 9999px;
            background: #000000;
            padding: 0 1rem;
            display: flex;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.6);
            transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
            box-sizing: border-box;
            cursor: pointer;
        }

        .dash-stat-pill:hover {
            transform: translateY(-2px);
            box-shadow: 0 0 16px rgba(255, 255, 255, 0.35);
            border-color: #ffffff;
        }

        .dash-stat-pill span {
            color: #ffffff;
            font-size: 1.05rem;
            font-weight: 400;
            letter-spacing: 0.3px;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
        }

        /* Hide dashboard quick action buttons as per user mockup */
        .st-key-dashboard_quick_actions,
        .st-key-create_project,
        .st-key-view_projects {
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            border: none !important;
            position: absolute !important;
            visibility: hidden !important;
            pointer-events: none !important;
            overflow: hidden !important;
            opacity: 0 !important;
        }

        /* Recent Projects Section Header & Divider */
        .dash-section-header {
            font-size: 1.45rem;
            font-weight: 400;
            color: #ffffff;
            margin: 2.2rem 0 0.4rem 0;
            letter-spacing: 0.3px;
        }

        .dash-section-divider {
            width: 100%;
            height: 1.5px;
            background: rgba(255, 255, 255, 0.85);
            margin: 0.4rem 0 1.8rem 0;
        }

        /* 5. Typography Across All Pages */
        h1, h2, h3, h4, h5, h6 {
            color: #ffffff !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            font-weight: 500 !important;
        }

        h1 {
            font-size: 1.85rem !important;
            border-bottom: 1.5px solid rgba(255, 255, 255, 0.85) !important;
            padding-bottom: 0.75rem !important;
            margin-bottom: 1.5rem !important;
        }

        p, span, div, li, label {
            color: #cbd5e1 !important;
        }

        strong, b {
            color: #ffffff !important;
        }

        /* 6. Form Inputs & Textareas (Pills & Chalk Containers) */
        .stTextInput > div > div > input,
        .stPasswordInput > div > div > input {
            background: rgba(30, 30, 40, 0.75) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 9999px !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            padding: 0.75rem 1.4rem !important;
            font-size: 0.95rem !important;
            box-shadow: none !important;
        }

        .stTextInput > div > div > input:focus,
        .stPasswordInput > div > div > input:focus {
            border-color: #ffffff !important;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.4) !important;
        }

        .stTextArea > div > div > textarea {
            background: rgba(30, 30, 40, 0.75) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 18px !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            padding: 1rem 1.25rem !important;
            font-size: 0.95rem !important;
            box-shadow: none !important;
        }

        .stTextArea > div > div > textarea:focus {
            border-color: #ffffff !important;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.4) !important;
        }

        .stSelectbox > div > div {
            background: rgba(30, 30, 40, 0.75) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.8) !important;
            border-radius: 9999px !important;
            color: #ffffff !important;
        }

        /* 7. Buttons Across Entire Application (Pill Shape) */
        .stButton > button {
            border: 1.5px solid rgba(255, 255, 255, 0.85) !important;
            border-radius: 9999px !important;
            background: rgba(55, 55, 68, 0.8) !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            padding: 0.65rem 1.4rem !important;
            font-weight: 500 !important;
            font-size: 0.95rem !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.4) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
        }

        .stButton > button:hover {
            background: #ffffff !important;
            color: #0b0b0f !important;
            -webkit-text-fill-color: #0b0b0f !important;
            box-shadow: 0 0 16px rgba(255, 255, 255, 0.5) !important;
            transform: translateY(-1px) !important;
        }

        /* 8. Cards Across All Pages */
        .card, .project-card {
            background: rgba(24, 24, 32, 0.75) !important;
            border: 1.5px solid rgba(255, 255, 255, 0.25) !important;
            border-radius: 20px !important;
            padding: 1.5rem !important;
            margin-bottom: 1.25rem !important;
            box-shadow: 0 4px 18px rgba(0, 0, 0, 0.5) !important;
            backdrop-filter: blur(10px) !important;
            transition: border-color 0.2s ease, box-shadow 0.2s ease;
            box-sizing: border-box !important;
            max-width: 100% !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
            word-break: break-word !important;
        }

        .card *, .project-card * {
            box-sizing: border-box !important;
            overflow-wrap: break-word !important;
            word-wrap: break-word !important;
            word-break: break-word !important;
        }

        .card:hover, .project-card:hover {
            border-color: rgba(255, 255, 255, 0.6) !important;
            box-shadow: 0 6px 22px rgba(0, 0, 0, 0.6) !important;
        }

        .card h3, .card h4, .project-card h3, .project-card h4 {
            color: #ffffff !important;
        }

        /* 9. Metric Pill Badges */
        .metric-badge {
            display: inline-block;
            background: rgba(255, 255, 255, 0.12) !important;
            border: 1px solid rgba(255, 255, 255, 0.5) !important;
            color: #ffffff !important;
            padding: 0.25rem 0.85rem !important;
            border-radius: 9999px !important;
            font-size: 0.8rem !important;
            font-weight: 500 !important;
            margin-right: 0.5rem !important;
            margin-bottom: 0.5rem !important;
        }

        /* 10. Message Alert Banners */
        .info-box {
            background: rgba(25, 35, 50, 0.75) !important;
            border: 1.5px solid rgba(56, 189, 248, 0.6) !important;
            border-radius: 16px !important;
            padding: 1rem 1.25rem !important;
            color: #e0f2fe !important;
            margin-bottom: 1.25rem !important;
            backdrop-filter: blur(10px) !important;
        }
        .info-box strong { color: #38bdf8 !important; }

        .success-box {
            background: rgba(18, 42, 28, 0.75) !important;
            border: 1.5px solid rgba(74, 222, 128, 0.6) !important;
            border-radius: 16px !important;
            padding: 1rem 1.25rem !important;
            color: #dcfce7 !important;
            margin-bottom: 1.25rem !important;
            backdrop-filter: blur(10px) !important;
        }
        .success-box strong { color: #4ade80 !important; }

        .warning-box {
            background: rgba(45, 30, 18, 0.75) !important;
            border: 1.5px solid rgba(251, 146, 60, 0.6) !important;
            border-radius: 16px !important;
            padding: 1rem 1.25rem !important;
            color: #ffedd5 !important;
            margin-bottom: 1.25rem !important;
            backdrop-filter: blur(10px) !important;
        }
        .warning-box strong { color: #fb923c !important; }

        /* 11. Tabs Styling - Floating Pill Capsules / Bubbles matching mockup */
        div[data-testid="stTabs"],
        .stTabs {
            background: transparent !important;
            margin-top: 0.5rem !important;
            margin-bottom: 1.5rem !important;
        }

        /* Tab list container */
        div[data-testid="stTabs"] [role="tablist"],
        div[data-testid="stTabs"] [data-baseweb="tab-list"],
        [data-baseweb="tab-list"],
        [role="tablist"] {
            background: transparent !important;
            border-bottom: none !important;
            border: none !important;
            gap: 1.25rem !important;
            padding: 0.5rem 0 1.25rem 0 !important;
            margin-bottom: 1rem !important;
            display: flex !important;
            flex-wrap: wrap !important;
            align-items: center !important;
            overflow: visible !important;
            overflow-y: visible !important;
        }

        /* Remove underline bar in React-Aria & BaseWeb */
        div[data-testid="stTabs"] [role="tablist"]::after,
        div[data-testid="stTabs"] div[role="tablist"]::after,
        div[data-testid="stTabs"] > div > div::after,
        .stTabs [role="tablist"]::after,
        [role="tablist"]::after {
            display: none !important;
            content: none !important;
            background: transparent !important;
            height: 0 !important;
            border: none !important;
            opacity: 0 !important;
            visibility: hidden !important;
        }

        /* Remove selection indicator (red underline) */
        div[data-testid="stTabs"] .react-aria-SelectionIndicator,
        .react-aria-SelectionIndicator,
        div[data-testid="stTabs"] [data-baseweb="tab-highlight"],
        div[data-testid="stTabs"] [data-baseweb="tab-border"],
        [data-baseweb="tab-highlight"],
        [data-baseweb="tab-border"] {
            display: none !important;
            height: 0 !important;
            width: 0 !important;
            opacity: 0 !important;
            visibility: hidden !important;
            border: none !important;
            background: transparent !important;
            pointer-events: none !important;
        }

        /* Individual Tab Capsule Bubble (React-Aria & BaseWeb) */
        div[data-testid="stTabs"] [data-testid="stTab"],
        div[data-testid="stTabs"] [role="tab"],
        div[data-testid="stTabs"] button[role="tab"],
        .stTabs [data-testid="stTab"],
        .stTabs [role="tab"],
        [data-testid="stTab"],
        div[data-testid="stTabs"] [data-baseweb="tab"],
        [data-baseweb="tab"] {
            border: 1.5px solid rgba(255, 255, 255, 0.85) !important;
            border-bottom: 1.5px solid rgba(255, 255, 255, 0.85) !important;
            border-radius: 9999px !important;
            background: rgba(65, 65, 75, 0.85) !important;
            padding: 0.65rem 1.6rem !important;
            margin: 0 !important;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.35) !important;
            transition: all 0.2s cubic-bezier(0.4, 0, 0.2, 1) !important;
            cursor: pointer !important;
            outline: none !important;
            height: auto !important;
            min-height: 42px !important;
            display: inline-flex !important;
            align-items: center !important;
            justify-content: center !important;
            text-decoration: none !important;
            box-sizing: border-box !important;
        }

        /* Typography inside tab capsule bubble */
        div[data-testid="stTabs"] [data-testid="stTab"] *,
        div[data-testid="stTabs"] [role="tab"] *,
        .stTabs [data-testid="stTab"] *,
        .stTabs [role="tab"] *,
        [data-testid="stTab"] *,
        div[data-testid="stTabs"] [data-baseweb="tab"] *,
        [data-baseweb="tab"] * {
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-size: 0.95rem !important;
            font-weight: 500 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
            line-height: 1.2 !important;
            margin: 0 !important;
            padding: 0 !important;
            text-decoration: none !important;
        }

        /* Hover state for inactive bubbles */
        div[data-testid="stTabs"] [data-testid="stTab"]:hover:not([data-selected]),
        div[data-testid="stTabs"] [data-testid="stTab"]:hover:not([aria-selected="true"]),
        div[data-testid="stTabs"] [role="tab"]:hover:not([data-selected]),
        div[data-testid="stTabs"] [role="tab"]:hover:not([aria-selected="true"]),
        .stTabs [data-testid="stTab"]:hover:not([data-selected]),
        .stTabs [role="tab"]:hover:not([data-selected]),
        div[data-testid="stTabs"] [data-baseweb="tab"]:hover:not([aria-selected="true"]) {
            background: rgba(255, 255, 255, 0.2) !important;
            border-color: #ffffff !important;
            border-bottom-color: #ffffff !important;
            transform: translateY(-1px) !important;
            box-shadow: 0 6px 16px rgba(0, 0, 0, 0.45) !important;
        }

        /* Selected / Active Tab Capsule Bubble */
        div[data-testid="stTabs"] [data-testid="stTab"][data-selected],
        div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"],
        div[data-testid="stTabs"] [role="tab"][data-selected],
        div[data-testid="stTabs"] [role="tab"][aria-selected="true"],
        .stTabs [data-testid="stTab"][data-selected],
        .stTabs [data-testid="stTab"][aria-selected="true"],
        .stTabs [role="tab"][data-selected],
        .stTabs [role="tab"][aria-selected="true"],
        div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] {
            background: #ffffff !important;
            border: 1.5px solid #ffffff !important;
            border-bottom: 1.5px solid #ffffff !important;
            border-radius: 9999px !important;
            box-shadow: 0 0 16px rgba(255, 255, 255, 0.45) !important;
            transform: translateY(-1px) !important;
        }

        div[data-testid="stTabs"] [data-testid="stTab"][data-selected] *,
        div[data-testid="stTabs"] [data-testid="stTab"][aria-selected="true"] *,
        div[data-testid="stTabs"] [role="tab"][data-selected] *,
        div[data-testid="stTabs"] [role="tab"][aria-selected="true"] *,
        .stTabs [data-testid="stTab"][data-selected] *,
        .stTabs [data-testid="stTab"][aria-selected="true"] *,
        .stTabs [role="tab"][data-selected] *,
        .stTabs [role="tab"][aria-selected="true"] *,
        div[data-testid="stTabs"] [data-baseweb="tab"][aria-selected="true"] * {
            color: #0b0b0f !important;
            -webkit-text-fill-color: #0b0b0f !important;
            font-weight: 600 !important;
        }

        /* Focus state */
        div[data-testid="stTabs"] [data-testid="stTab"]:focus,
        div[data-testid="stTabs"] [role="tab"]:focus,
        div[data-testid="stTabs"] [data-baseweb="tab"]:focus {
            outline: none !important;
        }

        div[data-testid="stTabContent"] {
            padding-top: 0.75rem !important;
        }

        /* 12. Progress Bar */
        .stProgress > div > div > div > div {
            background: linear-gradient(90deg, #38bdf8 0%, #ffffff 100%) !important;
            border-radius: 9999px !important;
        }
    </style>
    """, unsafe_allow_html=True)

def get_asset_data_uri(relative_path):
    """Return a data URI for a bundled image asset."""
    asset_path = Path(__file__).parent / relative_path
    if not asset_path.exists():
        return ""

    encoded = base64.b64encode(asset_path.read_bytes()).decode("utf-8")
    return f"data:image/png;base64,{encoded}"

def apply_login_background():
    """Apply clean, elegant chalkboard theme matching PROJECT NOVELTY ANALYSER aesthetic."""
    css = f"""
    <style>
        /* 1. Immersive Full-Screen Blackboard Stage */
        html, body, [data-testid="stAppViewContainer"], .main {{
            width: 100vw !important;
            min-height: 100vh !important;
            height: auto !important;
            overflow-y: auto !important;
            overflow-x: hidden !important;
            margin: 0 !important;
            padding: 0 !important;
            background-color: #121010 !important;
            background: radial-gradient(circle at 50% 50%, #161414 0%, #100e0e 85%) !important;
        }}

        /* 2. Suppress Streamlit Header, Toolbars, and Decorations */
        header,
        [data-testid="stHeader"],
        [data-testid="stAppHeader"],
        .stAppHeader,
        [data-testid="stAppToolbar"],
        .stAppToolbar,
        [data-testid="stToolbar"],
        .stToolbar,
        [data-testid="stDecoration"],
        .stDecoration,
        [data-testid="stStatusWidget"],
        [data-testid="stSidebar"],
        footer {{
            display: none !important;
            height: 0 !important;
            min-height: 0 !important;
            max-height: 0 !important;
            padding: 0 !important;
            margin: 0 !important;
            opacity: 0 !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }}

        /* 3. Flush top boundary - Zero out top padding on all Streamlit containers */
        .stApp,
        [data-testid="stApp"],
        .stAppViewContainer,
        [data-testid="stAppViewContainer"],
        section.main,
        section.stMain,
        [data-testid="stMain"],
        .main,
        .main .block-container,
        [data-testid="stMainBlockContainer"],
        .stMainBlockContainer,
        [data-testid="stAppViewBlockContainer"],
        div[data-testid="stAppViewContainer"] > section,
        div[data-testid="stAppViewContainer"] > section > div {{
            padding-top: 0 !important;
            margin-top: 0 !important;
        }}

        .main .block-container,
        [data-testid="stMainBlockContainer"],
        .stMainBlockContainer {{
            max-width: 1060px !important;
            width: min(1060px, 95vw) !important;
            min-height: 100vh !important;
            margin: 0 auto !important;
            padding-top: 0 !important;
            padding-left: 1rem !important;
            padding-right: 1rem !important;
            padding-bottom: 2.5rem !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: flex-start !important;
            box-sizing: border-box !important;
        }}

        /* 4. Allow visible overflow so cords are NEVER clipped */
        [data-testid="column"],
        div[data-testid="stVerticalBlock"],
        div[data-testid="stHorizontalBlock"],
        div[data-testid="stElementContainer"],
        .element-container,
        .stMarkdown,
        [data-testid="stMainBlockContainer"],
        .stMainBlockContainer,
        .block-container,
        section.main,
        section.stMain,
        [data-testid="stMain"] {{
            overflow: visible !important;
        }}

        /* Completely suppress Streamlit's "Press Enter to submit form" tooltip */
        [data-testid="InputInstructions"],
        .stInputInstructions,
        div[class*="InputInstructions"],
        div:has(> [data-testid="InputInstructions"]),
        div:has(> .stInputInstructions) {{
            display: none !important;
            visibility: hidden !important;
            height: 0 !important;
            max-height: 0 !important;
            width: 0 !important;
            margin: 0 !important;
            padding: 0 !important;
            opacity: 0 !important;
            pointer-events: none !important;
            overflow: hidden !important;
        }}

        /* Horizontal column blocks */
        .main .block-container > div:has([data-testid="column"]) > [data-testid="stHorizontalBlock"],
        .main .block-container > [data-testid="stHorizontalBlock"] {{
            width: 100% !important;
            max-width: 1040px !important;
            margin: 0 auto !important;
            align-items: flex-start !important;
            justify-content: center !important;
            gap: 1.5rem !important;
            overflow: visible !important;
        }}

        /* TOP-LEFT: Hanging Bulbs Stage - Hang directly from top ceiling */
        .login-hanging-stage {{
            width: 100% !important;
            display: flex !important;
            align-items: flex-start !important;
            justify-content: center !important;
            margin-top: -35px !important;
            padding: 0 !important;
            overflow: visible !important;
        }}

        .login-hanging-img {{
            width: 100% !important;
            max-width: 350px !important;
            height: auto !important;
            display: block !important;
            margin: 0 auto !important;
            filter: drop-shadow(0 0 25px rgba(255, 255, 255, 0.12)) !important;
            user-select: none !important;
            pointer-events: none !important;
        }}

        /* TOP-RIGHT: Title & Login Form Stage */
        .login-brand-title {{
            width: 100% !important;
            max-width: 420px !important;
            margin: 2.2rem auto 1.5rem auto !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        .login-brand-hero-img {{
            width: 100% !important;
            max-width: 390px !important;
            height: auto !important;
            display: block !important;
            margin: 0 auto !important;
            filter: drop-shadow(0 6px 20px rgba(0, 0, 0, 0.8)) !important;
            user-select: none !important;
            pointer-events: none !important;
        }}

        [data-testid="stForm"] {{
            width: 100% !important;
            max-width: 400px !important;
            min-height: auto !important;
            margin: 0 auto !important;
            padding: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: flex-start !important;
            border: none !important;
            border-radius: 0 !important;
            box-shadow: none !important;
            background: transparent !important;
            box-sizing: border-box !important;
            position: relative !important;
            z-index: 5 !important;
        }}

        [data-testid="stForm"] > div:first-child {{
            width: 100% !important;
            max-width: 400px !important;
            margin: 0 auto !important;
            padding: 0 !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
        }}

        /* Card Container (White Border, Rounded 36px, Transparent Fill) */
        [data-testid="stForm"] [data-testid="stVerticalBlockBorderWrapper"] {{
            width: 100% !important;
            max-width: 380px !important;
            border: 2px solid rgba(255, 255, 255, 0.95) !important;
            border-radius: 36px !important;
            background: transparent !important;
            padding: 24px 20px !important;
            margin: 0 auto !important;
            box-shadow: none !important;
            box-sizing: border-box !important;
        }}

        [data-testid="stForm"] [data-testid="stVerticalBlockBorderWrapper"] > div {{
            border: none !important;
            background: transparent !important;
            display: flex !important;
            flex-direction: column !important;
            gap: 14px !important;
            padding: 0 !important;
        }}

        /* Pill Inputs: USERNAME & PASSWORD */
        [data-testid="stForm"] [data-testid="stTextInput"] {{
            width: 100% !important;
            height: 52px !important;
            margin: 0 !important;
            padding: 0 !important;
            background: transparent !important;
            border: none !important;
        }}

        [data-testid="stForm"] [data-testid="stTextInput"] label {{
            display: none !important;
        }}

        [data-testid="stForm"] [data-testid="stTextInput"] > div {{
            border: none !important;
            background: transparent !important;
            padding: 0 !important;
            box-shadow: none !important;
        }}

        [data-testid="stForm"] [data-testid="stTextInputRootElement"] {{
            width: 100% !important;
            height: 52px !important;
            min-height: 52px !important;
            max-height: 52px !important;
            border: 1.5px solid rgba(255, 255, 255, 0.45) !important;
            border-radius: 9999px !important;
            background: #464545 !important;
            padding: 0 1.5rem !important;
            box-sizing: border-box !important;
            box-shadow: none !important;
            outline: none !important;
            transition: all 0.2s ease !important;
            display: flex !important;
            align-items: center !important;
        }}

        [data-testid="stForm"] [data-testid="stTextInputRootElement"]:focus-within {{
            border-color: #ffffff !important;
            box-shadow: 0 0 14px rgba(255, 255, 255, 0.35) !important;
            background: #504f4f !important;
        }}

        [data-testid="stForm"] [data-testid="stTextInput"] input {{
            width: 100% !important;
            height: 100% !important;
            background: transparent !important;
            background-color: transparent !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-size: 0.95rem !important;
            font-weight: 400 !important;
            letter-spacing: 2px !important;
            border: none !important;
            outline: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            box-sizing: border-box !important;
        }}

        [data-testid="stForm"] [data-testid="stTextInput"] input::placeholder {{
            color: rgba(255, 255, 255, 0.8) !important;
            -webkit-text-fill-color: rgba(255, 255, 255, 0.8) !important;
            opacity: 1 !important;
            font-size: 0.95rem !important;
            letter-spacing: 2px !important;
            text-transform: uppercase !important;
            font-weight: 400 !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif !important;
        }}

        [data-testid="stForm"] [data-testid="stTextInput"] button {{
            background: transparent !important;
            border: none !important;
            color: rgba(255, 255, 255, 0.55) !important;
            padding-right: 0.5rem !important;
            box-shadow: none !important;
        }}

        [data-testid="stForm"] [data-testid="stTextInput"] button:hover {{
            color: #ffffff !important;
        }}

        /* Action: Centered Pure Text LOGIN Button */
        [data-testid="stForm"] [data-testid="stFormSubmitButton"] {{
            width: 100% !important;
            margin: 1.25rem auto 0 auto !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        [data-testid="stForm"] [data-testid="stFormSubmitButton"] > button {{
            width: auto !important;
            min-width: 160px !important;
            height: 48px !important;
            min-height: 48px !important;
            max-height: 48px !important;
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
            font-size: 1.35rem !important;
            font-weight: 300 !important;
            letter-spacing: 5px !important;
            text-transform: uppercase !important;
            cursor: pointer !important;
            transition: all 0.25s ease !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 !important;
            margin: 0 auto !important;
        }}

        [data-testid="stForm"] [data-testid="stFormSubmitButton"] > button:hover {{
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            text-shadow: 0 0 12px rgba(255, 255, 255, 0.7) !important;
            transform: scale(1.04) !important;
        }}

        [data-testid="stForm"] [data-testid="stFormSubmitButton"] > button:active {{
            transform: scale(0.98) !important;
        }}

        [data-testid="stForm"] [data-testid="stFormSubmitButton"] p {{
            margin: 0 !important;
            padding: 0 !important;
            color: inherit !important;
            -webkit-text-fill-color: inherit !important;
            font-family: inherit !important;
            font-size: inherit !important;
            font-weight: inherit !important;
            letter-spacing: inherit !important;
        }}

        /* Error Alert */
        [data-testid="stForm"] div[data-testid="stAlert"] {{
            width: min(380px, 92vw) !important;
            margin: 1.25rem auto 0 auto !important;
            background: rgba(185, 28, 28, 0.92) !important;
            color: #ffffff !important;
            font-size: 0.82rem !important;
            padding: 0.45rem 1rem !important;
            border-radius: 9999px !important;
            border: 1px solid rgba(254, 202, 202, 0.5) !important;
            box-shadow: 0 4px 16px rgba(0, 0, 0, 0.6) !important;
            text-align: center !important;
            backdrop-filter: blur(8px) !important;
        }}

        [data-testid="stForm"] div[data-testid="stAlert"] [data-testid="stMarkdownContainer"] p {{
            color: #ffffff !important;
            font-size: 0.82rem !important;
            line-height: 1.25 !important;
            margin: 0 !important;
            font-weight: 500 !important;
        }}

        [data-testid="stForm"] div[data-testid="stAlert"] svg {{
            width: 14px !important;
            height: 14px !important;
            fill: #ffffff !important;
        }}

        /* BOTTOM-LEFT: Demo Accounts Stage */
        .login-demo-stage {{
            width: 100% !important;
            max-width: 320px !important;
            margin: 0.5rem auto 0.5rem auto !important;
            display: flex !important;
            flex-direction: column !important;
            align-items: center !important;
            justify-content: center !important;
        }}

        .login-demo-badge-img {{
            width: 100% !important;
            max-width: 275px !important;
            height: auto !important;
            display: block !important;
            margin: 0 auto !important;
            user-select: none !important;
            pointer-events: none !important;
        }}

        /* STUDENT 1 and STUDENT 2 Buttons */
        .main .block-container .stButton > button {{
            width: 100% !important;
            height: 38px !important;
            min-height: 38px !important;
            max-height: 38px !important;
            background: #201e1e !important;
            background-color: #201e1e !important;
            border: 1.5px solid rgba(255, 255, 255, 0.65) !important;
            border-radius: 9999px !important;
            color: #ffffff !important;
            -webkit-text-fill-color: #ffffff !important;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif !important;
            font-size: 0.82rem !important;
            font-weight: 500 !important;
            letter-spacing: 1px !important;
            text-transform: uppercase !important;
            white-space: nowrap !important;
            box-shadow: none !important;
            transition: all 0.2s ease !important;
            cursor: pointer !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            padding: 0 0.5rem !important;
        }}

        .main .block-container .stButton > button p {{
            white-space: nowrap !important;
            overflow: visible !important;
            text-overflow: clip !important;
            margin: 0 !important;
            padding: 0 !important;
            font-size: 0.82rem !important;
            letter-spacing: 1px !important;
        }}

        .main .block-container .stButton > button:hover {{
            background: #2f2c2c !important;
            background-color: #2f2c2c !important;
            border-color: #ffffff !important;
            box-shadow: 0 0 12px rgba(255, 255, 255, 0.4) !important;
            transform: translateY(-1px) !important;
        }}

        .main .block-container .stButton > button:active {{
            transform: translateY(1px) !important;
        }}

        /* BOTTOM-RIGHT: Upright Bulb Stage */
        .login-upright-stage {{
            width: 100% !important;
            display: flex !important;
            align-items: flex-start !important;
            justify-content: center !important;
            margin-top: 0 !important;
            padding: 0 !important;
        }}

        .login-upright-img {{
            width: 100% !important;
            max-width: 240px !important;
            height: auto !important;
            display: block !important;
            margin: 0 auto !important;
            filter: drop-shadow(0 0 25px rgba(255, 255, 255, 0.12)) !important;
            user-select: none !important;
            pointer-events: none !important;
        }}

        /* Responsive */
        @media (max-width: 768px) {{
            .login-hanging-stage,
            .login-upright-stage {{
                display: none !important;
            }}
            .main .block-container {{
                max-width: 480px !important;
                padding-top: 1.5rem !important;
            }}
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# ============================================================================
# UI HELPER FUNCTIONS
# ============================================================================

def show_header(title, subtitle=""):
    """Display a styled header in the chalkboard aesthetic."""
    st.markdown(f"""
    <div style='margin-bottom: 1.5rem;'>
        <h1 style='color: #ffffff !important; margin: 0 0 0.4rem 0; border-bottom: none !important;'>{title}</h1>
        {f"<p style='color: #cbd5e1 !important; font-size: 1.05rem; margin: 0;'>{subtitle}</p>" if subtitle else ""}
        <div style='width: 100%; height: 1.5px; background: rgba(255, 255, 255, 0.4); margin-top: 0.75rem;'></div>
    </div>
    """, unsafe_allow_html=True)

def show_welcome_message(name):
    """Display the chalkboard hanging-bulbs hero header with centered welcome pill matching mockup."""
    display_name = name if name and name.strip() else "Name"
    uri_hero = get_asset_data_uri("assets/dashboard_header_hero.png")
    st.markdown(f"""
    <div class="dash-hero-wrapper">
        <div class="dash-hero-stage">
            <img src="{uri_hero}" class="dash-hero-img" alt="Dashboard Hanging Bulbs Banner" />
            <div class="dash-hero-overlay">
                <div class="dash-welcome-title">Welcome, {display_name}</div>
                <div class="dash-welcome-subtitle">Discover the novelty in your research projects</div>
            </div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def render_html(html_str):
    """Safely render HTML without accidental markdown indented code blocks."""
    st.markdown(textwrap.dedent(html_str).strip(), unsafe_allow_html=True)

def show_project_card(project):
    """Display a project card matching the chalkboard theme."""
    selected_novelty_html = ""
    if project.get("selected_novelty"):
        selected_novelty_html = f"""
        <p style='color: #4ade80; margin: 0.5rem 0 0 0; font-size: 0.9rem;'>
            <strong style='color: #4ade80;'>✓ Selected Novelty:</strong> {project['selected_novelty']}
        </p>
        """

    html = f"""
    <div class='project-card'>
        <div style='display: flex; justify-content: space-between; align-items: start;'>
            <div style='flex: 1; min-width: 0;'>
                <h3 style='margin: 0 0 0.5rem 0; color: #ffffff; word-break: break-word;'>{project['title']}</h3>
                <p style='color: #94a3b8; margin: 0 0 0.85rem 0; font-size: 0.95rem;'>{project['domain']}</p>
                <div style='display: flex; gap: 0.5rem; flex-wrap: wrap; margin-bottom: 0.85rem;'>
                    <span class='metric-badge'>{project['status'].upper()}</span>
                    <span class='metric-badge'>{project['created_date']}</span>
                    <span class='metric-badge'>Method: {project['method']}</span>
                </div>
                <p style='color: #cbd5e1; margin: 0; font-size: 0.9rem;'>
                    <strong style='color: #ffffff;'>Dataset:</strong> {project['dataset']}
                </p>
                {selected_novelty_html}
            </div>
        </div>
    </div>
    """
    render_html(html)

def show_info_box(message):
    """Display an info box."""
    st.markdown(f"""
    <div class='info-box'>
        <strong>ℹ️ Information:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def show_success_box(message):
    """Display a success box."""
    st.markdown(f"""
    <div class='success-box'>
        <strong>✓ Success:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def show_warning_box(message):
    """Display a warning box."""
    st.markdown(f"""
    <div class='warning-box'>
        <strong>⚠️ Warning:</strong><br>
        {message}
    </div>
    """, unsafe_allow_html=True)

def format_technologies(techs):
    """Format technologies as styled pill badges matching the theme."""
    html = '<div style="margin: 0.5rem 0 1rem 0; display: flex; flex-wrap: wrap; gap: 0.5rem;">'
    colors = {
        "Python": "#38bdf8",
        "TensorFlow": "#fb923c",
        "PyTorch": "#f87171",
        "Transformers": "#a78bfa",
        "Pandas": "#818cf8",
        "NumPy": "#38bdf8",
        "Keras": "#f43f5e",
        "Scikit-learn": "#f59e0b"
    }
    
    for tech in techs:
        color = colors.get(tech, "#94a3b8")
        html += f"""
        <span style='display: inline-block; background: rgba(255, 255, 255, 0.08); 
                     color: #ffffff; padding: 0.35rem 0.85rem; 
                     border-radius: 9999px; font-size: 0.85rem; font-weight: 500;
                     border: 1.5px solid {color}; box-shadow: 0 2px 6px rgba(0, 0, 0, 0.3);'>
            <span style='color: {color}; margin-right: 4px;'>&bull;</span> {tech}
        </span>
        """
    html += '</div>'
    return html

def format_similarity_percentage(percentage):
    """Format similarity percentage with color coding matching the dark theme."""
    if percentage >= 75:
        color = "#f87171"
        bg = "rgba(239, 68, 68, 0.15)"
        border = "rgba(239, 68, 68, 0.6)"
    elif percentage >= 60:
        color = "#fb923c"
        bg = "rgba(249, 115, 22, 0.15)"
        border = "rgba(249, 115, 22, 0.6)"
    else:
        color = "#4ade80"
        bg = "rgba(34, 197, 94, 0.15)"
        border = "rgba(34, 197, 94, 0.6)"
    
    return f"<span style='font-size: 1.25rem; font-weight: 700; color: {color}; padding: 0.2rem 0.75rem; border-radius: 9999px; background: {bg}; border: 1px solid {border};'>{percentage}%</span>"

def show_loading_animation(message="Loading..."):
    """Show a loading animation."""
    st.markdown(f"""
    <div style='text-align: center; padding: 2rem;'>
        <div style='font-size: 3rem; margin-bottom: 1rem;'>⏳</div>
        <h3>{message}</h3>
        <p style='color: #64748b;'>This may take a few moments...</p>
    </div>
    """, unsafe_allow_html=True)

# ============================================================================
# SESSION MANAGEMENT
# ============================================================================

def initialize_session():
    """Initialize session state variables."""
    if "logged_in" not in st.session_state:
        st.session_state.logged_in = False
    if "current_user" not in st.session_state:
        st.session_state.current_user = None
    if "current_page" not in st.session_state:
        st.session_state.current_page = "login"
    if "current_project" not in st.session_state:
        st.session_state.current_project = None
    if "project_form_data" not in st.session_state:
        st.session_state.project_form_data = {}
    if "analysis_results" not in st.session_state:
        st.session_state.analysis_results = None
    if "selected_novelty" not in st.session_state:
        st.session_state.selected_novelty = None
    if "saved_projects" not in st.session_state:
        st.session_state.saved_projects = []
    if "auth_backend_error" not in st.session_state:
        st.session_state.auth_backend_error = None

def set_authenticated_user(student_id, username, email, name):
    """Store authenticated user details in session state."""
    st.session_state.logged_in = True
    st.session_state.current_user = {
        "id": str(student_id),
        "username": username,
        "email": email,
        "name": name
    }

def authenticate_user_from_mysql(username, password):
    """Authenticate against the MySQL students table.

    Returns True for a valid login, False for invalid credentials, and None
    when MySQL is not reachable so the demo fallback can still run.
    """
    username = username.strip()
    st.session_state.auth_backend_error = None

    try:
        connection = pymysql.connect(**MYSQL_CONFIG)
        with connection.cursor() as cursor:
            cursor.execute(
                """
                SELECT student_id, username, email, name, password_hash
                FROM students
                WHERE LOWER(username) = LOWER(%s) OR LOWER(email) = LOWER(%s)
                LIMIT 1
                """,
                (username, username)
            )
            student = cursor.fetchone()
        connection.close()
    except pymysql.MySQLError as exc:
        st.session_state.auth_backend_error = str(exc)
        return None

    if not student or not check_password_hash(student["password_hash"], password):
        return False

    set_authenticated_user(
        student["student_id"],
        student["username"],
        student["email"],
        student["name"]
    )
    return True

def authenticate_user_from_samples(username, password):
    """Authenticate user with bundled demo credentials."""
    username = username.strip().casefold()
    for student_id, student_data in SAMPLE_STUDENTS.items():
        if username in (student_data["username"].casefold(), student_data["email"].casefold()) \
           and student_data["password"] == password:
            set_authenticated_user(
                student_id,
                student_data["username"],
                student_data["email"],
                student_data["name"]
            )
            return True
    return False

def authenticate_user(username, password):
    """Authenticate user from MySQL first, then demo data if MySQL is unavailable."""
    mysql_result = authenticate_user_from_mysql(username, password)
    if mysql_result is not None:
        return mysql_result

    return authenticate_user_from_samples(username, password)

def logout():
    """Clear session and logout user."""
    st.session_state.logged_in = False
    st.session_state.current_user = None
    st.session_state.current_page = "login"
    st.session_state.current_project = None
    st.session_state.project_form_data = {}
    st.session_state.analysis_results = None
    st.session_state.selected_novelty = None

# ============================================================================
# PAGE FUNCTIONS
# ============================================================================

def show_login_page():
    """Display the clean chalkboard login page matching the exact user mockup."""
    apply_login_background()
    
    uri_hanging_bulbs = get_asset_data_uri("assets/login_hanging_bulbs.png")
    uri_title = get_asset_data_uri("assets/project_novelty_title_perfect.png")
    uri_demo_badge = get_asset_data_uri("assets/login_demo_badge.png")
    uri_upright_bulb = get_asset_data_uri("assets/login_upright_bulb.png")
    
    # ROW 1 (UPPER): Hanging bulbs on Left, Title & Login Form on Right
    col_top_left, col_top_right = st.columns([1.1, 1.15], gap="large")
    
    with col_top_left:
        st.markdown(f"""
        <div class="login-hanging-stage">
            <img src="{uri_hanging_bulbs}" class="login-hanging-img" alt="Hanging Bulbs" />
        </div>
        """, unsafe_allow_html=True)
        
    with col_top_right:
        with st.form("login_form"):
            st.markdown(f"""
            <div class="login-brand-title">
                <img src="{uri_title}" class="login-brand-hero-img" alt="PROJECT NOVELTY [ ANALYSER ]" />
            </div>
            """, unsafe_allow_html=True)
            
            with st.container(border=True):
                username = st.text_input(
                    "USERNAME",
                    key="login_username",
                    placeholder="USERNAME",
                    label_visibility="collapsed",
                )
                
                password = st.text_input(
                    "PASSWORD",
                    key="login_password",
                    type="password",
                    placeholder="PASSWORD",
                    label_visibility="collapsed",
                )
            
            submitted = st.form_submit_button("LOGIN", use_container_width=True)
            
            if submitted:
                if not username.strip() or not password:
                    st.error("❌ Please enter both username and password")
                elif authenticate_user(username, password):
                    st.success("✓ Login successful! Redirecting...")
                    st.session_state.current_page = "dashboard"
                    time.sleep(0.5)
                    st.rerun()
                else:
                    st.error("❌ Invalid username or password")
                    if st.session_state.auth_backend_error:
                        st.warning(
                            "MySQL login is unavailable, so only bundled demo credentials "
                            "can be used right now. Check MySQL configuration."
                        )
                        
    # ROW 2 (LOWER): Demo Accounts on Left, Upright Bulb on Right
    col_bot_left, col_bot_right = st.columns([1.1, 1.15], gap="large")
    
    with col_bot_left:
        st.markdown(f"""
        <div class="login-demo-stage">
            <img src="{uri_demo_badge}" class="login-demo-badge-img" alt="Demo Accounts" />
        </div>
        """, unsafe_allow_html=True)
        
        # Center the two student pill buttons underneath the badge
        _, col_btn_center, _ = st.columns([0.08, 0.84, 0.08])
        with col_btn_center:
            col_s1, col_s2 = st.columns(2, gap="small")
            with col_s1:
                if st.button("STUDENT 1", key="quick_login_student1", use_container_width=True):
                    if authenticate_user("john@university.edu", "password123"):
                        st.session_state.current_page = "dashboard"
                        st.rerun()
            with col_s2:
                if st.button("STUDENT 2", key="quick_login_student2", use_container_width=True):
                    if authenticate_user("jane_smith", "password123"):
                        st.session_state.current_page = "dashboard"
                        st.rerun()
                        
    with col_bot_right:
        st.markdown(f"""
        <div class="login-upright-stage">
            <img src="{uri_upright_bulb}" class="login-upright-img" alt="Lightbulb" />
        </div>
        """, unsafe_allow_html=True)

def show_dashboard():
    """Display the student dashboard matching the chalkboard pill mockup."""
    apply_custom_css()
    
    user = st.session_state.current_user
    user_name = user["name"] if user else "Name"
    
    # 1. Top Welcome Pill Capsule (Exact mockup match)
    show_welcome_message(user_name)
    
    user_projects = [p for p in SAMPLE_PROJECTS if p["student_id"] == user["id"]] if user else []
    saved_projects = len([p for p in user_projects if p["status"] == "saved"])
    analyzed_projects = len([p for p in user_projects if p["status"] == "analyzed"])
    
    # 2. Three Stat Pills (Exact mockup match: Total Projects, Completed, Analyzed)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"""
        <div class="dash-stat-pill" title="Total Projects: {len(user_projects)}">
            <span>Total Projects</span>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown(f"""
        <div class="dash-stat-pill" title="Completed: {saved_projects}">
            <span>Completed</span>
        </div>
        """, unsafe_allow_html=True)
    with col3:
        st.markdown(f"""
        <div class="dash-stat-pill" title="Analyzed: {analyzed_projects}">
            <span>Analyzed</span>
        </div>
        """, unsafe_allow_html=True)
    
    # Action handlers container (visually hidden via CSS to match mockup exactly)
    with st.container(key="dashboard_quick_actions"):
        if st.button("✨ Create New Project", key="create_project"):
            st.session_state.project_form_data = {}
            st.session_state.current_project = None
            st.session_state.current_page = "project_submission"
            st.rerun()
        if st.button("📋 My Projects", key="view_projects"):
            st.session_state.current_page = "my_projects"
            st.rerun()
    
    # 3. Section Title & Full-Width Divider Line (Exact mockup match)
    st.markdown('<div class="dash-section-header">Recent Projects</div>', unsafe_allow_html=True)
    st.markdown('<div class="dash-section-divider"></div>', unsafe_allow_html=True)
    
    if user_projects:
        for project in sorted(user_projects, key=lambda x: x["created_date"], reverse=True)[:3]:
            show_project_card(project)
            if st.button("View Full Details", key=f"recent_details_{project['id']}"):
                st.session_state.current_project = project
                st.session_state.current_page = "project_details"
                st.rerun()
    else:
        st.markdown("""
        <div class="card" style="text-align: center; color: #cbd5e1; padding: 2rem;">
            No projects yet. Click <strong>Create New Project</strong> to get started!
        </div>
        """, unsafe_allow_html=True)

def show_project_submission():
    """Display the project submission form."""
    apply_custom_css()
    
    show_header("Create New Project", "Submit your research project for novelty analysis")
    
    show_info_box(
        "Provide detailed information about your research project. "
        "This will be analyzed to identify its novelty and suggest improvements."
    )
    
    with st.form("project_form"):
        title = st.text_input(
            "Project Title *",
            value=st.session_state.project_form_data.get("title", ""),
            placeholder="e.g., AI-Powered Disease Detection System"
        )
        
        problem_statement = st.text_area(
            "Problem Statement *",
            value=st.session_state.project_form_data.get("problem_statement", ""),
            placeholder="Describe the problem your project solves...",
            height=100
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            domain = st.selectbox(
                "Domain *",
                options=[
                    "Natural Language Processing",
                    "Computer Vision",
                    "Medical AI",
                    "Time Series Analysis",
                    "Recommendation Systems",
                    "Reinforcement Learning",
                    "Graph Neural Networks",
                    "Other"
                ],
                index=0
            )
        
        with col2:
            dataset = st.text_input(
                "Dataset *",
                value=st.session_state.project_form_data.get("dataset", ""),
                placeholder="e.g., ImageNet, MNIST, Custom Dataset"
            )
        
        method = st.text_input(
            "Method/Algorithm *",
            value=st.session_state.project_form_data.get("method", ""),
            placeholder="e.g., CNN, BERT, Transformer, Federated Learning"
        )
        
        technologies_input = st.text_area(
            "Technologies Used *",
            value=st.session_state.project_form_data.get("technologies", ""),
            placeholder="e.g., Python, TensorFlow, PyTorch, Pandas (comma-separated)",
            height=80
        )
        
        st.markdown("### Additional Details (Optional)")
        
        additional_info = st.text_area(
            "Additional Information",
            value=st.session_state.project_form_data.get("additional_info", ""),
            placeholder="Any other relevant information about your project...",
            height=80
        )
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col1:
            if st.form_submit_button("← Back", use_container_width=True):
                st.session_state.current_page = "dashboard"
                st.rerun()
        
        with col3:
            submitted = st.form_submit_button("Analyze Project →", use_container_width=True, type="primary")
            
            if submitted:
                if not all([title, problem_statement, domain, dataset, method, technologies_input]):
                    st.error("❌ Please fill in all required fields (marked with *)")
                else:
                    st.session_state.project_form_data = {
                        "title": title,
                        "problem_statement": problem_statement,
                        "domain": domain,
                        "dataset": dataset,
                        "method": method,
                        "technologies": [t.strip() for t in technologies_input.split(",")],
                        "additional_info": additional_info
                    }
                    
                    st.session_state.current_page = "analysis"
                    st.rerun()

def show_analysis_page():
    """Display the analysis page with loading animation."""
    apply_custom_css()
    
    show_header("Analyzing Your Project", "Please wait while we process your submission")
    
    show_loading_animation("Analyzing your project...")
    
    progress_bar = st.progress(0)
    status_text = st.empty()
    
    steps = [
        ("Extracting project features...", 0.2),
        ("Comparing with existing projects...", 0.4),
        ("Identifying similar methodologies...", 0.6),
        ("Analyzing technology stack...", 0.8),
        ("Generating novelty suggestions...", 0.95),
        ("Finalizing results...", 1.0)
    ]
    
    for step_text, progress in steps:
        status_text.info(step_text)
        progress_bar.progress(progress)
        time.sleep(0.5)
    
    analysis_results = {
        "similar_projects": SAMPLE_SIMILAR_PROJECTS,
        "common_technologies": COMMON_TECHNOLOGIES,
        "common_datasets": COMMON_DATASETS,
        "common_methods": COMMON_METHODS,
        "novelty_ideas": NOVELTY_IDEAS,
        "existing_limitations": EXISTING_LIMITATIONS,
        "possible_gaps": POSSIBLE_GAPS
    }
    
    st.session_state.analysis_results = analysis_results
    
    progress_bar.empty()
    status_text.empty()
    
    st.markdown("""
    <div class='success-box'>
        <strong>✓ Analysis Complete!</strong><br>
        Your project has been analyzed. Redirecting to results page...
    </div>
    """, unsafe_allow_html=True)
    
    time.sleep(1)
    
    st.session_state.current_page = "novelty_results"
    st.rerun()

def show_novelty_results():
    """Display the novelty analysis results."""
    apply_custom_css()
    
    show_header("Novelty Analysis Results", "Review your project analysis and suggested improvements")
    
    project_data = st.session_state.project_form_data
    analysis_results = st.session_state.analysis_results
    
    if st.button("← Back"):
        st.session_state.current_page = "dashboard"
        st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Project Details",
        "Similar Projects",
        "Novelty Ideas",
        "Limitations & Gaps",
        "Technology Analysis"
    ])
    
    with tab1:
        st.markdown("### Your Project")
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_html(f"""
            <div class='card'>
                <h4 style='margin-top: 0; color: #ffffff; word-break: break-word;'>{project_data['title']}</h4>
                <p style='color: #cbd5e1; margin: 0.5rem 0;'><strong style='color: #ffffff;'>Domain:</strong> {project_data['domain']}</p>
                <p style='color: #cbd5e1; margin: 0.5rem 0;'><strong style='color: #ffffff;'>Method:</strong> {project_data['method']}</p>
                <p style='color: #cbd5e1; margin: 0.5rem 0;'><strong style='color: #ffffff;'>Dataset:</strong> {project_data['dataset']}</p>
            </div>
            """)
        
        with col2:
            render_html("""
            <div class='card'>
                <h4 style='margin-top: 0; color: #ffffff;'>Technologies</h4>
            </div>
            """)
            st.markdown(format_technologies(project_data['technologies']), unsafe_allow_html=True)
        
        st.markdown("#### Problem Statement")
        render_html(f"""
        <div class='card'>
            <p style='color: #cbd5e1; line-height: 1.6; margin: 0; word-break: break-word;'>
                {project_data['problem_statement']}
            </p>
        </div>
        """)
        
        if project_data.get('additional_info'):
            st.markdown("#### Additional Information")
            render_html(f"""
            <div class='card'>
                <p style='color: #cbd5e1; line-height: 1.6; margin: 0; word-break: break-word;'>
                    {project_data['additional_info']}
                </p>
            </div>
            """)
    
    with tab2:
        st.markdown("### Similar Existing Projects")
        show_info_box(
            "These are existing projects that share similar characteristics with yours. "
            "The similarity percentage indicates how closely they align with your project."
        )
        
        similar_projects = analysis_results['similar_projects']
        
        if similar_projects:
            for idx, project in enumerate(similar_projects, 1):
                with st.container():
                    render_html(f"""
                    <div class='card'>
                        <div style='display: flex; justify-content: space-between; align-items: start; margin-bottom: 1rem;'>
                            <div style='flex: 1; min-width: 0;'>
                                <h4 style='margin: 0 0 0.5rem 0; color: #ffffff; word-break: break-word;'>{project['title']}</h4>
                                <p style='color: #94a3b8; margin: 0; font-size: 0.9rem;'>
                                    {project['authors']} ({project['year']})
                                </p>
                            </div>
                            <div style='text-align: right; margin-left: 1rem;'>
                                <div style='margin-bottom: 0.5rem; color: #94a3b8; font-size: 0.85rem;'>Similarity</div>
                                {format_similarity_percentage(project['similarity'])}
                            </div>
                        </div>
                        <div style='background: rgba(255, 255, 255, 0.04); padding: 1rem; border-radius: 12px; border: 1px solid rgba(255, 255, 255, 0.1);'>
                            <p style='margin: 0.5rem 0; color: #cbd5e1; font-size: 0.9rem;'>
                                <strong style='color: #ffffff;'>Domain:</strong> {project['domain']}<br>
                                <strong style='color: #ffffff;'>Method:</strong> {project['method']}<br>
                            </p>
                            <div style='margin-top: 1rem;'>
                                <strong style='color: #cbd5e1; font-size: 0.9rem;'>Technologies:</strong><br>
                            </div>
                        </div>
                    </div>
                    """)
                    st.markdown(format_technologies(project['technologies']), unsafe_allow_html=True)
    
    with tab3:
        st.markdown("### Suggested Novelty Ideas")
        show_info_box(
            "These suggestions are ways to add novelty and innovation to your project. "
            "Select one to proceed with your project submission."
        )
        
        novelty_ideas = analysis_results['novelty_ideas']
        
        for novelty in novelty_ideas:
            with st.container():
                col1, col2 = st.columns([4, 1])
                
                with col1:
                    render_html(f"""
                    <div class='card'>
                        <h4 style='margin: 0 0 0.5rem 0; color: #ffffff; word-break: break-word;'>{novelty['title']}</h4>
                        <p style='color: #cbd5e1; margin: 0.5rem 0; font-size: 0.95rem; line-height: 1.6; word-break: break-word;'>
                            {novelty['description']}
                        </p>
                        <div style='margin-top: 1rem;'>
                            <span class='metric-badge'>Impact: {novelty['impact']}</span>
                            <span class='metric-badge'>Feasibility: {novelty['feasibility']}</span>
                        </div>
                        <p style='color: #94a3b8; margin: 1rem 0 0 0; font-size: 0.9rem;'>
                            <strong style='color: #ffffff;'>Details:</strong> {novelty['details']}
                        </p>
                    </div>
                    """)
                
                with col2:
                    if st.button("Select", key=f"select_{novelty['id']}", use_container_width=True):
                        st.session_state.selected_novelty = novelty
                        st.session_state.current_page = "select_novelty"
                        st.rerun()
    
    with tab4:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Existing Limitations")
            st.markdown("Common limitations found in similar projects:")
            for limitation in analysis_results['existing_limitations']:
                st.markdown(f"• {limitation}")
        
        with col2:
            st.markdown("### Possible Gaps")
            st.markdown("Opportunities for innovation in this field:")
            for gap in analysis_results['possible_gaps']:
                st.markdown(f"• {gap}")
    
    with tab5:
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Common Technologies")
            st.markdown("Frequently used technologies in your domain:")
            for tech in analysis_results['common_technologies']:
                st.markdown(f"**{tech['name']}** - {tech['usage_percent']}% usage")
        
        with col2:
            st.markdown("### Common Methods")
            st.markdown("Popular methods and algorithms in your domain:")
            for method in analysis_results['common_methods']:
                st.markdown(f"**{method['name']}** - {method['usage_percent']}% usage")
        
        st.markdown("### Common Datasets")
        st.markdown("Widely used datasets in your domain:")
        for dataset in analysis_results['common_datasets']:
            st.markdown(f"**{dataset['name']}** - {dataset['usage_percent']}% usage")

def show_select_novelty():
    """Display the select and save novelty page."""
    apply_custom_css()
    
    show_header("Review & Save Your Project", "Confirm your project with the selected novelty idea")
    
    project_data = st.session_state.project_form_data
    selected_novelty = st.session_state.selected_novelty
    
    if st.button("← Back to Results"):
        st.session_state.current_page = "novelty_results"
        st.rerun()
    
    st.markdown("---")
    
    show_info_box(
        "Review your project and the selected novelty idea below. "
        "Once saved, you'll be able to view this project in your project list."
    )
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### 📋 Original Project")
        
        render_html(f"""
        <div class='card'>
            <h4 style='margin-top: 0; color: #ffffff; word-break: break-word;'>{project_data['title']}</h4>
            
            <div style='background: rgba(255, 255, 255, 0.04); padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);'>
                <p style='margin: 0; color: #94a3b8;'><strong>Domain:</strong></p>
                <p style='margin: 0.25rem 0 1rem 0; color: #ffffff;'>{project_data['domain']}</p>
                
                <p style='margin: 0; color: #94a3b8;'><strong>Method/Algorithm:</strong></p>
                <p style='margin: 0.25rem 0 1rem 0; color: #ffffff;'>{project_data['method']}</p>
                
                <p style='margin: 0; color: #94a3b8;'><strong>Dataset:</strong></p>
                <p style='margin: 0.25rem 0; color: #ffffff;'>{project_data['dataset']}</p>
            </div>
            
            <p style='margin: 1rem 0 0.5rem 0; color: #cbd5e1;'><strong>Technologies:</strong></p>
        </div>
        """)
        
        st.markdown(format_technologies(project_data['technologies']), unsafe_allow_html=True)
        
        render_html(f"""
        <div class='card' style='margin-top: 1rem;'>
            <p style='margin: 0; color: #94a3b8;'><strong>Problem Statement:</strong></p>
            <p style='margin: 0.5rem 0; color: #cbd5e1; line-height: 1.6; word-break: break-word;'>
                {project_data['problem_statement']}
            </p>
        </div>
        """)
    
    with col2:
        st.markdown("### ✨ Selected Novelty Idea")
        
        render_html(f"""
        <div class='card' style='border-left: 4px solid #4ade80;'>
            <h4 style='margin-top: 0; color: #4ade80; word-break: break-word;'>{selected_novelty['title']}</h4>
            
            <p style='margin: 1rem 0; color: #cbd5e1; line-height: 1.6; word-break: break-word;'>
                {selected_novelty['description']}
            </p>
            
            <div style='background: rgba(255, 255, 255, 0.04); padding: 1rem; border-radius: 12px; margin: 1rem 0; border: 1px solid rgba(255, 255, 255, 0.1);'>
                <p style='margin: 0; color: #94a3b8;'><strong>Implementation Details:</strong></p>
                <p style='margin: 0.5rem 0; color: #ffffff; word-break: break-word;'>{selected_novelty['details']}</p>
            </div>
            
            <div style='display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem; margin: 1rem 0 0 0;'>
                <div style='background: rgba(74, 222, 128, 0.12); border: 1px solid rgba(74, 222, 128, 0.4); padding: 0.75rem; border-radius: 9999px; text-align: center;'>
                    <p style='margin: 0; color: #4ade80; font-size: 0.85rem;'>Impact</p>
                    <p style='margin: 0.25rem 0 0 0; color: #ffffff; font-weight: 600;'>{selected_novelty['impact']}</p>
                </div>
                <div style='background: rgba(56, 189, 248, 0.12); border: 1px solid rgba(56, 189, 248, 0.4); padding: 0.75rem; border-radius: 9999px; text-align: center;'>
                    <p style='margin: 0; color: #38bdf8; font-size: 0.85rem;'>Feasibility</p>
                    <p style='margin: 0.25rem 0 0 0; color: #ffffff; font-weight: 600;'>{selected_novelty['feasibility']}</p>
                </div>
            </div>
        </div>
        """)
    
    st.markdown("---")
    
    st.markdown("### Finalize Submission")
    
    notes = st.text_area(
        "Additional Notes (Optional)",
        placeholder="Add any additional notes or comments about your project and the selected novelty...",
        height=80
    )
    
    if st.button("💾 Save Project", use_container_width=True, type="primary"):
        final_project = {
            "title": project_data["title"],
            "problem_statement": project_data["problem_statement"],
            "domain": project_data["domain"],
            "dataset": project_data["dataset"],
            "method": project_data["method"],
            "technologies": project_data["technologies"],
            "selected_novelty": selected_novelty["title"],
            "novelty_id": selected_novelty["id"],
            "notes": notes,
            "status": "saved"
        }
        
        st.session_state.saved_projects.append(final_project)
        
        show_success_box(
            f"✓ Project '{project_data['title']}' has been saved successfully! "
            "Redirecting to your projects list..."
        )
        
        st.session_state.project_form_data = {}
        st.session_state.selected_novelty = None
        st.session_state.analysis_results = None
        
        time.sleep(2)
        
        st.session_state.current_page = "my_projects"
        st.rerun()

def show_my_projects():
    """Display all projects submitted by the student."""
    apply_custom_css()
    
    show_header("My Projects", "View all your submitted projects")
    
    user = st.session_state.current_user
    
    if st.button("← Dashboard"):
        st.session_state.current_page = "dashboard"
        st.rerun()
    
    st.markdown("---")
    
    user_projects = [p for p in SAMPLE_PROJECTS if p["student_id"] == user["id"]]
    
    if st.session_state.saved_projects:
        for saved_proj in st.session_state.saved_projects:
            user_projects.append({
                "id": f"proj_{len(user_projects) + 1:03d}",
                "student_id": user["id"],
                "title": saved_proj["title"],
                "problem_statement": saved_proj["problem_statement"],
                "domain": saved_proj["domain"],
                "dataset": saved_proj["dataset"],
                "method": saved_proj["method"],
                "technologies": saved_proj["technologies"],
                "selected_novelty": saved_proj["selected_novelty"],
                "status": saved_proj["status"],
                "created_date": "Today",
                "notes": saved_proj.get("notes", "")
            })
    
    if not user_projects:
        st.info("👋 You haven't submitted any projects yet. Create your first project!")
        
        if st.button("✨ Create New Project", use_container_width=True):
            st.session_state.project_form_data = {}
            st.session_state.current_page = "project_submission"
            st.rerun()
    else:
        col1, col2 = st.columns([2, 1])
        
        with col1:
            show_info_box(f"You have {len(user_projects)} project(s)")
        
        with col2:
            status_filter = st.selectbox(
                "Filter by Status",
                options=["All", "Saved", "Analyzed"],
                key="status_filter"
            )
        
        if status_filter != "All":
            filtered_projects = [p for p in user_projects if p["status"] == status_filter.lower()]
        else:
            filtered_projects = user_projects
        
        for project in sorted(filtered_projects, key=lambda x: x["created_date"], reverse=True):
            show_project_card(project)
            if st.button("View Full Details", key=f"details_{project['id']}", use_container_width=False):
                st.session_state.current_project = project
                st.session_state.current_page = "project_details"
                st.rerun()
        
        st.markdown("---")
        
        if st.button("✨ Create New Project", use_container_width=True):
            st.session_state.project_form_data = {}
            st.session_state.current_page = "project_submission"
            st.rerun()

def show_project_details():
    """Display complete project information."""
    apply_custom_css()
    
    project = st.session_state.current_project
    
    show_header(project["title"], f"Submitted for {project['domain']}")
    
    if st.button("← My Projects"):
        st.session_state.current_page = "my_projects"
        st.rerun()
    
    st.markdown("---")
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "Project Info",
        "Novelty Suggestion",
        "Similiar Projects",
        "Analysed Summary"
    ])
    
    with tab1:
        st.markdown("### Project Information")
        
        col1, col2 = st.columns(2)
        
        with col1:
            render_html(f"""
            <div class='card'>
                <p style='margin: 0; color: #94a3b8; font-size: 0.9rem;'><strong>Domain</strong></p>
                <p style='margin: 0.5rem 0; color: #ffffff; font-weight: 600;'>{project['domain']}</p>
                
                <p style='margin: 1rem 0 0 0; color: #94a3b8; font-size: 0.9rem;'><strong>Method/Algorithm</strong></p>
                <p style='margin: 0.5rem 0; color: #ffffff; font-weight: 600;'>{project['method']}</p>
                
                <p style='margin: 1rem 0 0 0; color: #94a3b8; font-size: 0.9rem;'><strong>Dataset</strong></p>
                <p style='margin: 0.5rem 0; color: #ffffff; font-weight: 600;'>{project['dataset']}</p>
            </div>
            """)
        
        with col2:
            render_html(f"""
            <div class='card'>
                <p style='margin: 0; color: #94a3b8; font-size: 0.9rem;'><strong>Status</strong></p>
                <p style='margin: 0.5rem 0; color: #38bdf8; font-weight: 600;'>{project['status'].upper()}</p>
                
                <p style='margin: 1rem 0 0 0; color: #94a3b8; font-size: 0.9rem;'><strong>Submitted</strong></p>
                <p style='margin: 0.5rem 0; color: #ffffff; font-weight: 600;'>{project['created_date']}</p>
            </div>
            """)
        
        st.markdown("#### Technologies Used")
        st.markdown(format_technologies(project['technologies']), unsafe_allow_html=True)
        
        st.markdown("#### Problem Statement")
        render_html(f"""
        <div class='card'>
            <p style='color: #cbd5e1; line-height: 1.6; margin: 0; word-break: break-word;'>
                {project['problem_statement']}
            </p>
        </div>
        """)
    
    with tab2:
        if project.get('selected_novelty'):
            st.markdown("### Selected Novelty Idea")
            render_html(f"""
            <div class='card' style='border-left: 4px solid #4ade80;'>
                <h4 style='margin-top: 0; color: #4ade80; word-break: break-word;'>{project['selected_novelty']}</h4>
                <p style='color: #cbd5e1; margin: 1rem 0; line-height: 1.6; word-break: break-word;'>
                    This novelty suggestion was selected to enhance your research project.
                </p>
            </div>
            """)
            
            if project.get('notes'):
                st.markdown("#### Your Notes")
                render_html(f"""
                <div class='card'>
                    <p style='color: #cbd5e1; line-height: 1.6; margin: 0; word-break: break-word;'>
                        {project['notes']}
                    </p>
                </div>
                """)
        else:
            st.info("No novelty idea selected for this project yet.")
    
    with tab3:
        st.markdown("### Similar Existing Projects")
        
        similar_projects = [
            {
                "title": "Deep Learning for Feature Analysis",
                "authors": "Smith et al.",
                "year": 2023,
                "similarity": 75
            },
            {
                "title": "Advanced Neural Network Architectures",
                "authors": "Johnson & Lee",
                "year": 2023,
                "similarity": 68
            },
            {
                "title": "Optimization Techniques for ML Models",
                "authors": "Chen et al.",
                "year": 2024,
                "similarity": 62
            }
        ]
        
        for proj in similar_projects:
            render_html(f"""
            <div class='card'>
                <div style='display: flex; justify-content: space-between; align-items: start;'>
                    <div style='flex: 1; min-width: 0;'>
                        <h4 style='margin: 0 0 0.5rem 0; color: #ffffff; word-break: break-word;'>{proj['title']}</h4>
                        <p style='color: #94a3b8; margin: 0; font-size: 0.9rem;'>
                            {proj['authors']} ({proj['year']})
                        </p>
                    </div>
                    <div style='text-align: right; margin-left: 1rem;'>
                        <div style='color: #94a3b8; font-size: 0.85rem; margin-bottom: 0.35rem;'>Similarity</div>
                        {format_similarity_percentage(proj['similarity'])}
                    </div>
                </div>
            </div>
            """)
    
    with tab4:
        st.markdown("### Analysis Summary")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Key Findings")
            st.markdown("""
            - Project addresses a relevant research problem
            - Comparable methodologies found in recent literature
            - Selected technologies are industry-standard
            - Novelty opportunity identified in implementation approach
            """)
        
        with col2:
            st.markdown("#### Recommendations")
            st.markdown("""
            1. Implement the selected novelty idea
            2. Review similar projects for best practices
            3. Consider adding explainability features
            4. Plan for comprehensive testing
            """)

# ============================================================================
# MAIN APPLICATION
# ============================================================================

def main():
    """Main application entry point."""
    initialize_session()
    apply_custom_css()

    # Explicit navigation prevents helper modules in pages/ being run as scripts.
    st.navigation(
        [st.Page(show_current_page, title="Project Novelty Detector", default=True)],
        position="hidden",
    ).run()


def show_navigation():
    """Keep sidebar actions within the application's session-based router."""
    if not st.session_state.logged_in:
        return
    def navigate(page):
        if page == "project_submission":
            st.session_state.project_form_data = {}
            st.session_state.current_project = None
        st.session_state.current_page = page

    with st.sidebar:
        st.markdown('<div class="sidebar-brand-pill">Project Novelty Detector</div>', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)
        user_name = st.session_state.current_user["name"] if st.session_state.current_user else "Name"
        st.markdown(f'<div class="sidebar-user-name">{user_name}</div>', unsafe_allow_html=True)
        for label, page in (
            ("Dashboard", "dashboard"),
            ("My Projects", "my_projects"),
            ("Create New Project", "project_submission"),
        ):
            st.button(label, key=f"nav_{page}", use_container_width=True,
                      on_click=navigate, args=(page,))
        st.button("Logout", key="nav_logout", use_container_width=True,
                  on_click=logout)


def show_current_page():
    """Render the requested view through the authenticated application router."""
    show_navigation()
    
    # Route to appropriate page based on session state
    current_page = st.session_state.current_page
    
    if not st.session_state.logged_in:
        show_login_page()
    elif current_page == "dashboard":
        show_dashboard()
    elif current_page == "project_submission":
        show_project_submission()
    elif current_page == "analysis":
        show_analysis_page()
    elif current_page == "novelty_results":
        show_novelty_results()
    elif current_page == "select_novelty":
        show_select_novelty()
    elif current_page == "my_projects":
        show_my_projects()
    elif current_page == "project_details":
        show_project_details()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
