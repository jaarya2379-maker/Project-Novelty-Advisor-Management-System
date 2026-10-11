import os
from PIL import Image, ImageDraw, ImageFont

os.makedirs("assets", exist_ok=True)

# Monochrome / Black & White Palette
BLACK = (0, 0, 0)
CHARCOAL = (35, 35, 35)
DARK_GRAY = (70, 70, 70)
MID_GRAY = (120, 120, 120)
LIGHT_GRAY = (242, 242, 242)
VERY_LIGHT_GRAY = (248, 248, 248)
BORDER_GRAY = (180, 180, 180)
WHITE = (255, 255, 255)

font_path = "/System/Library/Fonts/Supplemental/Arial.ttf"
if not os.path.exists(font_path):
    font_path = "/Library/Fonts/Arial.ttf"

def get_font(size, bold=False):
    try:
        if bold and os.path.exists("/System/Library/Fonts/Supplemental/Arial Bold.ttf"):
            return ImageFont.truetype("/System/Library/Fonts/Supplemental/Arial Bold.ttf", size)
        return ImageFont.truetype(font_path, size)
    except:
        return ImageFont.load_default()

def draw_rect(draw, xy, fill=WHITE, outline=BLACK, width=2, radius=8):
    x1, y1, x2, y2 = xy
    draw.rounded_rectangle([x1, y1, x2, y2], radius=radius, fill=fill, outline=outline, width=width)

def draw_arrow(draw, start, end, color=BLACK, width=2, arrow_size=8):
    x1, y1 = start
    x2, y2 = end
    draw.line([x1, y1, x2, y2], fill=color, width=width)
    if x1 == x2: # Vertical
        if y2 > y1: # Downwards
            draw.polygon([(x2, y2), (x2 - arrow_size, y2 - arrow_size*1.4), (x2 + arrow_size, y2 - arrow_size*1.4)], fill=color)
        else: # Upwards
            draw.polygon([(x2, y2), (x2 - arrow_size, y2 + arrow_size*1.4), (x2 + arrow_size, y2 + arrow_size*1.4)], fill=color)
    elif y1 == y2: # Horizontal
        if x2 > x1: # Right
            draw.polygon([(x2, y2), (x2 - arrow_size*1.4, y2 - arrow_size), (x2 - arrow_size*1.4, y2 + arrow_size)], fill=color)
        else: # Left
            draw.polygon([(x2, y2), (x2 + arrow_size*1.4, y2 - arrow_size), (x2 + arrow_size*1.4, y2 + arrow_size)], fill=color)

