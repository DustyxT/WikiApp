/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: AdminController.java
 * Purpose: PART B - The ADMIN-ONLY back-end. Provides CRUD pages for
 *          managing articles. Every method first checks the HttpSession
 *          to make sure the user is logged in - if not, they are redirected
 *          to the login page.
 *
 *          CRUD = Create, Read, Update, Delete. We have URL endpoints for
 *          each of those four operations.
 */
package com.wikiapp.controller;

import com.wikiapp.model.Article;
import com.wikiapp.service.ArticleService;
import jakarta.servlet.http.HttpSession;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.validation.BindingResult;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.ModelAttribute;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestMapping;

import java.util.Optional;

@Controller
@RequestMapping("/admin")
public class AdminController {

    private final ArticleService articleService;

    @Autowired
    public AdminController(ArticleService articleService) {
        this.articleService = articleService;
    }

    /**
     * Helper method - returns true if the current visitor is logged in as an
     * admin. We check this at the start of every admin endpoint so that
     * unauthenticated users cannot access these pages.
     */
    private boolean isLoggedIn(HttpSession session) {
        return session.getAttribute(AuthController.SESSION_ADMIN_KEY) != null;
    }

    // ---------- READ: dashboard listing all articles ----------

    @GetMapping
    public String dashboard(HttpSession session, Model model) {

        // Guard: not logged in -> send to login page.
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }

        // Show every article and the username of the logged-in admin.
        model.addAttribute("articles", articleService.findAll());
        model.addAttribute("adminUser",
                session.getAttribute(AuthController.SESSION_ADMIN_KEY));

        return "admin/dashboard";
    }

    // ---------- CREATE: show empty form ----------

    @GetMapping("/new")
    public String showCreateForm(HttpSession session, Model model) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }

        // An empty Article so the form has something to bind to.
        model.addAttribute("article", new Article());
        // "mode" controls the page heading and the form-action URL in the
        // shared template (admin/form.html).
        model.addAttribute("mode", "create");
        return "admin/form";
    }

    // ---------- CREATE: handle submission ----------

    @PostMapping
    public String createArticle(@Valid @ModelAttribute("article") Article article,
                                BindingResult bindingResult,
                                HttpSession session,
                                Model model) {

        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }

        // BindingResult collects validation errors from @NotBlank etc.
        // If anything failed, redisplay the form with those errors shown.
        if (bindingResult.hasErrors()) {
            model.addAttribute("mode", "create");
            return "admin/form";
        }

        articleService.save(article);
        return "redirect:/admin";
    }

    // ---------- UPDATE: show edit form pre-filled with the article ----------

    @GetMapping("/edit/{id}")
    public String showEditForm(@PathVariable("id") Long id,
                               HttpSession session,
                               Model model) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }

        Optional<Article> maybeArticle = articleService.findById(id);
        if (maybeArticle.isEmpty()) {
            model.addAttribute("errorMessage",
                    "The article you tried to edit does not exist.");
            return "error";
        }

        model.addAttribute("article", maybeArticle.get());
        model.addAttribute("mode", "edit");
        return "admin/form";
    }

    // ---------- UPDATE: handle submission ----------

    @PostMapping("/edit/{id}")
    public String updateArticle(@PathVariable("id") Long id,
                                @Valid @ModelAttribute("article") Article article,
                                BindingResult bindingResult,
                                HttpSession session,
                                Model model) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }

        if (bindingResult.hasErrors()) {
            model.addAttribute("mode", "edit");
            return "admin/form";
        }

        // Make sure the id from the URL is set on the article so JPA does
        // an UPDATE rather than an INSERT.
        article.setId(id);
        articleService.save(article);
        return "redirect:/admin";
    }

    // ---------- DELETE: confirmation page ----------

    @GetMapping("/delete/{id}")
    public String confirmDelete(@PathVariable("id") Long id,
                                HttpSession session,
                                Model model) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }

        Optional<Article> maybeArticle = articleService.findById(id);
        if (maybeArticle.isEmpty()) {
            model.addAttribute("errorMessage",
                    "The article you tried to delete does not exist.");
            return "error";
        }

        model.addAttribute("article", maybeArticle.get());
        return "admin/confirm-delete";
    }

    // ---------- DELETE: actually delete ----------

    @PostMapping("/delete/{id}")
    public String deleteArticle(@PathVariable("id") Long id,
                                HttpSession session) {
        if (!isLoggedIn(session)) {
            return "redirect:/login";
        }

        if (articleService.existsById(id)) {
            articleService.deleteById(id);
        }
        return "redirect:/admin";
    }
}
