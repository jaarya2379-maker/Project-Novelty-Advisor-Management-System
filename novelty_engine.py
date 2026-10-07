"""
Novelty Analysis Engine - Core Intelligence Module

This module performs complete novelty analysis for research projects:
1. Project attribute extraction
2. Similarity analysis with previous projects
3. Common/overused component detection
4. Limitation analysis
5. Gap/improvement identification
6. Novelty suggestion generation

Main function: analyze_project(project_data, previous_projects)
"""

import json
import re
from collections import Counter
from typing import Dict, List, Tuple, Any
from dataclasses import dataclass, asdict
from datetime import datetime


@dataclass
class AnalysisResult:
    """Result object for project analysis."""
    project_title: str
    similar_projects: List[Dict]
    common_technologies: List[Dict]
    common_datasets: List[Dict]
    common_methods: List[Dict]
    existing_limitations: List[str]
    possible_gaps: List[str]
    novelty_suggestions: List[Dict]
    timestamp: str


class ProjectAttributeExtractor:
    """Extract and normalize project attributes."""
    
    def __init__(self):
        """Initialize the extractor with common domains and keywords."""
        self.common_domains = [
            "Natural Language Processing",
            "Computer Vision",
            "Medical AI",
            "Time Series Analysis",
            "Recommendation Systems",
            "Reinforcement Learning",
            "Graph Neural Networks",
            "Cybersecurity",
            "IoT",
            "Blockchain",
            "Other"
        ]
        
        self.tech_categories = {
            "ML Frameworks": ["TensorFlow", "PyTorch", "Keras", "Scikit-learn", "XGBoost"],
            "Languages": ["Python", "Java", "C++", "R", "JavaScript"],
            "Data Processing": ["Pandas", "NumPy", "Spark", "Hadoop"],
            "NLP Tools": ["NLTK", "SpaCy", "Transformers", "BERT", "GPT"],
            "CV Tools": ["OpenCV", "PIL", "YOLOv8", "ResNet"],
            "Databases": ["MySQL", "PostgreSQL", "MongoDB", "Cassandra"],
            "Cloud": ["AWS", "Google Cloud", "Azure", "Heroku"]
        }
    
    def extract_keywords(self, text: str) -> List[str]:
        """Extract keywords from text using simple tokenization."""
        # Remove special characters and convert to lowercase
        text = re.sub(r'[^a-zA-Z0-9\s\-]', '', text.lower())
        words = text.split()
        
        # Filter out common stop words
        stop_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 
                     'of', 'is', 'are', 'was', 'were', 'been', 'be', 'have', 'has', 'had',
                     'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might',
                     'can', 'must', 'this', 'that', 'these', 'those', 'i', 'you', 'he', 'she',
                     'it', 'we', 'they', 'what', 'which', 'who', 'when', 'where', 'why', 'how'}
        
        keywords = [w for w in words if len(w) > 2 and w not in stop_words]
        return keywords
    
    def extract_project_attributes(self, project: Dict) -> Dict[str, Any]:
        """Extract and structure project attributes."""
        attributes = {
            "title": project.get("title", "").strip(),
            "domain": project.get("domain", "Other").strip(),
            "problem_keywords": self.extract_keywords(project.get("problem_statement", "")),
            "dataset": project.get("dataset", "").strip(),
            "method": project.get("method", "").strip(),
            "technologies": [t.strip() for t in project.get("technologies", [])],
            "additional_keywords": self.extract_keywords(
                project.get("problem_statement", "") + " " + 
                project.get("additional_info", "")
            ),
            "all_keywords": []
        }
        
        # Combine all keywords
        attributes["all_keywords"] = list(set(
            attributes["problem_keywords"] + 
            attributes["additional_keywords"] +
            [attributes["method"].lower()]
        ))
        
        return attributes


