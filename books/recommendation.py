# books/recommendations.py

from django.db.models import Count
from .models import Book, Favorite
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

def get_book_recommendations(user, num_recommendations=5):
    user_favorites = Favorite.objects.filter(user=user).select_related('book')
    
    if not user_favorites:
        # If the user has no favorites, return popular books
        return Book.objects.annotate(favorite_count=Count('favorite')).order_by('-favorite_count')[:num_recommendations]
    
    # Get all books that are not in the user's favorites
    all_books = Book.objects.exclude(id__in=user_favorites.values_list('book__id', flat=True))
    
    # Prepare data for TF-IDF
    favorite_books = [f.book for f in user_favorites]
    all_book_texts = [f"{book.title} {book.author.name} {book.description}" for book in favorite_books + list(all_books)]
    
    # Create TF-IDF matrix
    vectorizer = TfidfVectorizer(stop_words='english')
    tfidf_matrix = vectorizer.fit_transform(all_book_texts)
    
    # Calculate similarity between user's favorites and all other books
    user_profile = tfidf_matrix[:len(favorite_books)].mean(axis=0)
    cosine_similarities = cosine_similarity(user_profile, tfidf_matrix[len(favorite_books):])
    
    # Get top similar books
    similar_indices = cosine_similarities.argsort()[0][-num_recommendations:][::-1]
    recommended_books = [all_books[i] for i in similar_indices]
    
    return recommended_books