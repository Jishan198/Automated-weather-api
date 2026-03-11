# Automated Weather Data API (SaaS Backend)


## Overview
This project is an automated **Data-as-a-Service (DaaS)** platform built with Python and Django. It features a high-performance architecture designed to handle real-time data aggregation, secure delivery, and automated monetization.

As a backend engineering showcase, this system demonstrates a production-ready environment using **asynchronous task queues** to decouple heavy operations from the request-response cycle and **memory-level caching** to optimize read performance.

---

## System Architecture
This project utilizes a decoupled, enterprise-grade architecture to ensure fast read times and non-blocking write operations:

| Component | Technology |
| :--- | :--- |
| **Backend Framework** | Django REST Framework (DRF) |
| **Authentication** | JWT (JSON Web Tokens) |
| **Caching Layer** | **Redis** (Protects MySQL from heavy read traffic) |
| **Task Queue** | **Celery** (Handles background jobs asynchronously) |
| **Message Broker** | Redis |
| **Payment Gateway** | Stripe Webhooks |
| **Database** | MySQL |



---

## Core Features
* **Automated ETL Pipeline**: Custom Django management commands handle automated data ingestion, transformation, and database synchronization.
* **High-Speed Caching**: Integrated **Redis** caching layer to reduce database load and provide lightning-fast responses for frequently accessed weather data.
* **Asynchronous Background Tasks**: Utilizes **Celery** to handle time-intensive operations (like sending welcome emails and account upgrades) in the background.
* **Identity & Security**: Robust security implementation using **JSON Web Tokens (JWT)** for stateless authentication.
* **Access Control & Paywall**: Tiered rate limiting (**Throttling**) that distinguishes between Free and Premium tiers.
* **Monetization Engine**: Full **Stripe Checkout** integration with a secure **Webhook listener** for automated account upgrades.
* **Interactive Documentation**: Automated OpenAPI schema generation via **drf-spectacular** for professional Swagger UI testing.

---

## Local Setup Instructions

1.  **Clone the repository.**
2.  **Install dependencies**:  
    `pip install -r requirements.txt`
3.  **Environment Config**:  
    Configure your `.env` file with MySQL credentials, Redis URL, Django Secret Key, and Stripe API Keys.
4.  **Database Setup**:
    * Run migrations: `python manage.py migrate`
    * Fetch initial data: `python manage.py fetch_weather`
5.  **Start Services (Requires 3 Terminals)**:
    * **Terminal 1 (Django)**: `python manage.py runserver`
    * **Terminal 2 (Celery)**: `celery -A data_dashboard worker -l info --pool=solo`
    * **Terminal 3 (Stripe)**: `stripe listen --forward-to localhost:8000/api/webhook/`

---
**Author: Jishan Mohammed**