class SimilarityAnalyzer:
    """Calculate similarity between projects using multiple metrics."""
    
    def __init__(self):
        """Initialize similarity weights."""
        self.weights = {
            "domain": 0.25,
            "method": 0.25,
            "dataset": 0.20,
            "technologies": 0.15,
            "keywords": 0.15
        }
    
    def calculate_jaccard_similarity(self, set1: set, set2: set) -> float:
        """Calculate Jaccard similarity between two sets."""
        if not set1 and not set2:
            return 1.0
        if not set1 or not set2:
            return 0.0
        
        intersection = len(set1 & set2)
        union = len(set1 | set2)
        return intersection / union if union > 0 else 0.0
    
    def calculate_string_similarity(self, str1: str, str2: str) -> float:
        """Calculate similarity between two strings (case-insensitive)."""
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()
        
        # Exact match
        if str1 == str2:
            return 1.0
        
        # Substring match
        if str1 in str2 or str2 in str1:
            return 0.8
        
        # Token-based similarity
        tokens1 = set(str1.split())
        tokens2 = set(str2.split())
        
        return self.calculate_jaccard_similarity(tokens1, tokens2)
    
    def calculate_overall_similarity(self, new_project: Dict, previous_project: Dict) -> float:
        """Calculate overall similarity score between two projects."""
        scores = {}
        
        # Domain similarity
        scores["domain"] = self.calculate_string_similarity(
            new_project.get("domain", ""),
            previous_project.get("domain", "")
        )
        
        # Method similarity
        scores["method"] = self.calculate_string_similarity(
            new_project.get("method", ""),
            previous_project.get("method", "")
        )
        
        # Dataset similarity
        scores["dataset"] = self.calculate_string_similarity(
            new_project.get("dataset", ""),
            previous_project.get("dataset", "")
        )
        
        # Technologies similarity
        new_techs = set(t.lower() for t in new_project.get("technologies", []))
        prev_techs = set(t.lower() for t in previous_project.get("technologies", []))
        scores["technologies"] = self.calculate_jaccard_similarity(new_techs, prev_techs)
        
        # Keywords similarity
        new_keywords = set(new_project.get("all_keywords", []))
        prev_keywords = set(previous_project.get("all_keywords", []))
        scores["keywords"] = self.calculate_jaccard_similarity(new_keywords, prev_keywords)
        
        # Calculate weighted average
        overall_score = sum(
            scores[key] * self.weights[key] 
            for key in self.weights
        )
        
        return round(overall_score * 100, 2)  # Convert to percentage
    
    def find_similar_projects(self, new_project: Dict, previous_projects: List[Dict], 
                            threshold: int = 30) -> List[Dict]:
        """Find and rank similar projects."""
        similar = []
        
        for prev_project in previous_projects:
            similarity = self.calculate_overall_similarity(new_project, prev_project)
            
            if similarity >= threshold:
                similar.append({
                    "title": prev_project.get("title", ""),
                    "domain": prev_project.get("domain", ""),
                    "method": prev_project.get("method", ""),
                    "dataset": prev_project.get("dataset", ""),
                    "technologies": prev_project.get("technologies", []),
                    "similarity": similarity,
                    "id": prev_project.get("id", "")
                })
        
        # Sort by similarity (descending) and return top 5
        similar.sort(key=lambda x: x["similarity"], reverse=True)
        return similar[:5]


