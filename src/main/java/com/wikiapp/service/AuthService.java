/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: AuthService.java
 * Purpose: The Service (business logic) layer for authentication.
 *          PART A: Used a hard-coded UserRepository.
 *          PART B: Now talks to the database through AdminRepository.
 *          The Controller and the Controller's view code did NOT change -
 *          this is exactly the benefit of layered design.
 */
package com.wikiapp.service;

import com.wikiapp.model.Admin;
import com.wikiapp.model.LoginForm;
import com.wikiapp.repository.AdminRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

import java.util.Optional;

@Service
public class AuthService {

    // The Repository this service depends on.
    private final AdminRepository adminRepository;

    // Constructor injection - Spring passes in the AdminRepository bean.
    @Autowired
    public AuthService(AdminRepository adminRepository) {
        this.adminRepository = adminRepository;
    }

    /**
     * Returns true if the supplied form contains valid credentials, otherwise
     * false. Validation rules and credential lookup are kept in one place.
     */
    public boolean isAuthenticated(LoginForm form) {

        // Defensive null check.
        if (form == null) {
            return false;
        }

        String username = form.getUsername();
        String password = form.getPassword();

        // Reject empty / whitespace-only inputs.
        if (username == null || username.trim().isEmpty()) {
            return false;
        }
        if (password == null || password.trim().isEmpty()) {
            return false;
        }

        // Normalise the username so "Movindu" or " movindu " still works.
        String cleanedUsername = username.trim().toLowerCase();

        // Look up the admin in the database. Optional means the result
        // might be empty - which is normal if no such username exists.
        Optional<Admin> maybeAdmin = adminRepository.findByUsername(cleanedUsername);

        // If no admin with that username exists, fail.
        if (maybeAdmin.isEmpty()) {
            return false;
        }

        // Compare the stored password to the supplied one.
        // .equals() compares the actual text - never use == for strings.
        Admin admin = maybeAdmin.get();
        return admin.getPassword().equals(password);
    }
}
