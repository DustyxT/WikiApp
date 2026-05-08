"""Generate the WikiApp Code Walkthrough PDF report (Part A + Part B)."""
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib.colors import HexColor
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, PageBreak,
                                Preformatted, Table, TableStyle)
import html as ihtml

OUTPUT = "WikiApp_Code_Walkthrough.pdf"
PAGE_W, PAGE_H = A4

# ---------- styles ----------
styles = getSampleStyleSheet()

BLUE = HexColor("#1e3a8a")
BLUE2 = HexColor("#2563eb")
GREEN = HexColor("#16a34a")
GREY = HexColor("#374151")
LIGHT = HexColor("#f3f4f6")
DARK = HexColor("#111827")

cover_title = ParagraphStyle("CoverTitle", parent=styles["Title"],
    fontSize=32, leading=38, textColor=BLUE, alignment=TA_CENTER, spaceAfter=18)
cover_sub = ParagraphStyle("CoverSub", parent=styles["Normal"],
    fontSize=16, leading=22, textColor=GREY, alignment=TA_CENTER, spaceAfter=12)
cover_meta = ParagraphStyle("CoverMeta", parent=styles["Normal"],
    fontSize=13, leading=18, textColor=DARK, alignment=TA_CENTER)

h1 = ParagraphStyle("H1", parent=styles["Heading1"],
    fontSize=20, leading=24, textColor=BLUE, spaceBefore=12, spaceAfter=10)
h1b = ParagraphStyle("H1b", parent=h1, textColor=GREEN)
part_h = ParagraphStyle("Part", parent=styles["Heading1"],
    fontSize=26, leading=32, textColor=BLUE, alignment=TA_CENTER,
    spaceBefore=20, spaceAfter=14)
h2 = ParagraphStyle("H2", parent=styles["Heading2"],
    fontSize=15, leading=19, textColor=BLUE2, spaceBefore=10, spaceAfter=6)

body = ParagraphStyle("Body", parent=styles["Normal"],
    fontSize=10.5, leading=15, textColor=DARK, alignment=TA_JUSTIFY, spaceAfter=6)
bullet = ParagraphStyle("Bullet", parent=body, leftIndent=14, bulletIndent=4, spaceAfter=2)
note = ParagraphStyle("Note", parent=body, textColor=GREY, fontSize=9.5, leading=13)

code_style = ParagraphStyle("Code", parent=styles["Code"],
    fontSize=8.5, leading=11, textColor=DARK, leftIndent=6, rightIndent=6,
    backColor=LIGHT, borderColor=HexColor("#d1d5db"), borderWidth=0.5,
    borderPadding=6, spaceBefore=4, spaceAfter=8)

# ---------- helpers ----------
def P(text, style=body):
    return Paragraph(text, style)

def code(text):
    return Preformatted(text, code_style)

def hr_table(color=BLUE):
    t = Table([[" "]], colWidths=[16*cm], rowHeights=[2])
    t.setStyle(TableStyle([("BACKGROUND",(0,0),(-1,-1),color)]))
    return t

def kv_table(rows, col_widths=(5*cm, 11*cm)):
    data = [[P(f"<b>{k}</b>", body), P(v, body)] for k, v in rows]
    t = Table(data, colWidths=col_widths, hAlign="LEFT")
    t.setStyle(TableStyle([
        ("VALIGN",(0,0),(-1,-1),"TOP"),
        ("BACKGROUND",(0,0),(0,-1),LIGHT),
        ("BOX",(0,0),(-1,-1),0.5,HexColor("#d1d5db")),
        ("INNERGRID",(0,0),(-1,-1),0.25,HexColor("#d1d5db")),
        ("LEFTPADDING",(0,0),(-1,-1),6),
        ("RIGHTPADDING",(0,0),(-1,-1),6),
        ("TOPPADDING",(0,0),(-1,-1),5),
        ("BOTTOMPADDING",(0,0),(-1,-1),5),
    ]))
    return t

def code_section(title, file_path, blocks, header_style=h1):
    elems = [P(title, header_style), P(f"<i>File: {file_path}</i>", note),
             Spacer(1, 0.2*cm)]
    for snippet, expl in blocks:
        elems.append(code(snippet))
        elems.append(P(expl, body))
        elems.append(Spacer(1, 0.15*cm))
    return elems

# ---------- header / footer ----------
def on_page(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8.5)
    canvas.setFillColor(GREY)
    canvas.drawString(2*cm, PAGE_H - 1.2*cm, "BIT235 Assessment 2 | WikiApp Code Walkthrough")
    canvas.drawRightString(PAGE_W - 2*cm, PAGE_H - 1.2*cm, "Movindu Lochana | s1577380")
    canvas.setStrokeColor(BLUE)
    canvas.setLineWidth(0.5)
    canvas.line(2*cm, PAGE_H - 1.35*cm, PAGE_W - 2*cm, PAGE_H - 1.35*cm)
    canvas.setFont("Helvetica", 8.5)
    canvas.drawCentredString(PAGE_W/2, 1.2*cm, f"Page {doc.page}")
    canvas.restoreState()

def on_cover(canvas, doc):
    canvas.saveState()
    canvas.restoreState()

# ---------- content ----------
story = []

# ============================================================ COVER
story.append(Spacer(1, 4*cm))
story.append(P("WikiApp", cover_title))
story.append(P("Code Walkthrough &amp; Viva Preparation Report", cover_sub))
story.append(P("Part A &amp; Part B", cover_sub))
story.append(Spacer(1, 1*cm))
story.append(P("BIT235 - Object Oriented Programming", cover_meta))
story.append(P("Assessment 2", cover_meta))
story.append(P("Semester 1, 2026", cover_meta))
story.append(Spacer(1, 3*cm))
story.append(P("<b>Author:</b> Movindu Lochana", cover_meta))
story.append(P("<b>Student ID:</b> s1577380", cover_meta))
story.append(P("<b>GitHub:</b> https://github.com/DustyxT/WikiApp", cover_meta))
story.append(Spacer(1, 1*cm))
story.append(hr_table())
story.append(Spacer(1, 0.5*cm))
story.append(P("A beginner-friendly explanation of every code block in the project, "
               "designed to help me understand and explain my own work during the viva.",
               ParagraphStyle("CoverNote", parent=body, alignment=TA_CENTER,
                              fontSize=10, textColor=GREY)))
story.append(PageBreak())

# ============================================================ TOC
story.append(P("Contents", h1))
story.append(P("<b>Overview</b>", body))
toc_overview = [
    ("1. Project Overview",        "What the app does (Part A + Part B)"),
    ("2. Architecture &amp; Request Flow", "How the layers talk to each other"),
    ("3. Project Structure",       "Folders and files explained"),
]
story.append(kv_table(toc_overview, col_widths=(7.5*cm, 8.5*cm)))
story.append(Spacer(1, 0.3*cm))

story.append(P("<b>Part A - Login (Files)</b>", body))
toc_a = [
    ("4. pom.xml",                  "Maven build file"),
    ("5. WikiAppApplication.java",  "Application entry point"),
    ("6. LoginForm.java",           "Form-backing data object"),
    ("7. AuthService.java",         "Updated in Part B - now uses the database"),
    ("8. AuthController.java",      "Updated in Part B - uses HttpSession"),
    ("9. application.properties",   "Spring Boot configuration (Part B adds DB)"),
    ("10. login.html",              "Login form template"),
    ("11. welcome.html / error.html / register.html", "Other templates"),
    ("12. style.css",               "Page styling (extended for Part B)"),
]
story.append(kv_table(toc_a, col_widths=(7.5*cm, 8.5*cm)))
story.append(Spacer(1, 0.3*cm))

story.append(P("<b>Part B - Database, Wiki, CRUD (Files)</b>", body))
toc_b = [
    ("13. Article.java",            "JPA entity for Wiki articles"),
    ("14. Admin.java",              "JPA entity for administrators"),
    ("15. ArticleRepository.java",  "Spring Data JPA interface"),
    ("16. AdminRepository.java",    "Spring Data JPA interface"),
    ("17. ArticleService.java",     "Business logic for articles"),
    ("18. WikiController.java",     "Public read-only pages"),
    ("19. AdminController.java",    "Admin-only CRUD pages"),
    ("20. data.sql",                "Seeds the database with sample data"),
    ("21. wiki/list.html",          "Public articles list"),
    ("22. wiki/view.html",          "Single article page"),
    ("23. admin/dashboard.html",    "Admin home with article table"),
    ("24. admin/form.html",         "Create / edit article form"),
    ("25. admin/confirm-delete.html","Delete confirmation page"),
]
story.append(kv_table(toc_b, col_widths=(7.5*cm, 8.5*cm)))
story.append(Spacer(1, 0.3*cm))

