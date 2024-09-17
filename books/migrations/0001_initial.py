# Generated by Django 5.1.1 on 2024-09-16 15:59

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Author",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(db_index=True, max_length=200)),
                (
                    "goodreads_id",
                    models.CharField(blank=True, max_length=20, null=True, unique=True),
                ),
                ("role", models.CharField(blank=True, max_length=100)),
                ("ratings_count", models.IntegerField(default=0)),
                ("average_rating", models.FloatField(default=0.0)),
                ("text_reviews_count", models.IntegerField(default=0)),
                ("works_count", models.IntegerField(default=0)),
                ("gender", models.CharField(blank=True, max_length=20)),
                ("image_url", models.URLField(blank=True, max_length=500)),
                ("fans_count", models.IntegerField(default=0)),
            ],
        ),
        migrations.CreateModel(
            name="Work",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("work_id", models.CharField(max_length=20, unique=True)),
                ("title", models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name="Book",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("title", models.CharField(max_length=255)),
                ("isbn", models.CharField(max_length=13, unique=True)),
                ("isbn13", models.CharField(max_length=13, unique=True)),
                ("asin", models.CharField(blank=True, max_length=10)),
                ("language", models.CharField(max_length=3)),
                ("average_rating", models.FloatField(default=0.0)),
                ("rating_dist", models.CharField(max_length=100)),
                ("ratings_count", models.IntegerField(default=0)),
                ("text_reviews_count", models.IntegerField(default=0)),
                ("publication_date", models.DateField()),
                ("original_publication_date", models.DateField(blank=True, null=True)),
                ("format", models.CharField(max_length=50)),
                ("edition_information", models.CharField(blank=True, max_length=255)),
                ("image_url", models.URLField(max_length=500)),
                ("publisher", models.CharField(max_length=255)),
                ("num_pages", models.IntegerField()),
                ("series_id", models.CharField(blank=True, max_length=20)),
                ("series_name", models.CharField(blank=True, max_length=255)),
                ("series_position", models.CharField(blank=True, max_length=10)),
                ("description", models.TextField()),
                (
                    "authors",
                    models.ManyToManyField(related_name="books", to="books.author"),
                ),
                (
                    "work",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        related_name="books",
                        to="books.work",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="Favorite",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE, to="books.book"
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="favorites",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "unique_together": {("user", "book")},
            },
        ),
        migrations.CreateModel(
            name="Shelf",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=100)),
                ("count", models.IntegerField(default=0)),
                (
                    "book",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="shelves",
                        to="books.book",
                    ),
                ),
            ],
            options={
                "unique_together": {("name", "book")},
            },
        ),
    ]
