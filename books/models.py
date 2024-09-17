from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.postgres.search import SearchVectorField
from django.contrib.postgres.indexes import GinIndex
User = get_user_model()

class Author(models.Model):
    name = models.CharField(max_length=200, db_index=True)
    goodreads_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    role = models.CharField(max_length=100, blank=True)
    ratings_count = models.IntegerField(default=0)
    average_rating = models.FloatField(default=0.0)
    text_reviews_count = models.IntegerField(default=0)
    works_count = models.IntegerField(default=0)
    gender = models.CharField(max_length=20, blank=True)
    image_url = models.URLField(max_length=500, blank=True)
    fans_count = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Work(models.Model):
    work_id = models.CharField(max_length=20, unique=True)
    title = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Book(models.Model):
    title = models.CharField(max_length=255)
    authors = models.ManyToManyField(Author, related_name='books')
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True, related_name='books')
    isbn = models.CharField(max_length=13, unique=True)
    isbn13 = models.CharField(max_length=13, unique=True)
    asin = models.CharField(max_length=10, blank=True)
    language = models.CharField(max_length=3)
    average_rating = models.FloatField(default=0.0)
    rating_dist = models.CharField(max_length=100)
    ratings_count = models.IntegerField(default=0)
    text_reviews_count = models.IntegerField(default=0)
    publication_date = models.DateField()
    original_publication_date = models.DateField(null=True, blank=True)
    format = models.CharField(max_length=50)
    edition_information = models.CharField(max_length=255, blank=True)
    image_url = models.URLField(max_length=500)
    publisher = models.CharField(max_length=255)
    num_pages = models.IntegerField()
    series_id = models.CharField(max_length=20, blank=True)
    series_name = models.CharField(max_length=255, blank=True)
    series_position = models.CharField(max_length=10, blank=True)
    description = models.TextField()
    search_vector = SearchVectorField(null=True)

    class Meta:
        indexes = [
            GinIndex(fields=['search_vector'])
        ]

    def __str__(self):
        return self.title

class Shelf(models.Model):
    name = models.CharField(max_length=100)
    count = models.IntegerField(default=0)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='shelves')

    class Meta:
        unique_together = ('name', 'book')

    def __str__(self):
        return f"{self.name} - {self.book.title}"
    

class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'book')

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"