class ComponentAnalyzer:
    """Analyze common and overused components."""
    
    def analyze_common_technologies(self, previous_projects: List[Dict]) -> List[Dict]:
        """Identify commonly used technologies."""
        tech_counter = Counter()
        
        for project in previous_projects:
            for tech in project.get("technologies", []):
                tech_counter[tech.strip()] += 1
        
        total_projects = len(previous_projects)
        common_techs = [
            {
                "name": tech,
                "usage_percent": round((count / total_projects) * 100, 1),
                "count": count
            }
            for tech, count in tech_counter.most_common(8)
        ]
        
        return common_techs
    
    def analyze_common_datasets(self, previous_projects: List[Dict]) -> List[Dict]:
        """Identify commonly used datasets."""
        dataset_counter = Counter()
        
        for project in previous_projects:
            dataset = project.get("dataset", "").strip()
            if dataset:
                dataset_counter[dataset] += 1
        
        total_projects = len(previous_projects)
        common_datasets = [
            {
                "name": dataset,
                "usage_percent": round((count / total_projects) * 100, 1),
                "count": count
            }
            for dataset, count in dataset_counter.most_common(6)
        ]
        
        return common_datasets
    
    def analyze_common_methods(self, previous_projects: List[Dict]) -> List[Dict]:
        """Identify commonly used methods/algorithms."""
        method_counter = Counter()
        
        for project in previous_projects:
            method = project.get("method", "").strip()
            if method:
                method_counter[method] += 1
        
        total_projects = len(previous_projects)
        common_methods = [
            {
                "name": method,
                "usage_percent": round((count / total_projects) * 100, 1),
                "count": count
            }
            for method, count in method_counter.most_common(6)
        ]
        
        return common_methods


class LimitationAnalyzer:
    """Analyze limitations of similar projects."""
    
    def __init__(self):
        """Initialize common limitation patterns."""
        self.common_limitations = [
            "Limited to small batch sizes due to memory constraints",
            "Training time exceeds 24 hours for large datasets",
            "Model performance degrades with domain shift",
            "Lack of real-time inference capabilities",
            "High computational requirements for deployment",
            "Limited cross-domain generalization",
            "Absence of uncertainty quantification",
            "Scalability issues with increasing data volume",
            "Lack of explainability in model decisions",
            "Limited robustness to adversarial examples",
            "Insufficient evaluation on diverse datasets",
            "Missing privacy-preserving mechanisms"
        ]
    
    def extract_limitations(self, similar_projects: List[Dict]) -> List[str]:
        """Extract limitations based on similar projects."""
        limitations = []
        
        # If too many projects use the same method, it's a limitation
        for project in similar_projects[:3]:
            method = project.get("method", "")
            if method in ["CNN", "RNN/LSTM", "Transfer Learning", "Random Forest"]:
                if "may have limited novelty due to common methods" not in limitations:
                    limitations.append(
                        f"Most similar projects use {method}, indicating potential saturation"
                    )
        
        # Add generic limitations
        limitations.extend(self.common_limitations[:5])
        
        return limitations


class GapAnalyzer:
    """Identify gaps and improvement opportunities."""
    
    def __init__(self):
        """Initialize gap analysis patterns."""
        self.potential_gaps = [
            "No standardized benchmarking framework for this domain",
            "Lack of interpretability in model decisions",
            "Limited focus on edge deployment and mobile optimization",
            "Missing privacy-preserving training methods",
            "No comprehensive comparison of recent architectures",
            "Insufficient real-world dataset diversity",
            "Limited multi-modal learning approaches",
            "Lack of automated hyperparameter optimization",
            "Missing real-time monitoring and drift detection",
            "Insufficient focus on model compression techniques"
        ]
    
    def identify_gaps(self, new_project: Dict, similar_projects: List[Dict], 
                     common_techs: List[Dict]) -> List[str]:
        """Identify gaps specific to the project."""
        gaps = []
        
        # Check if project uses uncommon technologies
        new_techs = set(t.lower() for t in new_project.get("technologies", []))
        common_tech_names = set(t["name"].lower() for t in common_techs)
        
        uncommon_techs = new_techs - common_tech_names
        if uncommon_techs:
            gaps.append(
                f"Opportunity to explore novel applications of less common technologies: {', '.join(list(uncommon_techs)[:2])}"
            )
        
        # Check domain saturation
        if len(similar_projects) > 3:
            gaps.append("High saturation in this domain - consider adding unique aspects")
        
        # Add generic gaps
        gaps.extend(self.potential_gaps[:4])
        
        return gaps


