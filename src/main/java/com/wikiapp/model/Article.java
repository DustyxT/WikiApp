/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: Article.java
 * Purpose: PART B - A JPA entity that represents a single Wiki article in
 *          the database. Each instance of this class corresponds to one row
 *          in the ARTICLE table. JPA (the Java Persistence API) will create
 *          and manage that table for us automatically.
 */
package com.wikiapp.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.validation.constraints.NotBlank;
import java.time.LocalDateTime;

// @Entity tells JPA: "create a database table for this class".
@Entity
public class Article {

    // @Id marks the primary key (the unique row identifier).
    // @GeneratedValue with IDENTITY tells the database to auto-generate
    // the id whenever a new article is saved.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // The article's title. @NotBlank stops empty submissions in the form.
    // @Column(nullable = false) makes the database column NOT NULL too.
    @NotBlank(message = "Title is required")
    @Column(nullable = false)
    private String title;

    // The category this article belongs to (e.g. "Programming", "History").
    @NotBlank(message = "Category is required")
    @Column(nullable = false)
    private String category;

    // The article body. We use length = 5000 so we can store long text.
    @NotBlank(message = "Content is required")
    @Column(nullable = false, length = 5000)
    private String content;

    // When the article was last modified. Set automatically by ArticleService
    // every time the article is saved or updated.
    private LocalDateTime lastUpdated;

    // No-args constructor: JPA needs this to create a blank Article and then
    // fill it in with values from the database row.
    public Article() {
    }

    // Convenience constructor for creating articles in code (e.g. in data.sql
    // we do not use this, but it makes manual testing easier).
    public Article(String title, String category, String content) {
        this.title = title;
        this.category = category;
        this.content = content;
        this.lastUpdated = LocalDateTime.now();
    }

    // ----- Getters and setters: standard POJO accessors. -----
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getTitle() {
        return title;
    }

    public void setTitle(String title) {
        this.title = title;
    }

    public String getCategory() {
        return category;
    }

    public void setCategory(String category) {
        this.category = category;
    }

    public String getContent() {
        return content;
    }

    public void setContent(String content) {
        this.content = content;
    }

    public LocalDateTime getLastUpdated() {
        return lastUpdated;
    }

    public void setLastUpdated(LocalDateTime lastUpdated) {
        this.lastUpdated = lastUpdated;
    }
}
