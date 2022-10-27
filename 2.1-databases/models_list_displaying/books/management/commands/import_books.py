import json

from django.core.management.base import BaseCommand
from django.template.defaultfilters import slugify

from books.models import Book


class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        with open('fixtures/books.json', 'r') as file:
            books = list(json.load(file))

            for book in books:
                book_label = Book(
                    name=book['fields']['name'],
                    author=book['fields']['author'],
                    pub_date=book['fields']['pub_date'],
                )
                book_label.save()

                self.stdout.write(self.style.SUCCESS('Successfully added book "%s"' % book['fields']['name']))
