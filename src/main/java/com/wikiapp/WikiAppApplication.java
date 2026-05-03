/*
 * Author: Movindu Lochana
 * Student ID: s1577380
 * File: WikiAppApplication.java
 * Purpose: Entry point of the Spring Boot application. Running this class
 *          starts the embedded Tomcat server on http://localhost:8080.
 */
package com.wikiapp;

// Imports the annotation that bundles @Configuration, @ComponentScan and @EnableAutoConfiguration
import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

// @SpringBootApplication tells Spring to auto-configure the app and scan
// the "com.wikiapp" package (and its sub-packages) for Controllers, Services, etc.
@SpringBootApplication
public class WikiAppApplication {

    // The main method is what the JVM runs first. It hands control to Spring Boot,
    // which then starts the web server and wires our beans together.
    public static void main(String[] args) {
        SpringApplication.run(WikiAppApplication.class, args);
    }
}
