/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: WikiController.java
 * Purpose: PART B - The PUBLIC wiki interface. Anyone (logged in or not) can
 *          browse and read articles. No authentication is required for these
 *          pages, exactly like a real wiki.
 */
package com.wikiapp.controller;

import com.wikiapp.model.Article;
import com.wikiapp.service.ArticleService;
import jakarta.servlet.http.HttpSession;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.util.Optional;
import java.util.stream.Collectors;

@Controller
@RequestMapping("/wiki")
public class WikiController {

    private final ArticleService articleService;

    @Autowired
    public WikiController(ArticleService articleService) {
        this.articleService = articleService;
    }

    /**
     * Show the list of articles. Optionally filter by category or search by
     * title text using URL parameters such as /wiki?category=Programming
     * or /wiki?search=spring.
     *
     * @RequestParam(required=false) means the parameter is optional - if the
     * URL does not include it, Spring passes null.
     */
    /**
     * Helper: returns true when an admin session is active.
     * We check this here in the Controller (the proper MVC layer) and pass
     * a simple boolean to the template, rather than letting the template
     * reach into the session directly.
     */
    private boolean isAdmin(HttpSession session) {
        return session.getAttribute(AuthController.SESSION_ADMIN_KEY) != null;
    }

    @GetMapping
    public String listArticles(
            @RequestParam(value = "category", required = false) String category,
            @RequestParam(value = "search",   required = false) String search,
            HttpSession session,
            Model model) {

        List<Article> articles;

        // Pick which Service method to call based on the URL parameters.
        if (search != null && !search.trim().isEmpty()) {
            articles = articleService.search(search);
        } else if (category != null && !category.trim().isEmpty()) {
            articles = articleService.findByCategory(category);
        } else {
            articles = articleService.findAll();
        }

        // Build a sorted list of unique category names from ALL articles so the
        // template can show category filter buttons. Stream.distinct() removes
        // duplicates; sorted() alphabetises them.
        List<String> categories = articleService.findAll()
                .stream()
                .map(Article::getCategory)
                .distinct()
                .sorted()
                .collect(Collectors.toList());

        // Put the list and the current filter values into the Model so the
        // template can display them.
        model.addAttribute("articles", articles);
        model.addAttribute("categories", categories);
        model.addAttribute("category", category);
        model.addAttribute("search", search);
        // isAdmin tells the template whether to show admin controls.
        model.addAttribute("isAdmin", isAdmin(session));

        return "wiki/list";
    }

    /**
     * Show one article by its id. The {id} placeholder in the URL is captured
     * by @PathVariable - so /wiki/3 will set id = 3.
     */
    @GetMapping("/{id}")
    public String viewArticle(@PathVariable("id") Long id,
                              HttpSession session,
                              Model model) {

        Optional<Article> maybeArticle = articleService.findById(id);

        // If no article with that id exists, send the user to a friendly
        // "not found" page instead of crashing.
        if (maybeArticle.isEmpty()) {
            model.addAttribute("errorMessage",
                    "The article you requested does not exist.");
            return "error";
        }

        model.addAttribute("article", maybeArticle.get());
        model.addAttribute("isAdmin", isAdmin(session));
        return "wiki/view";
    }
}