story.append(P("<b>Reference &amp; Viva</b>", body))
toc_ref = [
    ("26. Annotation Cheat Sheet",  "Every annotation in plain English"),
    ("27. Thymeleaf Cheat Sheet",   "Template syntax explained"),
    ("28. Likely Viva Questions",   "30+ Q&amp;A covering both parts"),
    ("29. One-Minute Elevator Pitch","Memorise this"),
    ("30. Vocabulary Glossary",     "Key terms defined"),
]
story.append(kv_table(toc_ref, col_widths=(7.5*cm, 8.5*cm)))
story.append(PageBreak())

# ============================================================ 1. OVERVIEW
story.append(P("1. Project Overview", h1))
story.append(P(
    "WikiApp is a Spring Boot web application built in two stages.", body))
story.append(P("<b>Part A</b> implemented the Wiki administrator login screen with hard-coded "
               "credentials. The user submits a form, the controller hands the data to a service, "
               "the service validates it, and the user lands on a welcome or error page.", body))
story.append(P("<b>Part B</b> extended the application with a real H2 database, full CRUD "
               "operations, a public wiki interface, and an admin back-end. The hard-coded "
               "credentials were replaced with a JPA-managed Admin entity, and articles are now "
               "stored in the database. The Controller layer was extended with HttpSession-based "
               "authentication so that admin pages can only be accessed when logged in.", body))

story.append(P("What both parts share", h2))
story.append(P("The MVC pattern (Model - View - Controller) and a three-layer architecture "
               "(Controller -&gt; Service -&gt; Repository). Each class has exactly one job. "
               "When Part B added a database, the Controller and Service did not need to be "
               "rewritten - only the Repository changed (from a hard-coded class to a JPA "
               "interface). That is the reward of a well-layered design.", body))

story.append(P("HD-rubric criteria targeted", h2))
story.append(kv_table([
    ("MVC Structure", "Three packages: controller / service / repository, plus model"),
    ("Controllers / Mappings", "@GetMapping and @PostMapping; full request flow works for both parts"),
    ("Form &amp; Data Flow", "@ModelAttribute on LoginForm and Article; Model carries data to views"),
    ("Service Logic", "Validation, trim, lower-case, time-stamping all in service classes"),
    ("Database integration (Part B)", "JPA entities, Spring Data repositories, H2 file-based DB"),
    ("CRUD (Part B)", "Create / Read / Update / Delete pages for articles"),
    ("Interface", "Polished login card, gradient theme, navigation bar, article cards, data table"),
    ("Code Quality", "Header on every file; inline comments on every annotation"),
    ("Demo Explanation", "Covered by this document"),
]))
story.append(PageBreak())

# ============================================================ 2. ARCHITECTURE
story.append(P("2. Architecture &amp; Request Flow", h1))
story.append(P("Two flows operate side by side once Part B is added.", body))

story.append(P("Flow 1 - Login (Part A, updated for sessions)", h2))
flow_login = """\
   [ Browser ]
       |  POST /login
       v
+--------------------+
|   AuthController   |   - reads username & password from the form
+--------------------+
       |  authService.isAuthenticated(form)
       v
+--------------------+
|    AuthService     |   - trims/lower-cases the username
+--------------------+
       |  adminRepository.findByUsername(...)
       v
+--------------------+
|  AdminRepository   |   - JPA interface; Spring writes the SQL
+--------------------+
       |  Optional<Admin>
       v
+--------------------+
|   AuthController   |   - sets session attribute "loggedInAdmin"
+--------------------+   - redirect:/admin
       v
   [ Browser ]   <- admin dashboard rendered by Thymeleaf
"""
story.append(code(flow_login))

story.append(P("Flow 2 - Public wiki (Part B)", h2))
flow_wiki = """\
   [ Browser ]
       |  GET /wiki  (or /wiki/{id})
       v
+--------------------+
|   WikiController   |   - public; no login required
+--------------------+
       |
       v
+--------------------+
|   ArticleService   |   - findAll / findById / search / findByCategory
+--------------------+
       |
       v
+--------------------+
| ArticleRepository  |   - JPA interface
+--------------------+
       |  List<Article>  or  Optional<Article>
       v
   [ Browser ]   <- list page or single-article page
"""
story.append(code(flow_wiki))

story.append(P("Flow 3 - Admin CRUD (Part B)", h2))
flow_crud = """\
   [ Browser ]
       |  GET /admin/new                 GET /admin/edit/{id}
       v                                  v
+--------------------+                  +--------------------+
|  AdminController   |  -- session?  -> |  AdminController   |
+--------------------+   yes/no         +--------------------+
       |                                       |
       v                                       v
+--------------------+                  +--------------------+
|   ArticleService   |                  |   ArticleService   |
+--------------------+                  +--------------------+
       |  save()                               |  save() (UPDATE because id is set)
       v                                       v
   redirect:/admin                         redirect:/admin

For DELETE: GET /admin/delete/{id} -> confirmation page
            POST /admin/delete/{id} -> articleService.deleteById(id) -> redirect:/admin
"""
story.append(code(flow_crud))
story.append(PageBreak())

# ============================================================ 3. STRUCTURE
story.append(P("3. Project Structure", h1))
tree = """\
WikiApp/
+-- pom.xml                                  (Maven build)
+-- README.md
+-- .gitignore
+-- data/wikidb.mv.db                        (Part B - H2 file-based DB)
+-- src/main/
    +-- java/com/wikiapp/
    |   +-- WikiAppApplication.java          (entry point)
    |   +-- controller/
    |   |   +-- AuthController.java          (login / logout)
    |   |   +-- WikiController.java          (Part B - public)
    |   |   +-- AdminController.java         (Part B - protected CRUD)
    |   +-- service/
    |   |   +-- AuthService.java             (validates login against DB)
    |   |   +-- ArticleService.java          (Part B - article logic)
    |   +-- repository/
    |   |   +-- AdminRepository.java         (Part B - JPA)
    |   |   +-- ArticleRepository.java       (Part B - JPA)
    |   +-- model/
    |       +-- LoginForm.java               (form-backing POJO)
    |       +-- Admin.java                   (Part B - @Entity)
    |       +-- Article.java                 (Part B - @Entity)
    +-- resources/
        +-- application.properties           (port + DB config)
        +-- data.sql                         (Part B - seed admin + articles)
        +-- templates/
        |   +-- login.html
        |   +-- welcome.html / error.html / register.html
        |   +-- wiki/list.html               (Part B)
        |   +-- wiki/view.html               (Part B)
        |   +-- admin/dashboard.html         (Part B)
        |   +-- admin/form.html              (Part B - shared create/edit)
        |   +-- admin/confirm-delete.html    (Part B)
        +-- static/css/
            +-- style.css                    (login + Part B styles)
"""
story.append(code(tree))
story.append(P("Each Java package matches one layer in the architecture. Templates are split "
               "into <b>wiki/</b> (public) and <b>admin/</b> (protected) subfolders to make "
               "the access pattern obvious at a glance.", body))
story.append(PageBreak())

# =================================================================
#                            PART A SECTIONS
# =================================================================
story.append(P("PART A", part_h))
story.append(P("Login screen with hard-coded credentials.", note))
story.append(P("Note: AuthService and AuthController were upgraded in Part B to use the "
               "database and HttpSession. The walkthrough below describes the CURRENT, "
               "Part-B-aware versions of those files, so what you read matches the code "
               "that is actually running.", note))
story.append(Spacer(1, 1*cm))
story.append(hr_table())

# ---------- 4. pom.xml ----------
story.append(PageBreak())
story += code_section("4. pom.xml - Maven Build File",
    "WikiApp/pom.xml",
    [
        ("""<parent>
    <groupId>org.springframework.boot</groupId>
    <artifactId>spring-boot-starter-parent</artifactId>
    <version>3.3.4</version>
</parent>""",
         "<b>What it does:</b> Inherits Spring Boot's standard configuration so we do not "
         "have to pick versions for every dependency individually."),
        ("""<dependencies>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-web</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-thymeleaf</artifactId>
    </dependency>
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-validation</artifactId>
    </dependency>

    <!-- PART B additions -->
    <dependency>
        <groupId>org.springframework.boot</groupId>
        <artifactId>spring-boot-starter-data-jpa</artifactId>
    </dependency>
    <dependency>
        <groupId>com.h2database</groupId>
        <artifactId>h2</artifactId>
        <scope>runtime</scope>
    </dependency>
</dependencies>""",
         "<b>What it does:</b> <b>spring-boot-starter-web</b> gives us @Controller, "
         "@GetMapping, @PostMapping and the embedded Tomcat server. <b>thymeleaf</b> turns "
         "HTML into dynamic pages. <b>validation</b> enables @NotBlank. "
         "<b>data-jpa (Part B)</b> gives us JpaRepository so we can talk to the database "
         "with simple interfaces. <b>h2 (Part B)</b> is a small SQL database that runs "
         "inside our app - no separate install needed."),
    ])

