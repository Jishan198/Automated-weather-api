# Automated Weather Data API (SaaS Backend)

## Overview
This project is an automated Data-as-a-Service (DaaS) platform built with Python and Django. It extracts daily climate data from third-party sources, transforms it, and serves it through a secured RESTful API. 

Designed as a backend engineering portfolio piece, this system demonstrates production-ready architecture, including an automated ETL pipeline, JWT authentication, tiered rate limiting, and a payment gateway integration.

## Core Features
* **Automated ETL Pipeline:** A custom Django management command handles data ingestion and database updates automatically.
* **Identity & Security:** Secures endpoints using JSON Web Tokens (JWT) for robust user authentication.
* **Access Control & Paywall:** Implements custom Django REST Framework throttling to restrict Free users while granting unlimited access to Premium users.
* **Monetization Engine:** Integrates Stripe Checkout for processing payments and a Stripe Webhook listener for automated account upgrades.
* **Interactive Documentation:** Utilizes Swagger (OpenAPI) for live endpoint testing and developer onboarding.

## Tech Stack
* **Language:** Python 3
* **Framework:** Django, Django REST Framework (DRF)
* **Database:** MySQL
* **Security & Payments:** djangorestframework-simplejwt, Stripe API
* **Tools:** Pandas, Requests, drf-spectacular

## Local Setup Instructions
1. Clone the repository.
2. Create a virtual environment and install dependencies: `pip install -r requirements.txt`
3. Configure your `.env` file with your MySQL credentials, Django Secret Key, and Stripe API Keys.
4. Run migrations: `python manage.py migrate`
5. Fetch initial data: `python manage.py fetch_weather`
6. Create an admin user: `python manage.py createsuperuser`
7. Start the server: `python manage.py runserver`

**Author:** Jishan Mohammed

