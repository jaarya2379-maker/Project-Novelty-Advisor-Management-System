import os
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

def set_cell_margins(cell, top=100, bottom=100, left=140, right=140):
    """Set internal padding for a cell in dxa (1 pt = 20 dxa)."""
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

def set_table_borders(table, color="D1D5DB", sz="4", val="single"):
    """Apply neat light borders to a table."""
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

def add_header_footer(doc):
    for s in doc.sections:
        s.top_margin = Inches(0.9)
        s.bottom_margin = Inches(0.9)
        s.left_margin = Inches(0.9)
        s.right_margin = Inches(0.9)
        
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
        frun = fp.add_run("Project Novelty Advisor & Management System — Review 1 Design & Progress Report")
        frun.font.name = "Calibri"
        frun.font.size = Pt(8.5)
        frun.font.color.rgb = RGBColor(140, 140, 140)

def style_heading_1(p, text):
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(15)
    run.font.bold = True
    run.font.color.rgb = RGBColor(16, 54, 102) # Deep Navy
    return run

def style_heading_2(p, text):
    p.paragraph_format.space_before = Pt(13)
    p.paragraph_format.space_after = Pt(4)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(12.5)
    run.font.bold = True
    run.font.color.rgb = RGBColor(37, 99, 235) # Accent Blue
    return run

def style_heading_3(p, text):
    p.paragraph_format.space_before = Pt(9)
    p.paragraph_format.space_after = Pt(2)
    p.paragraph_format.keep_with_next = True
    run = p.add_run(text)
    run.font.name = "Calibri"
    run.font.size = Pt(11)
    run.font.bold = True
    run.font.color.rgb = RGBColor(51, 65, 85) # Slate
    return run

def add_body_p(doc, text="", bold_prefix=None, space_after=4):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.line_spacing = 1.15
    if bold_prefix:
        r_bold = p.add_run(bold_prefix)
        r_bold.font.name = "Calibri"
        r_bold.font.size = Pt(10)
        r_bold.font.bold = True
        r_bold.font.color.rgb = RGBColor(15, 23, 42)
    if text:
        r_text = p.add_run(text)
        r_text.font.name = "Calibri"
        r_text.font.size = Pt(10)
        r_text.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_bullet_p(doc, bold_prefix, text):
    p = doc.add_paragraph(style='List Bullet')
    p.paragraph_format.space_after = Pt(2.5)
    p.paragraph_format.line_spacing = 1.15
    r_bold = p.add_run(bold_prefix)
    r_bold.font.name = "Calibri"
    r_bold.font.size = Pt(10)
    r_bold.font.bold = True
    r_bold.font.color.rgb = RGBColor(15, 23, 42)
    r_text = p.add_run(text)
    r_text.font.name = "Calibri"
    r_text.font.size = Pt(10)
    r_text.font.color.rgb = RGBColor(51, 65, 85)
    return p

def add_callout_box(doc, title, content_lines, border_color="2563EB", bg_color="EFF6FF"):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, bg_color)
    set_cell_margins(cell, top=100, bottom=100, left=160, right=160)
    
    tcPr = cell._element.get_or_add_tcPr()
    borders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:left w:val="single" w:sz="18" w:space="0" w:color="{border_color}"/>'
        f'<w:bottom w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'<w:right w:val="single" w:sz="4" w:space="0" w:color="CBD5E1"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(borders)
    
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(3)
    p.paragraph_format.line_spacing = 1.1
    rt = p.add_run(title + "\n")
    rt.font.name = "Calibri"
    rt.font.size = Pt(10.5)
    rt.font.bold = True
    rt.font.color.rgb = RGBColor(16, 54, 102)
    
    for l in content_lines:
        rc = p.add_run(l + "\n")
        rc.font.name = "Calibri"
        rc.font.size = Pt(9.5)
        rc.font.color.rgb = RGBColor(30, 41, 59)
    doc.add_paragraph().paragraph_format.space_after = Pt(3)

