-- Author: Movindu Lochana
-- Student ID: s1577380
-- File: data.sql
-- Purpose: PART B - Seed the database with one admin account and a few
--          sample articles. Spring runs this script automatically every
--          time the application starts. The MERGE statements only insert
--          a row if one with the same id does not already exist, so the
--          script is safe to run repeatedly.

-- Seed admin (username "movindu", password "123" - same credentials as Part A)
MERGE INTO ADMIN (id, username, password) KEY(id) VALUES (1, 'movindu', '123');

-- Sample articles so the wiki has something to display straight away.
MERGE INTO ARTICLE (id, title, category, content, last_updated) KEY(id) VALUES
    (1, 'Welcome to WikiApp',
        'General',
        'This is a small Wiki built with Spring Boot for BIT235 Assessment 2. Browse the articles using the navigation above. Administrators can log in to add, edit and remove articles.',
        CURRENT_TIMESTAMP);

MERGE INTO ARTICLE (id, title, category, content, last_updated) KEY(id) VALUES
    (2, 'What is MVC?',
        'Programming',
        'MVC stands for Model-View-Controller. The Model represents the data, the View is what the user sees, and the Controller decides what happens when the user interacts with the page. Splitting these three concerns makes a web app easier to read, change and test.',
        CURRENT_TIMESTAMP);

MERGE INTO ARTICLE (id, title, category, content, last_updated) KEY(id) VALUES
    (3, 'Spring Boot in One Paragraph',
        'Programming',
        'Spring Boot is a framework that bundles the Spring ecosystem with sensible defaults and an embedded web server. You write a class with a main method, mark it @SpringBootApplication, and Spring Boot starts a fully working web app on port 8080. Most of the configuration is automatic.',
        CURRENT_TIMESTAMP);

MERGE INTO ARTICLE (id, title, category, content, last_updated) KEY(id) VALUES
    (4, 'Object Oriented Programming',
        'Programming',
        'OOP is built on four ideas: encapsulation (hiding internal state behind methods), inheritance (a class can extend another), polymorphism (one method behaves differently for different types) and abstraction (focus on what an object does, not how). Java is one of the most popular OOP languages.',
        CURRENT_TIMESTAMP);

MERGE INTO ARTICLE (id, title, category, content, last_updated) KEY(id) VALUES
    (5, 'A Brief History of Java',
        'History',
        'Java was created by James Gosling at Sun Microsystems and released in 1995. Its key idea was "write once, run anywhere": Java code compiles to bytecode that runs on the Java Virtual Machine, which is available for almost every operating system.',
        CURRENT_TIMESTAMP);

-- Bump the auto-increment counters past the seeded ids so that newly created
-- rows do not collide with the ones above.
ALTER TABLE ARTICLE ALTER COLUMN ID RESTART WITH 100;
ALTER TABLE ADMIN   ALTER COLUMN ID RESTART WITH 100;
