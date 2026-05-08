# WikiApp Part A — Viva Preparation Guide

**Author:** Movindu Lochana | **Student ID:** s1577380

This guide explains every part of the project in plain English so you can answer questions confidently in the demo.

---

## 1. The big picture (say this first if asked "explain your project")

> "I built a Spring Boot web application that shows a login page. When the user submits the form, a Controller receives the request, passes the data to a Service for validation, the Service asks a Repository to check the credentials, and then the Controller picks which HTML page to send back — welcome on success, error on failure. I split the code into three layers — Controller, Service, and Repository — so each class only has one job."

That single paragraph hits the MVC, layered design, and request flow rubric items.

---

## 2. The request flow (memorise this — they WILL ask)

```
Browser  ── GET / ──▶  AuthController.showLoginPage()  ──▶  login.html
Browser  ── POST /login (username, password) ──▶  AuthController.processLogin()
                       │
                       ▼
                AuthService.isAuthenticated(form)
                       │
                       ▼
                UserRepository.credentialsMatch(username, password)
                       │
                       ▼ true / false
         ┌─────────────┴─────────────┐
         ▼                           ▼
    welcome.html                 error.html
```

**One-sentence summary:** "Browser → Controller → Service → Repository → back up the chain → view chosen."

---

## 3. Layer-by-layer explanation

### Controller layer — `AuthController.java`
**Job:** Handle HTTP requests. Decide which view to render. No business logic.

| Annotation | What it does in plain words |
|---|---|
| `@Controller` | "This class handles web pages and returns view names." |
| `@GetMapping("/login")` | "When the browser asks for /login, run this method." |
| `@PostMapping("/login")` | "When the browser submits a form to /login, run this method." |
| `@ModelAttribute("loginForm") LoginForm form` | "Spring, build a LoginForm object from the submitted form fields and pass it in." |
| `Model model` | "A bag of data that gets sent to the HTML page." |
| `model.addAttribute("username", "movindu")` | "Put a piece of data into the bag under the name 'username'." |
| `return "welcome";` | "Render the file welcome.html from the templates folder." |

### Service layer — `AuthService.java`
**Job:** Business logic — the rules of "is this login valid?"

What it actually does:
1. Checks the form isn't null
2. Rejects empty / whitespace-only fields
3. Trims spaces and lower-cases the username (so "Movindu" still works)
4. Asks the Repository to compare credentials
5. Returns `true` or `false`

### Repository layer — `UserRepository.java`
**Job:** Data access. In Part A there's no database, so it hard-codes the values.

```java
private static final String VALID_USERNAME = "movindu";
private static final String VALID_PASSWORD = "123";
```

**Why a separate Repository when there's no database?**
> "Because in Part B I'll add a real database. By keeping data access in this class now, only this class will change later — the Service and Controller stay exactly the same. That's the layered-design principle."

### Model layer — `LoginForm.java`
**Job:** A plain data carrier (POJO) with two fields, getters, and setters. Spring fills in the values from the submitted form automatically.

---

## 4. Annotation cheat sheet (likely viva questions)

| Annotation | Plain-English explanation |
|---|---|
| `@SpringBootApplication` | "Bundles three other annotations. Tells Spring to start up, scan for components, and auto-configure itself." |
| `@Controller` | "This is a web controller — methods return view names." |
| `@Service` | "This is a service bean that holds business logic." |
| `@Repository` | "This is a data access bean." |
| `@GetMapping` | "Handle HTTP GET requests at this URL." |
| `@PostMapping` | "Handle HTTP POST (form submission) requests at this URL." |
| `@RequestMapping("/")` | "Prefix for all URLs in this controller." |
| `@Autowired` | "Spring, please inject the required dependency here automatically." |
| `@ModelAttribute` | "Bind the form fields to this Java object." |
| `@NotBlank` | "This field must not be empty." |

---

## 5. Thymeleaf cheat sheet

| Syntax | Plain English |
|---|---|
| `xmlns:th="http://www.thymeleaf.org"` | "Lets us use th:* attributes in this HTML." |
| `th:action="@{/login}"` | "Build the URL /login (handles context paths)." |
| `th:object="${loginForm}"` | "This whole form is bound to the loginForm object in the model." |
| `th:field="*{username}"` | "This input is bound to the 'username' property of loginForm. Sets name, id, value automatically." |
| `th:text="${username}"` | "Replace this tag's text with the value of model attribute 'username'." |
| `th:href="@{/login}"` | "Build a URL link." |

---

## 6. MVC explained simply

**Model** = data (LoginForm, the values inside Model object)
**View** = how it looks (login.html, welcome.html, error.html)
**Controller** = traffic cop (AuthController routes requests to views)

> "The Model is the data, the View is the HTML, and the Controller decides what data goes to which view."

---

## 7. Common viva questions and good answers

**Q: Why did you split your code into three layers?**
A: "Separation of concerns. The Controller only handles HTTP, the Service holds the business rules, and the Repository owns the data. That way, when I add a database in Part B, I only change the Repository — the Controller and Service don't need to be touched."