# ---------- 5. WikiAppApplication ----------
story.append(PageBreak())
story += code_section("5. WikiAppApplication.java - Entry Point",
    "src/main/java/com/wikiapp/WikiAppApplication.java",
    [
        ("""@SpringBootApplication
public class WikiAppApplication {
    public static void main(String[] args) {
        SpringApplication.run(WikiAppApplication.class, args);
    }
}""",
         "<b>What it does:</b> @SpringBootApplication is a shortcut for three annotations: "
         "@Configuration (this class can define beans), @EnableAutoConfiguration (Spring sets "
         "up sensible defaults like the Tomcat server and now also the H2 database connection), "
         "and @ComponentScan (Spring searches this package and below for @Controller, @Service, "
         "@Repository and @Entity classes). The main method hands control to Spring Boot."),
    ])

# ---------- 6. LoginForm ----------
story.append(PageBreak())
story += code_section("6. LoginForm.java - The Login Model",
    "src/main/java/com/wikiapp/model/LoginForm.java",
    [
        ("""public class LoginForm {

    @NotBlank(message = "Username is required")
    private String username;

    @NotBlank(message = "Password is required")
    private String password;

    public LoginForm() { }

    public String getUsername() { return username; }
    public void setUsername(String username) { this.username = username; }

    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}""",
         "<b>What it does:</b> A POJO (Plain Old Java Object) - private fields, a no-args "
         "constructor, getters and setters. Spring uses this class to receive the data the "
         "user typed into the login form. <b>@NotBlank</b> says the field must not be null "
         "and must not be empty/whitespace. The <b>private</b> fields plus get/set is "
         "<b>encapsulation</b>, a fundamental OOP principle."),
    ])

# ---------- 7. AuthService (Part B version) ----------
story.append(PageBreak())
story += code_section("7. AuthService.java - The Auth Service (Part B updated)",
    "src/main/java/com/wikiapp/service/AuthService.java",
    [
        ("""@Service
public class AuthService {

    private final AdminRepository adminRepository;

    @Autowired
    public AuthService(AdminRepository adminRepository) {
        this.adminRepository = adminRepository;
    }""",
         "<b>What it does:</b> @Service marks this as a business-logic bean. "
         "<b>Constructor injection</b>: the Service declares it needs an AdminRepository, "
         "and Spring passes the bean it created earlier into the constructor. "
         "<b>final</b> means we never reassign this reference - safer code."),
        ("""public boolean isAuthenticated(LoginForm form) {
    if (form == null) return false;

    String username = form.getUsername();
    String password = form.getPassword();

    if (username == null || username.trim().isEmpty()) return false;
    if (password == null || password.trim().isEmpty()) return false;

    String cleanedUsername = username.trim().toLowerCase();""",
         "<b>What it does:</b> Validation rules that belong in the Service layer. We reject "
         "null forms and empty/whitespace fields. Then we trim and lower-case the username "
         "so 'Movindu' or ' movindu ' still works. Note we do NOT lower-case the password - "
         "passwords are case-sensitive."),
        ("""    Optional<Admin> maybeAdmin = adminRepository.findByUsername(cleanedUsername);
    if (maybeAdmin.isEmpty()) return false;

    Admin admin = maybeAdmin.get();
    return admin.getPassword().equals(password);
}""",
         "<b>What it does:</b> Looks up the admin by username. <b>Optional&lt;Admin&gt;</b> "
         "means 'either an Admin or nothing' - safer than returning null because the caller "
         "is forced to handle the missing case. If no admin exists, fail. Otherwise compare "
         "the stored password to the supplied one with .equals()."),
    ])

# ---------- 8. AuthController (Part B version) ----------
story.append(PageBreak())
story += code_section("8. AuthController.java - The Auth Controller (Part B updated)",
    "src/main/java/com/wikiapp/controller/AuthController.java",
    [
        ("""@Controller
@RequestMapping("/")
public class AuthController {

    public static final String SESSION_ADMIN_KEY = "loggedInAdmin";

    private final AuthService authService;

    @Autowired
    public AuthController(AuthService authService) {
        this.authService = authService;
    }""",
         "<b>What it does:</b> @Controller marks this as a web controller; methods return "
         "view names (HTML files). The <b>SESSION_ADMIN_KEY</b> constant is the key under "
         "which we store the logged-in username in the HttpSession. Using a constant prevents typos."),
        ("""@GetMapping({"/", "/login"})
public String showLoginPage(Model model) {
    model.addAttribute("loginForm", new LoginForm());
    return "login";
}""",
         "<b>What it does:</b> Handles GET requests to / or /login. We put an empty LoginForm "
         "into the Model so the form has something to bind to. Returning \"login\" tells Spring "
         "to render <b>templates/login.html</b>."),
        ("""@PostMapping("/login")
public String processLogin(@ModelAttribute("loginForm") LoginForm loginForm,
                           HttpSession session,
                           Model model) {
    boolean ok = authService.isAuthenticated(loginForm);
    if (ok) {
        String cleaned = loginForm.getUsername().trim().toLowerCase();
        session.setAttribute(SESSION_ADMIN_KEY, cleaned);
        return "redirect:/admin";
    }
    model.addAttribute("errorMessage",
            "Invalid username or password. Please try again.");
    return "error";
}""",
         "<b>What it does:</b> Handles the login form submission. <b>@ModelAttribute</b> "
         "tells Spring to build a LoginForm from the form fields. We ask the Service if the "
         "credentials are valid; if yes, we store the username in the <b>HttpSession</b> "
         "and <b>redirect</b> the browser to the admin dashboard. The 'redirect:' prefix "
         "tells Spring to send a 302 response instead of rendering a template - this avoids "
         "the browser's 'resubmit form?' warning if the user refreshes."),
        ("""@GetMapping("/logout")
public String logout(HttpSession session) {
    session.invalidate();
    return "redirect:/login";
}""",
         "<b>What it does:</b> Handles logout. <b>session.invalidate()</b> throws away every "
         "value stored in this user's session, so the next request looks unauthenticated. "
         "Then we redirect back to the login page."),
    ])

# ---------- 9. application.properties ----------
story.append(PageBreak())
story += code_section("9. application.properties - Spring Boot Configuration",
    "src/main/resources/application.properties",
    [
        ("""server.port=8080
spring.thymeleaf.cache=false
spring.application.name=WikiApp""",
         "<b>What it does:</b> Tomcat runs on port 8080. Thymeleaf caching is off so HTML "
         "edits show up without restarting. The application has a friendly log name."),
        ("""# Part B - H2 file-based database
spring.datasource.url=jdbc:h2:file:./data/wikidb;AUTO_SERVER=TRUE
spring.datasource.driver-class-name=org.h2.Driver
spring.datasource.username=sa
spring.datasource.password=
spring.h2.console.enabled=true
spring.h2.console.path=/h2-console""",
         "<b>What it does:</b> Configures the H2 database. The data is stored in files inside "
         "<b>./data/</b> so it survives restarts. The H2 console is enabled at "
         "<b>/h2-console</b> - useful for showing the actual database tables during the demo."),
        ("""spring.jpa.hibernate.ddl-auto=update
spring.jpa.defer-datasource-initialization=true
spring.sql.init.mode=always""",
         "<b>What it does:</b> <b>ddl-auto=update</b> tells Hibernate to create missing tables "
         "and add new columns automatically based on our @Entity classes. "
         "<b>defer-datasource-initialization</b> ensures Hibernate creates the tables BEFORE "
         "data.sql runs, so the seed inserts succeed."),
    ])

