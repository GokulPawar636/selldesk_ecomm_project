# selldesk_ecomm_project

🛒 Selldesk – Dockerized Django E-Commerce Application

Selldesk is a full-stack e-commerce web application built using Django (Python) and containerized with Docker.

The project simulates a real-world online shopping platform and demonstrates backend development, user workflows, and deployment using modern DevOps practices.

The application covers the complete shopping lifecycle — from product browsing to order confirmation — and can be run locally using a single Docker command.

🚀 Features
--User authentication & profile management
--Product listing with categories 
--Product search functionality
--Wishlist management
--Shopping cart with quantity updates
--Checkout and order summary
--Address management
--Demo payment flow
--Automated order confirmation email
--Responsive and user-friendly UI

🐳 Dockerized Deployment
--The entire Django application is containerized using Docker to ensure:
--Consistent behavior across environments
--Easy setup without installing Python or Django locally
--Reusable and portable deployment

▶️ Run the Project Using Docker
_#bash_
-- "docker run -p 8000:8000 gokulpawar93/selldesk-ecomm"
_Then open your browser:_
-- "http://localhost:8000"

🛠️ Tech Stack
--Backend: Django (Python 3.12)
--Frontend: HTML, CSS, Bootstrap
--Database: SQLite
--Containerization: Docker
--Version Control: Git & GitHub
--Deployment: Docker Hub

📂 Project Structure (Simplified)
ECOMM/
├── ec_pr/
│   ├── manage.py
│   ├── app/
│   └── ec_pr/
├── requirements.txt
├── Dockerfile
├── .dockerignore
└── README.md

📌 What I Learned
--Designing and structuring a Django e-commerce application
--Implementing real-world shopping workflows
--Writing efficient Dockerfiles
--Debugging Docker container issues
--Deploying applications using Docker Hub
--Understanding backend + DevOps integration

🔗 Links
Docker Hub: https://hub.docker.com/r/gokulpawar93/selldesk-ecomm
