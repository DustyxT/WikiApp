"""
WikiApp Viva Preparation Guide - PDF Generator
Author: Movindu Lochana (s1577380)
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor, white, black
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    PageBreak, HRFlowable, KeepTogether
)

OUTPUT = "WikiApp_Viva_Guide.pdf"

# ── Colours ──────────────────────────────────────────────────────────────────
NAVY   = HexColor("#1e3a8a")
BLUE   = HexColor("#2563eb")
LBLUE  = HexColor("#dbeafe")
GREY   = HexColor("#f1f5f9")
DGREY  = HexColor("#374151")
LGREY  = HexColor("#6b7280")
RED    = HexColor("#dc2626")
GREEN  = HexColor("#16a34a")
AMBER  = HexColor("#d97706")
WHITE  = white
CODE_BG = HexColor("#1e293b")
CODE_FG = HexColor("#e2e8f0")

# ── Styles ────────────────────────────────────────────────────────────────────
styles = getSampleStyleSheet()

def s(name, **kw):
    return ParagraphStyle(name, parent=styles["Normal"], **kw)

cover_title = s("CT", fontSize=36, leading=44, textColor=WHITE,
                alignment=TA_CENTER, fontName="Helvetica-Bold")
cover_sub   = s("CS", fontSize=16, leading=24, textColor=LBLUE,
                alignment=TA_CENTER)
cover_info  = s("CI", fontSize=13, leading=20, textColor=WHITE,
                alignment=TA_CENTER)

h1 = s("H1", fontSize=20, leading=28, textColor=WHITE,
        fontName="Helvetica-Bold", spaceBefore=0, spaceAfter=0)
h2 = s("H2", fontSize=14, leading=20, textColor=NAVY,
        fontName="Helvetica-Bold", spaceBefore=14, spaceAfter=6)
h3 = s("H3", fontSize=12, leading=18, textColor=BLUE,
        fontName="Helvetica-Bold", spaceBefore=10, spaceAfter=4)

body  = s("B",  fontSize=10, leading=16, textColor=DGREY,
           alignment=TA_JUSTIFY, spaceAfter=6)
body2 = s("B2", fontSize=10, leading=16, textColor=DGREY, spaceAfter=4)

code  = s("C",  fontSize=8.5, leading=13, textColor=CODE_FG,
           fontName="Courier", spaceAfter=2)
code_label = s("CL", fontSize=8, leading=12, textColor=LGREY,
                fontName="Courier-Oblique", spaceAfter=0)

qa_q = s("QQ", fontSize=10.5, leading=16, textColor=NAVY,
          fontName="Helvetica-Bold", spaceAfter=3, spaceBefore=10)
qa_a = s("QA", fontSize=10, leading=16, textColor=DGREY,
          alignment=TA_JUSTIFY, spaceAfter=6)

tip  = s("TIP", fontSize=9.5, leading=15, textColor=HexColor("#92400e"),
          spaceAfter=4)
note = s("NOTE", fontSize=9.5, leading=15, textColor=HexColor("#1e40af"),
          spaceAfter=4)

bullet = s("BL", fontSize=10, leading=16, textColor=DGREY,
            leftIndent=16, spaceAfter=3,
            bulletIndent=4, bulletFontName="Helvetica",
            bulletFontSize=10, bulletText="•")

toc_item = s("TOC", fontSize=11, leading=18, textColor=NAVY, spaceAfter=2)

# ── Helper builders ───────────────────────────────────────────────────────────

def section_header(text, colour=NAVY):
    """Dark banner with white heading."""
    tbl = Table([[Paragraph(text, h1)]], colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colour),
        ("TOPPADDING",    (0,0), (-1,-1), 10),
        ("BOTTOMPADDING", (0,0), (-1,-1), 10),
        ("LEFTPADDING",   (0,0), (-1,-1), 14),
        ("RIGHTPADDING",  (0,0), (-1,-1), 14),
        ("ROUNDEDCORNERS",(0,0), (-1,-1), [6,6,6,6]),
    ]))
    return tbl

def code_block(label, lines):
    """Dark code panel."""
    code_rows = [[Paragraph(label, code_label)]]
    for line in lines:
        code_rows.append([Paragraph(line, code)])
    tbl = Table(code_rows, colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), CODE_BG),
        ("TOPPADDING",    (0,0), (-1,-1), 4),
        ("BOTTOMPADDING", (0,0), (-1,-1), 4),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
        ("RIGHTPADDING",  (0,0), (-1,-1), 8),
    ]))
    return tbl

def tip_box(text, colour=HexColor("#fffbeb"), border=AMBER, label="TIP"):
    row = [[Paragraph(f"<b>{label}:</b> {text}", tip)]]
    tbl = Table(row, colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), colour),
        ("LINEAFTER",     (0,0), (0,-1),  0, WHITE),
        ("LINEBEFORE",    (0,0), (0,-1),  4, border),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
    ]))
    return tbl

def note_box(text):
    return tip_box(text, colour=LBLUE, border=BLUE, label="NOTE")

def qa_box(question, answer):
    q_row = [[Paragraph(f"Q: {question}", qa_q)]]
    a_row = [[Paragraph(f"A: {answer}",   qa_a)]]
    tbl = Table(q_row + a_row, colWidths=[17*cm])
    tbl.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,-1), HexColor("#f8fafc")),
        ("BACKGROUND",    (0,0), (0,0),   LBLUE),
        ("LINEABOVE",     (0,0), (-1,0),  1, BLUE),
        ("LINEBELOW",     (0,-1),(-1,-1), 1, HexColor("#e2e8f0")),
        ("TOPPADDING",    (0,0), (-1,-1), 8),
        ("BOTTOMPADDING", (0,0), (-1,-1), 8),
        ("LEFTPADDING",   (0,0), (-1,-1), 12),
    ]))
    return tbl

def sp(n=0.3):
    return Spacer(1, n*cm)

# ── Story ─────────────────────────────────────────────────────────────────────
story = []

# ═══════════════════════════════════════════════════════════════════════════════
# COVER PAGE
# ═══════════════════════════════════════════════════════════════════════════════
cover = Table([[
    Paragraph("WikiApp", cover_title),
    Paragraph("Viva Preparation Guide", cover_sub),
    Paragraph("Movindu Lochana &nbsp;|&nbsp; s1577380", cover_info),
    Paragraph("BIT235 Object Oriented Programming — Assessment 2", cover_info),
]], colWidths=[17*cm])
cover.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,-1), NAVY),
    ("ALIGN",         (0,0), (-1,-1), "CENTER"),
    ("TOPPADDING",    (0,0), (-1,-1), 28),
    ("BOTTOMPADDING", (0,0), (-1,-1), 28),
    ("ROUNDEDCORNERS",(0,0), (-1,-1), [10,10,10,10]),
]))
story += [sp(1), cover, sp(0.6)]

story.append(note_box(
    "This guide explains every single file and code block in the WikiApp project. "
    "Read it like a story — from top to bottom — and you will be able to answer any "
    "viva question confidently. Every explanation is written assuming you are new to "
    "Spring Boot."
))
story.append(sp(0.4))

# Table of Contents
story.append(section_header("Table of Contents"))
story.append(sp(0.3))
toc = [
    "1.  The Big Picture — What is Spring Boot and MVC?",
    "2.  Project Structure — Where every file lives",
    "3.  pom.xml — The shopping list of libraries",
    "4.  application.properties — App settings",
    "5.  data.sql — Seeding the database",
    "6.  WikiAppApplication.java — The entry point",
    "7.  Model: LoginForm.java",
    "8.  Model: Article.java",
    "9.  Model: Admin.java",
    "10. Repository: ArticleRepository.java",
    "11. Repository: AdminRepository.java",
    "12. Service: AuthService.java",
    "13. Service: ArticleService.java",
    "14. Controller: AuthController.java",
    "15. Controller: WikiController.java",
    "16. Controller: AdminController.java",
    "17. Template: login.html",
    "18. Template: wiki/list.html",
    "19. Template: wiki/view.html",
    "20. Template: admin/dashboard.html",
    "21. Template: admin/form.html",
    "22. Template: admin/confirm-delete.html",
    "23. Viva Q&A — 30 likely questions with answers",
]
for t in toc:
    story.append(Paragraph(t, toc_item))

story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 1 — THE BIG PICTURE
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("1.  The Big Picture — Spring Boot & MVC"))
story.append(sp())
story.append(Paragraph(
    "Before looking at any code, it helps to understand the two main ideas behind this project.", body))

story.append(Paragraph("<b>What is Spring Boot?</b>", h2))
story.append(Paragraph(
    "Spring Boot is a Java framework that makes it easy to build web applications. "
    "Normally you would have to install a web server (like Apache Tomcat), write a lot "
    "of configuration, and wire hundreds of pieces together manually. "
    "Spring Boot does all of that for you automatically. "
    "You just write your business logic, run the app, and a working website appears at "
    "http://localhost:8080.", body))

story.append(Paragraph("<b>What is MVC?</b>", h2))
story.append(Paragraph(
    "MVC stands for Model-View-Controller. It is a way to organise code so that "
    "each part has one clear job:", body))
story.append(Paragraph("<b>Model</b> — the data (Article, Admin, LoginForm classes)", bullet))
story.append(Paragraph("<b>View</b> — the HTML pages shown to the user (Thymeleaf templates)", bullet))
story.append(Paragraph("<b>Controller</b> — the traffic cop that receives a browser request, asks the "
                        "Service for data, and picks the right View to display", bullet))
story.append(sp(0.2))

story.append(Paragraph("<b>The three-layer architecture in this project:</b>", h3))
story.append(Paragraph("Controller (handles HTTP) → Service (business logic) → Repository (database)", bullet))
story.append(Paragraph("Each layer only talks to the one directly below it.", bullet))
story.append(Paragraph("This makes it easy to change one layer without breaking the others.", bullet))
story.append(sp(0.2))

story.append(Paragraph("<b>How a typical request flows through the app:</b>", h3))
flow = [
    ["Step", "What happens"],
    ["1", "User opens http://localhost:8080/wiki in the browser"],
    ["2", "Spring routes the GET /wiki request to WikiController.listArticles()"],
    ["3", "WikiController asks ArticleService for all articles"],
    ["4", "ArticleService asks ArticleRepository to run SELECT * FROM article"],
    ["5", "The list of articles travels back up to WikiController"],
    ["6", "WikiController puts them in the Model and returns 'wiki/list'"],
    ["7", "Thymeleaf fills wiki/list.html with the data and sends HTML to the browser"],
]
flow_tbl = Table(flow, colWidths=[1.5*cm, 15.5*cm])
flow_tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("BACKGROUND",    (0,1), (-1,-1), HexColor("#f8fafc")),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [HexColor("#f8fafc"), WHITE]),
    ("GRID",          (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
]))
story.append(flow_tbl)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 2 — PROJECT STRUCTURE
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("2.  Project Structure"))
story.append(sp())
story.append(Paragraph(
    "Every file in the project has a specific home. Spring Boot expects this structure "
    "and will not find your files if they are in the wrong place.", body))
story.append(sp(0.2))
story.append(code_block("Project folder layout", [
    "WikiApp/",
    "  pom.xml                          &lt;-- Maven build file (libraries list)",
    "  src/main/java/com/wikiapp/",
    "    WikiAppApplication.java         &lt;-- Entry point, starts the server",
    "    model/",
    "      LoginForm.java                &lt;-- Form data object (Part A)",
    "      Article.java                  &lt;-- Database table: ARTICLE",
    "      Admin.java                    &lt;-- Database table: ADMIN",
    "    repository/",
    "      ArticleRepository.java        &lt;-- Database queries for articles",
    "      AdminRepository.java          &lt;-- Database queries for admins",
    "    service/",
    "      AuthService.java              &lt;-- Login business logic",
    "      ArticleService.java           &lt;-- Article business logic",
    "    controller/",
    "      AuthController.java           &lt;-- Handles /login and /logout",
    "      WikiController.java           &lt;-- Handles /wiki (public)",
    "      AdminController.java          &lt;-- Handles /admin (protected)",
    "  src/main/resources/",
    "    application.properties          &lt;-- App settings (port, database)",
    "    data.sql                        &lt;-- Seed data run at startup",
    "    templates/",
    "      login.html, welcome.html, error.html",
    "      wiki/list.html, wiki/view.html",
    "      admin/dashboard.html, admin/form.html, admin/confirm-delete.html",
    "    static/css/style.css            &lt;-- Stylesheet",
]))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 3 — pom.xml
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("3.  pom.xml — The Library Shopping List"))
story.append(sp())
story.append(Paragraph(
    "Maven is the build tool. pom.xml is the configuration file that tells Maven "
    "which libraries to download from the internet and include in the project. "
    "You never have to download JAR files manually.", body))
story.append(sp(0.2))
story.append(Paragraph("<b>The five key dependencies:</b>", h3))
deps = [
    ["Dependency", "What it gives us"],
    ["spring-boot-starter-web", "Embedded Tomcat server, @Controller, @GetMapping, @PostMapping"],
    ["spring-boot-starter-thymeleaf", "Thymeleaf template engine — turns .html files into dynamic pages"],
    ["spring-boot-starter-validation", "@NotBlank and other form validation annotations"],
    ["spring-boot-starter-data-jpa", "JPA / Hibernate — talks to the database; JpaRepository"],
    ["h2", "H2 in-memory/file database — no install needed, stores data in ./data/wikidb"],
]
dep_tbl = Table(deps, colWidths=[7*cm, 10*cm])
dep_tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [HexColor("#f8fafc"), WHITE]),
    ("GRID",          (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(dep_tbl)
story.append(sp(0.3))
story.append(tip_box(
    "In the viva, if asked 'why do you use H2?', say: "
    "H2 is an embedded database — it runs inside the Java process, needs no installation, "
    "and stores data in a file so it survives restarts. Perfect for development and assessment."
))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 4 — application.properties
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("4.  application.properties — App Settings"))
story.append(sp())
story.append(Paragraph(
    "This file configures how the application runs. Spring Boot reads it at startup. "
    "Each line is a key=value pair.", body))
story.append(sp(0.2))
story.append(code_block("src/main/resources/application.properties", [
    "server.port=8080",
    "spring.thymeleaf.cache=false",
    "spring.application.name=WikiApp",
    "",
    "spring.datasource.url=jdbc:h2:file:./data/wikidb;AUTO_SERVER=TRUE",
    "spring.datasource.driver-class-name=org.h2.Driver",
    "spring.datasource.username=sa",
    "spring.datasource.password=",
    "",
    "spring.h2.console.enabled=true",
    "spring.h2.console.path=/h2-console",
    "",
    "spring.jpa.hibernate.ddl-auto=update",
    "spring.jpa.show-sql=false",
    "spring.jpa.properties.hibernate.dialect=org.hibernate.dialect.H2Dialect",
    "",
    "spring.jpa.defer-datasource-initialization=true",
    "spring.sql.init.mode=always",
]))
story.append(sp(0.3))
props = [
    ["Setting", "Plain-English explanation"],
    ["server.port=8080", "The web server listens on port 8080, so the URL is localhost:8080"],
    ["thymeleaf.cache=false", "HTML changes show immediately without restarting the server"],
    ["datasource.url=jdbc:h2:file:./data/wikidb", "Store the database in the ./data/ folder as a file (survives restarts)"],
    ["AUTO_SERVER=TRUE", "Allows the H2 console and the app to share the same database file simultaneously"],
    ["h2.console.enabled=true", "Enables a browser-based database viewer at /h2-console"],
    ["ddl-auto=update", "JPA creates tables if they don't exist, updates them if the entity changes. Never drops data."],
    ["defer-datasource-initialization=true", "Runs data.sql AFTER JPA has created the tables (important for seeding)"],
    ["sql.init.mode=always", "Runs data.sql on every startup, not just the first one"],
]
p_tbl = Table(props, colWidths=[6.5*cm, 10.5*cm])
p_tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,-1), "Courier"),
    ("FONTNAME",      (1,0), (1,0),   "Helvetica-Bold"),
    ("TEXTCOLOR",     (1,0), (1,0),   WHITE),
    ("FONTNAME",      (1,1), (1,-1),  "Helvetica"),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [HexColor("#f8fafc"), WHITE]),
    ("GRID",          (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(p_tbl)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 5 — data.sql
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("5.  data.sql — Seeding the Database"))
story.append(sp())
story.append(Paragraph(
    "Spring runs this SQL file automatically every time the application starts. "
    "It pre-fills the database with one admin account and five sample articles so the "
    "wiki has content to show straight away.", body))
story.append(sp(0.2))
story.append(code_block("src/main/resources/data.sql  (simplified)", [
    "MERGE INTO ADMIN (id, username, password) KEY(id)",
    "  VALUES (1, 'movindu', '123');",
    "",
    "MERGE INTO ARTICLE (id, title, category, content, last_updated) KEY(id) VALUES",
    "  (1, 'Welcome to WikiApp', 'General', 'This is a small Wiki...', CURRENT_TIMESTAMP);",
    "  ... (4 more articles) ...",
    "",
    "ALTER TABLE ARTICLE ALTER COLUMN ID RESTART WITH 100;",
    "ALTER TABLE ADMIN   ALTER COLUMN ID RESTART WITH 100;",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>Why MERGE instead of INSERT?</b>", h3))
story.append(Paragraph(
    "INSERT would fail on the second startup because the rows already exist. "
    "MERGE means: 'insert this row if it does not exist yet, otherwise leave it alone'. "
    "It is safe to run every startup.", body))
story.append(sp(0.2))
story.append(Paragraph("<b>Why ALTER COLUMN ID RESTART WITH 100?</b>", h3))
story.append(Paragraph(
    "The seeded articles use IDs 1 to 5. If the auto-increment counter also starts at 1, "
    "the first new article you create would try to use ID 1 and crash with a duplicate-key "
    "error. Restarting the counter at 100 means new rows get IDs 100, 101, 102 ... "
    "which never collide with the seeded ones.", body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 6 — WikiAppApplication.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("6.  WikiAppApplication.java — The Entry Point"))
story.append(sp())
story.append(code_block("src/main/java/com/wikiapp/WikiAppApplication.java", [
    "@SpringBootApplication",
    "public class WikiAppApplication {",
    "    public static void main(String[] args) {",
    "        SpringApplication.run(WikiAppApplication.class, args);",
    "    }",
    "}",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>Line by line:</b>", h3))
story.append(Paragraph(
    "<b>@SpringBootApplication</b> — One annotation that does three things at once: "
    "(1) marks this as a configuration class, "
    "(2) tells Spring to scan the com.wikiapp package for Controllers, Services and Repositories, "
    "(3) enables auto-configuration (Spring guesses the right settings based on the libraries in pom.xml).", body))
story.append(Paragraph(
    "<b>SpringApplication.run(...)</b> — Hands control to Spring Boot. "
    "Spring then starts the embedded Tomcat web server, connects to the H2 database, "
    "creates the JPA tables, runs data.sql, and wires all the beans (Controllers, Services, "
    "Repositories) together. After this one line finishes, the app is fully running.", body))
story.append(sp(0.2))
story.append(tip_box(
    "If asked 'what does @SpringBootApplication do?' — say it triggers component scanning "
    "(finds all your @Controller, @Service, @Repository classes automatically) and enables "
    "auto-configuration (sets up the database, Thymeleaf, validation with no extra code)."
))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 7 — LoginForm.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("7.  Model: LoginForm.java"))
story.append(sp())
story.append(Paragraph(
    "LoginForm is a simple Java class (called a POJO — Plain Old Java Object) "
    "that holds the username and password the user typed into the login form. "
    "It is NOT stored in the database — it only exists during a single request.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/model/LoginForm.java", [
    "public class LoginForm {",
    "",
    "    @NotBlank(message = \"Username is required\")",
    "    private String username;",
    "",
    "    @NotBlank(message = \"Password is required\")",
    "    private String password;",
    "",
    "    public LoginForm() { }          // Spring needs this to create an empty object",
    "",
    "    public String getUsername() { return username; }",
    "    public void setUsername(String username) { this.username = username; }",
    "    public String getPassword() { return password; }",
    "    public void setPassword(String password) { this.password = password; }",
    "}",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>@NotBlank</b>", h3))
story.append(Paragraph(
    "This annotation tells Spring's validation system: 'reject this form if the field "
    "is null, empty, or only spaces'. If validation fails, Spring fills a BindingResult "
    "object with the error messages and the Controller can re-display the form.", body))
story.append(Paragraph("<b>Getters and setters</b>", h3))
story.append(Paragraph(
    "Spring uses the setter (setUsername) to copy the form field value into the object. "
    "Thymeleaf uses the getter (getUsername) to read the value back when re-displaying "
    "the form. Without them, the binding would silently fail.", body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 8 — Article.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("8.  Model: Article.java"))
story.append(sp())
story.append(Paragraph(
    "Article is a JPA entity — a Java class that is automatically mapped to a database "
    "table called ARTICLE. Every field becomes a column. Every instance becomes a row.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/model/Article.java", [
    "@Entity",
    "public class Article {",
    "",
    "    @Id",
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)",
    "    private Long id;",
    "",
    "    @NotBlank(message = \"Title is required\")",
    "    @Column(nullable = false)",
    "    private String title;",
    "",
    "    @NotBlank(message = \"Category is required\")",
    "    @Column(nullable = false)",
    "    private String category;",
    "",
    "    @NotBlank(message = \"Content is required\")",
    "    @Column(nullable = false, length = 5000)",
    "    private String content;",
    "",
    "    private LocalDateTime lastUpdated;",
    "",
    "    // No-args constructor required by JPA",
    "    public Article() { }",
    "",
    "    // Getters and setters for all fields ...",
    "}",
]))
story.append(sp(0.3))
anns = [
    ["Annotation", "What it means in plain English"],
    ["@Entity", "Maps this Java class to a database table (JPA creates the table for you)"],
    ["@Id", "Marks the primary key — the unique identifier for each row"],
    ["@GeneratedValue(IDENTITY)", "The database auto-increments the ID — you never set it manually"],
    ["@Column(nullable=false)", "The database column cannot be NULL — enforced at the DB level too"],
    ["@Column(length=5000)", "Sets the VARCHAR column size to 5000 characters for long article bodies"],
    ["@NotBlank", "Validates the field in the form before saving — shows an error if empty"],
    ["LocalDateTime lastUpdated", "Not annotated separately — JPA creates a TIMESTAMP column automatically"],
]
a_tbl = Table(anns, colWidths=[5.5*cm, 11.5*cm])
a_tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTNAME",      (0,1), (0,-1),  "Courier"),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [HexColor("#f8fafc"), WHITE]),
    ("GRID",          (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
    ("FONTSIZE",      (0,0), (-1,-1), 9),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 10),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(a_tbl)
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 9 — Admin.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("9.  Model: Admin.java"))
story.append(sp())
story.append(Paragraph(
    "Admin is the other JPA entity — it maps to the ADMIN table. "
    "In Part A the credentials were hard-coded in Java. "
    "In Part B they live in the database, which means you can add more admins "
    "without touching the code.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/model/Admin.java", [
    "@Entity",
    "public class Admin {",
    "",
    "    @Id",
    "    @GeneratedValue(strategy = GenerationType.IDENTITY)",
    "    private Long id;",
    "",
    "    @Column(nullable = false, unique = true)",
    "    private String username;",
    "",
    "    @Column(nullable = false)",
    "    private String password;   // plain text (acceptable for this assessment)",
    "",
    "    public Admin() { }",
    "    // Getters and setters ...",
    "}",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>unique = true on username</b>", h3))
story.append(Paragraph(
    "This creates a UNIQUE constraint in the database so two admins cannot share the "
    "same username. The database enforces this even if the Java code accidentally "
    "tries to insert a duplicate.", body))
story.append(tip_box(
    "If asked 'why store passwords in plain text?', say: "
    "For simplicity and ease of explanation in this assessment. In a real production "
    "application we would always hash passwords using BCrypt so that even if the "
    "database is stolen, the passwords cannot be read."
))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 10 — ArticleRepository.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("10. Repository: ArticleRepository.java"))
story.append(sp())
story.append(Paragraph(
    "The Repository layer is the only part of the code that talks to the database. "
    "We never write SQL — instead we extend Spring's JpaRepository interface and "
    "Spring generates all the SQL at startup.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/repository/ArticleRepository.java", [
    "public interface ArticleRepository extends JpaRepository&lt;Article, Long&gt; {",
    "",
    "    List&lt;Article&gt; findByCategoryIgnoreCase(String category);",
    "",
    "    List&lt;Article&gt; findByTitleContainingIgnoreCase(String text);",
    "}",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>JpaRepository&lt;Article, Long&gt;</b>", h3))
story.append(Paragraph(
    "The two type parameters mean: 'the entity is Article, the primary key type is Long'. "
    "By extending this interface we automatically get these methods for free — no code needed:", body))
for m in ["findAll() — SELECT * FROM article",
          "findById(id) — SELECT * FROM article WHERE id = ?",
          "save(article) — INSERT or UPDATE (JPA decides based on whether id is set)",
          "deleteById(id) — DELETE FROM article WHERE id = ?",
          "existsById(id) — SELECT COUNT(*) FROM article WHERE id = ?"]:
    story.append(Paragraph(m, bullet))
story.append(sp(0.2))
story.append(Paragraph("<b>Custom query methods — naming convention magic</b>", h3))
story.append(Paragraph(
    "Spring reads the method name and generates the SQL automatically. "
    "findByCategoryIgnoreCase(String category) becomes:", body))
story.append(code_block("Generated SQL", [
    "SELECT * FROM article WHERE UPPER(category) = UPPER(?)",
]))
story.append(sp(0.2))
story.append(Paragraph(
    "findByTitleContainingIgnoreCase(String text) becomes:", body))
story.append(code_block("Generated SQL", [
    "SELECT * FROM article WHERE UPPER(title) LIKE UPPER('%' || ? || '%')",
]))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 11 — AdminRepository.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("11. Repository: AdminRepository.java"))
story.append(sp())
story.append(code_block("src/main/java/com/wikiapp/repository/AdminRepository.java", [
    "public interface AdminRepository extends JpaRepository&lt;Admin, Long&gt; {",
    "",
    "    Optional&lt;Admin&gt; findByUsername(String username);",
    "}",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>Why Optional&lt;Admin&gt; instead of Admin?</b>", h3))
story.append(Paragraph(
    "If the username does not exist in the database, returning plain Admin would give "
    "us null, and any code that forgets to null-check would crash with a "
    "NullPointerException. "
    "Optional forces the caller to handle both cases — found and not-found — "
    "without any null checking. "
    "We call maybeAdmin.isEmpty() to check if nothing was found, and maybeAdmin.get() "
    "to retrieve the actual Admin object.", body))
story.append(sp(0.2))
story.append(note_box(
    "Think of Optional like a gift box. The box is always there (never null). "
    "Sometimes there is a present inside (the Admin), sometimes the box is empty. "
    "You check the box before reaching in."
))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 12 — AuthService.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("12. Service: AuthService.java"))
story.append(sp())
story.append(Paragraph(
    "The Service layer holds business logic. AuthService decides whether a given "
    "username/password combination is valid. The Controller does not know HOW "
    "authentication works — it just calls isAuthenticated() and gets a yes or no.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/service/AuthService.java", [
    "@Service",
    "public class AuthService {",
    "",
    "    private final AdminRepository adminRepository;",
    "",
    "    @Autowired",
    "    public AuthService(AdminRepository adminRepository) {",
    "        this.adminRepository = adminRepository;",
    "    }",
    "",
    "    public boolean isAuthenticated(LoginForm form) {",
    "        if (form == null) return false;",
    "",
    "        String username = form.getUsername();",
    "        String password = form.getPassword();",
    "",
    "        if (username == null || username.trim().isEmpty()) return false;",
    "        if (password == null || password.trim().isEmpty()) return false;",
    "",
    "        // Normalise: 'Movindu' and 'movindu' both work",
    "        String cleanedUsername = username.trim().toLowerCase();",
    "",
    "        Optional&lt;Admin&gt; maybeAdmin = adminRepository.findByUsername(cleanedUsername);",
    "        if (maybeAdmin.isEmpty()) return false;",
    "",
    "        Admin admin = maybeAdmin.get();",
    "        return admin.getPassword().equals(password);  // .equals() compares text",
    "    }",
    "}",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>@Service</b>", h3))
story.append(Paragraph(
    "Marks this class as a Spring-managed bean. Spring creates one instance and "
    "injects it wherever it is needed (e.g. into AuthController).", body))
story.append(Paragraph("<b>@Autowired constructor injection</b>", h3))
story.append(Paragraph(
    "Spring sees that AuthService needs an AdminRepository, finds the one it already "
    "created, and passes it in through the constructor automatically. "
    "This is called Dependency Injection — we do not call new AdminRepository() ourselves.", body))
story.append(Paragraph("<b>Why .equals() and not ==?</b>", h3))
story.append(Paragraph(
    "In Java, == on String objects compares memory addresses, not content. "
    "Two different String objects with the same text would return false with ==. "
    ".equals() compares the actual characters, which is what we want.", body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 13 — ArticleService.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("13. Service: ArticleService.java"))
story.append(sp())
story.append(Paragraph(
    "ArticleService is the go-between for article data. The Controller asks it to "
    "find/save/delete articles. The Service adds any extra logic (like stamping the "
    "lastUpdated time) before delegating to the Repository.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/service/ArticleService.java  (key methods)", [
    "public List&lt;Article&gt; findAll() {",
    "    return articleRepository.findAll();",
    "}",
    "",
    "public Optional&lt;Article&gt; findById(Long id) {",
    "    return articleRepository.findById(id);",
    "}",
    "",
    "public List&lt;Article&gt; findByCategory(String category) {",
    "    if (category == null || category.trim().isEmpty()) return findAll();",
    "    return articleRepository.findByCategoryIgnoreCase(category.trim());",
    "}",
    "",
    "public List&lt;Article&gt; search(String text) {",
    "    if (text == null || text.trim().isEmpty()) return findAll();",
    "    return articleRepository.findByTitleContainingIgnoreCase(text.trim());",
    "}",
    "",
    "public Article save(Article article) {",
    "    article.setLastUpdated(LocalDateTime.now());  // always stamp the time",
    "    return articleRepository.save(article);",
    "}",
    "",
    "public void deleteById(Long id) { articleRepository.deleteById(id); }",
    "public boolean existsById(Long id) { return articleRepository.existsById(id); }",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>Why does save() work for both CREATE and UPDATE?</b>", h3))
story.append(Paragraph(
    "JPA's save() checks whether the Article has an id set. "
    "If the id is null (new article) — it runs INSERT. "
    "If the id is already set (existing article) — it runs UPDATE. "
    "In AdminController we call article.setId(id) before saving an edit, "
    "which tells JPA to update the existing row.", body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 14 — AuthController.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("14. Controller: AuthController.java"))
story.append(sp())
story.append(Paragraph(
    "AuthController handles login, logout and the register placeholder. "
    "It is the first controller the user interacts with.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/controller/AuthController.java", [
    "@Controller",
    "@RequestMapping(\"/\")",
    "public class AuthController {",
    "",
    "    public static final String SESSION_ADMIN_KEY = \"loggedInAdmin\";",
    "",
    "    private final AuthService authService;",
    "",
    "    @Autowired",
    "    public AuthController(AuthService authService) {",
    "        this.authService = authService;",
    "    }",
    "",
    "    @GetMapping({\"/\", \"/login\"})",
    "    public String showLoginPage(Model model) {",
    "        model.addAttribute(\"loginForm\", new LoginForm());",
    "        return \"login\";",
    "    }",
    "",
    "    @PostMapping(\"/login\")",
    "    public String processLogin(@ModelAttribute LoginForm loginForm,",
    "                               HttpSession session, Model model) {",
    "        boolean ok = authService.isAuthenticated(loginForm);",
    "        if (ok) {",
    "            session.setAttribute(SESSION_ADMIN_KEY, loginForm.getUsername().trim().toLowerCase());",
    "            return \"redirect:/admin\";",
    "        }",
    "        model.addAttribute(\"errorMessage\", \"Invalid username or password.\");",
    "        return \"error\";",
    "    }",
    "",
    "    @GetMapping(\"/logout\")",
    "    public String logout(HttpSession session) {",
    "        session.invalidate();",
    "        return \"redirect:/login\";",
    "    }",
    "}",
]))
story.append(sp(0.3))
auth_rows = [
    ["Code", "Plain-English meaning"],
    ["@Controller", "Marks this class as a Spring MVC controller (handles HTTP requests)"],
    ["@RequestMapping(\"/\")", "All URLs in this class start from the root path /"],
    ["SESSION_ADMIN_KEY = \"loggedInAdmin\"", "A constant string used as the key when storing the username in the session"],
    ["@GetMapping({\"/\", \"/login\"})", "Respond to GET requests for both / and /login with the same method"],
    ["model.addAttribute(\"loginForm\", ...)", "Put an empty LoginForm in the Model so Thymeleaf can bind the form fields to it"],
    ["@PostMapping(\"/login\")", "Respond to the form submission (browser sends POST when user clicks Log in)"],
    ["@ModelAttribute LoginForm", "Spring reads the posted form fields and fills them into a LoginForm object"],
    ["session.setAttribute(...)", "Store the admin's username in the session — like a sticky note on the browser"],
    ["return \"redirect:/admin\"", "Tell the browser to navigate to /admin (Post-Redirect-Get pattern)"],
    ["session.invalidate()", "Delete everything in the session — the user is now logged out"],
]
at = Table(auth_rows, colWidths=[6*cm, 11*cm])
at.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  NAVY),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTNAME",      (0,1), (0,-1),  "Courier"),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [HexColor("#f8fafc"), WHITE]),
    ("GRID",          (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(at)
story.append(sp(0.3))
story.append(tip_box(
    "If asked 'what is a session?': a session is server-side storage tied to one browser. "
    "Spring gives each browser a unique cookie (JSESSIONID). When the browser sends a request, "
    "Spring looks up that cookie and retrieves any data we stored with setAttribute. "
    "When we call invalidate(), that data is deleted and the user must log in again."
))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 15 — WikiController.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("15. Controller: WikiController.java"))
story.append(sp())
story.append(Paragraph(
    "WikiController handles the public-facing wiki pages. Anyone can access these — "
    "no login required. It also passes an isAdmin flag to the templates so they can "
    "show extra buttons when an admin is logged in.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/controller/WikiController.java  (key parts)", [
    "@Controller",
    "@RequestMapping(\"/wiki\")",
    "public class WikiController {",
    "",
    "    private boolean isAdmin(HttpSession session) {",
    "        return session.getAttribute(AuthController.SESSION_ADMIN_KEY) != null;",
    "    }",
    "",
    "    @GetMapping",
    "    public String listArticles(",
    "            @RequestParam(required = false) String category,",
    "            @RequestParam(required = false) String search,",
    "            HttpSession session, Model model) {",
    "",
    "        List&lt;Article&gt; articles;",
    "        if (search != null &amp;&amp; !search.trim().isEmpty())",
    "            articles = articleService.search(search);",
    "        else if (category != null &amp;&amp; !category.trim().isEmpty())",
    "            articles = articleService.findByCategory(category);",
    "        else",
    "            articles = articleService.findAll();",
    "",
    "        // Build a sorted list of unique category names for the filter buttons.",
    "        // Loop through every article; if the category is not already in the",
    "        // list, add it. Then sort the list alphabetically.",
    "        List&lt;String&gt; categories = new ArrayList&lt;&gt;();",
    "        for (Article a : articleService.findAll()) {",
    "            if (!categories.contains(a.getCategory())) {",
    "                categories.add(a.getCategory());",
    "            }",
    "        }",
    "        Collections.sort(categories);",
    "",
    "        model.addAttribute(\"articles\", articles);",
    "        model.addAttribute(\"categories\", categories);",
    "        model.addAttribute(\"category\", category);",
    "        model.addAttribute(\"search\", search);",
    "        model.addAttribute(\"isAdmin\", isAdmin(session));",
    "        return \"wiki/list\";",
    "    }",
    "",
    "    @GetMapping(\"/{id}\")",
    "    public String viewArticle(@PathVariable Long id,",
    "                              HttpSession session, Model model) {",
    "        Optional&lt;Article&gt; maybeArticle = articleService.findById(id);",
    "        if (maybeArticle.isEmpty()) {",
    "            model.addAttribute(\"errorMessage\", \"Article not found.\");",
    "            return \"error\";",
    "        }",
    "        model.addAttribute(\"article\", maybeArticle.get());",
    "        model.addAttribute(\"isAdmin\", isAdmin(session));",
    "        return \"wiki/view\";",
    "    }",
    "}",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>@RequestParam(required = false)</b>", h3))
story.append(Paragraph(
    "URL parameters like /wiki?search=java or /wiki?category=Programming are optional. "
    "If the URL does not include them, Spring passes null instead of crashing.", body))
story.append(Paragraph("<b>How the categories list is built</b>", h3))
story.append(Paragraph(
    "We start with an empty ArrayList called categories. "
    "We loop through every article with a for loop. "
    "For each article, we check: is this article's category already in the list? "
    "If not, we add it. "
    "After the loop, Collections.sort() sorts the list alphabetically. "
    "This gives us e.g. ['General', 'History', 'Programming', 'Testing'] "
    "which the template uses to display the clickable filter pills.", body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 16 — AdminController.java
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("16. Controller: AdminController.java"))
story.append(sp())
story.append(Paragraph(
    "AdminController is the most complex controller. It handles the full CRUD cycle "
    "for articles and protects every method with a session check.", body))
story.append(sp(0.2))
story.append(code_block("src/main/java/com/wikiapp/controller/AdminController.java  (structure)", [
    "@Controller",
    "@RequestMapping(\"/admin\")",
    "public class AdminController {",
    "",
    "    private boolean isLoggedIn(HttpSession session) {",
    "        return session.getAttribute(AuthController.SESSION_ADMIN_KEY) != null;",
    "    }",
    "",
    "    // READ — show all articles",
    "    @GetMapping",
    "    public String dashboard(HttpSession session, Model model) {",
    "        if (!isLoggedIn(session)) return \"redirect:/login\";",
    "        model.addAttribute(\"articles\", articleService.findAll());",
    "        model.addAttribute(\"adminUser\",",
    "            session.getAttribute(AuthController.SESSION_ADMIN_KEY));",
    "        return \"admin/dashboard\";",
    "    }",
    "",
    "    // CREATE — show empty form",
    "    @GetMapping(\"/new\")",
    "    public String showCreateForm(HttpSession session, Model model) {",
    "        if (!isLoggedIn(session)) return \"redirect:/login\";",
    "        model.addAttribute(\"article\", new Article());",
    "        model.addAttribute(\"mode\", \"create\");",
    "        return \"admin/form\";",
    "    }",
    "",
    "    // CREATE — save the new article",
    "    @PostMapping",
    "    public String createArticle(@Valid @ModelAttribute Article article,",
    "                                BindingResult bindingResult, ...)",
    "        if (bindingResult.hasErrors()) { return \"admin/form\"; }",
    "        articleService.save(article);",
    "        return \"redirect:/admin\";",
    "    }",
    "",
    "    // UPDATE — show pre-filled edit form",
    "    @GetMapping(\"/edit/{id}\")",
    "    // UPDATE — save the changes",
    "    @PostMapping(\"/edit/{id}\")",
    "        article.setId(id);   // &lt;-- crucial: tells JPA to UPDATE not INSERT",
    "        articleService.save(article);",
    "",
    "    // DELETE — confirmation page",
    "    @GetMapping(\"/delete/{id}\")",
    "    // DELETE — actually delete",
    "    @PostMapping(\"/delete/{id}\")",
    "        articleService.deleteById(id);",
    "        return \"redirect:/admin\";",
    "}",
]))
story.append(sp(0.3))
story.append(Paragraph("<b>The guard pattern — isLoggedIn check</b>", h3))
story.append(Paragraph(
    "Every method starts with: if (!isLoggedIn(session)) return 'redirect:/login'; "
    "This means if someone manually types /admin/new into the browser without logging in, "
    "they are immediately sent back to the login page. "
    "The session attribute is only set by AuthController after a successful login.", body))
story.append(Paragraph("<b>@Valid and BindingResult</b>", h3))
story.append(Paragraph(
    "@Valid triggers the @NotBlank validation on the Article object. "
    "BindingResult collects any errors. "
    "If hasErrors() is true, we return the form template again (with errors shown) "
    "instead of saving.", body))
story.append(Paragraph("<b>article.setId(id) before save for UPDATE</b>", h3))
story.append(Paragraph(
    "When the edit form is submitted, Spring creates a new Article object from the "
    "form data — but this new object has no id (so JPA would INSERT a duplicate). "
    "We call article.setId(id) — copying the id from the URL path — before saving. "
    "Now JPA sees an existing id and runs UPDATE instead of INSERT.", body))
story.append(tip_box(
    "CRUD stands for Create, Read, Update, Delete. AdminController implements all four: "
    "GET /admin/new + POST /admin = Create; "
    "GET /admin = Read (list); "
    "GET + POST /admin/edit/{id} = Update; "
    "GET + POST /admin/delete/{id} = Delete."
))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# TEMPLATES SECTION
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("17. Template: login.html", GREEN))
story.append(sp())
story.append(Paragraph(
    "Thymeleaf templates are normal HTML files with special th: attributes. "
    "The browser never sees these attributes — Thymeleaf processes them on the "
    "server and sends plain HTML to the browser.", body))
story.append(sp(0.2))
story.append(code_block("src/main/resources/templates/login.html  (key parts)", [
    "&lt;form th:action=\"@{/login}\" th:object=\"${loginForm}\" method=\"post\"&gt;",
    "    &lt;input type=\"text\" th:field=\"*{username}\" /&gt;",
    "    &lt;input type=\"password\" th:field=\"*{password}\" /&gt;",
    "    &lt;button type=\"submit\"&gt;Log in&lt;/button&gt;",
    "&lt;/form&gt;",
]))
story.append(sp(0.2))
thymel = [
    ["Thymeleaf attribute", "What it does"],
    ["th:action=\"@{/login}\"", "Sets the form's action URL to /login (builds the correct URL even with a context path)"],
    ["th:object=\"${loginForm}\"", "Binds the whole form to the loginForm object placed in the Model by the Controller"],
    ["th:field=\"*{username}\"", "Shortcut for name=\"username\" id=\"username\" value=\"${loginForm.username}\" — binds the field to the username property"],
    ["th:href=\"@{/wiki}\"", "@{} always builds the correct URL — use it instead of hard-coding href values"],
    ["th:text=\"${value}\"", "Sets the text content of an element from the Model"],
    ["th:if=\"${condition}\"", "Renders the element only if the condition is true"],
    ["th:unless=\"${condition}\"", "Renders the element only if the condition is FALSE (opposite of th:if)"],
    ["th:each=\"a : ${articles}\"", "Loops over the articles list — like a Java for-each loop"],
    ["th:errors=\"*{title}\"", "Displays the @NotBlank error message for the title field"],
]
t_tbl = Table(thymel, colWidths=[6*cm, 11*cm])
t_tbl.setStyle(TableStyle([
    ("BACKGROUND",    (0,0), (-1,0),  GREEN),
    ("TEXTCOLOR",     (0,0), (-1,0),  WHITE),
    ("FONTNAME",      (0,0), (-1,0),  "Helvetica-Bold"),
    ("FONTNAME",      (0,1), (0,-1),  "Courier"),
    ("ROWBACKGROUNDS",(0,1), (-1,-1), [HexColor("#f0fdf4"), WHITE]),
    ("GRID",          (0,0), (-1,-1), 0.5, HexColor("#e2e8f0")),
    ("FONTSIZE",      (0,0), (-1,-1), 8.5),
    ("TOPPADDING",    (0,0), (-1,-1), 7),
    ("BOTTOMPADDING", (0,0), (-1,-1), 7),
    ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ("VALIGN",        (0,0), (-1,-1), "TOP"),
]))
story.append(t_tbl)
story.append(PageBreak())

# 18 — wiki/list.html
story.append(section_header("18. Template: wiki/list.html", GREEN))
story.append(sp())
story.append(Paragraph(
    "The public wiki home page. Shows the article grid, search bar, "
    "category filter pills, and admin controls if the user is logged in.", body))
story.append(sp(0.2))
story.append(code_block("templates/wiki/list.html  (key sections)", [
    "&lt;!-- Category filter pills --&gt;",
    "&lt;div class=\"category-filters\"&gt;",
    "  &lt;a class=\"filter-pill\" th:href=\"@{/wiki}\"&gt;All&lt;/a&gt;",
    "  &lt;a class=\"filter-pill\"",
    "     th:each=\"cat : ${categories}\"",
    "     th:classappend=\"${category == cat} ? ' active'\"",
    "     th:href=\"@{/wiki(category=${cat})}\"",
    "     th:text=\"${cat}\"&gt;Category&lt;/a&gt;",
    "&lt;/div&gt;",
    "",
    "&lt;!-- Article cards --&gt;",
    "&lt;article class=\"article-card\" th:each=\"a : ${articles}\"&gt;",
    "  &lt;span class=\"badge\" th:text=\"${a.category}\"&gt;&lt;/span&gt;",
    "  &lt;h2&gt;&lt;a th:href=\"@{'/wiki/' + ${a.id}}\" th:text=\"${a.title}\"&gt;&lt;/a&gt;&lt;/h2&gt;",
    "  &lt;p th:text=\"${#strings.abbreviate(a.content, 120)}\"&gt;&lt;/p&gt;",
    "  &lt;p th:text=\"${#temporals.format(a.lastUpdated, 'dd MMM yyyy')}\"&gt;&lt;/p&gt;",
    "  &lt;div class=\"card-actions\" th:if=\"${isAdmin}\"&gt;",
    "    &lt;a class=\"btn small\" th:href=\"@{'/admin/edit/' + ${a.id}}\"&gt;Edit&lt;/a&gt;",
    "    &lt;a class=\"btn small danger\" th:href=\"@{'/admin/delete/' + ${a.id}}\"&gt;Delete&lt;/a&gt;",
    "  &lt;/div&gt;",
    "&lt;/article&gt;",
]))
story.append(sp(0.2))
story.append(Paragraph("<b>th:classappend</b>", h3))
story.append(Paragraph(
    "Adds an extra CSS class to an element without removing existing classes. "
    "Here it adds ' active' to the pill whose category matches the current filter, "
    "making it appear highlighted in blue.", body))
story.append(Paragraph("<b>#strings.abbreviate(text, 120)</b>", h3))
story.append(Paragraph(
    "Thymeleaf's built-in utility. Cuts the content text at 120 characters and adds "
    "'...' at the end, so the article cards all have the same height.", body))
story.append(Paragraph("<b>#temporals.format(date, pattern)</b>", h3))
story.append(Paragraph(
    "Formats a LocalDateTime into a readable string like '03 Jun 2026'. "
    "Without this, the raw Java timestamp would show an ugly number.", body))
story.append(PageBreak())

# 19 — wiki/view.html
story.append(section_header("19. Template: wiki/view.html", GREEN))
story.append(sp())
story.append(code_block("templates/wiki/view.html  (key parts)", [
    "&lt;!-- Admin controls — only shown when isAdmin is true --&gt;",
    "&lt;div class=\"article-nav-row\"&gt;",
    "  &lt;a class=\"back\" th:href=\"@{/wiki}\"&gt;&amp;larr; Back to all articles&lt;/a&gt;",
    "  &lt;div class=\"admin-actions\" th:if=\"${isAdmin}\"&gt;",
    "    &lt;a class=\"btn small\" th:href=\"@{'/admin/edit/' + ${article.id}}\"&gt;Edit article&lt;/a&gt;",
    "    &lt;a class=\"btn small danger\" th:href=\"@{'/admin/delete/' + ${article.id}}\"&gt;Delete article&lt;/a&gt;",
    "  &lt;/div&gt;",
    "&lt;/div&gt;",
    "",
    "&lt;article class=\"article-full\"&gt;",
    "  &lt;span class=\"badge\" th:text=\"${article.category}\"&gt;&lt;/span&gt;",
    "  &lt;h1 th:text=\"${article.title}\"&gt;&lt;/h1&gt;",
    "  &lt;div class=\"content\" th:text=\"${article.content}\"&gt;&lt;/div&gt;",
    "&lt;/article&gt;",
]))
story.append(sp(0.2))
story.append(Paragraph("<b>Why th:text instead of th:utext for content?</b>", h3))
story.append(Paragraph(
    "th:text auto-escapes HTML special characters (< becomes &lt; etc.). "
    "This means if someone puts &lt;script&gt; tags in an article, the browser "
    "displays them as plain text instead of running them. "
    "This protects against Cross-Site Scripting (XSS) attacks. "
    "th:utext would render raw HTML — only use it when you fully trust the content.", body))
story.append(PageBreak())

# 20 — admin/dashboard.html
story.append(section_header("20. Template: admin/dashboard.html", GREEN))
story.append(sp())
story.append(code_block("templates/admin/dashboard.html  (key parts)", [
    "&lt;nav class=\"topbar admin\"&gt;",
    "  &lt;span&gt;Logged in as &lt;strong th:text=\"${adminUser}\"&gt;&lt;/strong&gt;&lt;/span&gt;",
    "  &lt;a th:href=\"@{/wiki}\"&gt;View public wiki&lt;/a&gt;",
    "  &lt;a th:href=\"@{/logout}\"&gt;Log out&lt;/a&gt;",
    "&lt;/nav&gt;",
    "",
    "&lt;!-- th:unless hides the table when there are no articles --&gt;",
    "&lt;table class=\"data-table\" th:unless=\"${#lists.isEmpty(articles)}\"&gt;",
    "  &lt;tr th:each=\"a : ${articles}\"&gt;",
    "    &lt;td th:text=\"${a.id}\"&gt;&lt;/td&gt;",
    "    &lt;td&gt;&lt;a th:href=\"@{'/wiki/' + ${a.id}}\" th:text=\"${a.title}\"&gt;&lt;/a&gt;&lt;/td&gt;",
    "    &lt;td th:text=\"${#temporals.format(a.lastUpdated, 'dd MMM yyyy HH:mm')}\"&gt;&lt;/td&gt;",
    "    &lt;td&gt;",
    "      &lt;a th:href=\"@{'/admin/edit/' + ${a.id}}\"&gt;Edit&lt;/a&gt;",
    "      &lt;a th:href=\"@{'/admin/delete/' + ${a.id}}\"&gt;Delete&lt;/a&gt;",
    "    &lt;/td&gt;",
    "  &lt;/tr&gt;",
    "&lt;/table&gt;",
]))
story.append(sp(0.2))
story.append(Paragraph("<b>#lists.isEmpty(articles)</b>", h3))
story.append(Paragraph(
    "Thymeleaf utility method. Returns true if the list has zero items. "
    "Used here to show a friendly 'No articles yet' message instead of an empty table.", body))
story.append(PageBreak())

# 21 — admin/form.html
story.append(section_header("21. Template: admin/form.html", GREEN))
story.append(sp())
story.append(Paragraph(
    "One template that handles BOTH create and edit. The 'mode' attribute passed "
    "by the Controller controls the heading text, the form action URL, and the button label.", body))
story.append(sp(0.2))
story.append(code_block("templates/admin/form.html  (key parts)", [
    "&lt;!-- Title switches based on mode --&gt;",
    "&lt;h1 th:text=\"${mode == 'edit'} ? 'Edit article' : 'New article'\"&gt;&lt;/h1&gt;",
    "",
    "&lt;!-- Form action switches too --&gt;",
    "&lt;form th:action=\"${mode == 'edit'} ? @{'/admin/edit/' + ${article.id}} : @{/admin}\"",
    "      th:object=\"${article}\" method=\"post\"&gt;",
    "",
    "  &lt;label for=\"title\"&gt;Title&lt;/label&gt;",
    "  &lt;input type=\"text\" id=\"title\" th:field=\"*{title}\"/&gt;",
    "  &lt;p class=\"error-text\" th:if=\"${#fields.hasErrors('title')}\"",
    "                         th:errors=\"*{title}\"&gt;&lt;/p&gt;",
    "",
    "  &lt;label for=\"category\"&gt;Category&lt;/label&gt;",
    "  &lt;input type=\"text\" id=\"category\" th:field=\"*{category}\"/&gt;",
    "",
    "  &lt;label for=\"content\"&gt;Content&lt;/label&gt;",
    "  &lt;textarea id=\"content\" th:field=\"*{content}\" rows=\"10\"&gt;&lt;/textarea&gt;",
    "",
    "  &lt;a class=\"btn secondary\" th:href=\"@{/admin}\"&gt;Cancel&lt;/a&gt;",
    "  &lt;button class=\"btn primary\" type=\"submit\"",
    "     th:text=\"${mode == 'edit'} ? 'Save changes' : 'Create article'\"&gt;&lt;/button&gt;",
    "&lt;/form&gt;",
]))
story.append(sp(0.2))
story.append(Paragraph("<b>The ternary operator in Thymeleaf — ? :</b>", h3))
story.append(Paragraph(
    "${mode == 'edit'} ? 'Edit article' : 'New article' "
    "means: if mode equals 'edit', use 'Edit article'; otherwise use 'New article'. "
    "Same as the Java ternary operator (condition ? valueIfTrue : valueIfFalse).", body))
story.append(Paragraph("<b>#fields.hasErrors('title') and th:errors</b>", h3))
story.append(Paragraph(
    "#fields.hasErrors checks whether the BindingResult has an error for a specific field. "
    "th:errors displays the error message text (e.g. 'Title is required'). "
    "These only appear after a failed form submission.", body))
story.append(PageBreak())

# 22 — admin/confirm-delete.html
story.append(section_header("22. Template: admin/confirm-delete.html", GREEN))
story.append(sp())
story.append(code_block("templates/admin/confirm-delete.html  (key parts)", [
    "&lt;div class=\"card error\"&gt;",
    "  &lt;h1&gt;Delete article?&lt;/h1&gt;",
    "  &lt;blockquote&gt;",
    "    &lt;strong th:text=\"${article.title}\"&gt;&lt;/strong&gt;",
    "    &lt;span class=\"badge\" th:text=\"${article.category}\"&gt;&lt;/span&gt;",
    "  &lt;/blockquote&gt;",
    "  &lt;p&gt;This action cannot be undone.&lt;/p&gt;",
    "",
    "  &lt;form th:action=\"@{'/admin/delete/' + ${article.id}}\" method=\"post\"&gt;",
    "    &lt;a class=\"btn secondary\" th:href=\"@{/admin}\"&gt;Cancel&lt;/a&gt;",
    "    &lt;button class=\"btn danger\" type=\"submit\"&gt;Yes, delete&lt;/button&gt;",
    "  &lt;/form&gt;",
    "&lt;/div&gt;",
]))
story.append(sp(0.2))
story.append(Paragraph("<b>Why use a POST form for delete instead of just a link?</b>", h3))
story.append(Paragraph(
    "A normal link (anchor tag) sends a GET request. GET requests should never change "
    "data — they are meant for reading. If delete were a GET link, a browser prefetch, "
    "a search-engine crawler, or someone accidentally opening the link could delete "
    "an article without confirmation. "
    "Using a POST form means the browser only sends the delete request when the user "
    "actually clicks the 'Yes, delete' button. This is called the "
    "Post-Redirect-Get (PRG) pattern.", body))
story.append(PageBreak())

# ═══════════════════════════════════════════════════════════════════════════════
# 23 — VIVA Q&A
# ═══════════════════════════════════════════════════════════════════════════════
story.append(section_header("23. Viva Q&A — 30 Likely Questions", RED))
story.append(sp())
story.append(Paragraph(
    "Read each answer aloud at least once before the viva. "
    "Use your own words — do not memorise word for word.", body))
story.append(sp(0.3))

qas = [
    ("What does @SpringBootApplication do?",
     "It does three things: (1) enables auto-configuration so Spring sets up the database and "
     "Thymeleaf automatically, (2) triggers component scanning so Spring finds all my @Controller, "
     "@Service and @Repository classes, and (3) marks the class as a configuration source."),

    ("What is MVC and how does your project use it?",
     "MVC is Model-View-Controller. The Model is my Article and Admin classes (data). "
     "The View is my Thymeleaf HTML templates. The Controller layer handles HTTP requests, "
     "calls the Service for data, puts it in the Model, and returns the template name. "
     "This separation means I can change the HTML without touching the Java code."),

    ("What is the difference between @GetMapping and @PostMapping?",
     "@GetMapping handles GET requests — when the browser navigates to a URL or clicks a link. "
     "I use it to show forms and pages. @PostMapping handles POST requests — when a form is "
     "submitted. I use it to process login, create articles and delete articles."),

    ("What is Thymeleaf?",
     "Thymeleaf is a Java template engine. I write normal HTML files with extra th: attributes. "
     "When a request comes in, Thymeleaf processes the template on the server, replaces all "
     "the th: attributes with real values from the Model, and sends plain HTML to the browser. "
     "The browser never sees any Thymeleaf code."),

    ("What is a JPA entity?",
     "A JPA entity is a Java class annotated with @Entity that is automatically mapped to a "
     "database table. Each field becomes a column. Each instance of the class becomes a row. "
     "In my project, Article maps to the ARTICLE table and Admin maps to the ADMIN table."),

    ("What does JpaRepository give you?",
     "By extending JpaRepository, I automatically get findAll(), findById(), save(), "
     "deleteById() and existsById() without writing any code. Spring generates the SQL "
     "queries at startup. I can also declare custom methods just by naming them correctly, "
     "like findByCategoryIgnoreCase()."),

    ("How does the login work end to end?",
     "The user submits the login form. The browser sends a POST to /login. "
     "AuthController receives it, calls AuthService.isAuthenticated(). "
     "AuthService looks up the username in the ADMIN table using AdminRepository. "
     "If found and the password matches, AuthController stores the username in the "
     "HttpSession and redirects to /admin. If not, it shows the error page."),

    ("What is an HttpSession and how do you use it?",
     "HttpSession is server-side storage tied to one browser. Spring gives each browser "
     "a unique cookie. When I call session.setAttribute('loggedInAdmin', username), "
     "the username is stored on the server linked to that cookie. "
     "On every admin page, I check session.getAttribute('loggedInAdmin') — if it is null, "
     "the user is not logged in and I redirect them to /login. "
     "session.invalidate() on logout deletes everything."),

    ("How do you protect the admin pages?",
     "Every method in AdminController starts with: if (!isLoggedIn(session)) return 'redirect:/login'; "
     "The isLoggedIn() helper checks whether the session has the 'loggedInAdmin' key. "
     "If not, the user is sent to the login page regardless of what URL they typed."),

    ("What is the difference between @NotBlank on LoginForm and @NotBlank on Article?",
     "On LoginForm, @NotBlank prevents the login form from being submitted empty. "
     "The Controller uses @ModelAttribute (not @Valid), so AuthService does its own null checks. "
     "On Article, @NotBlank triggers Spring's validation when @Valid is used in AdminController. "
     "If any field is blank, BindingResult captures the error and the form is re-displayed "
     "with the error message shown next to the field."),

    ("What does Optional<T> mean?",
     "Optional is a wrapper that either contains a value or is empty — it is never null. "
     "When findById() cannot find an article, it returns an empty Optional instead of null. "
     "I call maybeArticle.isEmpty() to check if nothing was found, and maybeArticle.get() "
     "to get the actual article. This avoids NullPointerExceptions."),

    ("How does CREATE work in AdminController?",
     "GET /admin/new shows an empty form (a new Article() with no id). "
     "POST /admin receives the submitted form, validates it with @Valid, "
     "and calls articleService.save(article). Since the article has no id, "
     "JPA runs INSERT INTO article ... and assigns a new id automatically."),

    ("How does UPDATE differ from CREATE?",
     "GET /admin/edit/{id} loads the existing article from the database and pre-fills the form. "
     "When the form is submitted (POST /admin/edit/{id}), Spring creates a new Article "
     "from the form data — but this new object has no id. "
     "I call article.setId(id) to set the id from the URL, then save(). "
     "JPA sees an existing id and runs UPDATE instead of INSERT."),

    ("Why do you use a POST form for delete instead of a link?",
     "A link sends a GET request. GET should never change data. "
     "A browser might prefetch links or a search engine might crawl them, "
     "accidentally deleting articles. Using a POST form means the delete only "
     "happens when the user physically clicks the 'Yes, delete' button on the "
     "confirmation page."),

    ("What is the Post-Redirect-Get pattern?",
     "After processing a POST request (create, update, delete), the controller "
     "returns 'redirect:/admin' instead of rendering a template directly. "
     "This tells the browser to make a new GET request to /admin. "
     "If the user refreshes the page, the GET is repeated — not the POST. "
     "Without this, refreshing would re-submit the form and create duplicate articles."),

    ("What is H2 and why did you use it?",
     "H2 is a small SQL database written in Java. It runs inside the application process — "
     "no installation needed. I configured it to store data in a file (./data/wikidb) so "
     "articles survive server restarts. It also has a browser console at /h2-console "
     "which is useful for showing the database contents during a demo."),

    ("What does ddl-auto=update mean?",
     "It tells Hibernate (the JPA implementation) to automatically create the ARTICLE and "
     "ADMIN tables if they do not exist, and update the schema if I add a new field to an "
     "entity class. It never drops existing data. I use this during development; "
     "in production you would use 'validate' or 'none'."),

    ("What is data.sql and why does it use MERGE?",
     "data.sql is a SQL file that Spring runs automatically every startup to seed the database "
     "with an admin account and sample articles. I use MERGE instead of INSERT because the "
     "file runs on every startup. INSERT would fail the second time because the rows already "
     "exist. MERGE says: insert if not there, skip if already there."),

    ("What is constructor injection and why is it preferred?",
     "Constructor injection is when Spring passes the dependencies (like ArticleRepository) "
     "through the constructor. This is preferred over field injection (@Autowired on a field) "
     "because: the dependency cannot be null (it is required at construction time), "
     "the class can be tested by just passing a mock in the constructor, "
     "and it makes dependencies explicit and visible."),

    ("What does @RequestParam do?",
     "@RequestParam extracts a value from the URL query string. "
     "For example, /wiki?search=java passes 'java' to the search parameter. "
     "I use required=false so the parameter is optional — if the URL has no ?search=..., "
     "Spring passes null and the controller shows all articles."),

    ("What does @PathVariable do?",
     "@PathVariable extracts a value from the URL path. "
     "In @GetMapping('/{id}'), the {id} is a placeholder. "
     "When someone visits /wiki/3, Spring extracts '3', converts it to a Long, "
     "and passes it to the id parameter."),

    ("What is the Model in Spring MVC?",
     "The Model is a container (like a Map) that the Controller uses to pass data to the template. "
     "model.addAttribute('articles', list) puts the list in the Model with the key 'articles'. "
     "In the Thymeleaf template, ${articles} reads it back. "
     "The Model only exists for the duration of one request."),

    ("How do you build the categories list in WikiController?",
     "I use a simple for loop. I start with an empty ArrayList. "
     "I loop through every article using a for-each loop. "
     "Inside the loop I check: if the article's category is not already in the list, I add it. "
     "After the loop I call Collections.sort() to sort the list alphabetically. "
     "This produces ['General', 'History', 'Programming', 'Testing'] "
     "which the template displays as clickable filter pills."),

    ("What is the layered architecture and why is it important?",
     "My project has three layers: Controller, Service, Repository. "
     "The Controller only handles HTTP — it does not write SQL. "
     "The Repository only talks to the database — it does not know about HTTP. "
     "The Service holds the business logic in between. "
     "This means I can change the database (e.g. swap H2 for MySQL) by only changing "
     "the Repository, without touching the Controller or templates."),

    ("What is the difference between Part A and Part B?",
     "Part A: login with hard-coded credentials (no database), only the login flow. "
     "Part B: H2 database, JPA entities (Article, Admin), Spring Data repositories, "
     "full CRUD for articles via AdminController, public wiki via WikiController, "
     "and HttpSession-based authentication instead of hard-coded checks."),

    ("How does the category filter work?",
     "WikiController loops through all articles and collects unique category names into an ArrayList. "
     "It sorts the list and puts it in the Model as 'categories'. "
     "The template shows each as a clickable pill link: /wiki?category=Programming. "
     "When clicked, the browser sends a GET with ?category=Programming, the Controller "
     "reads it with @RequestParam and calls articleService.findByCategory(category), "
     "which runs SELECT ... WHERE UPPER(category) = UPPER(?)."),

    ("What is isAdmin and how do templates use it?",
     "WikiController checks session.getAttribute('loggedInAdmin') and puts a boolean "
     "isAdmin = true/false in the Model. The template uses th:if='${isAdmin}' to show "
     "the Edit/Delete buttons and the admin nav links only when isAdmin is true. "
     "This is the correct MVC approach — the Controller decides, the template just displays."),

    ("What happens if I try to edit an article that does not exist?",
     "AdminController calls articleService.findById(id) which returns an Optional. "
     "If the Optional is empty (no such id), the controller adds an errorMessage to the Model "
     "and returns the 'error' template, which shows a friendly message. "
     "It does not crash with an exception."),

    ("What is the @Service annotation?",
     "@Service marks a class as a Spring-managed service bean. "
     "Spring creates one instance of it when the application starts and injects it "
     "wherever it is needed (e.g. into AuthController and AdminController). "
     "Without this annotation, Spring would not find the class during component scanning."),

    ("How would you add a second admin user?",
     "I would add another MERGE INTO ADMIN ... row in data.sql with a different id and username. "
     "When the application next starts, data.sql runs and inserts the new row. "
     "The AdminRepository.findByUsername() query will then find this user when they log in. "
     "No Java code changes needed — that is the benefit of using a database instead of "
     "hard-coded credentials."),
]

for q, a in qas:
    story.append(KeepTogether([qa_box(q, a), sp(0.2)]))

story.append(sp(0.4))
story.append(tip_box(
    "Final viva tip: if you get a question you are not sure about, do not panic. "
    "Say: 'Let me walk you through the code'. Open the relevant file in your IDE, "
    "point to the lines, and explain what each annotation or method does. "
    "Examiners value understanding over memorisation.",
    colour=HexColor("#f0fdf4"), border=GREEN, label="FINAL TIP"
))

# ── Build ─────────────────────────────────────────────────────────────────────
doc = SimpleDocTemplate(
    OUTPUT,
    pagesize=A4,
    leftMargin=2*cm, rightMargin=2*cm,
    topMargin=2*cm, bottomMargin=2*cm,
    title="WikiApp Viva Preparation Guide",
    author="Movindu Lochana (s1577380)"
)

def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.setFillColor(LGREY)
    canvas.drawString(2*cm, 1.2*cm,
        "WikiApp Viva Guide  |  Movindu Lochana (s1577380)  |  BIT235 Assessment 2")
    canvas.drawRightString(19*cm, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()

doc.build(story, onFirstPage=on_page, onLaterPages=on_page)
print(f"Wrote: {OUTPUT}")
