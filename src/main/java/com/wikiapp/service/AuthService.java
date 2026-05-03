/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: AuthService.java
 * Purpose: The Service (business logic) layer. The Controller asks this class
 *          "is this login valid?" and this class decides — possibly after
 *          trimming whitespace, lower-casing the username, or running other
 *          validation rules. The actual data lookup is delegated to the
 *          Repository, so each layer has ONE clear responsibility.
 */
package com.wikiapp.service;

import com.wikiapp.model.LoginForm;
import com.wikiapp.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;

// @Service tells Spring this is a business-logic bean. Spring will create one
// instance at start-up and inject it into any controller that needs it.
@Service
public class AuthService {

    // The Repository this service depends on. We never create it ourselves —
    // Spring "injects" the same single UserRepository instance into here.
    private final UserRepository userRepository;

    // Constructor injection (preferred over field injection because it makes
    // the dependency obvious and the class easier to unit-test).
    @Autowired
    public AuthService(UserRepository userRepository) {
        this.userRepository = userRepository;
    }

    /**
     * Checks whether the data inside the submitted LoginForm is valid.
     * Returns true only when the credentials match the stored ones.
     */
    public boolean isAuthenticated(LoginForm form) {

        // Guard against a null form (should not happen, but safe to check).
        if (form == null) {
            return false;
        }

        // Read the values typed by the user.
        String username = form.getUsername();
        String password = form.getPassword();

        // Extra validation rule: reject empty / whitespace-only input early
        // so we don't even bother asking the repository.
        if (username == null || username.trim().isEmpty()) {
            return false;
        }
        if (password == null || password.trim().isEmpty()) {
            return false;
        }

        // Normalise the username: trim whitespace and force lower-case so the
        // user can type "Movindu" or " movindu " and still log in successfully.
        String cleanedUsername = username.trim().toLowerCase();

        // Delegate the actual credential lookup to the Repository layer.
        return userRepository.credentialsMatch(cleanedUsername, password);
    }
}
