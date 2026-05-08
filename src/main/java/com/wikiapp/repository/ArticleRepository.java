/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: ArticleRepository.java
 * Purpose: PART B - Data access for Article entities. By extending Spring's
 *          JpaRepository, we get a fully working repository with no code:
 *          findAll(), findById(id), save(article), deleteById(id), etc.
 *          Spring writes the SQL for us at startup.
 */
package com.wikiapp.repository;

import com.wikiapp.model.Article;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.List;

// JpaRepository<Entity, IdType> - the two type parameters say:
//   "this is a repository for Article objects whose primary key is a Long".
public interface ArticleRepository extends JpaRepository<Article, Long> {

    // We can also declare custom query methods just by following Spring's
    // naming convention. Spring reads the method name and writes the SQL:
    //   "findByCategory" -> SELECT * FROM article WHERE category = ?
    List<Article> findByCategoryIgnoreCase(String category);

    // Returns articles whose title contains the given text (case-insensitive).
    // Useful for a simple search box.
    List<Article> findByTitleContainingIgnoreCase(String text);
}
