from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup

from django.core.management import BaseCommand
from newspaper import Article

from dissercat.models import Post, Category

START_URL = "http://www.dissercat.com/"


class Command(BaseCommand):

    def handle(self, *args, **options):
        self.stdout.write('Fetch catalogs')
        c = 0
        for post in Post.objects.filter(fetched=False):
            try:
                c += 1

                r = requests.get(urljoin(START_URL, post.url))
                soup = BeautifulSoup(r.content, "html.parser")
                toc = soup.select_one(".field-field-toc .field-items")
                introduction = soup.select_one(".field-field-preface .field-items")
                close = soup.select_one(".field-field-conclusion .field-items")
                biblio = soup.select_one(".field-field-biblio .field-items")

                if toc:
                    post.head = toc.text
                if introduction:
                    post.introduction = introduction.text

                if close:
                    post.close = close.text

                if biblio:
                    post.biblio = biblio.text

                post.fetched = True
                post.save()
                print(post.name, "--fetched, ", c)
            except:
                pass
