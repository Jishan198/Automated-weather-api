#Automated Weather Data API (SaaS Backend):- 


##Overview:-
This project is an automated Data-as-a-Service (DaaS) platform built with Python and Django. It features a high-performance architecture designed to handle real-time data aggregation, secure delivery, and automated monetization.

As a backend engineering showcase, this system demonstrates a production-ready environment using asynchronous task queues to decouple heavy operations from the request-response cycle, and memory-level caching to optimize read performance.

## System Architecture
This project utilizes a decoupled, enterprise-grade architecture to ensure fast read times and non-blocking write operations:
* **Backend Framework:** Django REST Framework (DRF)
* **Authentication:** JWT (JSON Web Tokens)
* **Caching Layer:** Redis (Protects the database from heavy read traffic)
* **Asynchronous Task Queue:** Celery (Handles background jobs like sending emails and database upgrades without freezing the web server)
* **Monetization/Payment Gateway:** Stripe Webhooks
* **Database:** MySQL

##Core Features
* **Automated ETL Pipeline**: Custom Django management commands handle automated data ingestion, transformation, and database synchronization.

* **High-Speed Caching**: Integrated Redis caching layer to reduce database load and provide lightning-fast responses for frequently accessed weather data.

* **Asynchronous Background Tasks**: Utilizes Celery and Redis to handle time-intensive operations (like sending welcome emails and processing account upgrades) in the background, ensuring zero-latency for the end user.

* **Identity & Security**: Robust security implementation using JSON Web Tokens (JWT) for stateless authentication.

* **Access Control & Paywall**: Tiered rate limiting (Throttling) that distinguishes between Free and Premium tiers, enforced via custom DRF permission classes.

* **Monetization Engine**: Full Stripe Checkout integration with a secure Webhook listener to automate the user-to-premium conversion flow.

* **Interactive Documentation**: Automated OpenAPI schema generation via drf-spectacular for a professional Swagger UI testing environment.

##Local Setup Instructions
* **Clone the repository.**

* **Install dependencies**: pip install -r requirements.txt

* **Environment Config**: Configure your .env file with MySQL credentials, Redis URL, Django Secret Key, and Stripe API Keys.

* **Database Setup**: * Run migrations: python manage.py migrate

* **Fetch initial data**: python manage.py fetch_weather

* **Start Services (Requires 3 Terminals)**:

* **Django Server**: python manage.py runserver

* **Celery Worker**: celery -A data_dashboard worker -l info --pool=solo

* **Stripe Tunnel**: stripe listen --forward-to localhost:8000/api/webhook/

* **Access Dashboard**: Open http://127.0.0.1:8000/ to view the authenticated frontend.

**----------------------Author: Jishan Mohammed-------------------------------**