# ---------- 10. login.html ----------
story.append(PageBreak())
story += code_section("10. login.html - The Login Form",
    "src/main/resources/templates/login.html",
    [
        ("""<html lang="en" xmlns:th="http://www.thymeleaf.org">""",
         "<b>What it does:</b> The xmlns:th namespace unlocks the th:* attributes."),
        ("""<form th:action="@{/login}" th:object="${loginForm}" method="post">
    <label for="username">Username</label>
    <input type="text" id="username" th:field="*{username}" autofocus/>

    <label for="password">Password</label>
    <input type="password" id="password" th:field="*{password}"/>

    <a class="btn secondary" th:href="@{/register}">Register</a>
    <button class="btn primary" type="submit">Log in</button>
</form>""",
         "<b>What it does:</b> The form posts to /login. <b>th:object</b> binds the whole form "
         "to the LoginForm object the controller put in the model. <b>th:field=\"*{username}\"</b> "
         "automatically generates name=, id= and value= attributes that map to the LoginForm's "
         "username property. When submitted, Spring calls setUsername() with whatever was typed."),
    ])

# ---------- 11. other Part A templates ----------
story.append(PageBreak())
story += code_section("11. welcome.html / error.html / register.html",
    "src/main/resources/templates/",
    [
        ("""<!-- welcome.html -->
<p>Hello <strong th:text="${username}">user</strong>, you have logged in successfully.</p>
<a class="btn primary" th:href="@{/login}">Log out</a>""",
         "<b>welcome.html:</b> Originally shown after a successful Part A login. With Part B "
         "added, the controller redirects straight to /admin instead, but this template stays "
         "as a backup view. <b>th:text</b> replaces the tag's body with the model attribute."),
        ("""<!-- error.html -->
<p th:text="${errorMessage}">Something went wrong.</p>
<a class="btn primary" th:href="@{/login}">Try again</a>""",
         "<b>error.html:</b> Shown for failed logins and 'article not found' errors. The same "
         "template handles both cases - the controller decides what message to put in the model."),
        ("""<!-- register.html -->
<p th:text="${message}">Coming soon.</p>
<a class="btn primary" th:href="@{/login}">Back to Login</a>""",
         "<b>register.html:</b> Placeholder. The brief did not require self-registration; "
         "admin accounts are seeded into the database at startup instead."),
    ])

# ---------- 12. style.css ----------
story.append(PageBreak())
story += code_section("12. style.css - Page Styling",
    "src/main/resources/static/css/style.css",
    [
        ("""body {
    background: linear-gradient(135deg, #1e3a8a 0%, #2563eb 50%, #38bdf8 100%);
    min-height: 100vh;
    display: flex;
    justify-content: center;
    align-items: center;
}""",
         "<b>Login page:</b> Centred white card on a gradient background using flexbox. "
         "<b>100vh</b> means 100% of the viewport height."),
        ("""/* Part B - top navigation bar */
.topbar {
    background: #1e3a8a;
    color: #ffffff;
    padding: 14px 28px;
    display: flex;
    justify-content: space-between;
    align-items: center;
}
.topbar.admin { background: #111827; }""",
         "<b>Part B nav bar:</b> Used on every wiki and admin page. The <b>.admin</b> class "
         "switches to a darker colour so it is visually obvious which area you are in."),
        ("""/* Part B - article cards */
.article-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
    gap: 18px;
}""",
         "<b>Article grid:</b> CSS Grid creates a responsive layout - cards are at least 280px "
         "wide and the browser fits as many per row as possible. Resize the window to see it adapt."),
        ("""/* Part B - admin data table */
.data-table { width: 100%; border-collapse: collapse; }
.data-table th { background: #f9fafb; }
.data-table tbody tr:hover { background: #f9fafb; }""",
         "<b>Admin table:</b> Standard table styling with a hover effect on each row to "
         "indicate it is interactive."),
    ])

# =================================================================
#                            PART B SECTIONS
# =================================================================
story.append(PageBreak())
story.append(P("PART B", part_h))
story.append(P("Database, public wiki, and admin CRUD.", note))
story.append(Spacer(1, 1*cm))
story.append(hr_table(GREEN))

# ---------- 13. Article entity ----------
story.append(PageBreak())
story += code_section("13. Article.java - JPA Entity",
    "src/main/java/com/wikiapp/model/Article.java", [
        ("""@Entity
public class Article {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;""",
         "<b>What it does:</b> <b>@Entity</b> tells JPA to create a database table for this "
         "class. <b>@Id</b> marks the primary key (the unique row identifier). "
         "<b>@GeneratedValue(IDENTITY)</b> tells the database to auto-generate the id when "
         "we save a new article."),
        ("""    @NotBlank(message = "Title is required")
    @Column(nullable = false)
    private String title;

    @NotBlank(message = "Category is required")
    @Column(nullable = false)
    private String category;

    @NotBlank(message = "Content is required")
    @Column(nullable = false, length = 5000)
    private String content;

    private LocalDateTime lastUpdated;""",
         "<b>What it does:</b> Three text fields plus a timestamp. <b>@NotBlank</b> validates "
         "the form input. <b>@Column(nullable = false)</b> makes the database column NOT NULL "
         "too. <b>length = 5000</b> overrides the default 255-char limit so we can store long "
         "article content. <b>LocalDateTime</b> is the modern Java date/time type."),
        ("""    public Article() { }

    public Article(String title, String category, String content) {
        this.title = title;
        this.category = category;
        this.content = content;
        this.lastUpdated = LocalDateTime.now();
    }

    // ... getters and setters for all fields ...""",
         "<b>What it does:</b> A no-args constructor (required by JPA so it can build a blank "
         "object and fill it in from the database row), and a convenience constructor for "
         "creating articles in code. Standard getters and setters follow."),
    ], header_style=h1b)

# ---------- 14. Admin entity ----------
story.append(PageBreak())
story += code_section("14. Admin.java - JPA Entity",
    "src/main/java/com/wikiapp/model/Admin.java", [
        ("""@Entity
public class Admin {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String username;

    @Column(nullable = false)
    private String password;

    public Admin() { }
    public Admin(String username, String password) {
        this.username = username;
        this.password = password;
    }
    // ... getters and setters ...
}""",
         "<b>What it does:</b> Replaces the hard-coded credentials we used in Part A. Each row "
         "in the ADMIN table is one administrator. <b>unique = true</b> on username means the "
         "database itself rejects duplicate usernames. The password is stored in plain text for "
         "simplicity (the brief does not require hashing). In a real system we would always "
         "hash passwords with BCrypt or Argon2."),
    ], header_style=h1b)

# ---------- 15. ArticleRepository ----------
story.append(PageBreak())
story += code_section("15. ArticleRepository.java - JPA Interface",
    "src/main/java/com/wikiapp/repository/ArticleRepository.java", [
        ("""public interface ArticleRepository extends JpaRepository<Article, Long> {

    List<Article> findByCategoryIgnoreCase(String category);

    List<Article> findByTitleContainingIgnoreCase(String text);
}""",
         "<b>What it does:</b> The most powerful single line in the project. By extending "
         "<b>JpaRepository&lt;Article, Long&gt;</b>, we get a fully working repository with "
         "no code: findAll(), findById(id), save(article), deleteById(id), count(), and many "
         "more. Spring writes all the SQL for us. The two custom methods follow Spring Data's "
         "<b>naming convention</b>: Spring reads the method name and writes a query for it. "
         "<b>findByCategoryIgnoreCase</b> becomes 'SELECT * FROM article WHERE LOWER(category) "
         "= LOWER(?)'. We never write SQL ourselves."),
    ], header_style=h1b)

# ---------- 16. AdminRepository ----------
story.append(PageBreak())
story += code_section("16. AdminRepository.java - JPA Interface",
    "src/main/java/com/wikiapp/repository/AdminRepository.java", [
        ("""public interface AdminRepository extends JpaRepository<Admin, Long> {

    Optional<Admin> findByUsername(String username);
}""",
         "<b>What it does:</b> Same idea as ArticleRepository but for Admin. "
         "<b>findByUsername</b> is converted by Spring into the SQL "
         "'SELECT * FROM admin WHERE username = ?'. Returning <b>Optional&lt;Admin&gt;</b> "
         "instead of Admin forces the caller to handle the case where no admin with that "
         "username exists - this prevents accidental NullPointerExceptions."),
    ], header_style=h1b)