class NoveltyIdeasGenerator:
    """Generate novelty suggestions specific to each project."""
    
    def __init__(self):
        """Initialize novelty idea templates."""
        self.idea_templates = [
            {
                "template": "Implement {feature} to enhance {aspect}",
                "features": ["Federated Learning", "Explainability with SHAP", "Adversarial Robustness"],
                "aspects": ["model interpretability", "privacy", "robustness"]
            },
            {
                "template": "Add {tech} integration for {benefit}",
                "tech": ["Edge Deployment", "Real-time Inference", "AutoML"],
                "benefit": ["scalability", "performance", "automation"]
            },
            {
                "template": "Combine {method1} with {method2} for {outcome}",
                "method1": ["Transformer Models", "Graph Neural Networks", "Attention Mechanisms"],
                "method2": ["Classical ML", "Ensemble Methods", "Reinforcement Learning"],
                "outcome": ["improved accuracy", "better efficiency", "novel approaches"]
            }
        ]
    
    def generate_novelty_suggestions(self, new_project: Dict, similar_projects: List[Dict],
                                    common_techs: List[Dict], gaps: List[str]) -> List[Dict]:
        """Generate 3-5 specific novelty suggestions."""
        suggestions = []
        
        # Suggestion 1: Based on common limitations
        suggestions.append({
            "id": "novelty_001",
            "title": "Implement Federated Learning",
            "description": "Add federated learning capabilities to train the model across distributed devices while maintaining data privacy.",
            "impact": "High",
            "feasibility": "Medium",
            "details": "Distribute model training across multiple devices without centralizing data",
            "reason": "Privacy-preserving ML is increasingly important and underutilized in this domain"
        })
        
        # Suggestion 2: Based on domain
        domain = new_project.get("domain", "")
        if "NLP" in domain or "Natural Language" in domain:
            suggestions.append({
                "id": "novelty_002",
                "title": "Multi-Language Support",
                "description": "Extend the project to support multiple languages with language-specific optimizations.",
                "impact": "High",
                "feasibility": "High",
                "details": "Implement language detection, translation, and domain-specific embeddings",
                "reason": f"Most {domain} projects are limited to English; multi-language support adds novelty"
            })
        elif "Computer Vision" in domain or "Vision" in domain:
            suggestions.append({
                "id": "novelty_002",
                "title": "Real-time Performance Optimization",
                "description": "Optimize the model for edge deployment and real-time inference.",
                "impact": "High",
                "feasibility": "High",
                "details": "Implement model quantization, pruning, and TensorRT optimization",
                "reason": "Real-time deployment is a key gap in most vision projects"
            })
        else:
            suggestions.append({
                "id": "novelty_002",
                "title": "Add Explainability with SHAP",
                "description": "Integrate SHAP to make model predictions interpretable and trustworthy.",
                "impact": "High",
                "feasibility": "High",
                "details": "Provide feature importance and decision explanations for each prediction",
                "reason": "Interpretability is crucial for gaining trust in AI systems"
            })
        
        # Suggestion 3: Based on dataset
        dataset = new_project.get("dataset", "").lower()
        if "custom" in dataset or "proprietary" in dataset:
            suggestions.append({
                "id": "novelty_003",
                "title": "Implement Transfer Learning from Pre-trained Models",
                "description": "Leverage transfer learning to improve performance with limited data.",
                "impact": "High",
                "feasibility": "High",
                "details": "Use pre-trained models as base and fine-tune on your specific dataset",
                "reason": "Custom datasets often have limited samples; transfer learning maximizes performance"
            })
        else:
            suggestions.append({
                "id": "novelty_003",
                "title": "Multi-Modal Learning Approach",
                "description": "Combine multiple data modalities for improved predictions.",
                "impact": "High",
                "feasibility": "Medium",
                "details": "Fuse different data types with ensemble methods for better results",
                "reason": "Multi-modal learning is underutilized and provides significant novelty"
            })
        
        # Suggestion 4: Based on technologies
        if "PyTorch" in new_project.get("technologies", []):
            suggestions.append({
                "id": "novelty_004",
                "title": "Implement Adversarial Robustness",
                "description": "Add adversarial training and robustness testing to enhance model reliability.",
                "impact": "Medium",
                "feasibility": "Medium",
                "details": "Train and test against adversarial examples to improve robustness",
                "reason": "Robustness is critical for production systems but often overlooked"
            })
        else:
            suggestions.append({
                "id": "novelty_004",
                "title": "Real-time Inference Optimization",
                "description": "Optimize the model for edge deployment with quantization and pruning.",
                "impact": "Medium",
                "feasibility": "High",
                "details": "Deploy lightweight models for mobile and IoT devices",
                "reason": "Edge deployment is increasingly important for IoT and mobile applications"
            })
        
        # Suggestion 5: Generic high-impact suggestion
        suggestions.append({
            "id": "novelty_005",
            "title": "Automated Hyperparameter Optimization",
            "description": "Implement automated hyperparameter tuning using Bayesian optimization or similar techniques.",
            "impact": "Medium",
            "feasibility": "High",
            "details": "Use tools like Optuna or Ray Tune for systematic hyperparameter search",
            "reason": "AutoML techniques are underutilized and can significantly improve model performance"
        })
        
        return suggestions[:5]  # Return top 5 suggestions