def add_code_block(doc, code_text):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = tbl.cell(0, 0)
    set_cell_background(cell, "F8FAFC")
    set_cell_margins(cell, top=120, bottom=120, left=160, right=160)
    
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

def insert_figure(doc, img_path, caption_text, width=Inches(6.2)):
    if os.path.exists(img_path):
        p_img = doc.add_paragraph()
        p_img.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_img.paragraph_format.space_before = Pt(8)
        p_img.paragraph_format.space_after = Pt(4)
        run_img = p_img.add_run()
        run_img.add_picture(img_path, width=width)
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(8)
        p_cap.paragraph_format.keep_with_next = True
        r_cap = p_cap.add_run(caption_text)
        r_cap.font.name = "Calibri"
        r_cap.font.size = Pt(9.5)
        r_cap.font.bold = True
        r_cap.font.color.rgb = RGBColor(71, 85, 105)

def build_data_dictionary_table(doc, table_name, columns_data):
    """
    Build a clean data dictionary table.
    columns_data: list of tuples (Col Name, Type, Constraints, Description)
    """
    tbl = doc.add_table(rows=len(columns_data) + 1, cols=4)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(tbl, color="CBD5E1", sz="4")
    
    col_widths = [Inches(1.5), Inches(1.3), Inches(1.5), Inches(2.2)]
    headers = ["Attribute / Column", "SQL Data Type", "Keys & Constraints", "Role & Description"]
    
    # Header Row
    hdr_row = tbl.rows[0]
    for j, h in enumerate(headers):
        c = hdr_row.cells[j]
        c.width = col_widths[j]
        set_cell_background(c, "103666") # Dark Navy
        set_cell_margins(c, top=80, bottom=80, left=80, right=80)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        r = p.add_run(h)
        r.font.bold = True
        r.font.size = Pt(8.5)
        r.font.color.rgb = RGBColor(255, 255, 255)
        
    for i, (col, dtype, constr, desc) in enumerate(columns_data):
        row = tbl.rows[i + 1]
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate([col, dtype, constr, desc]):
            c = row.cells[j]
            c.width = col_widths[j]
            set_cell_background(c, bg)
            set_cell_margins(c, top=60, bottom=60, left=70, right=70)
            p = c.paragraphs[0]
            r = p.add_run(val)
            r.font.size = Pt(8.5)
            if j == 0:
                r.font.bold = True
                r.font.color.rgb = RGBColor(16, 54, 102)
            elif j == 2 and ("PRIMARY KEY" in val or "FOREIGN KEY" in val or "UNIQUE" in val):
                r.font.bold = True
                r.font.color.rgb = RGBColor(37, 99, 235)
            else:
                r.font.color.rgb = RGBColor(51, 65, 85)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(4)