# ---------- 17. ArticleService ----------
story.append(PageBreak())
story += code_section("17. ArticleService.java - Business Logic",
    "src/main/java/com/wikiapp/service/ArticleService.java", [
        ("""@Service
public class ArticleService {

    private final ArticleRepository articleRepository;

    @Autowired
    public ArticleService(ArticleRepository articleRepository) {
        this.articleRepository = articleRepository;
    }""",
         "<b>What it does:</b> Same Service-layer pattern we used in Part A. Constructor "
         "injection wires in the repository."),
        ("""public List<Article> findAll() {
    return articleRepository.findAll();
}

public Optional<Article> findById(Long id) {
    return articleRepository.findById(id);
}

public List<Article> findByCategory(String category) {
    if (category == null || category.trim().isEmpty()) return findAll();
    return articleRepository.findByCategoryIgnoreCase(category.trim());
}

public List<Article> search(String text) {
    if (text == null || text.trim().isEmpty()) return findAll();
    return articleRepository.findByTitleContainingIgnoreCase(text.trim());
}""",
         "<b>What it does:</b> The READ side of CRUD. Each method is a thin wrapper around "
         "the repository, but with one small business rule: empty filter inputs fall back "
         "to listing all articles."),
        ("""public Article save(Article article) {
    article.setLastUpdated(LocalDateTime.now());
    return articleRepository.save(article);
}

public void deleteById(Long id) {
    articleRepository.deleteById(id);
}

public boolean existsById(Long id) {
    return articleRepository.existsById(id);
}""",
         "<b>What it does:</b> CREATE/UPDATE/DELETE side. <b>save()</b> handles BOTH inserts "
         "(when article.id is null) and updates (when it has an id) - JPA decides automatically. "
         "We always stamp the lastUpdated field, which is a nice business rule that lives in "
         "the Service exactly where it should."),
    ], header_style=h1b)

# ---------- 18. WikiController ----------
story.append(PageBreak())
story += code_section("18. WikiController.java - Public Read Pages",
    "src/main/java/com/wikiapp/controller/WikiController.java", [
        ("""@Controller
@RequestMapping("/wiki")
public class WikiController {

    private final ArticleService articleService;

    @Autowired
    public WikiController(ArticleService articleService) {
        this.articleService = articleService;
    }""",
         "<b>What it does:</b> @RequestMapping(\"/wiki\") prefixes every method's URL with "
         "/wiki, so the listing is at /wiki and individual articles are at /wiki/{id}. "
         "These are the PUBLIC pages - no login is required."),
        ("""@GetMapping
public String listArticles(
        @RequestParam(value = "category", required = false) String category,
        @RequestParam(value = "search",   required = false) String search,
        Model model) {

    List<Article> articles;
    if (search != null && !search.trim().isEmpty()) {
        articles = articleService.search(search);
    } else if (category != null && !category.trim().isEmpty()) {
        articles = articleService.findByCategory(category);
    } else {
        articles = articleService.findAll();
    }

    model.addAttribute("articles", articles);
    model.addAttribute("category", category);
    model.addAttribute("search", search);
    return "wiki/list";
}""",
         "<b>What it does:</b> Handles GET /wiki. <b>@RequestParam(required=false)</b> "
         "captures optional URL parameters - so /wiki?search=spring sets search='spring', "
         "and /wiki on its own makes both null. We pick the right Service method based on "
         "which (if any) parameter is present, then put the list and the current filter "
         "values into the Model so the template can show them."),
        ("""@GetMapping("/{id}")
public String viewArticle(@PathVariable("id") Long id, Model model) {
    Optional<Article> maybeArticle = articleService.findById(id);
    if (maybeArticle.isEmpty()) {
        model.addAttribute("errorMessage", "The article you requested does not exist.");
        return "error";
    }
    model.addAttribute("article", maybeArticle.get());
    return "wiki/view";
}""",
         "<b>What it does:</b> Handles GET /wiki/{id} where {id} is a number. "
         "<b>@PathVariable</b> captures that value from the URL. If no article with that id "
         "exists, we send the user to a friendly error page instead of crashing."),
    ], header_style=h1b)

# ---------- 19. AdminController ----------
story.append(PageBreak())
story += code_section("19. AdminController.java - Protected CRUD",
    "src/main/java/com/wikiapp/controller/AdminController.java", [
        ("""@Controller
@RequestMapping("/admin")
public class AdminController {

    private final ArticleService articleService;

    @Autowired
    public AdminController(ArticleService articleService) {
        this.articleService = articleService;
    }

    private boolean isLoggedIn(HttpSession session) {
        return session.getAttribute(AuthController.SESSION_ADMIN_KEY) != null;
    }""",
         "<b>What it does:</b> All admin URLs start with /admin. The <b>isLoggedIn</b> helper "
         "checks the session for the username we stored during login. Every admin endpoint "
         "calls this first - if it returns false, we redirect to /login. This is a very "
         "simple, viva-friendly authorisation check (no Spring Security needed)."),
        ("""@GetMapping
public String dashboard(HttpSession session, Model model) {
    if (!isLoggedIn(session)) return "redirect:/login";

    model.addAttribute("articles", articleService.findAll());
    model.addAttribute("adminUser",
            session.getAttribute(AuthController.SESSION_ADMIN_KEY));
    return "admin/dashboard";
}""",
         "<b>READ:</b> Lists every article in a table for the admin to manage. We also pass "
         "the logged-in username so the navigation bar can greet them by name."),
        ("""@GetMapping("/new")
public String showCreateForm(HttpSession session, Model model) {
    if (!isLoggedIn(session)) return "redirect:/login";
    model.addAttribute("article", new Article());
    model.addAttribute("mode", "create");
    return "admin/form";
}

@PostMapping
public String createArticle(@Valid @ModelAttribute("article") Article article,
                            BindingResult bindingResult,
                            HttpSession session,
                            Model model) {
    if (!isLoggedIn(session)) return "redirect:/login";
    if (bindingResult.hasErrors()) {
        model.addAttribute("mode", "create");
        return "admin/form";
    }
    articleService.save(article);
    return "redirect:/admin";
}""",
         "<b>CREATE:</b> Two methods - one shows the empty form (GET /admin/new), the other "
         "handles the submission (POST /admin). <b>@Valid</b> activates the @NotBlank checks "
         "on the Article. <b>BindingResult</b> collects any errors. If the input is invalid "
         "we redisplay the form with the error messages; otherwise we save and redirect."),
        ("""@GetMapping("/edit/{id}")
public String showEditForm(@PathVariable("id") Long id,
                           HttpSession session, Model model) {
    if (!isLoggedIn(session)) return "redirect:/login";
    Optional<Article> maybeArticle = articleService.findById(id);
    if (maybeArticle.isEmpty()) {
        model.addAttribute("errorMessage", "The article you tried to edit does not exist.");
        return "error";
    }
    model.addAttribute("article", maybeArticle.get());
    model.addAttribute("mode", "edit");
    return "admin/form";
}

@PostMapping("/edit/{id}")
public String updateArticle(@PathVariable("id") Long id,
                            @Valid @ModelAttribute("article") Article article,
                            BindingResult bindingResult,
                            HttpSession session, Model model) {
    if (!isLoggedIn(session)) return "redirect:/login";
    if (bindingResult.hasErrors()) {
        model.addAttribute("mode", "edit");
        return "admin/form";
    }
    article.setId(id);
    articleService.save(article);
    return "redirect:/admin";
}""",
         "<b>UPDATE:</b> Same two-step pattern. The GET pre-fills the form with the existing "
         "article; the POST saves changes. Setting <b>article.setId(id)</b> before save() is "
         "what makes JPA do an UPDATE rather than an INSERT - articles with an id get updated, "
         "articles without get inserted."),
        ("""@GetMapping("/delete/{id}")
public String confirmDelete(@PathVariable("id") Long id,
                            HttpSession session, Model model) {
    if (!isLoggedIn(session)) return "redirect:/login";
    // ... show "are you sure?" page ...
    return "admin/confirm-delete";
}

@PostMapping("/delete/{id}")
public String deleteArticle(@PathVariable("id") Long id, HttpSession session) {
    if (!isLoggedIn(session)) return "redirect:/login";
    if (articleService.existsById(id)) articleService.deleteById(id);
    return "redirect:/admin";
}""",
         "<b>DELETE:</b> Two steps for safety. The GET shows a confirmation page; only the "
         "POST actually deletes. We use POST (not GET) for the delete because GET requests "
         "should never change data - this stops accidental deletions from URL prefetching, "
         "browser caching, or web crawlers."),
    ], header_style=h1b)

# ---------- 20. data.sql ----------
story.append(PageBreak())
story += code_section("20. data.sql - Database Seeding",
    "src/main/resources/data.sql", [
        ("""MERGE INTO ADMIN (id, username, password) KEY(id)
    VALUES (1, 'movindu', '123');""",
         "<b>What it does:</b> Seeds the single admin account. <b>MERGE ... KEY(id)</b> means "
         "'insert if a row with this id does not exist; otherwise update it' - so the script "
         "is safe to run repeatedly without crashing on duplicates."),
        ("""MERGE INTO ARTICLE (id, title, category, content, last_updated) KEY(id) VALUES
    (1, 'Welcome to WikiApp', 'General', '...', CURRENT_TIMESTAMP);
-- ... and four more sample articles ...

ALTER TABLE ARTICLE ALTER COLUMN ID RESTART WITH 100;
ALTER TABLE ADMIN   ALTER COLUMN ID RESTART WITH 100;""",
         "<b>What it does:</b> Inserts five sample articles so the wiki has something to "
         "show on first run. <b>ALTER TABLE ... RESTART WITH 100</b> bumps the auto-increment "
         "counter past the seeded ids, so when the admin creates a new article it gets id 100, "
         "101, 102 ... rather than colliding with the seeded ones."),
    ], header_style=h1b)

