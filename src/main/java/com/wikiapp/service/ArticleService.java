/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: ArticleService.java
 * Purpose: PART B - Business logic for managing Wiki articles. The Controller
 *          asks this class to list / find / save / delete articles. The
 *          Service then asks the Repository to talk to the database.
 *
 *          One responsibility per layer keeps the code easy to test, easy
 *          to change, and easy to explain in the viva.
 */
package com.wikiapp.service;

import com.wikiapp.model.Article;
import com.wikiapp.repository.ArticleRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.List;
import java.util.Optional;

@Service
public class ArticleService {

    private final ArticleRepository articleRepository;

    @Autowired
    public ArticleService(ArticleRepository articleRepository) {
        this.articleRepository = articleRepository;
    }

    // ---------- READ ----------

    /** Returns every article in the database, used for the wiki listing. */
    public List<Article> findAll() {
        return articleRepository.findAll();
    }

    /** Returns one article by id, or empty if no such article exists. */
    public Optional<Article> findById(Long id) {
        return articleRepository.findById(id);
    }

    /** Returns articles in a specific category. */
    public List<Article> findByCategory(String category) {
        if (category == null || category.trim().isEmpty()) {
            return findAll();
        }
        return articleRepository.findByCategoryIgnoreCase(category.trim());
    }

    /** Simple title search. */
    public List<Article> search(String text) {
        if (text == null || text.trim().isEmpty()) {
            return findAll();
        }
        return articleRepository.findByTitleContainingIgnoreCase(text.trim());
    }

    // ---------- CREATE / UPDATE ----------

    /**
     * Saves a new article OR updates an existing one. JPA decides based on
     * whether the article already has an id. Either way, we stamp the
     * "lastUpdated" field with the current time.
     */
    public Article save(Article article) {
        article.setLastUpdated(LocalDateTime.now());
        return articleRepository.save(article);
    }

    // ---------- DELETE ----------

    /** Deletes the article with the given id. */
    public void deleteById(Long id) {
        articleRepository.deleteById(id);
    }

    // ---------- HELPER ----------

    /** Quick existence check, used to validate edit/delete URLs. */
    public boolean existsById(Long id) {
        return articleRepository.existsById(id);
    }
}
