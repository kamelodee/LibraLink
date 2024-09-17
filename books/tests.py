from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from .models import Author, Book, Favorite

User = get_user_model()

class BookAPITestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username='testuser', password='testpass123')
        self.client.force_authenticate(user=self.user)
        
        self.author = Author.objects.create(name='Test Author', bio='Test Bio')
        self.book = Book.objects.create(
            title='Test Book',
            author=self.author,
            isbn='1234567890123',
            publication_date='2023-01-01',
            description='Test Description'
        )

    def test_list_books(self):
        response = self.client.get('/api/books/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 1)

    def test_create_book(self):
        data = {
            'title': 'New Book',
            'author_id': self.author.id,
            'isbn': '9876543210987',
            'publication_date': '2023-02-01',
            'description': 'New Description'
        }
        response = self.client.post('/api/books/', data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_favorite_book(self):
        response = self.client.post(f'/api/favorites/', {'book': self.book.id})
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_get_recommendations(self):
        Favorite.objects.create(user=self.user, book=self.book)
        response = self.client.get('/api/favorites/recommendations/')
        self.assertEqual(response.status_code, status.HTTP_200_OK)