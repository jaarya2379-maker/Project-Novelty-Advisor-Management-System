import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import nsdecls, qn

def set_cell_background(cell, hex_color):
    """Set background color of a table cell."""
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    """Set internal padding for a cell."""
    tcPr = cell._element.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)

def add_header_footer(doc):
    for s in doc.sections:
        s.top_margin = Inches(1.0)
        s.bottom_margin = Inches(1.0)
        s.left_margin = Inches(1.0)
        s.right_margin = Inches(1.0)
        
        # Header
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("DBMS Course Project — Review 1 Report | Project Novelty Advisor")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(120, 120, 120)
        
        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Project Novelty Advisor & Management System — Review 1")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(140, 140, 140)

def style_heading_1(p, text):
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(16)
    run.font.bold = True
    run.font.color.rgb = RGBColor(16, 54, 102) # Deep Navy
    return run

def style_heading_2(p, text):
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(13)
    run.font.bold = True
    run.font.color.rgb = RGBColor(41, 105, 176) # Accent Blue
    return run

def style_heading_3(p, text):
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(60, 60, 60)
    return run

def add_body_p(doc, text="", bold_prefix=None, space_after=5):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Calibri"
        r_bold.font.size = Pt(10.5)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(30, 30, 30)
    if text:
        r_text = p.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(10.5)
        r_text.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_bullet_p(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.15
    r_bold = p.add_run(bold_prefix)
    r_bold.font.name = "Calibri"
    r_bold.font.size = Pt(10.5)
    r_bold.font.bold = True
    r_bold.font.color.rgb = RGBColor(30, 30, 30)
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10.5)
    r_text.font.color.rgb = RGBColor(50, 50, 50)
    return p

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F4F6F9")
    set_cell_margins(cell, top=140, bottom=140, left=200, right=200)
    
    # Border
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="16" w:space="0" w:color="2563EB"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_text)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

