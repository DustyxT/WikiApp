/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: LoginForm.java
 * Purpose: A plain Java object (POJO) that holds the data the user types into
 *          the login form. Spring will automatically copy each form field into
 *          the matching property here when the form is submitted.
 */
package com.wikiapp.model;

// Validation annotations: @NotBlank means the field must not be null/empty
import jakarta.validation.constraints.NotBlank;

public class LoginForm {

    // Holds the username typed in the form. @NotBlank shows an error if left empty.
    @NotBlank(message = "Username is required")
    private String username;

    // Holds the password typed in the form.
    @NotBlank(message = "Password is required")
    private String password;

    // No-argument constructor: Spring needs this to create an empty LoginForm
    // before filling in the values from the submitted HTML form.
    public LoginForm() {
    }

    // Standard "getter" — Thymeleaf and Spring read the value through this.
    public String getUsername() {
        return username;
    }

    // Standard "setter" — Spring writes the submitted value through this.
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
