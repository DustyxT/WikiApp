/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: AuthController.java
 * Purpose: The Controller layer of MVC. It receives HTTP requests, asks the
 *          Service whether the login is valid, and chooses which HTML view
 *          Thymeleaf should render. PART B adds session handling so that
 *          the admin pages know whether the user is logged in.
 */
package com.wikiapp.controller;

import com.wikiapp.model.LoginForm;
import com.wikiapp.service.AuthService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

@Controller
@RequestMapping("/")
public class AuthController {

    // Constant key used everywhere we read or write the logged-in admin name
    // in the HttpSession. Using a constant avoids typos.
    public static final String SESSION_ADMIN_KEY = "loggedInAdmin";

    private final AuthService authService;

    @Autowired
    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    /** Show the empty login form. */
    @GetMapping({"/", "/login"})
    public String showLoginPage(Model model) {
        model.addAttribute("loginForm", new LoginForm());
        return "login";
    }

    /**
     * Process the submitted login form.
     * If the credentials are valid, store the username in the HttpSession so
     * the admin pages know who is logged in, then redirect to the dashboard.
     */
    @PostMapping("/login")
    public String processLogin(@ModelAttribute("loginForm") LoginForm loginForm,
                               HttpSession session,
                               Model model) {

        boolean ok = authService.isAuthenticated(loginForm);

        if (ok) {
            // setAttribute stores a value that lives for the user's session
            // (until they log out or close the browser).
            String cleaned = loginForm.getUsername().trim().toLowerCase();
            session.setAttribute(SESSION_ADMIN_KEY, cleaned);

            // "redirect:" tells Spring to send the browser to a different URL
            // instead of rendering a template directly. This avoids the
            // browser's "resubmit form?" warning when the user refreshes.
            return "redirect:/admin";
        }

        // Failed login: show the error page.
        model.addAttribute("errorMessage",
                "Invalid username or password. Please try again.");
        return "error";
    }

    /** Log out: clear the session and go back to the login page. */
    @GetMapping("/logout")
    public String logout(HttpSession session) {
        // invalidate() throws away EVERYTHING stored in this user's session.
        session.invalidate();
        return "redirect:/login";
    }

    /** Placeholder register page (not implemented in this assignment). */
    @GetMapping("/register")
    public String showRegisterPage(Model model) {
        model.addAttribute("message",
                "Registration is not part of this assessment - admin accounts " +
                "are seeded into the database at startup.");
        return "register";
    }
}