**Q: What's the difference between @GetMapping and @PostMapping?**
A: "@GetMapping handles requests when the user just visits a URL — it should not change anything. @PostMapping handles form submissions — it's used when the user is sending data, like a username and password."

**Q: How does Spring know to inject the AuthService into the Controller?**
A: "I marked AuthService with @Service, so Spring creates one instance at startup. The Controller's constructor declares it needs an AuthService, and I added @Autowired, so Spring passes the same instance in automatically. That's called constructor dependency injection."

**Q: How does the username typed in the form end up in your Java code?**
A: "The HTML input has `th:field="*{username}"`. When the form is submitted, Spring sees `@ModelAttribute LoginForm` in the controller, creates a new LoginForm, and calls `setUsername()` with the typed value. Then I just call `form.getUsername()`."

**Q: What does Model do?**
A: "Model is like a basket. I put data into it with `addAttribute("username", "movindu")`, and Thymeleaf reads from that basket when rendering the HTML — so `${username}` in the template prints 'movindu'."

**Q: Why is the password 123 and the username "movindu"?**
A: "The brief says to hard-code the username as my first name in lowercase and the password as 123."

**Q: What happens if I type the wrong password?**
A: "AuthService.isAuthenticated() returns false, so the controller adds an error message to the model and returns the view name 'error', which renders error.html."

**Q: What is a POJO?**
A: "Plain Old Java Object — a simple class with private fields, a no-args constructor, and getters and setters. LoginForm is a POJO."

**Q: What does @SpringBootApplication actually do?**
A: "It's a shortcut for three annotations: @Configuration (this class can define beans), @EnableAutoConfiguration (Spring sets up sensible defaults like an embedded Tomcat server), and @ComponentScan (Spring finds all my @Controller, @Service, and @Repository classes in this package and below)."

**Q: What is the embedded Tomcat?**
A: "Tomcat is the web server that listens on port 8080. Spring Boot includes it inside the application, so I don't need to install or configure a separate server — running my main method starts the server."

**Q: Why use a no-args constructor in LoginForm?**
A: "Spring needs to create a new empty LoginForm before calling setUsername() and setPassword() with the form data. Without a no-args constructor, it can't do that."

**Q: What's the point of trimming and lower-casing the username in the service?**
A: "User-friendly validation. If someone types 'Movindu' or ' movindu ' with spaces, they should still be able to log in. That's a small business rule — and putting it in the Service layer is exactly the right place, not the Controller and not the Repository."

**Q: Walk me through what happens when I click Log in.**
A: "The browser sends a POST request to /login with username and password. Spring matches it to processLogin() in AuthController. Spring builds a LoginForm object from the form fields. The controller calls authService.isAuthenticated(loginForm). The service trims and lowercases the username, checks both fields aren't empty, then calls userRepository.credentialsMatch(). The repository compares the values to the hard-coded ones using .equals() and returns true or false. Back in the controller, if true I add the username to the model and return 'welcome', otherwise I add an error message and return 'error'. Spring renders the matching .html file and sends it back to the browser."

**Q: What's the difference between == and .equals() for strings?**
A: "== compares whether two variables point to the same memory location. .equals() compares the actual character contents. For strings, you should always use .equals()."

**Q: What is a bean?**
A: "A bean is just an object that Spring manages. I don't create it with `new` — Spring creates it once at startup, keeps a reference, and gives it to anyone that asks for it."

**Q: What does the application.properties file do?**
A: "It configures Spring Boot. I set server.port=8080 so the app runs on that port, and disabled Thymeleaf caching so HTML changes show up without restarting."

---

## 8. If something breaks during the demo

| Problem | Quick fix |
|---|---|
| Port 8080 already in use | Change `server.port` in application.properties to 8081 |
| `mvn` not found | Open new PowerShell, or run `C:\Tools\Maven\apache-maven-3.9.9\bin\mvn spring-boot:run` |
| Page won't load | Check the terminal — make sure it says "Started WikiAppApplication" |
| Wrong username works | Remember it's case-insensitive (lowercased) and trimmed |

---

## 9. Vocabulary you should know

- **MVC** — Model, View, Controller pattern
- **POJO** — Plain Old Java Object
- **Bean** — an object Spring manages
- **Dependency Injection** — Spring passes required objects in for you
- **Constructor injection** — DI through the constructor (what I used)
- **HTTP GET** — request a page
- **HTTP POST** — submit data
- **Thymeleaf** — the template engine that renders my HTML
- **Embedded server** — Tomcat runs inside the app
- **Hard-coded** — values written directly in the code (not from a database)

---

## 10. One-minute elevator pitch (practice this out loud)

> "This is Part A of my BIT235 Wiki application. It's a Spring Boot project that follows the MVC pattern with three layers — Controller, Service, and Repository. The user enters a username and password on the login page. The form is submitted to my AuthController, which uses @ModelAttribute to receive a LoginForm object. The Controller calls AuthService, which trims and lower-cases the username, then asks UserRepository to compare against the hard-coded values 'movindu' and '123'. If the credentials match, I send the user to a welcome page; if not, an error page. I separated the layers so that in Part B I can swap the hard-coded repository for one that talks to a real database without changing my Controller or Service."