# ---------- 21. wiki/list.html ----------
story.append(PageBreak())
story += code_section("21. wiki/list.html - Public Articles List",
    "src/main/resources/templates/wiki/list.html", [
        ("""<form class="search" th:action="@{/wiki}" method="get">
    <input type="text" name="search" th:value="${search}"
           placeholder="Search articles by title..."/>
    <button class="btn primary" type="submit">Search</button>
    <a class="btn secondary" th:href="@{/wiki}">Clear</a>
</form>""",
         "<b>Search bar:</b> method=\"get\" puts the search text into the URL "
         "(/wiki?search=spring) - this means the user can bookmark or share search results. "
         "<b>th:value</b> repopulates the box with the previous search so the user can see what "
         "they searched for."),
        ("""<div class="article-grid" th:unless="${#lists.isEmpty(articles)}">
    <article class="article-card" th:each="a : ${articles}">
        <span class="badge" th:text="${a.category}">Category</span>
        <h2><a th:href="@{'/wiki/' + ${a.id}}" th:text="${a.title}">Title</a></h2>
        <p class="preview" th:text="${#strings.abbreviate(a.content, 140)}">Preview</p>
        <p class="meta">Last updated:
            <span th:text="${#temporals.format(a.lastUpdated, 'dd MMM yyyy HH:mm')}">date</span>
        </p>
    </article>
</div>""",
         "<b>Article grid:</b> <b>th:each=\"a : ${articles}\"</b> is Thymeleaf's for-each "
         "loop - exactly like a Java for loop over a list. We render one card per article. "
         "<b>#strings.abbreviate(text, 140)</b> truncates the content to a 140-char preview. "
         "<b>#temporals.format(...)</b> formats the LocalDateTime into a friendly date string."),
    ], header_style=h1b)

# ---------- 22. wiki/view.html ----------
story.append(PageBreak())
story += code_section("22. wiki/view.html - Single Article",
    "src/main/resources/templates/wiki/view.html", [
        ("""<article class="article-full">
    <span class="badge" th:text="${article.category}">Category</span>
    <h1 th:text="${article.title}">Title</h1>
    <p class="meta">Last updated:
        <span th:text="${#temporals.format(article.lastUpdated, 'dd MMM yyyy HH:mm')}">date</span>
    </p>
    <div class="content" th:text="${article.content}">Content</div>
</article>""",
         "<b>What it does:</b> Renders one full article. <b>th:text</b> automatically "
         "HTML-escapes the content, so even if someone tries to put &lt;script&gt; tags into "
         "an article, they will appear as plain text - never executed. This is built-in XSS "
         "protection."),
    ], header_style=h1b)

# ---------- 23. admin/dashboard.html ----------
story.append(PageBreak())
story += code_section("23. admin/dashboard.html - Admin Home",
    "src/main/resources/templates/admin/dashboard.html", [
        ("""<nav class="topbar admin">
    <a class="brand" th:href="@{/admin}">WikiApp Admin</a>
    <div class="links">
        <span>Logged in as <strong th:text="${adminUser}">admin</strong></span>
        <a th:href="@{/wiki}">View public wiki</a>
        <a th:href="@{/logout}">Log out</a>
    </div>
</nav>""",
         "<b>Top bar:</b> Greets the logged-in admin by name (read from the session attribute) "
         "and provides links to the public wiki and the logout endpoint."),
        ("""<table class="data-table" th:unless="${#lists.isEmpty(articles)}">
    <thead><tr>
        <th>ID</th><th>Title</th><th>Category</th>
        <th>Last updated</th><th>Actions</th>
    </tr></thead>
    <tbody>
        <tr th:each="a : ${articles}">
            <td th:text="${a.id}">1</td>
            <td><a th:href="@{'/wiki/' + ${a.id}}" th:text="${a.title}">Title</a></td>
            <td><span class="badge" th:text="${a.category}">cat</span></td>
            <td th:text="${#temporals.format(a.lastUpdated, 'dd MMM yyyy HH:mm')}">date</td>
            <td class="actions">
                <a class="btn small"        th:href="@{'/admin/edit/'   + ${a.id}}">Edit</a>
                <a class="btn small danger" th:href="@{'/admin/delete/' + ${a.id}}">Delete</a>
            </td>
        </tr>
    </tbody>
</table>""",
         "<b>Article table:</b> Loops over every article and renders a row with Edit and "
         "Delete buttons. The URLs use Thymeleaf string concatenation: "
         "<b>@{'/admin/edit/' + ${a.id}}</b> builds /admin/edit/100 for an article with id 100."),
    ], header_style=h1b)

# ---------- 24. admin/form.html ----------
story.append(PageBreak())
story += code_section("24. admin/form.html - Create / Edit Form",
    "src/main/resources/templates/admin/form.html", [
        ("""<h1 th:text="${mode == 'edit'} ? 'Edit article' : 'New article'">Article form</h1>

<form th:action="${mode == 'edit'}
                 ? @{'/admin/edit/' + ${article.id}}
                 : @{/admin}"
      th:object="${article}" method="post" class="article-form">""",
         "<b>What it does:</b> ONE template handles both 'create' and 'edit'. The "
         "<b>mode</b> attribute (set by the controller) decides which heading and which form "
         "URL to use. The Thymeleaf ternary <b>$&#123;cond&#125; ? a : b</b> is the same as "
         "Java's a?b:c."),
        ("""<label for="title">Title</label>
<input type="text" id="title" th:field="*{title}"/>
<p class="error-text" th:if="${#fields.hasErrors('title')}" th:errors="*{title}"></p>

<label for="category">Category</label>
<input type="text" id="category" th:field="*{category}"/>
<p class="error-text" th:if="${#fields.hasErrors('category')}" th:errors="*{category}"></p>

<label for="content">Content</label>
<textarea id="content" th:field="*{content}" rows="10"></textarea>
<p class="error-text" th:if="${#fields.hasErrors('content')}" th:errors="*{content}"></p>""",
         "<b>What it does:</b> Three input fields bound to the Article object via "
         "<b>th:field</b>. <b>#fields.hasErrors('title')</b> checks if validation failed for "
         "this field, and <b>th:errors</b> displays the error message. This is how @NotBlank "
         "messages appear under the field that caused the error."),
    ], header_style=h1b)

# ---------- 25. admin/confirm-delete.html ----------
story.append(PageBreak())
story += code_section("25. admin/confirm-delete.html - Delete Confirmation",
    "src/main/resources/templates/admin/confirm-delete.html", [
        ("""<div class="card error">
    <h1>Delete article?</h1>
    <p>You are about to permanently delete this article:</p>
    <blockquote>
        <strong th:text="${article.title}">Title</strong><br/>
        <span class="badge" th:text="${article.category}">Category</span>
    </blockquote>

    <form th:action="@{'/admin/delete/' + ${article.id}}" method="post" class="buttons">
        <a class="btn secondary" th:href="@{/admin}">Cancel</a>
        <button class="btn danger" type="submit">Yes, delete</button>
    </form>
</div>""",
         "<b>What it does:</b> 'Are you sure?' page. The actual delete is a POST form (not "
         "just a link) so deleting requires an explicit click and cannot be triggered by URL "
         "prefetching, browser caching or accidental clicks. The Cancel button is a normal "
         "link back to the dashboard."),
    ], header_style=h1b)

# =================================================================
#                          REFERENCE SECTIONS
# =================================================================
story.append(PageBreak())
story.append(P("REFERENCE", part_h))

# ---------- 26. Annotation cheat sheet ----------
story.append(PageBreak())
story.append(P("26. Annotation Cheat Sheet", h1))
story.append(P("Every annotation used in the project, in plain English.", body))
story.append(Spacer(1, 0.2*cm))

