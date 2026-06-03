-- Create database
CREATE DATABASE IF NOT EXISTS bloodbridge;
USE bloodbridge;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('hospital_admin', 'blood_donor', 'blood_bank_manager') NOT NULL,
    full_name VARCHAR(100),
    phone VARCHAR(20),
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL
);

-- Donor profiles
CREATE TABLE IF NOT EXISTS donors (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    age INT,
    weight DECIMAL(5,2),
    medical_conditions TEXT,
    eligibility_status BOOLEAN DEFAULT TRUE,
    last_donation_date DATE,
    total_donations INT DEFAULT 0,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Blood inventory
CREATE TABLE IF NOT EXISTS inventory (
    id INT PRIMARY KEY AUTO_INCREMENT,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') UNIQUE NOT NULL,
    quantity_units INT DEFAULT 0,
    critical_threshold INT DEFAULT 10,
    last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    updated_by INT,
    FOREIGN KEY (updated_by) REFERENCES users(id)
);

-- Emergency requests
CREATE TABLE IF NOT EXISTS emergency_requests (
    id INT PRIMARY KEY AUTO_INCREMENT,
    hospital_id INT NOT NULL,
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    quantity INT NOT NULL,
    priority ENUM('low', 'medium', 'high', 'critical') DEFAULT 'medium',
    patient_name VARCHAR(100),
    patient_age INT,
    patient_condition TEXT,
    status ENUM('pending', 'fulfilled', 'cancelled') DEFAULT 'pending',
    request_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    fulfillment_date TIMESTAMP NULL,
    FOREIGN KEY (hospital_id) REFERENCES users(id)
);

-- Donation schedules
CREATE TABLE IF NOT EXISTS donations (
    id INT PRIMARY KEY AUTO_INCREMENT,
    donor_id INT NOT NULL,
    scheduled_date DATE NOT NULL,
    donation_time TIME,
    status ENUM('scheduled', 'completed', 'cancelled') DEFAULT 'scheduled',
    blood_type ENUM('A+', 'A-', 'B+', 'B-', 'AB+', 'AB-', 'O+', 'O-') NOT NULL,
    quantity_units INT DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (donor_id) REFERENCES users(id)
);

-- Notifications
CREATE TABLE IF NOT EXISTS notifications (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    title VARCHAR(200),
    message TEXT,
    is_read BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users(id) ON DELETE CASCADE
);

-- Insert default inventory
INSERT IGNORE INTO inventory (blood_type, quantity_units, critical_threshold) VALUES
('A+', 25, 10),
('A-', 10, 5),
('B+', 20, 10),
('B-', 8, 5),
('AB+', 5, 3),
('AB-', 3, 2),
('O+', 30, 15),
('O-', 15, 8);

-- Insert sample admin user (password: Admin@123)
INSERT IGNORE INTO users (username, email, password_hash, role, full_name) VALUES
('admin', 'admin@bloodbridge.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYOhQrVBvQFu', 'blood_bank_manager', 'System Administrator');

-- Insert sample hospital admin (password: Hospital@123)
INSERT IGNORE INTO users (username, email, password_hash, role, full_name, phone) VALUES
('cityhospital', 'hospital@cityhospital.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYOhQrVBvQFu', 'hospital_admin', 'City General Hospital', '+1234567890');

-- Insert sample donor (password: Donor@123)
INSERT IGNORE INTO users (username, email, password_hash, role, full_name, phone) VALUES
('johndoe', 'john@example.com', '$2b$12$LQv3c1yqBWVHxkd0LHAkCOYz6TtxMQJqhN8/X4.VTtYOhQrVBvQFu', 'blood_donor', 'John Doe', '+1987654321');

INSERT IGNORE INTO donors (user_id, blood_type, age, weight, eligibility_status) VALUES
((SELECT id FROM users WHERE username='johndoe'), 'O+', 28, 75.5, TRUE);

select * from users;

-- Show users and authentication methods
SELECT user, host, plugin FROM mysql.user WHERE user='root';

-- If using MySQL 8.0, you might need to change authentication
ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY 'Abcd@1234';
FLUSH PRIVILEGES;

UPDATE users SET password_hash = '$2a$10$KHLTZIvpY0g9Ln0oP72v4OOqoAS1ZFMZYKvwhEAZhqjy2VyhyW0tK' WHERE username = 'admin';
UPDATE users SET password_hash = '$2a$10$srl/FprovXwyB00bV9b6a.0woQf.xo221iRXXnbDV0AOuMGobCZ16' WHERE username = 'cityhospital';