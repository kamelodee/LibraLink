# books/admin.py

from django.contrib import admin
from .models import Author, Book, Work, Shelf, Favorite

@admin.register(Author)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('name', 'goodreads_id', 'average_rating', 'ratings_count', 'works_count')
    search_fields = ('name', 'goodreads_id')
    list_filter = ('gender',)
    ordering = ('name',)

@admin.register(Work)
class WorkAdmin(admin.ModelAdmin):
    list_display = ('work_id', 'title')
    search_fields = ('work_id', 'title')

class ShelfInline(admin.TabularInline):
    model = Shelf
    extra = 1

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'isbn', 'average_rating', 'ratings_count', 'publication_date')
    search_fields = ('title', 'isbn', 'isbn13', 'authors__name')
    list_filter = ('language', 'publication_date')
    date_hierarchy = 'publication_date'
    filter_horizontal = ('authors',)
    inlines = [ShelfInline]
    readonly_fields = ('ratings_count', 'text_reviews_count')

    fieldsets = (
        (None, {
            'fields': ('title', 'authors', 'work', 'description')
        }),
        ('Publication Info', {
            'fields': ('isbn', 'isbn13', 'asin', 'publication_date', 'original_publication_date', 'publisher', 'language')
        }),
        ('Book Details', {
            'fields': ('format', 'edition_information', 'num_pages', 'image_url')
        }),
        ('Series Info', {
            'fields': ('series_id', 'series_name', 'series_position'),
            'classes': ('collapse',)
        }),
        ('Ratings', {
            'fields': ('average_rating', 'ratings_count', 'text_reviews_count', 'rating_dist'),
            'classes': ('collapse',)
        }),
    )

@admin.register(Shelf)
class ShelfAdmin(admin.ModelAdmin):
    list_display = ('name', 'book', 'count')
    search_fields = ('name', 'book__title')
    list_filter = ('name',)

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'created_at')
    search_fields = ('user__username', 'book__title')
    list_filter = ('created_at',)
    date_hierarchy = 'created_at'

# Optionally, you can customize the admin site
admin.site.site_header = "LibraLink Administration"
admin.site.site_title = "LibraLink Admin Portal"
admin.site.index_title = "Welcome to LibraLink Admin Portal"