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
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Controller;
import org.springframework.ui.Model;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;

import java.util.List;
import java.util.Optional;

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
    @GetMapping
    public String listArticles(
            @RequestParam(value = "category", required = false) String category,
            @RequestParam(value = "search",   required = false) String search,
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

        // Put the list and the current filter values into the Model so the
        // template can display them.
        model.addAttribute("articles", articles);
        model.addAttribute("category", category);
        model.addAttribute("search", search);

        return "wiki/list";
    }

    /**
     * Show one article by its id. The {id} placeholder in the URL is captured
     * by @PathVariable - so /wiki/3 will set id = 3.
     */
    @GetMapping("/{id}")
    public String viewArticle(@PathVariable("id") Long id, Model model) {

        Optional<Article> maybeArticle = articleService.findById(id);

        // If no article with that id exists, send the user to a friendly
        // "not found" page instead of crashing.
        if (maybeArticle.isEmpty()) {
            model.addAttribute("errorMessage",
                    "The article you requested does not exist.");
            return "error";
        }

        model.addAttribute("article", maybeArticle.get());
        return "wiki/view";
    }
}