story.append(P("Spring core (Part A + B)", h2))
story.append(kv_table([
    ("@SpringBootApplication", "@Configuration + @EnableAutoConfiguration + @ComponentScan."),
    ("@Controller",            "Web controller; methods return view names (HTML files)."),
    ("@Service",               "Business-logic bean. Spring manages it as a singleton."),
    ("@Repository",            "Data-access bean. Marks a class for data access."),
    ("@RequestMapping(\"/\")",   "URL prefix at class level."),
    ("@GetMapping(\"/x\")",      "Handle HTTP GET at /x. Used for viewing pages."),
    ("@PostMapping(\"/x\")",     "Handle HTTP POST at /x. Used for form submissions."),
    ("@ModelAttribute",        "Build a Java object from form fields."),
    ("@Autowired",             "Inject the dependency. Used on the constructor."),
    ("@PathVariable",          "Capture a value from the URL, e.g. /wiki/{id}."),
    ("@RequestParam",          "Capture a query-string parameter, e.g. ?search=foo."),
    ("@Valid",                 "Run validation rules on the bound object."),
    ("@NotBlank",              "Field must not be null or empty/whitespace."),
]))

story.append(P("JPA (Part B)", h2))
story.append(kv_table([
    ("@Entity",                "This class maps to a database table."),
    ("@Id",                    "This field is the primary key."),
    ("@GeneratedValue(IDENTITY)", "Auto-generated id - the database picks the next number."),
    ("@Column(nullable=false)", "The database column cannot hold NULL."),
    ("@Column(unique=true)",   "The database enforces uniqueness."),
    ("@Column(length=5000)",   "Override the default 255-char limit."),
]))
story.append(PageBreak())

# ---------- 27. Thymeleaf cheat sheet ----------
story.append(P("27. Thymeleaf Cheat Sheet", h1))
story.append(P("Every Thymeleaf attribute used in the templates.", body))
story.append(Spacer(1, 0.2*cm))
story.append(kv_table([
    ("xmlns:th=\"...\"",       "Tells the parser to process th:* attributes."),
    ("@{/login}",              "URL expression - safer than hard-coding paths."),
    ("${variable}",            "Variable expression - reads from the Model."),
    ("*{property}",            "Selection expression - reads from the th:object."),
    ("th:object=\"${form}\"",  "Bind the whole form to this Model object."),
    ("th:field=\"*{name}\"",   "Bind input to a property; sets name, id and value."),
    ("th:text=\"${x}\"",       "Replace the tag's text with x. HTML-escaped automatically."),
    ("th:href=\"@{/x}\"",      "Build a URL for an &lt;a&gt; tag's href."),
    ("th:action=\"@{/x}\"",    "Build a URL for a form's submit target."),
    ("th:value=\"${x}\"",      "Set an input's value attribute."),
    ("th:if=\"${cond}\"",      "Render the element only when cond is true."),
    ("th:unless=\"${cond}\"",  "Render the element only when cond is false."),
    ("th:each=\"a : ${list}\"", "For-each loop - render once per element."),
    ("th:errors=\"*{x}\"",     "Show validation errors for the x property."),
    ("#fields.hasErrors('x')", "True when the x property failed validation."),
    ("#strings.abbreviate(s,n)", "Truncate string s to n characters."),
    ("#temporals.format(d,f)", "Format a LocalDateTime using pattern f."),
    ("#lists.isEmpty(l)",      "True when the list is empty."),
]))
story.append(PageBreak())

# ---------- 28. Viva Q&A ----------
story.append(P("28. Likely Viva Questions &amp; Answers", h1))
story.append(P("Read these out loud until they feel natural. The marker will probably ask "
               "5-8 of them. Part B questions appear at the end.", body))

qa = [
    # ---------- PART A ----------
    ("Walk me through what happens when I click 'Log in'.",
     "The browser sends a POST request to /login with the username and password. Spring "
     "matches it to processLogin() in AuthController. Spring builds a LoginForm using its "
     "setters. The controller calls authService.isAuthenticated(loginForm). The service "
     "trims and lower-cases the username and asks adminRepository.findByUsername(). The "
     "repository returns an Optional<Admin>. If it is empty, fail. Otherwise we compare "
     "the stored password to the supplied one with .equals(). On success the controller "
     "stores the username in the HttpSession and returns 'redirect:/admin'. Spring sends a "
     "302 response and the browser loads the admin dashboard."),
    ("Why did you split your code into three layers?",
     "Separation of concerns. The Controller handles HTTP. The Service holds the business "
     "rules. The Repository owns the data. When I added the database in Part B, only the "
     "Repository changed - the rest of the code stayed exactly the same. That is the reward "
     "of a layered design."),
    ("What is the difference between @GetMapping and @PostMapping?",
     "@GetMapping handles requests where the user just wants to view a page - it should not "
     "change anything. @PostMapping handles form submissions - it is used when the user is "
     "sending data, like a username and password or a new article."),
    ("How does Spring know to inject AuthService into the Controller?",
     "I marked AuthService with @Service so Spring creates one instance at startup. The "
     "Controller's constructor declares it needs an AuthService and I added @Autowired, so "
     "Spring passes the same instance in automatically. That is constructor dependency "
     "injection."),
    ("How does the username typed in the form end up in your Java code?",
     "The HTML input has th:field=\"*{username}\". When the form is submitted, Spring sees "
     "@ModelAttribute LoginForm in the controller, creates a new LoginForm, calls "
     "setUsername() with the typed value, then passes the filled object into my method."),
    ("What does Model do?",
     "Model is a container for data going to the view. I put values in with addAttribute(). "
     "Thymeleaf reads from it when rendering the HTML, so ${username} prints whatever I "
     "stored under the name 'username'."),
    ("What is a POJO?",
     "Plain Old Java Object - a simple class with private fields, a no-args constructor, "
     "and getters and setters. LoginForm is a POJO."),
    ("What does @SpringBootApplication actually do?",
     "It is a shortcut for @Configuration (this class can define beans), "
     "@EnableAutoConfiguration (Spring sets up sensible defaults like the embedded Tomcat "
     "server and now the H2 database connection), and @ComponentScan (Spring finds my "
     "@Controller, @Service, @Repository and @Entity classes)."),
    ("What is the embedded Tomcat?",
     "Tomcat is the web server that listens on port 8080. Spring Boot includes it inside "
     "the application, so I do not need to install or configure a separate server - "
     "running my main method starts the server."),
    ("What is the difference between == and .equals() for strings?",
     "== compares whether two variables point to the same memory location. .equals() "
     "compares the actual character contents. For strings you should always use .equals()."),
    ("What is a bean?",
     "An object that Spring manages. I do not create it with 'new' - Spring creates it once "
     "at startup, keeps a reference, and gives it to anyone that asks."),
    ("What is encapsulation?",
     "An OOP principle: hide internal state behind methods. My LoginForm has private fields "
     "and exposes them only through getters and setters."),
    ("What is dependency injection?",
     "Instead of a class creating its own dependencies with 'new', the dependencies are "
     "passed in from outside. Spring does this for me by matching constructor parameters "
     "to beans."),
    # ---------- PART B ----------
    ("Walk me through what happens when an admin creates a new article.",
     "The admin clicks 'New article' on the dashboard, which sends GET /admin/new. "
     "AdminController checks the session, then puts an empty Article into the model and "
     "renders admin/form.html. The form is bound to that Article via th:object. When the "
     "admin submits, POST /admin runs createArticle(). @ModelAttribute fills in an Article, "
     "@Valid runs the @NotBlank checks, BindingResult collects any errors. If there are no "
     "errors, articleService.save(article) stamps lastUpdated and asks the JPA repository "
     "to INSERT a new row. The controller then returns redirect:/admin so the user lands "
     "back on the dashboard with their new article visible."),
    ("How does JPA know what tables to create?",
     "Hibernate (the JPA implementation Spring Boot ships with) scans for @Entity classes "
     "at startup. For each one, it creates a table with the same name and a column for each "
     "field. With spring.jpa.hibernate.ddl-auto=update it creates tables that are missing "
     "and adds new columns when I add new fields, but never drops data."),
    ("What is JpaRepository and why is it just an interface?",
     "JpaRepository is a Spring Data interface that declares the standard CRUD methods - "
     "findAll, findById, save, deleteById and many more. When I extend it, Spring scans my "
     "interface at startup and writes a class that implements every method, including the "
     "SQL. So I get a fully working data access layer with literally one line of code."),
    ("How does Spring know what SQL to generate for findByCategoryIgnoreCase?",
     "Spring Data parses the method name. 'findBy' means SELECT, 'Category' means "
     "WHERE category = ?, and 'IgnoreCase' wraps both sides in LOWER(). So the method "
     "becomes SELECT * FROM article WHERE LOWER(category) = LOWER(?). I never wrote a "
     "single line of SQL."),
    ("What is @Entity?",
     "An annotation from JPA that tells Hibernate to map this class to a database table. "
     "Each instance of the class is one row. The fields become columns - unless we mark "
     "one with @Transient."),
    ("What is @Id and @GeneratedValue?",
     "@Id marks a field as the primary key - the unique row identifier. "
     "@GeneratedValue(IDENTITY) tells the database to auto-generate the value, so I do not "
     "have to pick ids myself when creating new articles."),
    ("Why use Optional<Admin> instead of Admin in findByUsername?",
     "Because the lookup might find nothing. If I returned Admin and the username did not "
     "exist, I would have to return null - and the caller could forget to check, leading "
     "to a NullPointerException. Optional forces the caller to handle the empty case "
     "explicitly with isEmpty() or isPresent()."),
    ("How does HttpSession work?",
     "When a browser first visits the site, Tomcat assigns it a unique session id and sends "
     "it back as a cookie. On every later request the browser sends that cookie, so Tomcat "
     "knows which session to load. session.setAttribute(key, value) stores something in "
     "memory tied to that session. session.invalidate() throws everything away - that is "
     "how logout works."),
    ("Why redirect after login instead of rendering the dashboard directly?",
     "Two reasons. One: it changes the URL in the address bar from /login to /admin, so the "
     "user can bookmark or refresh without resubmitting the form. Two: most browsers warn "
     "'do you want to resubmit?' on refreshes of POST results - redirect avoids that warning."),
    ("How is the admin area protected?",
     "Every method in AdminController calls isLoggedIn(session) first. That helper just "
     "checks whether session.getAttribute(\"loggedInAdmin\") is null. If it is, the method "
     "returns 'redirect:/login' so the user is sent to the login page. It is a simple, "
     "explicit check that anyone can read and understand."),
    ("Why use POST for delete and not GET?",
     "GET requests are supposed to be safe - they should never change data. Browsers "
     "prefetch GET URLs, web crawlers follow them, and they get cached. If delete were a "
     "GET, any of those could accidentally wipe an article. Using POST means the browser "
     "will only fire it when the user explicitly submits the form."),
    ("Why are articles stored in plain text but in a real app you would not store passwords "
     "in plain text?",
     "Article content is meant to be read - storing it as plain text is correct. Passwords "
     "are secrets - if the database leaks, plain-text passwords let an attacker log in as "
     "anyone. In a real app I would hash passwords with BCrypt before storing. The brief "
     "did not require it, so I kept the code simple to explain."),
    ("What does redirect: do?",
     "It tells Spring to send a 302 HTTP response with a Location header pointing to a "
     "different URL, instead of rendering a template. The browser then makes a fresh GET "
     "request to that URL."),
    ("How do you stop someone from forging a session cookie?",
     "Tomcat generates session ids that are long random strings, so they cannot be guessed. "
     "In a production deployment we would also set the cookie to HttpOnly (not readable by "
     "JavaScript) and Secure (only sent over HTTPS). For Part B that level of hardening was "
     "not in scope."),
    ("Why use one form template for both create and edit?",
     "DRY - Don't Repeat Yourself. The form looks the same; only the title and the submit "
     "URL differ. I pass a 'mode' attribute to decide between them with a Thymeleaf "
     "ternary. If I needed to change the form layout, I only change one file."),
    ("What does .save() actually do for a new vs existing entity?",
     "If the entity's id is null, JPA does an INSERT and the database fills in the id. If "
     "the id is already set, JPA does an UPDATE on the row with that id. That is why my "
     "updateArticle() controller does article.setId(id) before calling save() - it tells "
     "JPA which row to update."),
    ("What would be the first thing you would change about this project if you had more time?",
     "Hash passwords with BCrypt and add proper Spring Security so I do not have to write "
     "the session-check helper myself. Then maybe add image uploads and a markdown editor "
     "for the article content."),
]
for q, a in qa:
    story.append(P(f"<b>Q: {ihtml.escape(q)}</b>", body))
    story.append(P(f"<b>A:</b> {ihtml.escape(a)}", body))
    story.append(Spacer(1, 0.15*cm))
