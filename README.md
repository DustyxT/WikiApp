# WikiApp — BIT235 Assessment 2 Part A

**Author:** Movindu Lochana
**Student ID:** s1577380
**Subject:** BIT235 Object Oriented Programming — Semester 1, 2026

A Spring Boot MVC web application implementing the Wiki administrator login screen.
Authentication uses a single hard-coded username/password pair as required by the brief.

## Credentials

| Field    | Value     |
|----------|-----------|
| Username | `movindu` |
| Password | `123`     |

## How to run

Requires Java 17 and Maven.

```bash
mvn spring-boot:run
```

Then open <http://localhost:8080> in your browser.

## Project structure (MVC + layered design)

```
src/main/java/com/wikiapp/
├── WikiAppApplication.java       # entry point
├── controller/AuthController.java  # routes HTTP requests (View ↔ Controller)
├── service/AuthService.java        # business / validation logic
├── repository/UserRepository.java  # data access (hard-coded for Part A)
└── model/LoginForm.java            # form-backing object

src/main/resources/
├── application.properties
├── templates/                      # Thymeleaf views
│   ├── login.html
│   ├── welcome.html
│   ├── error.html
│   └── register.html
└── static/css/style.css            # custom styles
```

## Request flow

1. **GET /** or **GET /login** → `AuthController.showLoginPage` → `login.html`
2. User submits form → **POST /login** → `AuthController.processLogin`
3. Controller calls `AuthService.isAuthenticated(form)`
4. Service trims/lower-cases the username and asks `UserRepository.credentialsMatch`
5. If valid → `welcome.html`, else → `error.html`

Each layer has one clear job — this satisfies the HD rubric's "Clear separation
of Controller, Service, Repository" criterion.
