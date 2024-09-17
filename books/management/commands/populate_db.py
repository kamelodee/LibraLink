# books/management/commands/populate_db.py

from django.core.management.base import BaseCommand
from books.models import Author, Book, Work, Shelf
from django.utils.dateparse import parse_date

class Command(BaseCommand):
    help = 'Populate the database with sample authors and books'

    def handle(self, *args, **kwargs):
        # Sample data (authors_data and books_data remain the same)
        authors_data = [
    {
        "goodreads_id": "1077326",
        "name": "J.K. Rowling",
        "role": "Author",
        "average_rating": 4.46,
        "ratings_count": 29750052,
        "text_reviews_count": 190684,
        "works_count": 237,
        "gender": "female",
        "image_url": "https://images.gr-assets.com/authors/1596216614p5/1077326.jpg",
        "fans_count": 178927
    },
    {
        "goodreads_id": "1265",
        "name": "George R.R. Martin",
        "role": "Author",
        "average_rating": 4.15,
        "ratings_count": 9457980,
        "text_reviews_count": 176366,
        "works_count": 391,
        "gender": "male",
        "image_url": "https://images.gr-assets.com/authors/1351944410p5/346732.jpg",
        "fans_count": 118125
    },
    {
        "goodreads_id": "3389",
        "name": "Stephen King",
        "role": "Author",
        "average_rating": 3.98,
        "ratings_count": 21050245,
        "text_reviews_count": 658405,
        "works_count": 1024,
        "gender": "male",
        "image_url": "https://images.gr-assets.com/authors/1362814142p5/3389.jpg",
        "fans_count": 162819
    },
    {
        "goodreads_id": "1825",
        "name": "Jane Austen",
        "role": "Author",
        "average_rating": 4.13,
        "ratings_count": 8354861,
        "text_reviews_count": 136674,
        "works_count": 60,
        "gender": "female",
        "image_url": "https://images.gr-assets.com/authors/1616803034p5/1265.jpg",
        "fans_count": 40589
    },
    {
        "goodreads_id": "7128",
        "name": "Neil Gaiman",
        "role": "Author",
        "average_rating": 4.12,
        "ratings_count": 7076600,
        "text_reviews_count": 286903,
        "works_count": 759,
        "gender": "male",
        "image_url": "https://images.gr-assets.com/authors/1234150163p5/1221698.jpg",
        "fans_count": 137324
    },
    {
        "goodreads_id": "9810",
        "name": "Agatha Christie",
        "role": "Author",
        "average_rating": 4.15,
        "ratings_count": 6359455,
        "text_reviews_count": 187821,
        "works_count": 914,
        "gender": "female",
        "image_url": "https://images.gr-assets.com/authors/1321738793p5/123715.jpg",
        "fans_count": 34619
    },
    {
        "goodreads_id": "11494",
        "name": "Margaret Atwood",
        "role": "Author",
        "average_rating": 3.95,
        "ratings_count": 3405790,
        "text_reviews_count": 213621,
        "works_count": 475,
        "gender": "female",
        "image_url": "https://images.gr-assets.com/authors/1582881190p5/3472.jpg",
        "fans_count": 22367
    },
    {
        "goodreads_id": "1069006",
        "name": "Suzanne Collins",
        "role": "Author",
        "average_rating": 4.11,
        "ratings_count": 22542435,
        "text_reviews_count": 468405,
        "works_count": 40,
        "gender": "female",
        "image_url": "https://images.gr-assets.com/authors/1630199330p5/1069006.jpg",
        "fans_count": 100781
    },
    {
        "goodreads_id": "4339",
        "name": "Dan Brown",
        "role": "Author",
        "average_rating": 3.77,
        "ratings_count": 8602910,
        "text_reviews_count": 176431,
        "works_count": 44,
        "gender": "male",
        "image_url": "https://images.gr-assets.com/authors/1367229786p5/630.jpg",
        "fans_count": 16071
    },
    {
        "goodreads_id": "1303",
        "name": "Haruki Murakami",
        "role": "Author",
        "average_rating": 4.08,
        "ratings_count": 3820041,
        "text_reviews_count": 235437,
        "works_count": 241,
        "gender": "male",
        "image_url": "https://images.gr-assets.com/authors/1350236259p5/3354.jpg",
        "fans_count": 61305
    }
]
        books_data = [
    # ... (previous 14 books)
    {
        "goodreads_id": "13642",
        "title": "Good Omens: The Nice and Accurate Prophecies of Agnes Nutter, Witch",
        "author_id": "7128",  # Neil Gaiman (co-authored with Terry Pratchett)
        "work_id": "1970248",
        "isbn": "0060853980",
        "isbn13": "9780060853983",
        "language": "eng",
        "average_rating": 4.24,
        "ratings_count": 620183,
        "text_reviews_count": 28850,
        "publication_date": "1990-05-01",
        "format": "Mass Market Paperback",
        "publisher": "HarperTorch",
        "num_pages": 412
    },
    {
        "goodreads_id": "16201",
        "title": "Murder on the Orient Express",
        "author_id": "9810",  # Agatha Christie
        "work_id": "3038982",
        "isbn": "0007119313",
        "isbn13": "9780007119318",
        "language": "eng",
        "average_rating": 4.20,
        "ratings_count": 890284,
        "text_reviews_count": 27761,
        "publication_date": "1934-01-01",
        "format": "Paperback",
        "publisher": "HarperCollins",
        "num_pages": 256
    },
    {
        "goodreads_id": "17345",
        "title": "Oryx and Crake",
        "author_id": "11494",  # Margaret Atwood
        "work_id": "866693",
        "isbn": "0385721676",
        "isbn13": "9780385721677",
        "language": "eng",
        "average_rating": 4.01,
        "ratings_count": 274159,
        "text_reviews_count": 15432,
        "publication_date": "2003-05-06",
        "format": "Paperback",
        "publisher": "Anchor",
        "num_pages": 376,
        "series_id": "49081",
        "series_name": "MaddAddam",
        "series_position": "1"
    },
    {
        "goodreads_id": "6148028",
        "title": "Catching Fire",
        "author_id": "1069006",  # Suzanne Collins
        "work_id": "6288877",
        "isbn": "0439023491",
        "isbn13": "9780439023498",
        "language": "eng",
        "average_rating": 4.30,
        "ratings_count": 2702126,
        "text_reviews_count": 104687,
        "publication_date": "2009-09-01",
        "format": "Hardcover",
        "publisher": "Scholastic Press",
        "num_pages": 391,
        "series_id": "45462",
        "series_name": "The Hunger Games",
        "series_position": "2"
    },
    {
        "goodreads_id": "89717",
        "title": "Angels & Demons",
        "author_id": "4339",  # Dan Brown
        "work_id": "4735",
        "isbn": "0671027360",
        "isbn13": "9780671027360",
        "language": "eng",
        "average_rating": 3.93,
        "ratings_count": 2834639,
        "text_reviews_count": 19649,
        "publication_date": "2000-05-01",
        "format": "Paperback",
        "publisher": "Pocket Books",
        "num_pages": 572,
        "series_id": "41905",
        "series_name": "Robert Langdon",
        "series_position": "1"
    },
    {
        "goodreads_id": "11275",
        "title": "Kafka on the Shore",
        "author_id": "1303",  # Haruki Murakami
        "work_id": "6191072",
        "isbn": "1400079276",
        "isbn13": "9781400079278",
        "language": "eng",
        "average_rating": 4.14,
        "ratings_count": 371882,
        "text_reviews_count": 21793,
        "publication_date": "2002-09-12",
        "format": "Paperback",
        "publisher": "Vintage",
        "num_pages": 467
    }
]
        # Insert Authors
        for author_data in authors_data:
            author, created = Author.objects.get_or_create(
                name=author_data['name'],
                defaults={
                    'goodreads_id': author_data['goodreads_id'],
                    'role': author_data['role'],
                    'average_rating': author_data['average_rating'],
                    'ratings_count': author_data['ratings_count'],
                    'text_reviews_count': author_data['text_reviews_count'],
                    'works_count': author_data['works_count'],
                    'gender': author_data['gender'],
                    'image_url': author_data['image_url'],
                    'fans_count': author_data['fans_count']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created author: {author.name}'))

        # Insert Books
        for book_data in books_data:
            try:
                author = Author.objects.get(goodreads_id=book_data['author_id'])
                work, _ = Work.objects.get_or_create(
                    work_id=book_data['work_id'],
                    defaults={'title': book_data['title']}
                )
                book, created = Book.objects.get_or_create(
                    isbn=book_data['isbn'],
                    defaults={
                        'title': book_data['title'],
                        'work': work,
                        'isbn13': book_data['isbn13'],
                        'language': book_data['language'],
                        'average_rating': book_data['average_rating'],
                        'rating_dist': f"5:{book_data['ratings_count']}|4:0|3:0|2:0|1:0|total:{book_data['ratings_count']}",
                        'ratings_count': book_data['ratings_count'],
                        'text_reviews_count': book_data['text_reviews_count'],
                        'publication_date': parse_date(book_data['publication_date']),
                        'format': book_data['format'],
                        'publisher': book_data['publisher'],
                        'num_pages': book_data['num_pages'],
                        'series_id': book_data.get('series_id', ''),
                        'series_name': book_data.get('series_name', ''),
                        'series_position': book_data.get('series_position', '')
                    }
                )
                book.authors.add(author)
                if created:
                    self.stdout.write(self.style.SUCCESS(f'Created book: {book.title}'))
                    
                    # Create a sample shelf for each book
                    Shelf.objects.create(
                        name='to-read',
                        count=100,
                        book=book
                    )
            except Author.DoesNotExist:
                self.stdout.write(self.style.WARNING(f"Author not found for book: {book_data['title']}"))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f"Error creating book {book_data['title']}: {str(e)}"))

        self.stdout.write(self.style.SUCCESS(f"Database population completed successfully. Created {Author.objects.count()} authors and {Book.objects.count()} books."))