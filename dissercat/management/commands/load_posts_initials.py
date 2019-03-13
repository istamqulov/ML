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
        for category in Category.objects.filter(fetched=False):
            print('fetching of ', category.name)
            curl = urljoin(START_URL, category.url)
            r = requests.get(
                curl
            )

            soup = BeautifulSoup(r.content, "html.parser")
            last_page = soup.select_one(".pager-last a")

            if not last_page:
                try:
                    last_page = soup.select(".pager-item a")[-1]
                except Exception as e:
                    pass

            pages = []
            if last_page:
                print(last_page)
                last_page_href = last_page.attrs['href']
                p = int(last_page_href.split("/")[-1][1:])
                for i in range(int(p)):
                    pages.append(
                        curl + "/p%s" % i
                    )
            else:
                pages.append(curl)

            for page in pages:
                r = requests.get(page)
                soup = BeautifulSoup(r.content, 'html.parser')
                rows = soup.select('.category-products tbody tr')

                for row in rows:

                    td1, td2, td3, *_ = row
                    a = td1.select_one('a')
                    title = a.text
                    url = a.attrs.get('href')
                    author = td2.text

                    try:
                        year = int(td3.text)
                    except Exception:
                        year = None

                    Post(
                        name=title,
                        category=category,
                        url=url,
                        author=author
                    ).save()
                    print(title, 'created')

            category.fetched = True
            category.save()

