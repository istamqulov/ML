import asyncio
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
from django.core.management import BaseCommand


from dissercat.models import Post, Category

START_URL = "http://www.dissercat.com/"

sema = asyncio.BoundedSemaphore(32)

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/39.0.2171.95 Safari/537.36',
    # 'Upgrade-Insecure-Requests': 1
}


def fetch():
    try:
        post = Post.objects.filter(fetched=False).first()

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

    except Exception:
        pass


class Command(BaseCommand):

    counter = 0

    def handle(self, *args, **options):

        posts = Post.objects.filter(fetched=False)
        total = posts.count()
        if not total:
            return
        loop = asyncio.get_event_loop()
        tasks = asyncio.wait(
            [
                self.send_request(
                    loop,
                    total
                )
                for i in range(total)
            ]
        )
        loop.run_until_complete(tasks)

    async def send_request(self, loop,  total):

        async with sema:

            status = await loop.run_in_executor(
                None,
                fetch,
            )
            self.counter += 1
            self.stdout.write("%s / %s %s" %(self.counter, total, status))