# ==========================================
# MAIN DOCUMENT GENERATOR
# ==========================================
def generate_complete_doc():
    doc = Document()
    add_header_footer(doc)
    
    # ----------------------------------------------------
    # COVER / TITLE HEADER CARD
    # ----------------------------------------------------
    title_p = doc.add_paragraph()
    title_p.paragraph_format.space_before = Pt(8)
    title_p.paragraph_format.space_after = Pt(2)
    title_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    trun = title_p.add_run("PROJECT NOVELTY ADVISOR & MANAGEMENT SYSTEM")
    trun.font.name = "Calibri"
    trun.font.size = Pt(20)
    trun.font.bold = True
    trun.font.color.rgb = RGBColor(16, 54, 102)
    
    sub_p = doc.add_paragraph()
    sub_p.paragraph_format.space_after = Pt(12)
    sub_p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    srun = sub_p.add_run("DBMS Course Project — Review 1 Design & Progress Report")
    srun.font.name = "Calibri"
    srun.font.size = Pt(12)
    srun.font.bold = True
    srun.font.color.rgb = RGBColor(37, 99, 235)
    
    # Metadata Card Table
    meta_table = doc.add_table(rows=6, cols=2)
    meta_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(meta_table, color="CBD5E1", sz="4")
    col_widths = [Inches(2.2), Inches(4.3)]
    
    meta_data = [
        ("Course", "Database Management Systems (DBMS) Course Project"),
        ("Project Title", "Project Novelty Advisor & Management System"),
        ("Faculty Guide / Reviewer", "Dr. Katari Balakrishna"),
        ("Team Member 1", "Aarya Jadhav (Reg No: 25BCE2975) — DB Architecture & Engine"),
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
        set_cell_margins(c0, top=50, bottom=50, left=90, right=90)
        set_cell_margins(c1, top=50, bottom=50, left=90, right=90)
        
        p0 = c0.paragraphs[0]
        p0.paragraph_format.space_after = Pt(0)
        r0 = p0.add_run(label)
        r0.font.bold = True
        r0.font.size = Pt(9.0)
        r0.font.color.rgb = RGBColor(16, 54, 102)
        
        p1 = c1.paragraphs[0]
        p1.paragraph_format.space_after = Pt(0)
        r1 = p1.add_run(val)
        r1.font.size = Pt(9.0)
        r1.font.color.rgb = RGBColor(30, 41, 59)
        if "25B" in val or "Dr." in val:
            r1.font.bold = True

    doc.add_paragraph().paragraph_format.space_after = Pt(8)
    
    # ----------------------------------------------------
    # SECTION 1: EXECUTIVE SUMMARY / ABSTRACT
    # ----------------------------------------------------
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
    
    # ----------------------------------------------------
    # SECTION 2: PROBLEM STATEMENT & MOTIVATION
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # SECTION 3: LITERATURE SURVEY
    # ----------------------------------------------------
    style_heading_1(doc.add_paragraph(), "3. Literature Survey")
    add_body_p(doc, "A comprehensive survey of information retrieval models, document classification algorithms, and commercial plagiarism platforms was conducted to contextualize the novelty detector within academic research.")
    
    # Literature Matrix Table
    lit_table = doc.add_table(rows=6, cols=4)
    lit_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(lit_table, color="CBD5E1", sz="4")
    col_widths_lit = [Inches(1.7), Inches(1.4), Inches(1.6), Inches(1.8)]
    headers = ["System / Author", "Core Technique", "Key Strengths", "Critical Limitations & Gaps"]
    
    for j, h in enumerate(headers):
        cell = lit_table.cell(0, j)
        cell.width = col_widths_lit[j]
        set_cell_background(cell, "103666")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(8.5)
        run.font.color.rgb = RGBColor(255, 255, 255)
        
    lit_data = [
        ("Salton & McGill (1983) Vector Space Model", "TF-IDF vectors & Cosine similarity", "Fast lexical similarity; robust baseline for plain text search.", "Completely ignores structured attributes (dataset, tech stack); purely lexical; misses conceptual duplication."),
        ("Blei et al. (2003) Topic Modeling (LDA)", "Probabilistic Latent Dirichlet Allocation", "Uncovers latent thematic topics across unstructured documents.", "High compute overhead; probabilistic outputs lack deterministic explainability needed for academic scoring."),
        ("Commercial Plagiarism Engines (Turnitin, Urkund)", "N-gram fingerprinting & string matching", "Industry standard for detecting verbatim or paraphrased copied text.", "Strictly punitive; cannot detect when two distinct text descriptions describe the exact same underlying ML pipeline."),
        ("Traditional Academic LMS (Moodle, Canvas)", "Relational CRUD with static file blob storage", "Strong student authentication and assignment hand-in workflows.", "Zero analytical intelligence; proposals stored as unindexed blobs without metadata or similarity indexing."),
        ("Proposed System: Project Novelty Advisor", "Normalized Relational DB + Multi-Metric Jaccard & Component Saturation", "Relational integrity (BCNF), multi-attribute decomposition, overused component detection, and constructive novelty advice.", "Currently rule-based; scheduled for dense vector embedding integration in Review 3.")
    ]
    
    for i, row_data in enumerate(lit_data):
        row = lit_table.rows[i+1]
        bg = "F8FAFC" if i % 2 == 0 else "FFFFFF"
        for j, val in enumerate(row_data):
            cell = row.cells[j]
            cell.width = col_widths_lit[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.0)
            run.font.color.rgb = RGBColor(30, 41, 59)
            if j == 0:
                run.font.bold = True
                
    doc.add_paragraph().paragraph_format.space_after = Pt(6)
    
    style_heading_2(doc.add_paragraph(), "3.2 Detailed Literature Synthesis")
    add_bullet_p(doc, "Decomposing Projects into Orthogonal Dimensions: ", 
        "Salton & McGill demonstrated the effectiveness of vector space retrieval, but treating an entire project proposal as a single bag-of-words obscures critical technical distinctions. A project utilizing a standard dataset with a novel architecture must not be penalized identically to one replicating both dataset and architecture.")
    add_bullet_p(doc, "Set-Theoretic Similarity for Technology Stacks: ", 
        "Following Paul Jaccard's mathematical formulations (1912), technical stacks (e.g., PyTorch, OpenCV, Flask, Docker) are discrete finite sets where order is irrelevant. The Jaccard Index provides an optimal, normalized, scale-invariant similarity measure.")
    add_bullet_p(doc, "Database Systems for Semi-Structured Analytical Data: ", 
        "As established by Elmasri & Navathe (2015), modern data architectures benefit from a hybrid model: strict Boyce-Codd Normal Form for transactional integrity (students, proposals, audits) paired with native JSON columns for dynamic, multi-dimensional analytical outputs.")

    # ----------------------------------------------------
    # SECTION 4: WHAT IS NOVEL IN THIS PROJECT
    # ----------------------------------------------------
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

    # ----------------------------------------------------
    # SECTION 5: TECHNICAL CHALLENGES
    # ----------------------------------------------------
    style_heading_1(doc.add_paragraph(), "5. Technical & DBMS Challenges Addressed")
    add_bullet_p(doc, "Hybrid Relational & Semi-Structured Data Storage: ", 
        "Student records and project headers require strict relational normalization (BCNF), whereas similarity rankings and generated suggestions vary in length per project. This was solved by utilizing MySQL InnoDB tables with native JSON columns for analytical payloads.")
    add_bullet_p(doc, "Eliminating Text Search Bottlenecks: ", 
        "Using SQL 'LIKE %keyword%' across large text fields causes full table scans (O(N)). The system implements MySQL FULLTEXT indexes on 'title' and 'problem_statement' to enable sub-millisecond inverted-index boolean searches.")
    add_bullet_p(doc, "Referential Integrity & Cascading Constraints: ", 
        "To prevent orphan records upon student graduation or proposal deletion, strict ON DELETE CASCADE foreign key constraints were engineered across students -> projects -> analysis_results and projects -> selected_novelties.")
    add_bullet_p(doc, "Cryptographic Credential Security: ", 
        "Student credentials are protected using salted PBKDF2 cryptographic password hashing (via Werkzeug) prior to persistence, ensuring plaintext passwords never touch the database.")

    # ----------------------------------------------------
    # SECTION 6: SYSTEM ARCHITECTURE & DIAGRAMS
    # ----------------------------------------------------
    doc.add_page_break()
    style_heading_1(doc.add_paragraph(), "6. System Architecture & Workflow")
    add_body_p(doc, "The system follows a decoupled 3-tier enterprise architecture separating UI presentation, business and intelligence logic, and ACID-compliant relational data management.")
    
    insert_figure(doc, "assets/system_architecture.png", "Figure 1: 3-Tier Enterprise System Architecture Diagram")
    
    add_body_p(doc, 
        "As illustrated in Figure 1, the Presentation Tier (Streamlit) interacts with the Application Tier (Flask) exclusively through structured JSON payloads over RESTful HTTP APIs. "
        "The Application Tier acts as an orchestration gateway: it validates incoming proposal payloads, queries the MySQL Database for historical benchmarks, triggers the Novelty Analysis Engine, "
        "and writes the resulting multi-metric similarity scores and generated novelty ideas back to the data tier."
    )
    
    style_heading_2(doc.add_paragraph(), "6.1 End-to-End System Workflow")
    insert_figure(doc, "assets/process_flowchart.png", "Figure 2: End-to-End Project Novelty & Management Workflow Flowchart")
    
    add_body_p(doc, 
        "Figure 2 illustrates the step-by-step processing lifecycle: from student authentication, multi-attribute form ingestion, fulltext candidate extraction, "
        "weighted similarity computation, component saturation analysis, to actionable novelty recommendation generation, student selection, and database commitment."
    )

    # ----------------------------------------------------
    # SECTION 7: DBMS DESIGN & NORMALIZATION (EXPANDED & CLEAR)
    # ----------------------------------------------------
    doc.add_page_break()
    style_heading_1(doc.add_paragraph(), "7. DBMS Architectural Design & Implementation")
    add_body_p(doc, 
        "A foundational component of this project is the engineering of an ACID-compliant, highly normalized relational database. "
        "The database is structured to balance strict relational consistency (for student profiles, project ownership, and selection history) "
        "with flexible JSON attribute storage (for dynamic similarity matrices and generated novelty suggestions)."
    )
    
    style_heading_2(doc.add_paragraph(), "7.1 Entity-Relationship (ER) Schema Diagram")
    insert_figure(doc, "assets/er_diagram.png", "Figure 3: Entity-Relationship (ER) Schema Diagram with Referential Constraints")

    add_body_p(doc, "The ER model in Figure 3 captures the structural relationships among entities:")
    add_bullet_p(doc, "STUDENTS to PROJECTS (1:N): ", "One student submits zero or more project proposals. Each project proposal is uniquely authored by exactly one student (FK student_id, ON DELETE CASCADE).")
    add_bullet_p(doc, "PROJECTS to ANALYSIS_RESULTS (1:1): ", "Each submitted project proposal generates exactly one comprehensive analysis result snapshot (FK project_id with UNIQUE constraint, ON DELETE CASCADE).")
    add_bullet_p(doc, "PROJECTS to SELECTED_NOVELTIES (1:N): ", "A project can have historical novelty selections if iterated, with the latest entry representing the active committed roadmap (FK project_id, ON DELETE CASCADE).")

    # ----------------------------------------------------
    # SUBSECTION 7.2: DATA DICTIONARY & NORMALIZATION STUDY
    # ----------------------------------------------------
    style_heading_2(doc.add_paragraph(), "7.2 Relational Data Dictionary & Normalization Study (BCNF / 3NF)")
    add_body_p(doc, "Below is the detailed attribute-level data dictionary and mathematical normalization proofs for each entity in the database:")

    # Table 1: STUDENTS
    style_heading_3(doc.add_paragraph(), "Entity 1: STUDENTS (User Profiles & Credentials)")
    students_cols = [
        ("student_id", "INT", "PRIMARY KEY, AUTO_INC", "Unique surrogate key identifying each registered student."),
        ("username", "VARCHAR(100)", "UNIQUE, NOT NULL", "Unique handle for system login and identification."),
        ("email", "VARCHAR(100)", "UNIQUE, NOT NULL", "Institutional email address for notifications."),
        ("password_hash", "VARCHAR(255)", "NOT NULL", "Salted PBKDF2 cryptographic password digest."),
        ("name", "VARCHAR(100)", "NOT NULL", "Full legal student name for academic records."),
        ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIME", "System registration timestamp.")
    ]
    build_data_dictionary_table(doc, "students", students_cols)
    
    add_callout_box(doc, "Normalization Proof: STUDENTS Table", [
        "• Candidate Keys: {student_id}, {username}, {email}",
        "• Functional Dependencies (FDs):",
        "    FD1: student_id → {username, email, password_hash, name, created_at}",
        "    FD2: username → {student_id, email, password_hash, name, created_at}",
        "    FD3: email → {student_id, username, password_hash, name, created_at}",
        "• 1NF: All attributes are atomic and single-valued; no repeating groups.",
        "• 2NF: The candidate keys are all single attributes (no composite keys), so no partial dependencies can exist.",
        "• 3NF: No non-prime attribute determines any other non-prime attribute; zero transitive dependencies.",
        "• BCNF: In all three FDs (FD1, FD2, FD3), the determinants (student_id, username, email) are candidate keys.",
        "► Conclusion: Relation is strictly in Boyce-Codd Normal Form (BCNF)."
    ], border_color="103666", bg_color="F0F4F8")

    # Table 2: PROJECTS
    style_heading_3(doc.add_paragraph(), "Entity 2: PROJECTS (Project Proposals & Metadata)")
    projects_cols = [
        ("project_id", "INT", "PRIMARY KEY, AUTO_INC", "Unique surrogate key identifying the project proposal."),
        ("student_id", "INT", "FOREIGN KEY, NOT NULL", "References students(student_id) with ON DELETE CASCADE."),
        ("title", "VARCHAR(255)", "NOT NULL, FULLTEXT", "Title of the proposed project."),
        ("problem_statement", "TEXT", "NOT NULL, FULLTEXT", "Detailed narrative describing the technical problem."),
        ("domain", "VARCHAR(100)", "NULLABLE", "High-level domain (e.g., Computer Vision, Medical AI)."),
        ("dataset", "VARCHAR(255)", "NULLABLE", "Name of the target benchmark or custom dataset."),
        ("method", "VARCHAR(255)", "NULLABLE", "Target methodology or algorithm (e.g., YOLOv8, ResNet)."),
        ("technologies", "JSON", "NULLABLE", "JSON array of libraries/tools (e.g., ['PyTorch', 'OpenCV'])."),
        ("additional_info", "TEXT", "NULLABLE", "Supplementary contextual notes and implementation details."),
        ("status", "VARCHAR(50)", "DEFAULT 'submitted'", "Lifecycle status: 'submitted', 'analyzed', 'novelty_selected', 'approved'."),
        ("created_at", "TIMESTAMP", "DEFAULT CURRENT_TIME", "Proposal submission timestamp."),
        ("updated_at", "TIMESTAMP", "ON UPDATE CURRENT_TIME", "Timestamp of last modification or status transition.")
    ]
    build_data_dictionary_table(doc, "projects", projects_cols)

    add_callout_box(doc, "Normalization Proof: PROJECTS Table", [
        "• Candidate Key: {project_id}",
        "• Foreign Key: student_id references students(student_id) ON DELETE CASCADE",
        "• Functional Dependencies (FDs):",
        "    FD1: project_id → {student_id, title, problem_statement, domain, dataset, method, technologies, additional_info, status, created_at, updated_at}",
        "• 1NF: Atomic scalar attributes; technologies stored as native JSON document object.",
        "• 2NF: In 1NF and candidate key is a single attribute (project_id), precluding partial dependencies.",
        "• 3NF: No transitive dependency X → Y where Y is non-prime and X is not a superkey.",
        "• BCNF: The sole determinant (project_id) is the candidate key and superkey.",
        "► Conclusion: Relation is strictly in Boyce-Codd Normal Form (BCNF)."
    ], border_color="2563EB", bg_color="EFF6FF")

    # Table 3: ANALYSIS_RESULTS
    style_heading_3(doc.add_paragraph(), "Entity 3: ANALYSIS_RESULTS (Analytical Similarity Output)")
    analysis_cols = [
        ("analysis_id", "INT", "PRIMARY KEY, AUTO_INC", "Unique surrogate key identifying each analysis result snapshot."),
        ("project_id", "INT", "FOREIGN KEY, UNIQUE, NOT NULL", "References projects(project_id) ON DELETE CASCADE (1:1 relation)."),
        ("similar_projects", "JSON", "NULLABLE", "Top 5 similar historical projects with percentage similarity."),
        ("common_technologies", "JSON", "NULLABLE", "Identified overused technologies and institutional usage rates."),
        ("common_datasets", "JSON", "NULLABLE", "Identified overused datasets and frequency statistics."),
        ("common_methods", "JSON", "NULLABLE", "Identified overused algorithms and frequency statistics."),
        ("existing_limitations", "JSON", "NULLABLE", "Extracted known literature limitations of matching projects."),
        ("possible_gaps", "JSON", "NULLABLE", "Discovered research gaps and improvement opportunities."),
        ("novelty_suggestions", "JSON", "NULLABLE", "5 algorithmically generated novelty ideas with impact & feasibility."),
        ("analysis_timestamp", "TIMESTAMP", "DEFAULT CURRENT_TIME", "Timestamp when the analysis engine executed.")
    ]
    build_data_dictionary_table(doc, "analysis_results", analysis_cols)

    add_callout_box(doc, "Normalization Proof: ANALYSIS_RESULTS Table", [
        "• Candidate Keys: {analysis_id}, {project_id} (enforced via UNIQUE constraint)",
        "• Foreign Key: project_id references projects(project_id) ON DELETE CASCADE",
        "• Functional Dependencies (FDs):",
        "    FD1: analysis_id → {project_id, similar_projects, common_technologies, common_datasets, common_methods, existing_limitations, possible_gaps, novelty_suggestions, analysis_timestamp}",
        "    FD2: project_id → {analysis_id, similar_projects, common_technologies, common_datasets, common_methods, existing_limitations, possible_gaps, novelty_suggestions, analysis_timestamp}",
        "• 1NF, 2NF, 3NF: Fully satisfied with atomic keys and zero transitive dependencies.",
        "• BCNF: Both determinants (analysis_id, project_id) are candidate keys.",
        "► Conclusion: Relation is strictly in Boyce-Codd Normal Form (BCNF)."
    ], border_color="166534", bg_color="F0FDF4")

    # Table 4: SELECTED_NOVELTIES
    style_heading_3(doc.add_paragraph(), "Entity 4: SELECTED_NOVELTIES (Student Roadmap Commitment)")
    novelties_cols = [
        ("novelty_id", "INT", "PRIMARY KEY, AUTO_INC", "Unique surrogate key identifying the selected novelty commitment."),
        ("project_id", "INT", "FOREIGN KEY, NOT NULL", "References projects(project_id) ON DELETE CASCADE."),
        ("novelty_title", "VARCHAR(255)", "NULLABLE", "Title of the student's chosen novelty enhancement."),
        ("novelty_description", "TEXT", "NULLABLE", "Detailed technical specification of the chosen novelty pivot."),
        ("novelty_impact", "VARCHAR(50)", "NULLABLE", "Expected academic/practical impact rating (e.g., 'High')."),
        ("novelty_feasibility", "VARCHAR(50)", "NULLABLE", "Implementation feasibility rating (e.g., 'Medium', 'High')."),
        ("notes", "TEXT", "NULLABLE", "Student's customized implementation notes and roadmap."),
        ("selected_at", "TIMESTAMP", "DEFAULT CURRENT_TIME", "Timestamp when student locked in the novelty selection.")
    ]
    build_data_dictionary_table(doc, "selected_novelties", novelties_cols)

    add_callout_box(doc, "Normalization Proof: SELECTED_NOVELTIES Table", [
        "• Candidate Key: {novelty_id}",
        "• Foreign Key: project_id references projects(project_id) ON DELETE CASCADE",
        "• Functional Dependencies (FDs):",
        "    FD1: novelty_id → {project_id, novelty_title, novelty_description, novelty_impact, novelty_feasibility, notes, selected_at}",
        "• BCNF: The determinant (novelty_id) is the candidate key and superkey.",
        "► Conclusion: Relation is strictly in Boyce-Codd Normal Form (BCNF)."
    ], border_color="6D28D9", bg_color="FAF5FF")

    # ----------------------------------------------------
    # SUBSECTION 7.3: DDL SPECIFICATION
    # ----------------------------------------------------
    style_heading_2(doc.add_paragraph(), "7.3 Data Definition Language (DDL) Specification")
    add_body_p(doc, "The MySQL DDL commands below demonstrate the creation of tables, foreign key constraints with ON DELETE CASCADE, and performance indexing:")
    
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
    add_code_block(doc, ddl_sql)

    # ----------------------------------------------------
    # SECTION 8: IMPLEMENTATION STATUS & QA
    # ----------------------------------------------------
    style_heading_1(doc.add_paragraph(), "8. Review 1 Implementation Status & Verification")
    
    status_table = doc.add_table(rows=7, cols=3)
    status_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(status_table, color="CBD5E1", sz="4")
    col_widths_st = [Inches(1.8), Inches(1.8), Inches(2.8)]
    
    status_headers = ["System Module", "Implementation Deliverable", "Review 1 Verification Status"]
    for j, h in enumerate(status_headers):
        cell = status_table.cell(0, j)
        cell.width = col_widths_st[j]
        set_cell_background(cell, "103666")
        set_cell_margins(cell, top=80, bottom=80, left=80, right=80)
        p = cell.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        run = p.add_run(h)
        run.font.bold = True
        run.font.size = Pt(8.5)
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
            cell.width = col_widths_st[j]
            set_cell_background(cell, bg)
            set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
            p = cell.paragraphs[0]
            run = p.add_run(val)
            run.font.size = Pt(8.5)
            if j == 2:
                run.font.bold = True
                run.font.color.rgb = RGBColor(22, 101, 52) # Dark Green
            else:
                run.font.color.rgb = RGBColor(30, 41, 59)
                
    doc.add_paragraph().paragraph_format.space_after = Pt(8)

    # ----------------------------------------------------
    # SECTION 9: ROADMAP
    # ----------------------------------------------------
    style_heading_1(doc.add_paragraph(), "9. Project Roadmap & Future Scope")
    style_heading_2(doc.add_paragraph(), "Review 2 Milestones:")
    add_bullet_p(doc, "Dynamic API Binding: ", "Wire the Streamlit interface directly to live MySQL REST endpoints for persistent multi-user storage.")
    add_bullet_p(doc, "Faculty Reviewer Portal: ", "Implement a dedicated faculty view to evaluate proposals, review novelty recommendations, and approve/reject project selections.")
    add_bullet_p(doc, "Database Triggers & Audit Logging: ", "Implement MySQL triggers to maintain an immutable 'project_audit_log' tracking all status changes and timestamps.")

    style_heading_2(doc.add_paragraph(), "Review 3 Milestones:")
    add_bullet_p(doc, "Dense Vector Embeddings: ", "Integrate Sentence-BERT embeddings for advanced semantic concept matching beyond token overlap.")
    add_bullet_p(doc, "Automated PDF Project Dossier Export: ", "Generate formal, downloadable PDF reports certifying project novelty for institutional records.")
    add_bullet_p(doc, "Role-Based Access Control (RBAC): ", "Implement JWT-based session tokens differentiating student and faculty permissions.")

    # ----------------------------------------------------
    # SECTION 10: REFERENCES
    # ----------------------------------------------------
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
        p.paragraph_format.space_after = Pt(2.5)
        p.paragraph_format.line_spacing = 1.15
        run = p.add_run(ref)
        run.font.name = "Calibri"
        run.font.size = Pt(9.0)
        run.font.color.rgb = RGBColor(60, 60, 60)
        
    output_path = "REVIEW_1_REPORT.docx"
    doc.save(output_path)
    print(f"Enhanced Document successfully created at {output_path}")

if __name__ == "__main__":
    generate_complete_doc()
