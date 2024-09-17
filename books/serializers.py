from rest_framework import serializers
from .models import Author, Book, Favorite, Work, Shelf

class AuthorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Author
        fields = ['id', 'name', 'goodreads_id', 'role', 'ratings_count', 'average_rating', 
                  'text_reviews_count', 'works_count', 'gender', 'image_url', 'fans_count']

class ShelfSerializer(serializers.ModelSerializer):
    class Meta:
        model = Shelf
        fields = ['name', 'count']

class WorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Work
        fields = ['work_id', 'title']

class BookSerializer(serializers.ModelSerializer):
    authors = AuthorSerializer(many=True, read_only=True)
    shelves = ShelfSerializer(many=True, read_only=True)
    work = WorkSerializer(read_only=True)

    class Meta:
        model = Book
        fields = ['id', 'title', 'authors', 'work', 'isbn', 'isbn13', 'asin', 'language',
                  'average_rating', 'rating_dist', 'ratings_count', 'text_reviews_count',
                  'publication_date', 'original_publication_date', 'format',
                  'edition_information', 'image_url', 'publisher', 'num_pages',
                  'series_id', 'series_name', 'series_position', 'description', 'shelves']

    def create(self, validated_data):
        authors_data = self.context['request'].data.get('authors', [])
        shelves_data = self.context['request'].data.get('shelves', [])
        work_data = self.context['request'].data.get('work', {})

        book = Book.objects.create(**validated_data)

        for author_data in authors_data:
            author, _ = Author.objects.get_or_create(
                goodreads_id=author_data.get('id'),
                defaults={'name': author_data['name'], 'role': author_data.get('role', '')}
            )
            book.authors.add(author)

        if work_data:
            work, _ = Work.objects.get_or_create(
                work_id=work_data['work_id'], 
                defaults={'title': work_data.get('title', book.title)}
            )
            book.work = work
            book.save()

        for shelf_data in shelves_data:
            Shelf.objects.create(book=book, **shelf_data)

        return book
    
class FavoriteSerializer(serializers.ModelSerializer):
    book = BookSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'book', 'created_at']
        read_only_fields = ['user']    