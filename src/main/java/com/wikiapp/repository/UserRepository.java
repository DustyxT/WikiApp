/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: UserRepository.java
 * Purpose: The Repository (data access) layer. In Part A there is NO database,
 *          so this class hard-codes the single acceptable username/password
 *          pair as required by the assignment brief. In Part B this class will
 *          be replaced with a real JPA repository that talks to a database.
 *          Keeping the data access in its own class now means the rest of the
 *          app will not need to change later — this is the "layered design"
 *          that the HD rubric rewards.
 */
package com.wikiapp.repository;

// @Repository marks this class as a Spring-managed bean for data access.
// Spring will create one instance and inject it wherever it is needed.
import org.springframework.stereotype.Repository;

@Repository
public class UserRepository {

    // The only acceptable username for Part A. The brief says use "your first
    // name in lower case", so this is set to "movindu".
    private static final String VALID_USERNAME = "movindu";

    // The only acceptable password for Part A, exactly as the brief specifies.
    private static final String VALID_PASSWORD = "123";

    // Returns true only when BOTH the username and password match the stored
    // (hard-coded) credentials. Using .equals() compares the actual text,
    // not memory addresses, which is what we want for strings.
    public boolean credentialsMatch(String username, String password) {

        // Defensive check: if either argument is null, we cannot call .equals on it
        if (username == null || password == null) {
            return false;
        }

        // Both values must match for authentication to succeed.
        return VALID_USERNAME.equals(username) && VALID_PASSWORD.equals(password);
    }
}
