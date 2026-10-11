import os
import docx
from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

def set_cell_bg(cell, hex_color):
    tcPr = cell._element.get_or_add_tcPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>')
    tcPr.append(shd)

def set_cell_margins(cell, top=90, bottom=90, left=130, right=130):
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

def set_table_borders(table, color="71717A", sz="4", val="single"):
    tblPr = table._element.xpath('w:tblPr')
    if tblPr:
        borders = parse_xml(
            f'<w:tblBorders {nsdecls("w")}>'
            f'<w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'<w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>'
            f'</w:tblBorders>'
        )
        tblPr[0].append(borders)

def setup_page(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.9)
        s.bottom_margin = Inches(0.9)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)
        
        # Header (Black and White)
        header = s.header
        hp = header.paragraphs[0]
        hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        hrun = hp.add_run("DBMS Course Project — Review 1 Report | Project Novelty Advisor")
        hrun.font.name = "Calibri"
        hrun.font.size = Pt(8.5)
        hrun.font.color.rgb = RGBColor(90, 90, 90)
        
        # Footer
        footer = s.footer
        fp = footer.paragraphs[0]
        fp.alignment = WD_ALIGN_PARAGRAPH.CENTER
        frun = fp.add_run("Project Novelty Advisor & Management System — Review 1")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(100, 100, 100)

