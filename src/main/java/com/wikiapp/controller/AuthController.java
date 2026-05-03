/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: AuthController.java
 * Purpose: The Controller layer of MVC. It receives HTTP requests from the
 *          browser, asks the Service whether the login is valid, and chooses
 *          which HTML view (login / welcome / error) Thymeleaf should render.
 *          Controllers should contain NO business logic — they only route.
 */
package com.wikiapp.controller;

import com.wikiapp.model.LoginForm;
import com.wikiapp.service.AuthService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

// @Controller marks this class as a web controller (returns view names, not JSON).
@Controller
// @RequestMapping at the class level prefixes every method's URL — but we leave
// the root mapping ("/") so each method below sets its own specific path.
@RequestMapping("/")
public class AuthController {

    // The service that contains the actual login validation logic.
    private final AuthService authService;

    // Constructor injection: Spring passes in the AuthService bean automatically.
    @Autowired
    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    /**
     * Handles GET requests for "/" and "/login".
     * Just shows the empty login form. The "Model" is Spring's container for
     * data that the HTML page will display — here we put an empty LoginForm
     * so Thymeleaf can bind each <input> to a property of that object.
     */
    @GetMapping({"/", "/login"})
    public String showLoginPage(Model model) {

        // Add an empty form object under the name "loginForm".
        // The login.html template references this name with th:object="${loginForm}".
        model.addAttribute("loginForm", new LoginForm());

        // Return the template file name (without the .html extension).
        // Spring will look for src/main/resources/templates/login.html
        return "login";
    }

    /**
     * Handles POST requests to "/login" — i.e. the form submission.
     * @ModelAttribute tells Spring to build a LoginForm object from the form
     * fields and pass it in. Then we ask the Service whether to accept it.
     */
    @PostMapping("/login")
    public String processLogin(@ModelAttribute("loginForm") LoginForm loginForm,
                               Model model) {

        // Ask the Service layer to validate the credentials.
        boolean ok = authService.isAuthenticated(loginForm);

        if (ok) {
            // SUCCESS path: pass the username to the welcome page so it can
            // greet the user by name, then render welcome.html.
            model.addAttribute("username", loginForm.getUsername().trim().toLowerCase());
            return "welcome";
        }

        // FAILURE path: put a helpful error message into the model and show
        // the dedicated error page.
        model.addAttribute("errorMessage",
                "Invalid username or password. Please try again.");
        return "error";
    }

    /**
     * Handles GET requests to "/register".
     * Part A does not require a working register flow, but the brief's mock-up
     * includes a Register button, so we show a simple placeholder page.
     */
    @GetMapping("/register")
    public String showRegisterPage(Model model) {
        model.addAttribute("message",
                "Registration will be available in Part B once the database is set up.");
        return "register";
    }
}
