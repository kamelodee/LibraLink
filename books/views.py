# views.py

from rest_framework import viewsets, mixins, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import action
from rest_framework.response import Response
from django.db.models import Q
from django.contrib.postgres.search import SearchQuery, SearchRank, SearchVector
from drf_spectacular.utils import extend_schema, OpenApiParameter
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from .models import Author, Book, Favorite, Work, Shelf
from .serializers import AuthorSerializer, BookSerializer, FavoriteSerializer, WorkSerializer, ShelfSerializer
from .recommendation import get_book_recommendations

class CustomMixin(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  mixins.UpdateModelMixin,   # Provides PUT
                  mixins.DestroyModelMixin,
                  mixins.ListModelMixin):
    """
    Custom mixin that includes all ModelViewSet mixins except PartialUpdateModelMixin.
    This excludes the PATCH method.
    """
    pass

class AuthorViewSet(CustomMixin, viewsets.GenericViewSet):
    queryset = Author.objects.all()
    serializer_class = AuthorSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']  # Excludes PATCH

    @extend_schema(description="List all authors")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Create a new author")
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    @extend_schema(description="Retrieve details of a specific author")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Update an author's information")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(description="Delete an author")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

class BookViewSet(CustomMixin, viewsets.GenericViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']  # Excludes PATCH

    @extend_schema(description="List all books")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Create a new book")
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    @extend_schema(description="Retrieve details of a specific book")
    def retrieve(self, request, *args, **kwargs):
        return super().retrieve(request, *args, **kwargs)

    @extend_schema(description="Update a book's information")
    def update(self, request, *args, **kwargs):
        return super().update(request, *args, **kwargs)

    @extend_schema(description="Delete a book")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(
        description="Search for books by title, author name, or description",
        parameters=[
            OpenApiParameter(name="q", description="Search query", required=True, type=str),
        ]
    )
    @action(detail=False, methods=['get'])
    def search(self, request):
        query = request.query_params.get('q', '')
        if not query:
            return Response({"error": "Please provide a search query."}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Try vector search first
            search_query = SearchQuery(query)
            vector_results = Book.objects.annotate(
                search=SearchVector('title', 'description', 'authors__name'),
                rank=SearchRank(SearchVector('title', 'description', 'authors__name'), search_query)
            ).filter(search=search_query).order_by('-rank')

            # If vector search returns results, use them
            if vector_results.exists():
                results = vector_results
            else:
                # Fallback to basic field search
                results = Book.objects.filter(
                    Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(authors__name__icontains=query) |
                    Q(isbn__icontains=query) |
                    Q(isbn13__icontains=query)
                ).distinct()

            serializer = self.get_serializer(results, many=True)
            return Response(serializer.data)

        except Exception as e:
            # Log the error for debugging
            print(f"Search error: {str(e)}")
            return Response({"error": "An error occurred during search."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class WorkViewSet(CustomMixin, viewsets.GenericViewSet):
    queryset = Work.objects.all()
    serializer_class = WorkSerializer
    permission_classes = [IsAuthenticated]

class ShelfViewSet(CustomMixin, viewsets.GenericViewSet):
    queryset = Shelf.objects.all()
    serializer_class = ShelfSerializer
    permission_classes = [IsAuthenticated]

class FavoriteViewSet(CustomMixin, viewsets.GenericViewSet):
    serializer_class = FavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Favorite.objects.filter(user=self.request.user)

    @extend_schema(description="List user's favorite books")
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)

    @extend_schema(description="Add a book to user's favorites")
    def create(self, request, *args, **kwargs):
        book_id = request.data.get('book')
        if not book_id:
            return Response({"error": "Book ID is required"}, status=status.HTTP_400_BAD_REQUEST)

        if Favorite.objects.filter(user=request.user).count() >= 20:
            return Response({"error": "Maximum number of favorites reached"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            book = Book.objects.get(id=book_id)
        except Book.DoesNotExist:
            return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

        favorite, created = Favorite.objects.get_or_create(user=request.user, book=book)
        if not created:
            return Response({"error": "Book already in favorites"}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(favorite)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    @extend_schema(description="Remove a book from user's favorites")
    def destroy(self, request, *args, **kwargs):
        return super().destroy(request, *args, **kwargs)

    @extend_schema(description="Get personalized book recommendations based on user's favorites")
    @method_decorator(cache_page(60))  # Cache for 1 minute
    @action(detail=False, methods=['get'])
    def recommendations(self, request):
        favorites = self.get_queryset().values_list('book', flat=True)
        if not favorites:
            return Response({"error": "No favorites found"}, status=status.HTTP_400_BAD_REQUEST)

        recommended_books = get_book_recommendations(favorites)
        serializer = BookSerializer(recommended_books, many=True)
        return Response(serializer.data)