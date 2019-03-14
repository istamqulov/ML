from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from newspaper import Article

from dissercat.models import Post, Category

START_URL = "http://www.dissercat.com/"


class Command(BaseCommand):

    def get_catalogs(self):
        r = requests.get(START_URL)
        soup = BeautifulSoup(r.content, "html.parser")
        main_catalogs = soup.select('.category h2 a')

        for main_catalog in main_catalogs:
            url = main_catalog.attrs.get('href')
            parent_catalog = Category(
                name=main_catalog.text,
                url=url
            )
            parent_catalog.save()

            self.stdout.write('Getting child nodes for %s' % url)
            if url:
                try:
                    r = requests.get(urljoin(START_URL, url))
                    soup = BeautifulSoup(r.content, "html.parser")
                    catalogs = soup.select('.category h2 a')
                    for catalog in catalogs:
                        Category(
                            name=catalog.text,
                            url=catalog.attrs.get('href'),
                            parent=parent_catalog
                        ).save()
                except Exception:
                    pass

    def handle(self, *args, **options):
        self.stdout.write('Fetch catalogs')
        catalogs = self.get_catalogs()