class NoveltyAnalysisEngine:
    """Main analysis engine orchestrating all components."""
    
    def __init__(self):
        """Initialize all analysis components."""
        self.attribute_extractor = ProjectAttributeExtractor()
        self.similarity_analyzer = SimilarityAnalyzer()
        self.component_analyzer = ComponentAnalyzer()
        self.limitation_analyzer = LimitationAnalyzer()
        self.gap_analyzer = GapAnalyzer()
        self.novelty_generator = NoveltyIdeasGenerator()
    
    def analyze_project(self, project_data: Dict, previous_projects: List[Dict]) -> AnalysisResult:
        """
        Main analysis function - orchestrates complete novelty analysis.
        
        Args:
            project_data: Dictionary containing new project details
                {
                    "title": str,
                    "problem_statement": str,
                    "domain": str,
                    "dataset": str,
                    "method": str,
                    "technologies": List[str],
                    "additional_info": str (optional)
                }
            previous_projects: List of dictionaries containing previous project data
        
        Returns:
            AnalysisResult object with complete analysis
        """
        
        # Step 1: Extract attributes
        new_project_attrs = self.attribute_extractor.extract_project_attributes(project_data)
        previous_projects_attrs = [
            self.attribute_extractor.extract_project_attributes(p)
            for p in previous_projects
        ]
        
        # Enrich project data with extracted attributes
        for key, value in new_project_attrs.items():
            if key not in project_data:
                project_data[key] = value
        
        for prev_proj, attrs in zip(previous_projects, previous_projects_attrs):
            for key, value in attrs.items():
                if key not in prev_proj:
                    prev_proj[key] = value
        
        # Step 2: Find similar projects
        similar_projects = self.similarity_analyzer.find_similar_projects(
            project_data, previous_projects
        )
        
        # Step 3: Analyze common components
        common_technologies = self.component_analyzer.analyze_common_technologies(
            previous_projects
        )
        common_datasets = self.component_analyzer.analyze_common_datasets(
            previous_projects
        )
        common_methods = self.component_analyzer.analyze_common_methods(
            previous_projects
        )
        
        # Step 4: Extract limitations from similar projects
        existing_limitations = self.limitation_analyzer.extract_limitations(similar_projects)
        
        # Step 5: Identify gaps
        possible_gaps = self.gap_analyzer.identify_gaps(
            project_data, similar_projects, common_technologies
        )
        
        # Step 6: Generate novelty suggestions
        novelty_suggestions = self.novelty_generator.generate_novelty_suggestions(
            project_data, similar_projects, common_technologies, possible_gaps
        )
        
        # Step 7: Create result object
        result = AnalysisResult(
            project_title=project_data.get("title", "Unknown"),
            similar_projects=similar_projects,
            common_technologies=common_technologies,
            common_datasets=common_datasets,
            common_methods=common_methods,
            existing_limitations=existing_limitations,
            possible_gaps=possible_gaps,
            novelty_suggestions=novelty_suggestions,
            timestamp=datetime.now().isoformat()
        )
        
        return result