def build_review_1_doc(output_path):
    doc = Document()
    add_header_footer(doc)
    
    # Title & Header
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(10)
    title_p.paragraph_format.space_after = Pt(4)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    trun = title_p.add_run("PROJECT NOVELTY ADVISOR & MANAGEMENT SYSTEM")
    trun.font.name = "Calibri"
    trun.font.size = Pt(22)
    trun.font.bold = True
    trun.font.color.rgb = RGBColor(16, 54, 102)
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(14)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    srun = sub_p.add_run("DBMS Course Project — Review 1 Design & Progress Report")
    srun.font.name = "Calibri"
    srun.font.size = Pt(13)
    srun.font.bold = True
    srun.font.color.rgb = RGBColor(41, 105, 176)
    
    # Metadata Card Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    col_widths = [Inches(2.2), Inches(4.3)]
    
    meta_data = [
        ("Course", "Database Management Systems (DBMS) Course Project"),
        ("Project Title", "Project Novelty Advisor & Management System"),
        ("Faculty Guide / Reviewer", "Dr. Katari Balakrishna"),
        ("Team Member 1", "Aarya Jadhav (Reg No: 25BCE2975) — DB Design & Backend"),
        ("Team Member 2", "Diya S (Reg No: 25BAI0235) — Novelty & Gap Analytics Engine"),
        ("Team Member 3", "Hamsapriya V (Reg No: 25BCE2754) — Frontend UI & User Workflows")
    ]
    
    for i, (label, val) in enumerate(meta_data):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = col_widths[0]
        c1.width = col_widths[1]
        set_cell_background(c0, "F0F4F8")
        set_cell_background(c1, "FFFFFF")
        set_cell_margins(c0, top=60, bottom=60, left=100, right=100)
        set_cell_margins(c1, top=60, bottom=60, left=100, right=100)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        r0.font.color.rgb = RGBColor(16, 54, 102)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.5)
        r1.font.color.rgb = RGBColor(40, 40, 40)
        if "25B" in val or "Dr." in val:
            r1.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(10)
    
    # Section 1: Executive Summary
    style_heading_1(doc.add_paragraph(), "1. Executive Summary & Abstract")
    add_body_p(doc, 
        "In university computer science departments, thousands of student teams submit capstone, semester, and mini-project proposals each year. "
        "A chronic issue facing academic evaluation committees is the rampant redundancy and lack of novelty in submitted projects. Students frequently replicate "
        "previous cohorts' work with cosmetic adjustments—most notably applying standard machine learning algorithms (such as Logistic Regression, Random Forest, "
        "or basic CNN/BERT models) onto saturated benchmark datasets (such as Kaggle Titanic, Iris, Credit Card Fraud, and standard Twitter Sentiment Analysis) "
        "without making genuine technical, algorithmic, or domain-specific contributions."
    )
    add_body_p(doc,
        "Existing institutional systems present critical operational deficiencies: Learning Management Systems (e.g., Moodle, Blackboard, Canvas) operate "
        "merely as passive file-drop repositories that lack semantic indexing, while commercial plagiarism tools (e.g., Turnitin) evaluate only verbatim textual "
        "n-gram overlap rather than architectural or methodological duplication. Moreover, traditional tools are strictly punitive (rejecting submissions) rather "
        "than advisory (guiding students toward innovation)."
    )
    add_body_p(doc,
        "The Project Novelty Advisor & Management System addresses this fundamental gap through a database-centric decision support architecture. Built on an "
        "ACID-compliant MySQL relational core operating in Boyce-Codd Normal Form (BCNF), the system maintains student portfolios, structured project proposals, "
        "analytical similarity matrices, and committed novelty roadmaps. Integrated with an explainable multi-metric novelty engine, the platform benchmarks incoming "
        "proposals across five weighted dimensions (domain, method, dataset, tech stack, and keywords). Crucially, the system does not simply output a similarity score: "
        "it diagnoses component saturation, isolates research limitations, detects technical gaps, and algorithmically recommends five concrete novelty enhancement paths. "
        "This Review 1 report details the literature survey, technical challenges, relational schema design, normal form proofs, algorithmic formulation, and working deliverables."
    )
    
    # Section 2: Problem Statement & Motivation
    style_heading_1(doc.add_paragraph(), "2. Problem Statement & Motivation")
    style_heading_2(doc.add_paragraph(), "2.1 The Real-World Problems It Solves")
    add_bullet_p(doc, "Severe Academic Project Duplication: ", "Academic departments repeatedly evaluate projects with identical methodologies and problem statements, degrading academic rigor and wasting departmental evaluation bandwidth.")
    add_bullet_p(doc, "Cognitive Overload on Faculty Evaluators: ", "Faculty members and project coordinators must manually cross-reference new proposals against years of historical project records without standardized objective metrics.")
    add_bullet_p(doc, "Absence of Constructive Feedback Loops: ", "When proposals are rejected for being unoriginal, students receive no automated guidance or actionable suggestions on how to elevate the technical depth of their ideas.")
    add_bullet_p(doc, "Disorganized Institutional Project Repositories: ", "Historical capstones are traditionally archived in disparate spreadsheets or flat PDF files, preventing structured querying, longitudinal analytics, tech stack trend monitoring, and historical audits.")

    style_heading_2(doc.add_paragraph(), "2.2 Core Project Objectives")
    add_bullet_p(doc, "Relational DBMS Foundation: ", "Design and implement a robust, normalized relational database to maintain student accounts, project proposals, multi-attribute similarity scores, and chosen novelty paths.")
    add_bullet_p(doc, "Objective Multi-Metric Similarity Scoring: ", "Provide deterministic, explainable similarity scores combining set-theoretic Jaccard metrics and token overlap across five orthogonal project dimensions.")
    add_bullet_p(doc, "Automated Constructive Novelty Recommendations: ", "Formulate a rule-based recommendation generator that proposes 5 high-impact, feasible novelty pivots (e.g., cross-domain transfer, edge deployment, multimodal integration, hybrid ensembling).")
    add_bullet_p(doc, "Full Lifecycle Proposal Management: ", "Track proposal statuses through sequential states ('submitted', 'analyzed', 'novelty_selected', 'approved').")

    # Section 3: Literature Survey
    style_heading_1(doc.add_paragraph(), "3. Literature Survey")
    add_body_p(doc, "A comprehensive survey of information retrieval models, document classification algorithms, and commercial plagiarism platforms was conducted to contextualize the novelty detector within academic research.")
    
    # Literature Matrix Table
    lit_table = doc.add_table(rows=6, cols=4)
    lit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["System / Author", "Core Technique", "Key Strengths", "Critical Limitations & Gaps"]
    
    # Format Header Row
    for j, h in enumerate(headers):
        cell = lit_table.cell(0, j)
        set_cell_background(cell, "103666")
        set_cell_margins(cell, top=100, bottom=100, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    lit_data = [
        ("Salton & McGill (1983) Vector Space Model", "TF-IDF vectors & Cosine similarity", "Fast lexical similarity; robust baseline for plain text search.", "Completely ignores structured attributes (dataset, tech stack); purely lexical; misses conceptual duplication."),
        ("Blei et al. (2003) Topic Modeling (LDA)", "Probabilistic Latent Dirichlet Allocation", "Uncovers latent thematic topics across unstructured documents.", "High compute overhead; probabilistic outputs lack deterministic explainability needed for academic scoring."),
        ("Commercial Plagiarism Engines (Turnitin, Urkund)", "N-gram fingerprinting & string matching", "Industry standard for detecting verbatim or paraphrased copied text.", "Strictly punitive; cannot detect when two distinct text descriptions describe the exact same underlying ML pipeline."),
        ("Traditional Academic LMS (Moodle, Canvas)", "Relational CRUD with static file blob storage", "Strong student authentication and assignment hand-in workflows.", "Zero analytical intelligence; proposals stored as unindexed blobs without metadata or similarity indexing."),
        ("Proposed System: Project Novelty Advisor", "Normalized Relational DB + Multi-Metric Jaccard & Component Saturation", "Relational integrity (BCNF), multi-attribute decomposition, overused component detection, and constructive novelty advice.", "Currently rule-based; scheduled for vector embedding integration in Review 3.")
    ]
    
    for i, row_data in enumerate(lit_data):
        row = lit_table.rows[i+1]
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            run.font.color.rgb = RGBColor(40, 40, 40)
            if j == 0:
                run.font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    style_heading_2(doc.add_paragraph(), "3.2 Detailed Literature Synthesis")
    add_bullet_p(doc, "Decomposing Projects into Orthogonal Dimensions: ", 
        "Salton & McGill demonstrated the effectiveness of vector space retrieval, but treating an entire project proposal as a single bag-of-words obscures critical technical distinctions. A project utilizing a standard dataset with a novel architecture must not be penalized identically to one replicating both dataset and architecture.")
    add_bullet_p(doc, "Set-Theoretic Similarity for Technology Stacks: ", 
        "Following Paul Jaccard's mathematical formulations (1912), technical stacks (e.g., PyTorch, OpenCV, Flask, Docker) are discrete finite sets where order is irrelevant. The Jaccard Index provides an optimal, normalized, scale-invariant similarity measure.")
    add_bullet_p(doc, "Database Systems for Semi-Structured Analytical Data: ", 
        "As established by Elmasri & Navathe (2015), modern data architectures benefit from a hybrid model: strict Boyce-Codd Normal Form for transactional integrity (students, proposals, audits) paired with native JSON columns for dynamic, multi-dimensional analytical outputs.")

    # Section 4: What is Novel in This Project
    style_heading_1(doc.add_paragraph(), "4. What is Novel in This Project?")
    add_body_p(doc, "The Project Novelty Advisor & Management System introduces four distinctive innovations that set it apart from conventional project management tools and plagiarism engines:")
    add_bullet_p(doc, "1. Constructive Advisory Model vs. Punitive Rejection: ", 
        "Conventional systems operate punitively: 'Your submission has 65% similarity; proposal rejected.' Our platform acts as a virtual research guide: 'Your proposal shares 75% similarity due to the overused combination of BERT + Twitter Dataset for Sentiment Analysis. Here are 5 ways to make it novel: (1) Domain transfer to low-resource languages; (2) Edge deployment using MobileBERT; (3) Incorporating multimodal audio-text cues.'")
    add_bullet_p(doc, "2. Multi-Attribute Decomposition Framework: ", 
        "Rather than treating text descriptions as monolithic paragraphs, the system evaluates proposals across five independent dimensions: Domain (25%), Methodology (25%), Dataset (20%), Tech Stack (15%), and Problem Keywords (15%).")
    add_bullet_p(doc, "3. Component Saturation & Research Gap Detection: ", 
        "By querying historical database distributions, the system calculates frequency distributions across datasets and algorithms. When a threshold is breached, the engine isolates known literature limitations and surfaces research gaps.")
    add_bullet_p(doc, "4. Closed-Loop Novelty Selection Tracking: ", 
        "After reviewing novelty suggestions, students select and commit to a specific novelty pivot. This is persisted in the 'selected_novelties' table with foreign key linkage, forming an immutable baseline for final faculty grading.")

    # Section 5: Technical Challenges
    style_heading_1(doc.add_paragraph(), "5. Technical & DBMS Challenges Addressed")
    add_bullet_p(doc, "Hybrid Relational & Semi-Structured Data Storage: ", 
        "Student records and project headers require strict relational normalization (BCNF), whereas similarity rankings and generated suggestions vary in length per project. This was solved by utilizing MySQL InnoDB tables with native JSON columns for analytical payloads.")
    add_bullet_p(doc, "Eliminating Text Search Bottlenecks: ", 
        "Using SQL 'LIKE %keyword%' across large text fields causes full table scans (O(N)). The system implements MySQL FULLTEXT indexes on 'title' and 'problem_statement' to enable sub-millisecond inverted-index boolean searches.")
    add_bullet_p(doc, "Referential Integrity & Cascading Constraints: ", 
        "To prevent orphan records upon student graduation or proposal deletion, strict ON DELETE CASCADE foreign key constraints were engineered across students -> projects -> analysis_results and projects -> selected_novelties.")
    add_bullet_p(doc, "Cryptographic Credential Security: ", 
        "Student credentials are protected using salted PBKDF2 cryptographic password hashing (via Werkzeug) prior to persistence, ensuring plaintext passwords never touch the database.")

    # Section 6: DBMS Architecture & Implementation
    style_heading_1(doc.add_paragraph(), "6. DBMS Architectural Design & Implementation")
    style_heading_2(doc.add_paragraph(), "6.1 Relational Schema & Normalization Analysis (BCNF / 3NF)")
    add_body_p(doc, "A rigorous normalization study was executed to ensure the schema is free of insertion, update, and deletion anomalies:")
    
    add_body_p(doc, 
        "Table 1: students(student_id [PK], username [UK], email [UK], password_hash, name, created_at)\n"
        "• Functional Dependencies: student_id -> {username, email, password_hash, name, created_at}; username -> {...}; email -> {...}\n"
        "• Candidate Keys: {student_id}, {username}, {email}\n"
        "• Normal Form Proof: Every determinant is a candidate key. Therefore, the relation is strictly in Boyce-Codd Normal Form (BCNF).",
        bold_prefix="• "
    )
    add_body_p(doc, 
        "Table 2: projects(project_id [PK], student_id [FK], title, problem_statement, domain, dataset, method, technologies [JSON], additional_info, status, created_at, updated_at)\n"
        "• Functional Dependencies: project_id -> {student_id, title, problem_statement, domain, dataset, method, technologies, additional_info, status, created_at, updated_at}\n"
        "• Candidate Key: {project_id}\n"
        "• Normal Form Proof: All non-key attributes are fully functionally dependent on the primary key (no partial dependencies -> 2NF). No non-prime attribute determines another non-prime attribute (no transitive dependencies -> 3NF). The only determinant is the primary key -> BCNF.",
        bold_prefix="• "
    )
    add_body_p(doc, 
        "Table 3: analysis_results(analysis_id [PK], project_id [FK, UK], similar_projects, common_technologies, common_datasets, common_methods, existing_limitations, possible_gaps, novelty_suggestions, analysis_timestamp)\n"
        "• Candidate Keys: {analysis_id}, {project_id} (enforced via UNIQUE constraint).\n"
        "• Normal Form Proof: 1:1 mandatory relationship with projects. Determinants are candidate keys -> BCNF.",
        bold_prefix="• "
    )
    add_body_p(doc, 
        "Table 4: selected_novelties(novelty_id [PK], project_id [FK], novelty_title, novelty_description, novelty_impact, novelty_feasibility, notes, selected_at)\n"
        "• Candidate Key: {novelty_id}\n"
        "• Normal Form Proof: In BCNF.",
        bold_prefix="• "
    )

    style_heading_2(doc.add_paragraph(), "6.2 Data Definition Language (DDL) Specification")
    ddl_sql = (
        "-- 1. Students Entity\n"
        "CREATE TABLE IF NOT EXISTS students (\n"
        "    student_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    username VARCHAR(100) UNIQUE NOT NULL,\n"
        "    email VARCHAR(100) UNIQUE NOT NULL,\n"
        "    password_hash VARCHAR(255) NOT NULL,\n"
        "    name VARCHAR(100) NOT NULL,\n"
        "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 2. Projects Entity\n"
        "CREATE TABLE IF NOT EXISTS projects (\n"
        "    project_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    student_id INT NOT NULL,\n"
        "    title VARCHAR(255) NOT NULL,\n"
        "    problem_statement TEXT NOT NULL,\n"
        "    domain VARCHAR(100),\n"
        "    dataset VARCHAR(255),\n"
        "    method VARCHAR(255),\n"
        "    technologies JSON,\n"
        "    additional_info TEXT,\n"
        "    status VARCHAR(50) DEFAULT 'submitted',\n"
        "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (student_id) REFERENCES students(student_id) ON DELETE CASCADE,\n"
        "    INDEX idx_student_id (student_id),\n"
        "    INDEX idx_status (status),\n"
        "    FULLTEXT INDEX ft_title (title),\n"
        "    FULLTEXT INDEX ft_problem (problem_statement)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 3. Analysis Results Entity\n"
        "CREATE TABLE IF NOT EXISTS analysis_results (\n"
        "    analysis_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    project_id INT NOT NULL UNIQUE,\n"
        "    similar_projects JSON,\n"
        "    common_technologies JSON,\n"
        "    common_datasets JSON,\n"
        "    common_methods JSON,\n"
        "    existing_limitations JSON,\n"
        "    possible_gaps JSON,\n"
        "    novelty_suggestions JSON,\n"
        "    analysis_timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,\n"
        "    INDEX idx_project_id (project_id)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 4. Selected Novelties Entity\n"
        "CREATE TABLE IF NOT EXISTS selected_novelties (\n"
        "    novelty_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    project_id INT NOT NULL,\n"
        "    novelty_title VARCHAR(255),\n"
        "    novelty_description TEXT,\n"
        "    novelty_impact VARCHAR(50),\n"
        "    novelty_feasibility VARCHAR(50),\n"
        "    notes TEXT,\n"
        "    selected_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,\n"
        "    FOREIGN KEY (project_id) REFERENCES projects(project_id) ON DELETE CASCADE,\n"
        "    INDEX idx_project_id (project_id)\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;"
    )
    add_code_block(doc, ddl_sql)

    # Section 7: Algorithmic Methodology
    style_heading_1(doc.add_paragraph(), "7. System Architecture & Algorithmic Methodology")
    add_body_p(doc, 
        "The overall project similarity score S_total in [0, 100%] is calculated via a multi-attribute weighted linear combination:\n\n"
        "S_total = (0.25 * S_domain + 0.25 * S_method + 0.20 * S_dataset + 0.15 * S_tech + 0.15 * S_keywords) * 100\n\n"
        "Where:\n"
        "• S_domain: Hierarchical exact/fuzzy domain match (1.0 for exact, 0.5 for related, 0.0 otherwise)\n"
        "• S_method: String normalization & substring token overlap between proposed and historical algorithms\n"
        "• S_dataset: Exact and substring matching on dataset benchmarks\n"
        "• S_tech: Jaccard similarity = |Tech_new ∩ Tech_old| / |Tech_new ∪ Tech_old|\n"
        "• S_keywords: Jaccard similarity across non-stopword token sets extracted from the problem statement\n"
        "• Similarity Cutoff (tau = 0.30): Historical projects with S_total >= 30% are flagged as similar projects."
    )

    # Section 8: Review 1 Implementation Status
    style_heading_1(doc.add_paragraph(), "8. Review 1 Implementation Status & Verification")
    
    status_table = doc.add_table(rows=7, cols=3)
    status_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    status_headers = ["System Module", "Implementation Deliverable", "Review 1 Verification Status"]
    for j, h in enumerate(status_headers):
        cell = status_table.cell(0, j)
        set_cell_background(cell, "103666")
        set_cell_margins(cell, top=80, bottom=80, left=100, right=100)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    status_data = [
        ("Database Tier", "setup_database.py", "Completed & Verified: All 4 tables created with indexes, cascades, and seed records."),
        ("Novelty Engine", "novelty_engine.py (686 lines)", "Completed & Verified: Similarity analyzer, component analyzer, and idea generator operational."),
        ("Backend REST API", "backend.py (599 lines)", "Completed & Verified: 10 Flask REST endpoints implemented for auth, submission, and analysis."),
        ("Frontend UI", "app_single_file.py & app.py", "Completed & Verified: 8 interactive screens in Streamlit (Dashboard, Submit, Results, Novelties)."),
        ("Automated Tests", "test_complete_workflow.py", "Completed & Verified: End-to-end integration test passing."),
        ("Version Control", "GitHub Repository", "Completed & Synced: Repository live at https://github.com/jaarya2379-maker/Project-Novelty-Advisor-Management-System")
    ]
    
    for i, row_data in enumerate(status_data):
        row = status_table.rows[i+1]
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=60, bottom=60, left=80, right=80)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if j == 2:
                run.font.bold = True
                run.font.color.rgb = RGBColor(22, 101, 52) # Dark Green
            else:
                run.font.color.rgb = RGBColor(40, 40, 40)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # Section 9: Roadmap
    style_heading_1(doc.add_paragraph(), "9. Project Roadmap & Future Scope")
    style_heading_2(doc.add_paragraph(), "Review 2 Milestones:")
    add_bullet_p(doc, "Dynamic API Binding: ", "Wire the Streamlit interface directly to live MySQL REST endpoints for persistent multi-user storage.")
    add_bullet_p(doc, "Faculty Reviewer Portal: ", "Implement a dedicated faculty view to evaluate proposals, review novelty recommendations, and approve/reject project selections.")
    add_bullet_p(doc, "Database Triggers & Audit Logging: ", "Implement MySQL triggers to maintain an immutable 'project_audit_log' tracking all status changes and timestamps.")

    style_heading_2(doc.add_paragraph(), "Review 3 Milestones:")
    add_bullet_p(doc, "Dense Vector Embeddings: ", "Integrate Sentence-BERT embeddings for advanced semantic concept matching beyond token overlap.")
    add_bullet_p(doc, "Automated PDF Project Dossier Export: ", "Generate formal, downloadable PDF reports certifying project novelty for institutional records.")
    add_bullet_p(doc, "Role-Based Access Control (RBAC): ", "Implement JWT-based session tokens differentiating student and faculty permissions.")

    # Section 10: References
    style_heading_1(doc.add_paragraph(), "10. References (IEEE Format)")
    references = [
        "[1] G. Salton and M. J. McGill, Introduction to Modern Information Retrieval. New York: McGraw-Hill, 1983.",
        "[2] R. Elmasri and S. B. Navathe, Fundamentals of Database Systems, 7th ed. Hoboken, NJ: Pearson, 2015.",
        "[3] A. Silberschatz, H. F. Korth, and S. Sudarshan, Database System Concepts, 7th ed. New York: McGraw-Hill Education, 2019.",
        "[4] D. M. Blei, A. Y. Ng, and M. I. Jordan, 'Latent Dirichlet Allocation,' Journal of Machine Learning Research, vol. 3, pp. 993-1022, 2003.",
        "[5] T. Lancaster and F. Culwin, 'Investigations into plagiarism detection systems: The development of an electronic tool to facilitate the detection of contract cheating,' Research in Education, vol. 74, no. 1, pp. 10-24, 2005.",
        "[6] P. Jaccard, 'The distribution of the flora in the alpine zone,' New Phytologist, vol. 11, no. 2, pp. 37-50, 1912.",
        "[7] N. Reimers and I. Gurevych, 'Sentence-BERT: Sentence Embeddings using Siamese BERT-Networks,' in Proc. Conf. Empirical Methods in Natural Language Processing (EMNLP), 2019.",
        "[8] MySQL 8.0 Reference Manual, JSON Data Type, Indexes, and InnoDB Architecture, Oracle Corporation, 2024."
    ]
    for ref in references:
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(ref)
        run.font.name = "Calibri"
        run.font.size = Pt(9.5)
        run.font.color.rgb = RGBColor(60, 60, 60)
        
    doc.save(output_path)
    print(f"Document successfully created at {output_path}")

if __name__ == "__main__":
    import sys
    out = sys.argv[1] if len(sys.argv) > 1 else "REVIEW_1_REPORT.docx"
    build_review_1_doc(out)
