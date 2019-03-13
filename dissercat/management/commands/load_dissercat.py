from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand
from newspaper import Article

from dissercat.models import Post

START_URL = "http://www.dissercat.com/"


class Command(BaseCommand):

    def save_posts(self, posts_urls):
        for post_url in posts_urls:
            post = Article(urljoin(START_URL, post_url))
            post.download()
            post.parse()
            authors = post.authors
            title = post.title
            content = post.text
            post_object = Post(
                name=title,
                author=authors[0] if authors else '-',
                content=content
            )
            post_object.save()
            self.stdout('%s added' % title)

    def get_posts_urls(self, catalog_url):
        r = requests.get(catalog_url)
        soup = BeautifulSoup(r.content, "html.parser")

        ass = soup.select(".category-products tr td a")

        return [a.attrs.get('href') for a in ass]

    def get_catalog_pages(self, catalog_start_url):
        r = requests.get(catalog_start_url)
        soup = BeautifulSoup(r.content, "html.parser")
        last_page = soup.find('.pager-last a')

        if last_page:
            last_page_href = last_page.attrs['href']
            p = int(last_page_href.split("/")[-1][1:])
            return [
                urljoin(
                    catalog_start_url, "p%s" % ind
                ) for ind in range(int(p))
            ]
        else:
            return catalog_start_url

    def get_catalogs(self):
        r = requests.get(START_URL)
        soup = BeautifulSoup(r.content, "html.parser")
        main_catalogs = soup.select('.category h2 a')
        urls = []
        for main_catalog in main_catalogs:
            url = main_catalog.attrs.get('href')
            self.stdout.write('Getting child nodes for %s' % url)
            if url:
                urls.append(url)
                r = requests.get(START_URL, url)
                soup = BeautifulSoup(r.content, "html.parser")
                catalogs = soup.select('.category h2 a')
                for catalog in catalogs:
                    urls.append(catalog.attrs.get('href'))
        return urls

    def handle(self, *args, **options):
        self.stdout.write('Fetch catalogs')
        catalogs = self.get_catalogs()
        self.stdout.write('Fetch catalog pages')
        pages = []
        for catalog in catalogs:
            pages.extend(self.get_catalog_pages(urljoin(START_URL, catalog)))

        posts = []

        for page in pages:
            posts.extend(self.get_posts_urls(urljoin(START_URL, page)))

        with open('posts.txt', 'w') as file_:
            for post in posts:
                file_.write(post)