# ============================================================================
# EXAMPLE USAGE AND TESTING
# ============================================================================

def test_novelty_engine():
    """Test the novelty analysis engine with sample data."""
    
    # Sample previous projects
    previous_projects = [
        {
            "id": "proj_001",
            "title": "Sentiment Analysis using BERT",
            "problem_statement": "Classify social media posts for sentiment",
            "domain": "Natural Language Processing",
            "dataset": "Twitter Dataset",
            "method": "BERT Transfer Learning",
            "technologies": ["Python", "PyTorch", "Transformers", "Pandas"],
            "additional_info": "Real-time sentiment classification on streaming data"
        },
        {
            "id": "proj_002",
            "title": "Image Classification with CNN",
            "problem_statement": "Classify medical images for disease detection",
            "domain": "Computer Vision",
            "dataset": "Medical Image Dataset",
            "method": "Convolutional Neural Networks",
            "technologies": ["Python", "TensorFlow", "OpenCV", "NumPy"],
            "additional_info": "Multi-class classification with attention mechanisms"
        },
        {
            "id": "proj_003",
            "title": "Time Series Forecasting",
            "problem_statement": "Predict stock prices using historical data",
            "domain": "Time Series Analysis",
            "dataset": "Stock Market Data",
            "method": "LSTM Networks",
            "technologies": ["Python", "TensorFlow", "Pandas", "Scikit-learn"],
            "additional_info": "Multi-step ahead forecasting"
        }
    ]
    
    # Sample new project
    new_project = {
        "title": "Real-time Multi-language Sentiment Analysis",
        "problem_statement": "Analyze sentiment across multiple social media platforms in different languages",
        "domain": "Natural Language Processing",
        "dataset": "Multi-language Social Media Corpus",
        "method": "Transformer-based Model with Language Detection",
        "technologies": ["Python", "PyTorch", "Transformers", "FastAPI"],
        "additional_info": "Should handle streaming data and support 10+ languages"
    }
    
    # Run analysis
    engine = NoveltyAnalysisEngine()
    result = engine.analyze_project(new_project, previous_projects)
    
    return result


if __name__ == "__main__":
    # Run test
    result = test_novelty_engine()
    
    print("\n" + "="*80)
    print("NOVELTY ANALYSIS ENGINE - TEST RESULTS")
    print("="*80)
    
    print(f"\nProject: {result.project_title}")
    print(f"Analysis Timestamp: {result.timestamp}")
    
    print("\n--- SIMILAR PROJECTS ---")
    for proj in result.similar_projects:
        print(f"  {proj['title']} ({proj['domain']}) - Similarity: {proj['similarity']}%")
    
    print("\n--- COMMON TECHNOLOGIES ---")
    for tech in result.common_technologies:
        print(f"  {tech['name']}: {tech['usage_percent']}% usage")
    
    print("\n--- EXISTING LIMITATIONS ---")
    for limit in result.existing_limitations:
        print(f"  • {limit}")
    
    print("\n--- POSSIBLE GAPS ---")
    for gap in result.possible_gaps:
        print(f"  • {gap}")
    
    print("\n--- NOVELTY SUGGESTIONS ---")
    for sugg in result.novelty_suggestions:
        print(f"  {sugg['id']}: {sugg['title']}")
        print(f"    Impact: {sugg['impact']}, Feasibility: {sugg['feasibility']}")
        print(f"    Reason: {sugg['reason']}")
    
    print("\n" + "="*80)
    print("JSON OUTPUT (for API response)")
    print("="*80)
    print(json.dumps(asdict(result), indent=2))