def h1(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(14)
    r.font.bold = True
    r.font.color.rgb = RGBColor(0, 0, 0)
    return p

def h2(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(12)
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(12)
    r.font.bold = True
    r.font.color.rgb = RGBColor(30, 30, 30)
    return p

def h3(doc, text):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    r = p.add_run(text)
    r.font.name = "Calibri"
    r.font.size = Pt(10.5)
    r.font.bold = True
    r.font.color.rgb = RGBColor(40, 40, 40)
    return p

def body(doc, text="", bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        rb = p.add_run(bold_prefix)
        rb.font.name = "Calibri"
        rb.font.size = Pt(10)
        rb.font.bold = True
        rb.font.color.rgb = RGBColor(0, 0, 0)
    if text:
        rt = p.add_run(text)
        rt.font.name = "Calibri"
        rt.font.size = Pt(10)
        rt.font.color.rgb = RGBColor(35, 35, 35)
    return p

def bullet(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.15
    rb = p.add_run(bold_prefix)
    rb.font.name = "Calibri"
    rb.font.size = Pt(10)
    rb.font.bold = True
    rb.font.color.rgb = RGBColor(0, 0, 0)
    rt = p.add_run(text)
    rt.font.name = "Calibri"
    rt.font.size = Pt(10)
    rt.font.color.rgb = RGBColor(35, 35, 35)
    return p

def callout_bw(doc, title, lines):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_bg(cell, "F4F4F5")
    set_cell_margins(cell, top=90, bottom=90, left=140, right=140)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="D4D4D8"/>'
        f'<w:left w:val="single" w:sz="18" w:space="0" w:color="18181B"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D4D4D8"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="D4D4D8"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.1
    rt = p.add_run(title + "\n")
    rt.font.name = "Calibri"
    rt.font.size = Pt(10)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(0, 0, 0)
    
    for l in lines:
        rc = p.add_run(l + "\n")
        rc.font.name = "Calibri"
        rc.font.size = Pt(9.5)
        rc.font.color.rgb = RGBColor(30, 30, 30)
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def code_box_bw(doc, code_str):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_bg(cell, "FAFAFA")
    set_cell_margins(cell, top=100, bottom=100, left=140, right=140)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="D4D4D8"/>'
        f'<w:left w:val="single" w:sz="16" w:space="0" w:color="27272A"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="D4D4D8"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="D4D4D8"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.line_spacing = 1.05
    run = p.add_run(code_str)
    run.font.name = "Consolas"
    run.font.size = Pt(8.5)
    run.font.color.rgb = RGBColor(24, 24, 27)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

def insert_fig_bw(doc, path, caption, width=Inches(6.2)):
    if os.path.exists(path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(6)
        p_img.paragraph_format.space_after = Pt(3)
        r_img = p_img.add_run()
        r_img.add_picture(path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(6)
        p_cap.paragraph_format.keep_with_next = True
        rc = p_cap.add_run(caption)
        rc.font.name = "Calibri"
        rc.font.size = Pt(9.0)
        rc.font.bold = True
        rc.font.color.rgb = RGBColor(60, 60, 60)

def build_data_dict_bw(doc, cols_data):
    tbl = doc.add_table(rows=len(cols_data)+1, cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="A1A1AA", sz="4")
    col_w = [Inches(1.5), Inches(1.3), Inches(1.5), Inches(2.2)]
    headers = ["Attribute / Column", "SQL Data Type", "Keys & Constraints", "Role & Description"]
    
    hdr = tbl.rows[0]
    for j, h in enumerate(headers):
        c = hdr.cells[j]
        c.width = col_w[j]
        set_cell_bg(c, "E4E4E7") # Light gray header for clean B&W printing
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    for i, (col, dtype, constr, desc) in enumerate(cols_data):
        row = tbl.rows[i+1]
        bg = "F4F4F5" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate([col, dtype, constr, desc]):
            c = row.cells[j]
            c.width = col_w[j]
            set_cell_bg(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=65, right=65)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(20, 20, 20)
            if j == 0:
                r.font.bold = True
            elif j == 2 and ("PRIMARY KEY" in val or "FOREIGN KEY" in val or "UNIQUE" in val):
                r.font.bold = True
    doc.add_paragraph().paragraph_format.space_after = Pt(2)

def generate_report():
    doc = Document()
    setup_page(doc)
    
    # Title & Header
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(4)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    tr = title_p.add_run("PROJECT NOVELTY ADVISOR & MANAGEMENT SYSTEM")
    tr.font.name = "Calibri"
    tr.font.size = Pt(18)
    tr.font.bold = True
    tr.font.color.rgb = RGBColor(0, 0, 0)
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(10)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    sr = sub_p.add_run("DBMS Course Project — Review 1 Design & Progress Report")
    sr.font.name = "Calibri"
    sr.font.size = Pt(11.5)
    sr.font.bold = True
    sr.font.color.rgb = RGBColor(60, 60, 60)
    
    # Metadata Table (Clean B&W)
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="A1A1AA", sz="4")
    col_w = [Inches(2.2), Inches(4.3)]
    
    meta_rows = [
        ("Course Name", "Database Management Systems (DBMS) Course Project"),
        ("Project Title", "Project Novelty Advisor & Management System"),
        ("Faculty Guide / Reviewer", "Dr. Katari Balakrishna"),
        ("Team Member 1", "Aarya Jadhav (25BCE2975) — DB Architecture & Engine Integration"),
        ("Team Member 2", "Diya S (25BAI0235) — Novelty Scoring Logic & Gap Analysis"),
        ("Team Member 3", "Hamsapriya V (25BCE2754) — Web Interface & Proposal Workflows")
    ]
    
    for i, (k, v) in enumerate(meta_rows):
        row = meta_table.rows[i]
        c0, c1 = row.cells[0], row.cells[1]
        c0.width = col_w[0]
        c1.width = col_w[1]
        set_cell_bg(c0, "F4F4F5")
        set_cell_bg(c1, "FFFFFF")
        set_cell_margins(c0, top=45, bottom=45, left=80, right=80)
        set_cell_margins(c1, top=45, bottom=45, left=80, right=80)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(k)
        r0.font.bold = True
        r0.font.size = Pt(8.5)
        r0.font.color.rgb = RGBColor(0, 0, 0)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(v)
        r1.font.size = Pt(8.5)
        r1.font.color.rgb = RGBColor(20, 20, 20)
        if "25B" in v or "Dr." in v:
            r1.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    # 1. Executive Summary & Background
    h1(doc, "1. Executive Summary & Background")
    body(doc, 
        "Every academic year, students in our university submit hundreds of capstone, mini-project, and course proposals. "
        "A common frustration for professors and evaluation committees is seeing the same topics submitted repeatedly across batches. "
        "For instance, almost every semester multiple teams propose predicting credit card fraud with logistic regression, classifying Iris flowers, "
        "or running sentiment analysis on Twitter data using BERT without any unique contribution or real engineering effort."
    )
    body(doc, 
        "In most cases, students do not copy maliciously. They simply do not have visibility into past years' project archives, "
        "nor do they know how to take a familiar topic and push it further into something original. At the same time, faculty evaluators have "
        "to manually read through proposal submissions and try to remember whether a similar project was already evaluated last semester."
    )
    body(doc, 
        "Existing tools do not address this problem. Learning Management Systems (LMS) like Moodle or Canvas store proposals as unindexed attachments. "
        "Plagiarism detectors like Turnitin only look for verbatim copied text; if two students describe the exact same architecture in different words, "
        "Turnitin shows 0% plagiarism. Moreover, traditional tools are strictly punitive—they reject proposals without giving constructive feedback."
    )
    body(doc, 
        "To solve this, we designed the Project Novelty Advisor & Management System. It is a database-backed web application built on MySQL "
        "and normalized in Boyce-Codd Normal Form (BCNF). It stores student accounts, project proposals, similarity analytics, and committed novelty paths. "
        "Instead of just rejecting duplicate proposals, the system analyzes proposals across five structured dimensions (domain, method, dataset, tech stack, keywords), "
        "identifies saturated components, extracts research limitations, and gives students five concrete, practical suggestions to make their project original."
    )

    # 2. Problem Statement & Motivation
    h1(doc, "2. Problem Statement & Motivation")
    h2(doc, "2.1 Real-World Problems We Are Addressing")
    bullet(doc, "Topic Saturation in Academic Projects: ", "Students frequently re-implement textbook examples or past capstones without adding real technical or research value.")
    bullet(doc, "High Cognitive Workload on Faculty: ", "Professors spend significant time cross-checking project titles and abstracts against past archives without any structured search or similarity tools.")
    bullet(doc, "Lack of Constructive Guidance for Students: ", "When a proposal is turned down for being unoriginal, students are usually left without specific advice on how to improve its technical depth.")
    bullet(doc, "Unstructured Historical Archives: ", "Past projects are scattered across Google Forms, spreadsheets, or physical folders, making it impossible to run queries or track technology trends over time.")

    h2(doc, "2.2 What We Aim to Achieve in this Course Project")
    bullet(doc, "Robust Database Architecture: ", "Build a normalized, relational MySQL schema with primary keys, foreign keys, cascades, and indexes to manage proposals, analytics, and novelty choices.")
    bullet(doc, "Transparent Multi-Metric Scoring: ", "Implement an explainable scoring formula combining Jaccard set similarity and token matching across five specific project attributes.")
    bullet(doc, "Actionable Advisory Output: ", "Automatically generate five practical novelty pivots (e.g., cross-domain transfer, edge device optimization, hybrid methods, multimodal extensions) when high similarity is detected.")
    bullet(doc, "Proposal Lifecycle Tracking: ", "Track proposals through verified states ('submitted' → 'analyzed' → 'novelty_selected' → 'approved').")

    # 3. Literature Survey
    h1(doc, "3. Literature Survey")
    body(doc, "To understand how our system compares with existing approaches, we analyzed relevant information retrieval techniques and institutional platforms.")
    
    # B&W Table for Literature
    lit_table = doc.add_table(rows=6, cols=4)
    lit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(lit_table, color="A1A1AA", sz="4")
    col_w_lit = [Inches(1.7), Inches(1.4), Inches(1.6), Inches(1.8)]
    headers_lit = ["System / Author", "Core Technique", "Key Strengths", "Limitations & Gaps"]
    
    hdr_l = lit_table.rows[0]
    for j, h_txt in enumerate(headers_lit):
        c = hdr_l.cells[j]
        c.width = col_w_lit[j]
        set_cell_bg(c, "E4E4E7")
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h_txt)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    lit_rows = [
        ("Salton & McGill (1983) Vector Space Models", "TF-IDF text vectors & cosine similarity", "Fast lexical similarity; reliable baseline for raw text.", "Treats text as an unstructured bag-of-words; misses structured attributes like datasets and tech stacks."),
        ("Blei et al. (2003) Topic Modeling (LDA)", "Probabilistic Latent Dirichlet Allocation", "Finds hidden topics across document collections.", "Computationally heavy; probabilistic outputs lack deterministic explainability needed for academic grading."),
        ("Turnitin / Urkund Plagiarism Checkers", "N-gram fingerprinting & string matching", "Industry standard for detecting word-for-word copying.", "Strictly punitive; cannot detect when different words are used to describe an identical software pipeline."),
        ("Traditional Academic LMS (Moodle, Canvas)", "Relational CRUD database with file attachments", "Manages submissions, student accounts, and gradebooks.", "Zero analytical intelligence; proposals are stored as unindexed static files without semantic search."),
        ("Our Proposed System: Project Novelty Advisor", "Normalized Relational DB + Multi-Metric Jaccard & Rule-Based Advisory", "Relational integrity (BCNF), component saturation detection, transparent scoring, and actionable suggestions.", "Currently rule-based (planned to add dense vector embeddings in Review 3).")
    ]
    
    for i, row_data in enumerate(lit_rows):
        row = lit_table.rows[i+1]
        bg = "F4F4F5" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row_data):
            c = row.cells[j]
            c.width = col_w_lit[j]
            set_cell_bg(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=65, right=65)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.0)
            r.font.color.rgb = RGBColor(20, 20, 20)
            if j == 0:
                r.font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    h2(doc, "3.2 Key Insights from Literature")
    bullet(doc, "Separating Project Attributes: ", "A key lesson from Salton & McGill is that comparing an entire project description as one block of text loses critical details. For example, a student using an established algorithm on a brand-new dataset is very different from a student copying both the algorithm and the dataset. By breaking proposals into domain, method, dataset, tech stack, and keywords, we evaluate originality accurately.")
    bullet(doc, "Using Jaccard Similarity for Tech Stacks: ", "Paul Jaccard's set similarity metric (1912) is ideal for comparing programming languages, frameworks, and libraries: J(A, B) = |A ∩ B| / |A ∪ B|. Order does not matter, making it clean and scale-invariant.")
    bullet(doc, "Hybrid Relational-JSON Storage: ", "As highlighted by Elmasri & Navathe (2015), relational schemas offer strong ACID guarantees, while JSON data types handle dynamic analytical arrays without requiring bloated artificial columns.")

    # 4. What is Novel in This Project
    h1(doc, "4. What is Novel in This Project?")
    bullet(doc, "1. Constructive Advice Instead of Rejection: ", "Plagiarism checkers say: 'Similarity is 70%, proposal rejected.' Our system says: 'Your proposal has 70% similarity because BERT + Twitter Dataset for Sentiment Analysis is heavily overused. Here are 5 ways to make it original: (1) Test on low-resource regional languages; (2) Optimize for edge devices using MobileBERT; (3) Incorporate audio-text multimodal signals.'")
    bullet(doc, "2. Transparent 5-Dimensional Decomposition: ", "We evaluate proposals along five distinct axes: Domain (25%), Method (25%), Dataset (20%), Tech Stack (15%), and Problem Keywords (15%). This makes the similarity score fully explainable.")
    bullet(doc, "3. Saturation & Gap Discovery: ", "The system aggregates historical submissions to flag components that exceed frequency limits and extracts known limitations from previous projects.")
    bullet(doc, "4. Verifiable Novelty Commitment: ", "When a student selects a novelty suggestion, it is saved directly into the database (`selected_novelties`). This creates an agreed-upon baseline that faculty guides can verify during Review 2 and Final Review.")

    # 5. Technical & DBMS Challenges
    h1(doc, "5. Technical & DBMS Challenges Addressed")
    bullet(doc, "Balancing Relational Structure with Variable Analytical Outputs: ", "Student profiles and project headers require strict relational normalization (BCNF). However, the number of similar projects and suggestions changes with each run. We solved this using a hybrid schema: standard relational tables for core records, paired with native MySQL JSON columns for flexible analytical payloads.")
    bullet(doc, "Preventing Search Bottlenecks: ", "Running SQL LIKE '%keyword%' across hundreds of problem statement paragraphs causes slow full table scans. We added MySQL FULLTEXT indexes on project titles and problem statements to enable rapid keyword lookups.")
    bullet(doc, "Maintaining Clean Referential Integrity: ", "If a student account is removed or a proposal is deleted, child records should never be left orphaned. We enforced strict foreign key constraints with ON DELETE CASCADE across all child tables.")
    bullet(doc, "Secure Password Storage: ", "To protect user credentials, student passwords are encrypted using salted PBKDF2 hashing (via Werkzeug) before being stored in the database.")

    # 6. Architecture & Workflows (With Figures)
    doc.add_page_break()
    h1(doc, "6. System Architecture & Process Workflows")
    body(doc, "Our system is organized as a decoupled three-tier architecture, separating user interface, business logic, and relational storage.")
    
    insert_fig_bw(doc, "assets/system_architecture.png", "Figure 1: Three-Tier System Architecture (Streamlit, Flask API, and MySQL InnoDB)")
    
    body(doc, 
        "As shown in Figure 1, the Streamlit frontend communicates with the Flask backend over HTTP REST endpoints using JSON payloads. "
        "The Flask backend handles authentication, validates incoming proposals, queries historical records from MySQL, "
        "calls the novelty engine, and writes the analytical findings back into the database."
    )

    h2(doc, "6.1 End-to-End Execution Flow")
    insert_fig_bw(doc, "assets/process_flowchart.png", "Figure 2: End-to-End System Workflow Flowchart (Submission to Novelty Commitment)")

    body(doc, 
        "Figure 2 outlines the process: from student login, 5-part form ingestion, attribute extraction, and archive searching, "
        "to multi-metric similarity computation, saturation detection, 5-idea generation, and database commitment."
    )

    # 7. DBMS Design & Normalization Study
    doc.add_page_break()
    h1(doc, "7. DBMS Architectural Design & Implementation")
    body(doc, 
        "Our database is engineered to ensure transactional reliability (ACID compliance) and data integrity while supporting fast text search. "
        "Below is the Entity-Relationship (ER) diagram, followed by the data dictionary and formal normalization analysis for every table."
    )
    
    h2(doc, "7.1 Entity-Relationship (ER) Diagram")
    insert_fig_bw(doc, "assets/er_diagram.png", "Figure 3: Entity-Relationship Schema Diagram (Boyce-Codd Normal Form)")

    body(doc, "The ER diagram in Figure 3 models the core relationships:")
    bullet(doc, "STUDENTS to PROJECTS (1:N): ", "One registered student can submit multiple project proposals over different semesters. Every project belongs to exactly one student.")
    bullet(doc, "PROJECTS to ANALYSIS_RESULTS (1:1): ", "Each submitted project proposal produces exactly one comprehensive analytical result record (enforced with a UNIQUE constraint on project_id).")
    bullet(doc, "PROJECTS to SELECTED_NOVELTIES (1:N): ", "A project proposal can record multiple novelty commitments if iterated, with the latest entry representing the active scope.")

    # 7.2 Data Dictionaries and Normalization Proofs
    h2(doc, "7.2 Relational Data Dictionary & Normalization Study (BCNF / 3NF)")
    body(doc, "We evaluated each table against normalization principles to ensure zero insertion, update, or deletion anomalies.")

    # Table 1: students
    h3(doc, "Table 1: students (Student User Accounts & Credentials)")
    students_cols = [
        ("student_id", "INT", "PRIMARY KEY, AUTO_INC", "Unique surrogate key identifying each student."),
        ("username", "VARCHAR(100)", "UNIQUE, NOT NULL", "Unique handle used for login."),
        ("email", "VARCHAR(100)", "UNIQUE, NOT NULL", "Student institutional email address."),
        ("password_hash", "VARCHAR(255)", "NOT NULL", "Salted PBKDF2 cryptographic password digest."),
        ("name", "VARCHAR(100)", "NOT NULL", "Full student name for official academic records."),
        ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIME", "Timestamp when the account was registered.")
    ]
    build_data_dict_bw(doc, students_cols)
    
    callout_bw(doc, "Normalization Proof: students Table", [
        "• Candidate Keys: {student_id}, {username}, {email}",
        "• Functional Dependencies (FDs):",
        "    FD1: student_id → {username, email, password_hash, name, created_at}",
        "    FD2: username → {student_id, email, password_hash, name, created_at}",
        "    FD3: email → {student_id, username, password_hash, name, created_at}",
        "• 1NF: All columns store atomic, scalar values. No repeating fields.",
        "• 2NF: All candidate keys are single attributes (no composite keys), making partial dependencies impossible.",
        "• 3NF: No non-prime attribute determines any other non-prime attribute; zero transitive dependencies.",
        "• BCNF: In all three FDs, the determinants (student_id, username, email) are candidate keys and superkeys.",
        "► Conclusion: Relation is strictly in Boyce-Codd Normal Form (BCNF)."
    ])

    # Table 2: projects
    h3(doc, "Table 2: projects (Project Proposals & Metadata)")
    projects_cols = [
        ("project_id", "INT", "PRIMARY KEY, AUTO_INC", "Unique surrogate key for each project proposal."),
        ("student_id", "INT", "FOREIGN KEY, NOT NULL", "References students(student_id) with ON DELETE CASCADE."),
        ("title", "VARCHAR(255)", "NOT NULL, FULLTEXT", "Proposed project title."),
        ("problem_statement", "TEXT", "NOT NULL, FULLTEXT", "Problem statement description written by the student."),
        ("domain", "VARCHAR(100)", "NULLABLE", "Broad domain (e.g., Computer Vision, NLP, IoT)."),
        ("dataset", "VARCHAR(255)", "NULLABLE", "Name of the target dataset or benchmark."),
        ("method", "VARCHAR(255)", "NULLABLE", "Target methodology or model (e.g., YOLOv8, ResNet)."),
        ("technologies", "JSON", "NULLABLE", "Array of libraries/frameworks (e.g., ['PyTorch', 'OpenCV'])."),
        ("additional_info", "TEXT", "NULLABLE", "Supplementary notes and hardware/deployment details."),
        ("status", "VARCHAR(50)", "DEFAULT 'submitted'", "Status: 'submitted', 'analyzed', 'novelty_selected', 'approved'."),
        ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIME", "Submission timestamp."),
        ("updated_at", "TIMESTAMP", "ON UPDATE CURRENT_TIME", "Timestamp of last status update or edit.")
    ]
    build_data_dict_bw(doc, projects_cols)

    callout_bw(doc, "Normalization Proof: projects Table", [
        "• Candidate Key: {project_id}",
        "• Foreign Key: student_id references students(student_id) ON DELETE CASCADE",
        "• Functional Dependencies (FDs):",
        "    FD1: project_id → {student_id, title, problem_statement, domain, dataset, method, technologies, additional_info, status, created_at, updated_at}",
        "• 1NF: Atomic scalar attributes; technologies stored as native JSON document object.",
        "• 2NF: In 1NF and candidate key is a single attribute (project_id), precluding partial dependencies.",
        "• 3NF: No transitive dependency X → Y where Y is non-prime and X is not a superkey.",
        "• BCNF: The sole determinant (project_id) is the candidate key and superkey.",
        "► Conclusion: Relation is strictly in Boyce-Codd Normal Form (BCNF)."
    ])

    # Table 3: analysis_results
    h3(doc, "Table 3: analysis_results (Analytical Similarity Output)")
    analysis_cols = [
        ("analysis_id", "INT", "PRIMARY KEY, AUTO_INC", "Unique surrogate key for each analysis result."),
        ("project_id", "INT", "FOREIGN KEY, UNIQUE, NOT NULL", "References projects(project_id) ON DELETE CASCADE (1:1)."),
        ("similar_projects", "JSON", "NULLABLE", "Top 5 similar historical projects with percentage similarity."),
        ("common_technologies", "JSON", "NULLABLE", "Overused technologies and institutional usage rates."),
        ("common_datasets", "JSON", "NULLABLE", "Overused datasets and frequency statistics."),
        ("common_methods", "JSON", "NULLABLE", "Overused algorithms and frequency statistics."),
        ("existing_limitations", "JSON", "NULLABLE", "Known literature limitations of matching projects."),
        ("possible_gaps", "JSON", "NULLABLE", "Research gaps and improvement opportunities."),
        ("novelty_suggestions", "JSON", "NULLABLE", "5 algorithmically generated novelty ideas with impact/feasibility."),
        ("analysis_timestamp", "TIMESTAMP", "DEFAULT CURRENT_TIME", "Timestamp when the analysis engine executed.")
    ]
    build_data_dict_bw(doc, analysis_cols)

    callout_bw(doc, "Normalization Proof: analysis_results Table", [
        "• Candidate Keys: {analysis_id}, {project_id} (enforced via UNIQUE constraint)",
        "• Foreign Key: project_id references projects(project_id) ON DELETE CASCADE",
        "• Functional Dependencies (FDs):",
        "    FD1: analysis_id → {project_id, similar_projects, common_technologies, common_datasets, common_methods, existing_limitations, possible_gaps, novelty_suggestions, analysis_timestamp}",
        "    FD2: project_id → {analysis_id, similar_projects, common_technologies, common_datasets, common_methods, existing_limitations, possible_gaps, novelty_suggestions, analysis_timestamp}",
        "• 1NF, 2NF, 3NF: Fully satisfied with atomic keys and zero transitive dependencies.",
        "• BCNF: Both determinants (analysis_id, project_id) are candidate keys.",
        "► Conclusion: Relation is strictly in Boyce-Codd Normal Form (BCNF)."
    ])

    # Table 4: selected_novelties
    h3(doc, "Table 4: selected_novelties (Student Roadmap Commitment)")
    novelties_cols = [
        ("novelty_id", "INT", "PRIMARY KEY, AUTO_INC", "Unique surrogate key for the selected novelty record."),
        ("project_id", "INT", "FOREIGN KEY, NOT NULL", "References projects(project_id) ON DELETE CASCADE."),
        ("novelty_title", "VARCHAR(255)", "NULLABLE", "Title of the student's chosen novelty enhancement."),
        ("novelty_description", "TEXT", "NULLABLE", "Technical specification of the chosen novelty pivot."),
        ("novelty_impact", "VARCHAR(50)", "NULLABLE", "Expected academic/practical impact rating ('High', 'Medium')."),
        ("novelty_feasibility", "VARCHAR(50)", "NULLABLE", "Implementation feasibility rating ('High', 'Medium')."),
        ("notes", "TEXT", "NULLABLE", "Student implementation notes and planned milestones."),
        ("selected_at", "TIMESTAMP", "DEFAULT CURRENT_TIME", "Timestamp when student locked in the selection.")
    ]
    build_data_dict_bw(doc, novelties_cols)

    callout_bw(doc, "Normalization Proof: selected_novelties Table", [
        "• Candidate Key: {novelty_id}",
        "• Foreign Key: project_id references projects(project_id) ON DELETE CASCADE",
        "• Functional Dependencies (FDs):",
        "    FD1: novelty_id → {project_id, novelty_title, novelty_description, novelty_impact, novelty_feasibility, notes, selected_at}",
        "• BCNF: The determinant (novelty_id) is the candidate key and superkey.",
        "► Conclusion: Relation is strictly in Boyce-Codd Normal Form (BCNF)."
    ])

    # 7.3 SQL DDL Code
    h2(doc, "7.3 MySQL Data Definition Language (DDL)")
    body(doc, "Below is the SQL script used to create the database schema, foreign key cascades, and FULLTEXT indexes:")
    
    ddl_sql = (
        "-- 1. Students Table\n"
        "CREATE TABLE IF NOT EXISTS students (\n"
        "    student_id INT AUTO_INCREMENT PRIMARY KEY,\n"
        "    username VARCHAR(100) UNIQUE NOT NULL,\n"
        "    email VARCHAR(100) UNIQUE NOT NULL,\n"
        "    password_hash VARCHAR(255) NOT NULL,\n"
        "    name VARCHAR(100) NOT NULL,\n"
        "    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP\n"
        ") ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;\n\n"
        "-- 2. Projects Table\n"
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
        "-- 3. Analysis Results Table\n"
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
        "-- 4. Selected Novelties Table\n"
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
    code_box_bw(doc, ddl_sql)

    # 8. Implementation Status
    h1(doc, "8. Review 1 Implementation Status & Testing")
    body(doc, "For Review 1, our primary deliverables are operational and verified on local environments:")
    
    st_table = doc.add_table(rows=7, cols=3)
    st_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(st_table, color="A1A1AA", sz="4")
    col_w_st = [Inches(1.8), Inches(1.8), Inches(2.8)]
    st_hdrs = ["System Component", "Source Deliverable", "Verification Status"]
    
    hdr_s = st_table.rows[0]
    for j, txt in enumerate(st_hdrs):
        c = hdr_s.cells[j]
        c.width = col_w_st[j]
        set_cell_bg(c, "E4E4E7")
        set_cell_margins(c, top=70, bottom=70, left=70, right=70)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(txt)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(0, 0, 0)
        
    st_rows = [
        ("Database Setup", "setup_database.py", "Completed: All 4 tables created with indexes, cascades, and sample data."),
        ("Novelty Engine", "novelty_engine.py (686 lines)", "Completed: Attribute extractor, 5-metric similarity analyzer, and idea generator verified."),
        ("Flask REST Server", "backend.py (599 lines)", "Completed: 10 REST endpoints implemented for authentication, submission, and analytics."),
        ("Streamlit Web App", "app_single_file.py & app.py", "Completed: 8 interactive pages (Dashboard, Submit, Results, Novelties, My Projects)."),
        ("Automated Tests", "test_complete_workflow.py", "Verified: Full end-to-end integration test passes successfully."),
        ("Version Control", "GitHub Repository", "Completed: Project synced on GitHub at jaarya2379-maker/Project-Novelty-Advisor-Management-System")
    ]
    
    for i, row_data in enumerate(st_rows):
        row = st_table.rows[i+1]
        bg = "F4F4F5" if i % 2 == 1 else "FFFFFF"
        for j, val in enumerate(row_data):
            c = row.cells[j]
            c.width = col_w_st[j]
            set_cell_bg(c, bg)
            set_cell_margins(c, top=50, bottom=50, left=65, right=65)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor(20, 20, 20)
            if j == 2:
                r.font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)

    # 9. Roadmap
    h1(doc, "9. Project Roadmap & Future Scope")
    h2(doc, "Review 2 Goals:")
    bullet(doc, "Live MySQL Connection in Frontend: ", "Connect the Streamlit interface dynamically to the running Flask backend endpoints, moving from session data to persistent MySQL transactions.")
    bullet(doc, "Faculty Reviewer Dashboard: ", "Add a dedicated role for professors to view submitted proposals, review student-selected novelties, and approve or request revisions.")
    bullet(doc, "Database Audit Logging: ", "Implement MySQL triggers on the projects table to automatically log all status updates and timestamps into an audit table.")

    h2(doc, "Review 3 Goals:")
    bullet(doc, "Dense Sentence Embeddings: ", "Integrate Sentence-BERT embeddings to compare semantic problem meanings beyond exact keyword tokens.")
    bullet(doc, "PDF Novelty Dossier Export: ", "Add an automated download button in Streamlit to generate a formal PDF novelty certificate for grading records.")
    bullet(doc, "JWT Role-Based Access Control: ", "Implement JSON Web Tokens (JWT) for secure session management between frontend and backend.")

    # 10. References
    h1(doc, "10. References (IEEE Format)")
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
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        r = p.add_run(ref)
        r.font.name = "Calibri"
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(40, 40, 40)
        
    out = "REVIEW_1_REPORT.docx"
    doc.save(out)
    print(f"B&W Human Report created successfully at {out}")

if __name__ == "__main__":
    generate_report()
