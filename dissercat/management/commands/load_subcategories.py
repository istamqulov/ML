from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from newspaper import Article

from dissercat.models import Post, Category

START_URL = "http://www.dissercat.com/"


class Command(BaseCommand):

    def get_catalogs(self):
        for category in Category.objects.all():
            try:
                r = requests.get(category.url)
                soup = BeautifulSoup(r.content, 'html.parser')
                catalogs = soup.select('.category h2 a')
                for catalog in catalogs:

                    Category.objects.get_or_create(
                        name=catalog.text,
                        url=catalog.attrs.get('href'),
                        parent=category
                    ).save()

            except Exception:
                pass

    def handle(self, *args, **options):
        self.stdout.write('Fetch catalogs')
        catalogs = self.get_catalogs()
