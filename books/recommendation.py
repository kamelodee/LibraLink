# recommendation.py

from django.db.models import Count, Q
from .models import Book, Favorite

def get_book_recommendations(favorite_book_ids, num_recommendations=5):
    # If no favorites, return most popular books
    if not favorite_book_ids:
        return Book.objects.annotate(favorite_count=Count('favorite')).order_by('-favorite_count')[:num_recommendations]

    # Find users who have favorited the same books
    similar_users = Favorite.objects.filter(book_id__in=favorite_book_ids).values_list('user_id', flat=True)

    # Get books favorited by similar users, excluding the user's already favorited books
    recommended_books = Book.objects.filter(favorite__user_id__in=similar_users).exclude(id__in=favorite_book_ids).annotate(
        recommendation_score=Count('id')
    ).order_by('-recommendation_score')

    # If we don't have enough recommendations, add popular books
    if recommended_books.count() < num_recommendations:
        popular_books = Book.objects.annotate(favorite_count=Count('favorite')).exclude(
            Q(id__in=favorite_book_ids) | Q(id__in=recommended_books.values_list('id', flat=True))
        ).order_by('-favorite_count')
        
        recommended_books = list(recommended_books) + list(popular_books)

    # Ensure we only return the requested number of recommendations
    return recommended_books[:num_recommendations]