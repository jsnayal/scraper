# FastAPI Scraper Project

## Overview
This project is a FastAPI application designed to scrape product data from a website. It includes features for caching scraped products using Caching strategy such as redis, persisting data to a database using different database strategy such as JSON file, and notifying subscribers via different notification methods

## Installation
Prerequisites
Ensure you have the following installed:

Python 3.7 or higher

pip (Python package installer)

## Steps to run project

1. Clone the Repository

2. Create Virtual environment. We used pyenv and virtualenv

3. Install dependencies 
pip install -r requirements.txt

4. If using redis, you must have a running redis instance. We have used a docker image running locally.

4. Run the application
uvicorn main:app --reload

## API Endpoints
### /scrape
Method: POST

Request Body: JSON object with scraping settings (e.g., page limit, proxy).

Response: A message indicating the scraping status and completion notification.

### /register_recipient
Method: POST

Description: Registers a new recipient for notifications.

Request Body: JSON object with recipient details (name, email, phone).

Response: A message confirming subscription
