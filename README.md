# LibraLink

LibraLink is an advanced library management system built with Django 5.1.1 and Django REST Framework. It provides a RESTful API for managing books and authors, includes user authentication, search functionality, and a recommendation system.

## Features

- RESTful API for books and authors
- User authentication using JWT
- Search functionality for books and authors
- Recommendation system based on user favorites
- PostgreSQL database for efficient data storage and retrieval

## Installation

1. Clone the repository
2. Install dependencies: `pip install -r requirements.txt`
3. Set up PostgreSQL database
4. Run migrations: `python manage.py migrate`
5. Start the server: `python manage.py runserver`

## API Endpoints

- Books: CRUD operations at /api/books/
- Authors: CRUD operations at /api/authors/
- Users: Registration and authentication
- Favorites: Manage user's favorite books
- Recommendations: Get personalized book recommendations
