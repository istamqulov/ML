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
                r = requests.get(urljoin(START_URL, category.url))
                soup = BeautifulSoup(r.content, 'html.parser')
                catalogs = soup.select('.category h2 a')
                print('fetch', category.url)
                for catalog in catalogs:
                    if not Category.objects.filter(url=catalog.attrs.get('href')).exists():
                        Category(
                            name=catalog.text,
                            url=catalog.attrs.get('href'),
                            parent=category
                        ).save()

            except Exception:
                pass

    def handle(self, *args, **options):
        self.stdout.write('Fetch catalogs')
        catalogs = self.get_catalogs()

