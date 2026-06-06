# WikiApp — BIT235 Assessment 2

**Author:** Movindu Lochana  
**Student ID:** s1577380  
**Subject:** BIT235 Object Oriented Programming — Semester 1, 2026

A Spring Boot MVC Wiki application built for Assessment 2.  
**Part A** implements the administrator login screen.  
**Part B** adds a full H2 database, public wiki, and admin CRUD for articles.

---

## Credentials

| Field    | Value     |
|----------|-----------|
| Username | `movindu` |
| Password | `123`     |

---

## How to run

Requires **Java 17 or higher**. Maven is bundled via the Maven Wrapper — no installation needed.

**Windows:**
```bash
.\mvnw.cmd spring-boot:run
```

**Mac / Linux:**
```bash
./mvnw spring-boot:run
```

Then open <http://localhost:8080> in your browser.

---

## Branches

| Branch | Contents |
|--------|----------|
| `main` | Full project — Part A + Part B |
| `part-a` | Part A only (login screen, frozen snapshot) |

---

## Project structure (MVC + layered design)

```
src/main/java/com/wikiapp/
├── WikiAppApplication.java              # Entry point — starts the server
├── model/
│   ├── LoginForm.java                   # Form-backing object for login (Part A)
│   ├── Article.java                     # JPA entity → ARTICLE table (Part B)
│   └── Admin.java                       # JPA entity → ADMIN table (Part B)
├── repository/
│   ├── ArticleRepository.java           # Database queries for articles (Part B)
│   └── AdminRepository.java             # Database queries for admins (Part B)
├── service/
│   ├── AuthService.java                 # Login business logic
│   └── ArticleService.java              # Article business logic (Part B)
└── controller/
    ├── AuthController.java              # Handles /login and /logout
    ├── WikiController.java              # Handles /wiki (public, no auth required)
    └── AdminController.java             # Handles /admin (session-protected CRUD)

src/main/resources/
├── application.properties              # Port, H2 database, JPA settings
├── data.sql                            # Seed data (admin account + sample articles)
├── templates/
│   ├── login.html                      # Login form
│   ├── welcome.html                    # Post-login welcome
│   ├── error.html                      # Error page
│   ├── wiki/
│   │   ├── list.html                   # Public article list with search + category filters
│   │   └── view.html                   # Single article view
│   └── admin/
│       ├── dashboard.html              # Admin article management table
│       ├── form.html                   # Shared create / edit form
│       └── confirm-delete.html         # Delete confirmation page
└── static/css/style.css                # Stylesheet for all pages
```

---

## Part A — Administrator Login

- Login form bound to `LoginForm` via Thymeleaf `th:object` / `th:field`
- `AuthService` validates credentials against the `ADMIN` table in the database
- Successful login stores the username in `HttpSession` and redirects to `/admin`
- Failed login shows an error page

**Request flow:**
1. `GET /login` → `AuthController.showLoginPage` → `login.html`
2. User submits form → `POST /login` → `AuthController.processLogin`
3. Controller calls `AuthService.isAuthenticated(form)`
4. Valid → session set → `redirect:/admin` | Invalid → `error.html`

---

## Part B — Public Wiki + Admin CRUD

### Public wiki (no login required)
- `GET /wiki` — lists all articles; supports `?search=` and `?category=` URL filters
- `GET /wiki/{id}` — displays a single article

### Admin dashboard (login required)
- `GET /admin` — lists all articles with Edit / Delete buttons
- `GET /admin/new` + `POST /admin` — create a new article
- `GET /admin/edit/{id}` + `POST /admin/edit/{id}` — edit an existing article
- `GET /admin/delete/{id}` + `POST /admin/delete/{id}` — confirm and delete an article
- `GET /logout` — invalidates the session

### Database
- H2 file-based database stored in `./data/wikidb`
- Tables created automatically by JPA/Hibernate on startup
- `data.sql` seeds one admin account and five sample articles using `MERGE` statements
- H2 browser console available at <http://localhost:8080/h2-console>

### Session protection
Every method in `AdminController` calls `isLoggedIn(session)` first.  
If the session does not contain the `loggedInAdmin` key, the request is redirected to `/login`.

---

## Key technologies

| Technology | Role |
|------------|------|
| Spring Boot 3.3.4 | Framework, embedded Tomcat server |
| Spring MVC | @Controller, @GetMapping, @PostMapping |
| Thymeleaf | HTML template engine |
| Spring Data JPA | Repository layer, auto-generated SQL |
| H2 Database | Embedded file-based SQL database |
| Bean Validation | @NotBlank on form fields |
| HttpSession | Admin authentication state |
| Maven Wrapper | Zero-install build tool |
