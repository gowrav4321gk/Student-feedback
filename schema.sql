-- ==============================================================================
-- Student Feedback Analysis System - MySQL Database Schema
-- Academic Project for B.Tech CSE
-- ==============================================================================

-- 1. Create Database if it doesn't already exist
CREATE DATABASE IF NOT EXISTS student_feedback_db
    CHARACTER SET utf8mb4
    COLLATE utf8mb4_unicode_ci;

USE student_feedback_db;

-- 2. Departments Table
CREATE TABLE IF NOT EXISTS departments (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(10) NOT NULL UNIQUE,
    name VARCHAR(100) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
) ENGINE=InnoDB;

-- 3. Faculty Table
CREATE TABLE IF NOT EXISTS faculty (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    designation VARCHAR(100) NOT NULL,
    department_id INT NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    experience_years INT DEFAULT 1,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- 4. Courses Table
CREATE TABLE IF NOT EXISTS courses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    code VARCHAR(20) NOT NULL UNIQUE,
    name VARCHAR(150) NOT NULL,
    department_id INT NOT NULL,
    semester INT NOT NULL,
    credits INT NOT NULL DEFAULT 3,
    faculty_id INT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE SET NULL
) ENGINE=InnoDB;

-- 5. Feedback Table (100% Anonymous: no student ID, roll number, or IP stored)
CREATE TABLE IF NOT EXISTS feedback (
    id INT AUTO_INCREMENT PRIMARY KEY,
    department_id INT NOT NULL,
    course_id INT NOT NULL,
    faculty_id INT NOT NULL,
    academic_year VARCHAR(20) NOT NULL,
    semester VARCHAR(20) NOT NULL,
    
    -- Rating categories (1 to 5 scale)
    teaching_quality INT NOT NULL CHECK (teaching_quality BETWEEN 1 AND 5),
    course_content INT NOT NULL CHECK (course_content BETWEEN 1 AND 5),
    punctuality INT NOT NULL CHECK (punctuality BETWEEN 1 AND 5),
    doubt_solving INT NOT NULL CHECK (doubt_solving BETWEEN 1 AND 5),
    lab_work_fairness INT NOT NULL CHECK (lab_work_fairness BETWEEN 1 AND 5),
    
    -- Calculated average rating for quick queries
    overall_rating FLOAT NOT NULL,
    
    -- Qualitative feedback
    comments_positive TEXT NULL,
    comments_improvement TEXT NULL,
    
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    
    FOREIGN KEY (department_id) REFERENCES departments(id) ON DELETE CASCADE,
    FOREIGN KEY (course_id) REFERENCES courses(id) ON DELETE CASCADE,
    FOREIGN KEY (faculty_id) REFERENCES faculty(id) ON DELETE CASCADE
) ENGINE=InnoDB;

-- Indices for fast aggregation and analytics queries
CREATE INDEX idx_feedback_faculty ON feedback(faculty_id);
CREATE INDEX idx_feedback_course ON feedback(course_id);
CREATE INDEX idx_feedback_department ON feedback(department_id);
CREATE INDEX idx_feedback_overall ON feedback(overall_rating);
