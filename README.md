# Project Nexus: ProDev Backend Engineering Documentation

Welcome to **Project Nexus**, a documentation hub that captures my learning journey through the **ProDev Backend Engineering** program. This repository showcases the skills, tools, and backend engineering principles I have acquired and applied across multiple weeks of hands-on learning.

---

## 🚀 Program Overview

The **ProDev Backend Engineering Program** is an intensive, project-based learning track aimed at equipping learners with modern backend development skills. Over 12 weeks, I explored foundational to advanced backend technologies, practiced industry-standard workflows, and built real-world backend services.

---

## 🧠 Major Learnings

### 🔧 Key Technologies Covered

- **Python**: Core language used throughout, including advanced features like decorators, context managers, and asynchronous programming.
- **Django**: Main framework for building RESTful APIs, handling database interactions, middlewares, signals, and advanced ORM.
- **Django REST Framework (DRF)**: Used to create robust, secure, and well-documented APIs.
- **GraphQL**: Integrated with Django for flexible API querying and mutation.
- **Docker**: Used for containerizing applications and environments.
- **Kubernetes**: Introduced for orchestration of Docker containers.
- **CI/CD**: Implemented Continuous Integration and Deployment using **Jenkins** and **GitHub Actions**.
- **Redis**: Utilized for caching and performance improvements.
- **Celery & Celery Beat**: Scheduled tasks, background jobs, and asynchronous processing.
- **Datadog, NewRelic, UptimeRobot, Nagios, WaveFront**: For application performance monitoring and alerting.

---

### 🧱 Backend Concepts Mastered

- **Database Design & Modeling**: Created normalized schemas, ERDs, seeders, and optimized SQL queries.
- **Asynchronous Programming**: Utilized `asyncio`, asynchronous views, and task queues (Celery).
- **Caching Strategies**: Implemented caching layers using Redis; learned cache invalidation and hit-ratio monitoring.
- **Authentication & Authorization**: Built secure login systems with JWT, session-based and token-based auth.
- **Middleware Logic**: Created custom middleware for request filtering, time-based restrictions, logging, and offensive language detection.
- **API Security**: Applied rate limiting, IP tracking, blacklisting, HTTPS with SSL Termination, and user activity logging.
- **Event-Driven Architecture**: Used Django Signals to trigger workflows like notifications and cleanup.
- **Testing**: Wrote unit tests, integration tests with `pytest`, and applied TDD principles.
- **Shell Scripting**: Automated deployment, server setup, and debugging tasks using Bash.
- **Container Orchestration**: Deployed apps on Kubernetes using Minikube, Ingress, blue-green deployments, and rolling updates.
- **Monitoring and Logging**: Integrated tools like Datadog and NewRelic for observability.
- **CI/CD Pipelines**: Automated builds, tests, Docker image creation and deployment through Jenkins and GitHub Actions.

---

## 🔄 Weekly Breakdown

### Week 0: Getting Started
- Created a Vision Board and learning roadmap for the journey.

### Week 1: Foundations
- Mastered effective AI prompting and personal brand revamp.
- Learned database design principles and documentation best practices.

### Week 2: SQL & Django Setup
- Advanced SQL queries, indexing, optimization.
- Django setup: environment variables, Swagger integration.

### Week 3: Advanced Python
- Python decorators, context managers, and asynchronous patterns.

### Week 4: Testing & DRF
- Built testable APIs using DRF.
- Implemented models, serializers, and seeders.

### Week 5: Auth & Middleware
- Handled JWT-based authentication and developed custom middleware logic.

### Week 6: ORM and Signals
- Used signals for automation and advanced ORM for complex data queries.

### Week 7: DevOps Basics
- Learned advanced shell scripting, Git workflows, Docker, and web infrastructure concepts.

### Week 8: Container Orchestration & APIs
- Introduction to Kubernetes.
- Explored GraphQL and integrated Chapa payment gateway.

### Week 9: CI/CD & Scaling
- Set up Jenkins and GitHub Actions.
- Web server configuration, load balancing, and firewall rules.

### Week 10: Security & Caching
- SSL Termination with HAProxy.
- Redis caching, background jobs with Celery and crontab.

### Week 11: Deployment & Monitoring
- IP tracking, server monitoring with multiple tools.
- Final project deployment and API documentation.

### Week 12: Capstone Project - Online Poll System
- Documented learning journey so far in my README.md file

### Week 13: Capstone Project - Online Poll System
#### ✅ Day 1–2: Setup & Models
- Bootstrapped a Django project for the online poll system.
- Set up project structure and version control (`.gitignore`, `.env`).
- Created database models: `User`, `Poll`, `Question`, `Choice`, and `Vote`.
- Registered models with the Django admin site.
- Applied initial migrations and verified model relationships.
- Secured secrets using `django-environ` and environment variables.

#### ✅ Day 3: Poll Management API
- Created DRF views for `Poll`, `Question`, and `Choice` models.
- Implemented endpoints for poll creation, listing, and detail view.
- Added functionality to create questions for polls and choices for questions.
- Ensured expired polls cannot be created (expiry validation).
- Responses include nested questions and choices for better client consumption.
- Tested all endpoints with Postman using token-based authentication.

#### ✅ Day 4: Voting Logic and Tests
- Added voting functionality to allow users to vote on poll choices.
- Implemented validation to prevent duplicate votes from the same IP or session.
- Integrated the voting route into the API.
- Wrote unit tests to cover vote submissions, duplicate prevention, and expired polls.
- Confirmed all tests pass with `python manage.py test`.

#### ✅ Day 5: Results & Admin Enhancements
- Built real-time poll result aggregation using Django ORM annotations.
- Enhanced the Django Admin with vote statistics per poll and question.
- Admins can now:
    1. View total votes per poll and per question.
    2. Sort and filter questions based on total vote counts.
    3. Download poll results as CSV with total votes and percentage breakdowns.
- Ensured proper formatting and UX on the Admin interface for managing results.

#### ✅ Day 6: Swagger API Documentation

- Installed and configured `drf-yasg` for interactive API documentation.
- Enabled public access to Swagger UI at `/api/docs/` without login.
- Annotated API views and viewsets with detailed descriptions and example payloads using `@swagger_auto_schema`.
- Documented all input/output fields and expected responses.
---

## 🧩 Challenges Faced & Solutions Implemented

| Challenge | Solution |
|----------|----------|
| Setting up environment variables across Docker and Django | Used `django-environ` and `.env` files to manage secrets |
| Handling slow API responses | Implemented Redis caching and optimized querysets |
| Managing background tasks | Integrated Celery and Celery Beat with RabbitMQ |
| Coordinating Docker and PostgreSQL on local machine | Created Docker Compose setup for all services |
| CI/CD failures during builds | Debugged Dockerfile, added test stage to Jenkins pipeline |
| Load balancer not distributing traffic evenly | Reviewed HAProxy config and health checks |
| Monitoring setup complexity | Used Datadog agents and simplified logging strategies |

---

## 💡 Best Practices & Takeaways

- **Test Early, Test Often**: Testing isn't an afterthought; start with `pytest` from the beginning.
- **Write Reusable Code**: Use Python decorators and DRF ViewSets for clean, DRY code.
- **Document Everything**: Swagger, README.md, and comments aid collaboration.
- **Secure by Default**: Use HTTPS, sanitize inputs, restrict access.
- **Observe & Monitor**: Logs and metrics matter more than you think—integrate APMs early.
- **Automate Repetitive Tasks**: Use Bash scripts, cron jobs, and Celery workers.
- **Keep Learning**: The backend world evolves—keep refining your toolkit.

---

