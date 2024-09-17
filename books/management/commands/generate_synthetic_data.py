import random
from faker import Faker
from django.core.management.base import BaseCommand
from books.models import Author, Book, Work
from django.utils.dateparse import parse_date

# Initialize Faker
fake = Faker()

class Command(BaseCommand):
    help = 'Generate synthetic data for books and authors'

    def add_arguments(self, parser):
        parser.add_argument(
            '-n', '--number',
            type=int,
            default=100,
            help='The number of synthetic books and authors to create',
        )

    def handle(self, *args, **options):
        n = options['number']
        self.stdout.write(f"Generating {n} synthetic books and authors...")

        for _ in range(n):
            # Generate random author data
            author_name = fake.name()
            author_goodreads_id = str(fake.random_number(digits=8))
            author_ratings_count = random.randint(0, 1000)
            author_average_rating = round(random.uniform(1, 5), 2)
            author_text_reviews_count = random.randint(0, 100)
            author_works_count = random.randint(1, 10)
            author_image_url = fake.image_url()
            author_fans_count = random.randint(0, 5000)

            # Create or get author
            author, _ = Author.objects.get_or_create(
                name=author_name,
                defaults={
                    'goodreads_id': author_goodreads_id,
                    'ratings_count': author_ratings_count,
                    'average_rating': author_average_rating,
                    'text_reviews_count': author_text_reviews_count,
                    'works_count': author_works_count,
                    'image_url': author_image_url,
                    'fans_count': author_fans_count,
                }
            )

            # Generate random work data
            work_title = fake.sentence(nb_words=4)
            work_id = str(fake.random_number(digits=8))

            # Create or get work
            work, _ = Work.objects.get_or_create(
                work_id=work_id,
                defaults={'title': work_title}
            )

            # Generate random book data
            book_title = fake.sentence(nb_words=5)
            book_isbn = fake.isbn10()[:13]  
            book_isbn13 = fake.isbn13()[:13]
            book_language = random.choice(['eng', 'spa', 'fra', 'deu'])
            book_average_rating = round(random.uniform(1, 5), 2)
            book_ratings_count = random.randint(0, 1000)
            book_text_reviews_count = random.randint(0, 100)
            book_publication_date = fake.date_this_century()
            book_format = random.choice(['Hardcover', 'Paperback', 'eBook'])
            book_image_url = fake.image_url()
            book_publisher = fake.company()
            book_num_pages = random.randint(50, 1000)
            book_description = fake.paragraph(nb_sentences=5)

            # Create book
            book, _ = Book.objects.get_or_create(
                isbn=book_isbn,
                defaults={
                    'title': book_title,
                    'work': work,
                    'isbn13': book_isbn13,
                    'language': book_language,
                    'average_rating': book_average_rating,
                    'ratings_count': book_ratings_count,
                    'text_reviews_count': book_text_reviews_count,
                    'publication_date': book_publication_date,
                    'format': book_format,
                    'image_url': book_image_url,
                    'publisher': book_publisher,
                    'num_pages': book_num_pages,
                    'description': book_description,
                }
            )

            # Add author to book
            book.authors.add(author)
            book.save()

        self.stdout.write(self.style.SUCCESS(f"Successfully generated {n} synthetic books and authors!"))

