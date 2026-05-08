/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: AdminRepository.java
 * Purpose: PART B - Data access for Admin entities. Replaces the old
 *          UserRepository which used hard-coded values.
 */
package com.wikiapp.repository;

import com.wikiapp.model.Admin;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface AdminRepository extends JpaRepository<Admin, Long> {

    // Spring builds this query from the method name:
    //   SELECT * FROM admin WHERE username = ?
    // Optional<Admin> means "either an Admin or nothing" - safer than
    // returning null because the caller is forced to handle the missing case.
    Optional<Admin> findByUsername(String username);
}
