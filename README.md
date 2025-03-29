# URL Shortener Service

A minimal URL shortening service built with Django and MongoDB.

## Features
- Create, retrieve, update, and delete short URLs.
- Redirect to original URLs  using short codes.
- Track access statistics for each short URL.
- Minimal frontend for user interaction.

## Tech Stack
- **Backend:** Django
- **Database:** MongoDB (via Djongo)
- **Frontend:** HTML & JavaScript

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/muhammadinzamamamjad/inzamam-innovaxel-amjad
   
2.Create and activate a virtual environment:
  python -m venv venv
  source venv/bin/activate    # On Windows: venv\Scripts\activate

3. pip install -r requirements.txt
4. Run MongoDB server (make sure it's running on localhost:27017).
5. Apply migrations:
  python manage.py makemigrations
  python manage.py migrate
6. Run the development server:
  python manage.py runserver

# Usage
  Access the frontend at: http://127.0.0.1:8000/static/index.html
  Interact with the APIs using the frontend.