story.append(PageBreak())

# ---------- 29. Elevator pitch ----------
story.append(P("29. One-Minute Elevator Pitch", h1))
story.append(P("If asked 'tell me about your project', say this. Practice it out loud "
               "until it flows naturally.", body))
story.append(Spacer(1, 0.3*cm))

pitch_style = ParagraphStyle("Pitch", parent=body, fontSize=11, leading=17,
                             leftIndent=10, rightIndent=10, textColor=DARK,
                             backColor=LIGHT, borderPadding=12,
                             borderColor=BLUE, borderWidth=1)
story.append(P(
    "\"WikiApp is a Spring Boot project I built in two stages for BIT235. Part A was a "
    "simple login screen using the MVC pattern with three layers: Controller, Service "
    "and Repository. Part B replaced the hard-coded credentials with a JPA-managed "
    "database using H2, and added a public wiki for browsing articles plus an admin "
    "back-end with full CRUD - create, read, update and delete. The login now stores the "
    "admin's username in an HttpSession, and every admin endpoint checks that session "
    "before doing anything. The clean separation of layers meant the upgrade from Part A "
    "to Part B only required changing the Repository - the Controller and Service barely "
    "moved. The code uses fundamental Java only: classes, getters and setters, Spring "
    "annotations, simple if-statements and the JpaRepository interface. No streams, no "
    "lambdas, no Spring Security - everything I built I can explain.\"",
    pitch_style))
story.append(PageBreak())

# ---------- 30. Glossary ----------
story.append(P("30. Vocabulary Glossary", h1))
glossary = [
    ("MVC", "Model-View-Controller pattern. Model = data, View = HTML, Controller = traffic cop."),
    ("POJO", "Plain Old Java Object. Private fields + no-args constructor + getters/setters."),
    ("Bean", "An object that Spring creates and manages on your behalf."),
    ("Dependency Injection (DI)", "Spring passes required objects in instead of the class creating them."),
    ("Constructor Injection", "DI through constructor parameters - the technique I used."),
    ("HTTP GET", "A request asking the server for a page. Should not change anything."),
    ("HTTP POST", "A request submitting data to the server. Used by forms."),
    ("HTTP 302 redirect", "Server says 'go look at this other URL instead'."),
    ("Thymeleaf", "The template engine that turns my .html files into dynamic web pages."),
    ("Embedded Tomcat", "The web server bundled inside the application."),
    ("Hard-coded", "A value written directly in the source code, not loaded from a database."),
    ("Encapsulation", "OOP principle: hide internal state behind getters and setters."),
    ("Annotation", "Metadata starting with @, e.g. @Controller. Tells Spring how to treat the class."),
    ("Layered architecture", "Splitting code into Controller / Service / Repository layers."),
    ("Maven", "The build tool. Reads pom.xml, downloads dependencies, compiles, packages, runs the app."),
    ("Spring Boot", "A framework that makes Spring apps easy to set up and run."),
    ("JPA", "Java Persistence API - the standard way to map Java objects to database tables."),
    ("Hibernate", "The JPA implementation that Spring Boot ships with."),
    ("Entity", "A Java class marked @Entity that maps to a database table."),
    ("Repository", "A class or interface that talks to the database. JpaRepository in Part B."),
    ("CRUD", "Create, Read, Update, Delete - the four basic database operations."),
    ("HttpSession", "Server-side storage tied to a single user's browser via a cookie."),
    ("H2 database", "A small SQL database that runs inside the application. No install needed."),
    ("Optional<T>", "A wrapper that means 'either a T or nothing' - safer than returning null."),
    ("Foreign key (FK)", "A column that references the primary key of another table."),
    ("Primary key (PK)", "The column that uniquely identifies each row in a table."),
]
story.append(kv_table(glossary, col_widths=(4.5*cm, 11.5*cm)))
story.append(Spacer(1, 0.5*cm))
story.append(hr_table())
story.append(Spacer(1, 0.3*cm))
story.append(P("End of report - good luck with the viva!",
               ParagraphStyle("End", parent=body, alignment=TA_CENTER, fontSize=11,
                              textColor=BLUE)))


# ---------- build ----------
doc = SimpleDocTemplate(OUTPUT, pagesize=A4,
                        leftMargin=2*cm, rightMargin=2*cm,
                        topMargin=2*cm, bottomMargin=1.8*cm,
                        title="WikiApp Code Walkthrough (Part A + B)",
                        author="Movindu Lochana (s1577380)")

doc.build(story, onFirstPage=on_cover, onLaterPages=on_page)
print(f"Wrote: {OUTPUT}")