# ==========================================
# 1. B&W SYSTEM ARCHITECTURE DIAGRAM
# ==========================================
def create_architecture_diagram_bw():
    w, h = 1200, 780
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(15)
    f_box_title = get_font(16, bold=True)
    f_box_desc = get_font(13.5)
    f_tag = get_font(14, bold=True)

    # Outer border / Header box
    draw_rect(draw, (40, 20, 1160, 90), fill=CHARCOAL, outline=BLACK, radius=6)
    draw.text((600, 42), "PROJECT NOVELTY ADVISOR & MANAGEMENT SYSTEM", fill=WHITE, font=f_title, anchor="mm")
    draw.text((600, 70), "Three-Tier Relational Database System Architecture", fill=LIGHT_GRAY, font=f_sub, anchor="mm")

    # Tier 1: Presentation Layer
    draw_rect(draw, (40, 115, 1160, 235), fill=VERY_LIGHT_GRAY, outline=CHARCOAL, radius=8)
    draw.text((60, 130), "TIER 1: PRESENTATION LAYER (Streamlit Web Interface)", fill=BLACK, font=f_box_title)
    
    t1_boxes = [
        ("Student Login & Profile", "User auth, session state,\nand student dashboard", (60, 160, 310, 220)),
        ("Project Submission Form", "5-part proposal input:\nDomain, Method, Data, Tech", (330, 160, 590, 220)),
        ("Novelty Analytics UI", "Displays similarity %, top 5\nmatches & overused items", (610, 160, 870, 220)),
        ("Novelty Selection", "Student commits to a chosen\ninnovation roadmap", (890, 160, 1140, 220))
    ]
    for title, desc, coords in t1_boxes:
        draw_rect(draw, coords, fill=WHITE, outline=BLACK, radius=6)
        draw.text(((coords[0]+coords[2])//2, coords[1]+15), title, fill=BLACK, font=f_tag, anchor="mm")
        y_d = coords[1] + 32
        for line in desc.split("\n"):
            draw.text(((coords[0]+coords[2])//2, y_d), line, fill=DARK_GRAY, font=f_box_desc, anchor="mm")
            y_d += 16

    # Connector 1 -> 2
    draw_arrow(draw, (600, 235), (600, 275), color=BLACK, width=2)
    draw.text((615, 255), "HTTP REST API / JSON", fill=BLACK, font=f_box_desc)

    # Tier 2: Application Layer
    draw_rect(draw, (40, 275, 1160, 480), fill=WHITE, outline=CHARCOAL, radius=8)
    draw.text((60, 290), "TIER 2: APPLICATION & INTELLIGENCE LAYER (Flask Server + Novelty Engine)", fill=BLACK, font=f_box_title)

    # Left: Flask REST Gateway
    draw_rect(draw, (60, 320, 500, 465), fill=VERY_LIGHT_GRAY, outline=BORDER_GRAY, radius=6)
    draw.text((280, 340), "Flask REST API Gateway (backend.py)", fill=BLACK, font=f_tag, anchor="mm")
    endpoints = [
        "• POST /api/auth/register & /api/auth/login",
        "• POST /api/projects/submit",
        "• GET  /api/projects/<id> & /api/projects/user/<id>",
        "• POST /api/analyze/<project_id>",
        "• POST /api/novelty/select & GET /api/novelty/<id>"
    ]
    for idx, ep in enumerate(endpoints):
        draw.text((80, 365 + idx*19), ep, fill=CHARCOAL, font=f_box_desc)

    # Right: Novelty Engine
    draw_rect(draw, (520, 320, 1140, 465), fill=VERY_LIGHT_GRAY, outline=BORDER_GRAY, radius=6)
    draw.text((830, 340), "Novelty & Gap Analysis Engine (novelty_engine.py)", fill=BLACK, font=f_tag, anchor="mm")
    engine_steps = [
        ("Attribute Normalizer", "Cleans text, strips stopwords, extracts keywords"),
        ("Similarity Analyzer", "Weighted combination: Domain, Method, Data, Tech & Keywords"),
        ("Component Saturation", "Finds common datasets/methods from past database records"),
        ("5-Idea Generator", "Produces 5 actionable pivots: Transfer, Edge, Hybrid, etc.")
    ]
    for idx, (st_name, st_desc) in enumerate(engine_steps):
        draw.text((540, 365 + idx*24), f"• {st_name}:", fill=BLACK, font=f_tag)
        draw.text((710, 365 + idx*24), st_desc, fill=DARK_GRAY, font=f_box_desc)

    # Connector 2 -> 3
    draw_arrow(draw, (600, 480), (600, 520), color=BLACK, width=2)
    draw.text((615, 500), "SQL Queries & Transactions (MySQLdb / PyMySQL)", fill=BLACK, font=f_box_desc)

    # Tier 3: Database Storage Layer
    draw_rect(draw, (40, 520, 1160, 750), fill=VERY_LIGHT_GRAY, outline=CHARCOAL, radius=8)
    draw.text((60, 535), "TIER 3: DATABASE TIER (MySQL InnoDB — BCNF Normalized Schema)", fill=BLACK, font=f_box_title)

    t3_tables = [
        ("students", "PK: student_id\nUK: username, email\nSalted PBKDF2 hash\nACID user records", (60, 565, 310, 735)),
        ("projects", "PK: project_id\nFK: student_id (CASCADE)\nFULLTEXT: title, problem\nJSON: technologies", (330, 565, 590, 735)),
        ("analysis_results", "PK: analysis_id\nFK, UK: project_id (1:1)\nJSON: similar_projects\nJSON: novelty_suggestions", (610, 565, 870, 735)),
        ("selected_novelties", "PK: novelty_id\nFK: project_id (CASCADE)\nCommitted novelty idea\nand student notes", (890, 565, 1140, 735))
    ]
    for t_name, t_info, coords in t3_tables:
        draw_rect(draw, coords, fill=WHITE, outline=BLACK, radius=6)
        draw.text(((coords[0]+coords[2])//2, coords[1]+18), t_name, fill=BLACK, font=f_tag, anchor="mm")
        y_t = coords[1] + 45
        for l in t_info.split("\n"):
            draw.text(((coords[0]+coords[2])//2, y_t), l, fill=DARK_GRAY, font=f_box_desc, anchor="mm")
            y_t += 20

    img.save("assets/system_architecture.png")
    print("Saved B&W assets/system_architecture.png")

# ==========================================
# 2. B&W ENTITY-RELATIONSHIP (ER) DIAGRAM
# ==========================================
def create_er_diagram_bw():
    w, h = 1200, 750
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(14)
    f_header = get_font(17, bold=True)
    f_attr = get_font(13.5)
    f_pk = get_font(13.5, bold=True)
    f_rel = get_font(13.5, bold=True)

    # Title
    draw.text((600, 35), "ENTITY-RELATIONSHIP (ER) DIAGRAM", fill=BLACK, font=f_title, anchor="mm")
    draw.text((600, 62), "Relational Database Schema in Boyce-Codd Normal Form (BCNF)", fill=DARK_GRAY, font=f_sub, anchor="mm")

    s_box = (60, 110, 360, 390)
    p_box = (450, 110, 770, 520)
    a_box = (860, 110, 1160, 400)
    n_box = (860, 450, 1160, 700)

    def draw_entity_bw(box, title, attrs, pk_indices=[0], fk_indices=[]):
        x1, y1, x2, y2 = box
        draw_rect(draw, box, fill=WHITE, outline=BLACK, width=2, radius=6)
        # Header banner (Dark charcoal with white text)
        draw.rounded_rectangle([x1, y1, x2, y1+40], radius=6, fill=CHARCOAL)
        draw.rectangle([x1, y1+20, x2, y1+40], fill=CHARCOAL)
        draw.text(((x1+x2)//2, y1+20), title, fill=WHITE, font=f_header, anchor="mm")
        
        y_cursor = y1 + 55
        for idx, attr in enumerate(attrs):
            if idx in pk_indices:
                draw.text((x1+15, y_cursor), "[PK] " + attr, fill=BLACK, font=f_pk)
            elif idx in fk_indices:
                draw.text((x1+15, y_cursor), "[FK] " + attr, fill=CHARCOAL, font=f_pk)
            else:
                draw.text((x1+15, y_cursor), "  • " + attr, fill=DARK_GRAY, font=f_attr)
            y_cursor += 25

    # 1. STUDENTS
    draw_entity_bw(s_box, "STUDENTS", [
        "student_id : INT (AI)",
        "username : VARCHAR(100) [UK]",
        "email : VARCHAR(100) [UK]",
        "password_hash : VARCHAR(255)",
        "name : VARCHAR(100)",
        "created_at : TIMESTAMP"
    ], pk_indices=[0])

    # 2. PROJECTS
    draw_entity_bw(p_box, "PROJECTS", [
        "project_id : INT (AI)",
        "student_id : INT",
        "title : VARCHAR(255)",
        "problem_statement : TEXT",
        "domain : VARCHAR(100)",
        "dataset : VARCHAR(255)",
        "method : VARCHAR(255)",
        "technologies : JSON",
        "additional_info : TEXT",
        "status : VARCHAR(50)",
        "created_at : TIMESTAMP",
        "updated_at : TIMESTAMP"
    ], pk_indices=[0], fk_indices=[1])

    # 3. ANALYSIS_RESULTS
    draw_entity_bw(a_box, "ANALYSIS_RESULTS", [
        "analysis_id : INT (AI)",
        "project_id : INT [UK]",
        "similar_projects : JSON",
        "common_technologies : JSON",
        "common_datasets : JSON",
        "common_methods : JSON",
        "existing_limitations : JSON",
        "possible_gaps : JSON",
        "novelty_suggestions : JSON",
        "analysis_timestamp : TIMESTAMP"
    ], pk_indices=[0], fk_indices=[1])

    # 4. SELECTED_NOVELTIES
    draw_entity_bw(n_box, "SELECTED_NOVELTIES", [
        "novelty_id : INT (AI)",
        "project_id : INT",
        "novelty_title : VARCHAR(255)",
        "novelty_description : TEXT",
        "novelty_impact : VARCHAR(50)",
        "novelty_feasibility : VARCHAR(50)",
        "notes : TEXT",
        "selected_at : TIMESTAMP"
    ], pk_indices=[0], fk_indices=[1])

    # Connectors
    # STUDENTS to PROJECTS (1:N)
    draw.line([(360, 230), (450, 230)], fill=BLACK, width=2)
    draw.polygon([(405, 212), (423, 230), (405, 248), (387, 230)], fill=WHITE, outline=BLACK)
    draw.text((365, 210), "1", fill=BLACK, font=f_pk)
    draw.text((435, 210), "N", fill=BLACK, font=f_pk)
    draw.text((405, 260), "submits", fill=BLACK, font=f_rel, anchor="mm")

    # PROJECTS to ANALYSIS_RESULTS (1:1)
    draw.line([(770, 230), (860, 230)], fill=BLACK, width=2)
    draw.polygon([(815, 212), (833, 230), (815, 248), (797, 230)], fill=WHITE, outline=BLACK)
    draw.text((775, 210), "1", fill=BLACK, font=f_pk)
    draw.text((845, 210), "1", fill=BLACK, font=f_pk)
    draw.text((815, 260), "generates", fill=BLACK, font=f_rel, anchor="mm")

    # PROJECTS to SELECTED_NOVELTIES (1:N)
    draw.line([(610, 520), (610, 570), (860, 570)], fill=BLACK, width=2)
    draw.polygon([(735, 552), (753, 570), (735, 588), (717, 570)], fill=WHITE, outline=BLACK)
    draw.text((615, 530), "1", fill=BLACK, font=f_pk)
    draw.text((845, 550), "N", fill=BLACK, font=f_pk)
    draw.text((735, 602), "commits_to", fill=BLACK, font=f_rel, anchor="mm")

    # Legend at bottom
    draw_rect(draw, (60, 680, 800, 725), fill=VERY_LIGHT_GRAY, outline=BORDER_GRAY, radius=4)
    draw.text((75, 695), "Legend:  [PK] Primary Key    [FK] Foreign Key (CASCADE)    [UK] Unique Constraint    (1:N) 1-to-Many    (1:1) 1-to-1", fill=CHARCOAL, font=f_attr)

    img.save("assets/er_diagram.png")
    print("Saved B&W assets/er_diagram.png")

# ==========================================
# 3. B&W WORKFLOW / PROCESS FLOWCHART
# ==========================================
def create_workflow_diagram_bw():
    w, h = 1200, 720
    img = Image.new("RGB", (w, h), WHITE)
    draw = ImageDraw.Draw(img)

    f_title = get_font(24, bold=True)
    f_sub = get_font(14)
    f_box_title = get_font(15, bold=True)
    f_box_desc = get_font(12)

    # Title
    draw.text((600, 30), "SYSTEM WORKFLOW & NOVELTY ADVISORY PROCESS", fill=BLACK, font=f_title, anchor="mm")
    draw.text((600, 56), "End-to-End Execution Flow from Proposal Submission to Decision Locking", fill=DARK_GRAY, font=f_sub, anchor="mm")

    row1 = [
        ("Step 1: Student Login", "Student authenticates via web UI.\nPassword verified against\nstudents table (salted PBKDF2).", (50, 105, 290, 235)),
        ("Step 2: Proposal Input", "Fill submission form:\n• Project Title & Problem Text\n• Domain, Dataset, Method\n• Technology list (JSON)", (340, 105, 580, 235)),
        ("Step 3: Attribute Parsing", "Tokenizes description text,\nremoves English stopwords,\nextracts core problem keywords.", (630, 105, 870, 235)),
        ("Step 4: Archive Search", "Queries historical database.\nUses FULLTEXT index to find\nrelevant past project candidates.", (920, 105, 1160, 235))
    ]

    for title, desc, box in row1:
        draw_rect(draw, box, fill=VERY_LIGHT_GRAY, outline=BLACK, radius=6)
        draw.text(((box[0]+box[2])//2, box[1]+20), title, fill=BLACK, font=f_box_title, anchor="mm")
        y_text = box[1] + 46
        for l in desc.split("\n"):
            draw.text((box[0]+15, y_text), l, fill=DARK_GRAY, font=f_box_desc)
            y_text += 19

    # Arrows Row 1
    draw_arrow(draw, (290, 170), (340, 170), color=BLACK)
    draw_arrow(draw, (580, 170), (630, 170), color=BLACK)
    draw_arrow(draw, (870, 170), (920, 170), color=BLACK)

    # Turn connector
    draw.line([(1040, 235), (1040, 300)], fill=BLACK, width=2)
    draw.line([(1040, 300), (1040, 370)], fill=BLACK, width=2)
    draw.polygon([(1040, 370), (1032, 354), (1048, 354)], fill=BLACK)

    # Row 2 (Right to Left)
    row2 = [
        ("Step 5: Similarity Scoring", "Computes weighted similarity:\nS = 0.25*Domain + 0.25*Method\n   + 0.20*Data + 0.15*Tech\n   + 0.15*Keywords (Cutoff: 30%)", (920, 370, 1160, 510)),
        ("Step 6: Gap & Saturation", "Checks component frequencies.\nFlags overused datasets/methods;\npulls known limitations.", (630, 370, 870, 510)),
        ("Step 7: 5 Novelty Ideas", "Generates concrete proposals:\n1. Domain Transfer\n2. Edge AI / Lightweight\n3. Hybrid Model Ensembles\n4. Multimodal Integration\n5. Benchmarking Matrix", (340, 370, 580, 530)),
        ("Step 8: Advisory Dashboard", "Student inspects similarity,\nsaturated elements, and 5 ideas.\nPicks a preferred novelty pivot.", (50, 370, 290, 510))
    ]

    for title, desc, box in row2:
        draw_rect(draw, box, fill=VERY_LIGHT_GRAY, outline=BLACK, radius=6)
        draw.text(((box[0]+box[2])//2, box[1]+20), title, fill=BLACK, font=f_box_title, anchor="mm")
        y_text = box[1] + 46
        for l in desc.split("\n"):
            draw.text((box[0]+15, y_text), l, fill=DARK_GRAY, font=f_box_desc)
            y_text += 19

    # Arrows Row 2
    draw_arrow(draw, (920, 440), (870, 440), color=BLACK)
    draw_arrow(draw, (630, 440), (580, 440), color=BLACK)
    draw_arrow(draw, (340, 440), (290, 440), color=BLACK)

    # Step 9 Bottom Box
    step9_box = (250, 575, 950, 685)
    draw_rect(draw, step9_box, fill=WHITE, outline=BLACK, width=2, radius=8)
    draw.line([(170, 510), (170, 630), (250, 630)], fill=BLACK, width=2)
    draw.polygon([(250, 630), (236, 622), (236, 638)], fill=BLACK)

    draw.text((600, 600), "Step 9: Database Persistence & Faculty Review Baseline", fill=BLACK, font=f_box_title, anchor="mm")
    desc_s9 = "Selected novelty is stored in `selected_novelties` table (FK to projects.project_id).\nStatus changes to 'novelty_selected'. Locks proposal as verifiable baseline for Review 2 & 3."
    y_s9 = 628
    for l in desc_s9.split("\n"):
        draw.text((600, y_s9), l, fill=DARK_GRAY, font=f_box_desc, anchor="mm")
        y_s9 += 20

    img.save("assets/process_flowchart.png")
    print("Saved B&W assets/process_flowchart.png")

if __name__ == "__main__":
    create_architecture_diagram_bw()
    create_er_diagram_bw()
    create_workflow_diagram_bw()
