# 🩸 BloodBridge - Optimizing Lifesaving Resources using AWS RDS & EC2

![Python](https://img.shields.io/badge/Python-3.9+-blue)
![Flask](https://img.shields.io/badge/Flask-2.3.3-green)
![AWS](https://img.shields.io/badge/AWS-EC2%20%7C%20RDS-orange)
![MySQL](https://img.shields.io/badge/MySQL-8.0-blue)
![Status](https://img.shields.io/badge/Status-Production%20Ready-success)

BloodBridge is a cloud-based blood management platform that streamlines the complete lifecycle of blood donation, inventory management, emergency request handling, and blood distribution. The system connects hospitals, blood banks, and donors through a centralized web application deployed on AWS infrastructure.

---

## 🌟 Live Demo

**Application URL:** http://16.170.239.117:5000

> The application is hosted on AWS EC2 and connected to an AWS RDS MySQL database for secure and scalable data management.

---

## 📋 Table of Contents

- Project Overview
- Problem Statement
- Proposed Solution
- Key Features
- Technology Stack
- System Architecture
- Database Design
- Installation & Setup
- AWS Deployment
- Repository Structure
- Project Screenshots
- Benefits & Advantages
- Future Scope
- Conclusion
- Developer
- License
- Acknowledgements

---

# 🎯 Project Overview

BloodBridge is an intelligent blood resource management system developed to improve the efficiency of blood donation and distribution processes. The platform provides real-time visibility into blood inventory, enables hospitals to raise emergency requests instantly, and allows blood banks to manage blood stock effectively.

The system eliminates communication delays and manual coordination by providing a centralized platform where hospitals, blood banks, and donors can collaborate seamlessly.

The application is designed using Python Flask and MySQL and is deployed on AWS EC2 with AWS RDS integration, ensuring scalability, reliability, and accessibility.

---

# 🚨 Problem Statement

Healthcare organizations often face significant challenges in managing blood resources efficiently.

### Existing Challenges

- Blood shortages during emergencies
- Lack of centralized communication
- Manual inventory management
- Delayed emergency request processing
- Inefficient donor coordination
- Inadequate tracking of blood availability
- Increased risk of blood wastage

These challenges can lead to delayed treatments and critical healthcare complications.

---

# 💡 Proposed Solution

BloodBridge addresses these challenges through a centralized cloud-based platform that provides:

- Real-time blood inventory monitoring
- Automated emergency request management
- Role-based user access
- Donor registration and scheduling
- Shortage alerts and notifications
- Dashboard analytics and reporting
- Secure cloud-hosted infrastructure

The platform ensures that lifesaving blood resources are delivered efficiently and promptly.

---

# ✨ Key Features

## 🏥 Hospital Administrator Module

- Create emergency blood requests
- Assign request priority levels
- Monitor request status
- Track patient-related requests
- Analyze request history
- Generate operational reports

## 🩸 Donor Management Module

- Donor registration
- Profile management
- Donation scheduling
- Eligibility verification
- Donation history tracking
- Emergency request participation

## 🏦 Blood Bank Management Module

- Real-time inventory management
- Blood stock updates
- Shortage monitoring
- Request fulfillment management
- Donation tracking
- Inventory reporting

## 📊 General System Features

- Role-Based Access Control (RBAC)
- Secure Authentication
- Password Encryption
- Responsive User Interface
- Real-Time Dashboard
- Analytics & Reporting
- Search and Filter Capabilities
- Notification System

---

# 🛠️ Technology Stack

## Backend Technologies

| Technology | Purpose |
|------------|----------|
| Python 3.9+ | Application Development |
| Flask 2.3.3 | Web Framework |
| Flask-SQLAlchemy | ORM |
| Flask-Login | Session Management |
| Flask-Bcrypt | Password Security |
| PyMySQL | Database Connectivity |

## Frontend Technologies

| Technology | Purpose |
|------------|----------|
| HTML5 | Structure |
| CSS3 | Styling |
| Bootstrap 5.3 | Responsive Design |
| JavaScript | Dynamic Functionality |
| Chart.js | Data Visualization |
| Font Awesome | Icons |

## Database

| Technology | Purpose |
|------------|----------|
| MySQL 8.0 | Relational Database |
| AWS RDS | Managed Cloud Database |

## Cloud Infrastructure

| Service | Purpose |
|----------|----------|
| AWS EC2 | Application Hosting |
| AWS RDS | Database Hosting |
| Ubuntu 22.04 | Operating System |
| Gunicorn | WSGI Server |
| Nginx | Reverse Proxy |

---

# 🏗️ System Architecture

```text
Client Browser
       │
       ▼
AWS EC2 Instance
       │
       ▼
Gunicorn Server
       │
       ▼
Flask Application
       │
       ▼
AWS RDS MySQL Database


Workflow
Users access BloodBridge through a web browser.
Requests are handled by the Flask application hosted on AWS EC2.
Business logic is processed using Flask and SQLAlchemy.
Data is stored and retrieved from AWS RDS MySQL.
Results are displayed through dynamic dashboards.

🗄️ Database Design

Table	Purpose
Users	Authentication & Authorization
Donors	Donor Information
Inventory	Blood Stock Management
Emergency_Requests	Request Tracking
Donations	Donation Records
Notifications	Alert Management
📥 Installation & Setup

(Keep your existing installation commands here)

☁️ AWS Deployment

(Keep EC2 and RDS configuration tables here)

📁 Repository Structure
BloodBridge/
├── app.py
├── config.py
├── requirements.txt
├── init_db.sql
├── static/
├── templates/
└── uploads/

```
--- 
📸 Project Screenshots
<img width="1920" height="1080" alt="Screenshot 2026-06-03 154517" src="https://github.com/user-attachments/assets/fdb77770-7855-4b19-99ca-b80c692cc1f6" />
<img width="1920" height="1080" alt="Screenshot 2026-06-03 154643" src="https://github.com/user-attachments/assets/ecccbbed-345f-4a66-8d42-2155d3b1c4c1" />

---
## 🎁 Benefits & Advantages

- Hospitals Faster emergency response
- Better patient management
- Centralized request tracking
- Blood Banks
- Improved inventory visibility
- Reduced blood wastage
- Efficient request fulfillment
- Donors Easy donation scheduling
- Donation impact tracking
- Faster emergency participation
- High Availability
---

## 🔮 Future Scope
Phase 2
Mobile Application
AI Demand Prediction
Geolocation Services
Online Payments
Phase 3
Blockchain Integration
Multi-Hospital Networks
Advanced Analytics
Smart Blood Matching
Phase 4
National Blood Grid
Ambulance Integration
SMS & Email Alerts
Government Health Integration

--- 

## 📝 Conclusion

BloodBridge demonstrates how cloud computing and modern web technologies can transform blood resource management. By integrating hospitals, donors, and blood banks into a unified ecosystem, the platform significantly improves response times, operational efficiency, and blood availability during emergencies.

The solution is scalable, secure, and production-ready, making it suitable for deployment across healthcare organizations and blood donation networks.

---

### 👨‍💻 Developer
Siddhesh Patil

Full Stack Developer | Cloud Enthusiast | AWS Practitioner

Python Flask Development
AWS EC2 & RDS Deployment
Database Design
RESTful Applications
Cloud Infrastructure

---
