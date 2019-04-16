from django.core.management import BaseCommand
from django.db import transaction

from dissercat.models import Post, Category


class Command(BaseCommand):

    def handle(self, *args, **options):
        print("starting migrating")
        categories = Category.objects.all().iterator(1000)
        ptc = Post.objects.count()
        cn = 0

        # for category in categories:
        #     print("Starting moving category ", category.name)
        #
        #     c = Category(
        #         id=category.id,
        #         parent_id=category.parent_id,
        #         url=category.url,
        #         fetched=category.fetched
        #     )
        #     c.save(using="mysql")

        for category in categories:
            posts = []
            for post in Post.objects.filter(category_id=category.id).iterator():
                cn += 1
                print("move post ", post.name, cn, "/", ptc)
                Post(
                    name=post.name,
                    category_id=post.category_id,
                    author=post.author,
                    url=post.url,
                    year=post.year,
                    head=post.head,
                    introduction=post.introduction,
                    close=post.close,
                    content=post.content,
                    biblio=post.biblio,
                    created=post.created,
                    updated=post.updated,
                    fetched=post.fetched,
                )
                posts.append(post)

            Post.objects.using('mysql').bulk_create(posts, batch_size=200)
            del posts
