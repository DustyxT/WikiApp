/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: Admin.java
 * Purpose: PART B - A JPA entity that represents an administrator user.
 *          Replaces the hard-coded credentials we used in Part A. Each row
 *          in the ADMIN table is one administrator who can log in.
 */
package com.wikiapp.model;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

@Entity
public class Admin {

    // Auto-generated primary key.
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    // The username must be unique - the database will reject duplicates.
    @Column(nullable = false, unique = true)
    private String username;

    // Stored as plain text for simplicity (the brief does not require hashing
    // and we want the code to be easy to explain). In a real app we would
    // ALWAYS hash passwords with BCrypt or similar.
    @Column(nullable = false)
    private String password;

    // No-args constructor required by JPA.
    public Admin() {
    }

    public Admin(String username, String password) {
        this.username = username;
        this.password = password;
    }

    // ----- Getters and setters -----
    public Long getId() {
        return id;
    }

    public void setId(Long id) {
        this.id = id;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }
}
