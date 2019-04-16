import csv
import os

from django.core.management import BaseCommand
from django.db import transaction

from dissercat.models import Post, Category


class Command(BaseCommand):

    def handle(self, *args, **options):

        for category in Category.objects.filter(parent=None):
            os.mkdir(category.name.replace(" ", "_"))
        categories = Category.objects.filter(parent__isnull=False)
        for category in categories:
            n = category.name.replace(" ", "_")[:100]
            p = "CSV/" + category.parent.name.replace(" ", "_") + "/" + n + ".csv"
            if not os.path.exists(p):
                with open(p, 'w') as csvfile:

                    writer = csv.DictWriter(
                        csvfile,
                        fieldnames=["name", 'introduction', 'category_name', "category_id"]
                    )
                    writer.writeheader()

                    print('fetch ', category.name)
                    for post in category.post_set.exclude(introduction=""):
                        print("export ", post.id)
                        writer.writerow(
                            {
                                "name": post.name,
                                "introduction": post.introduction,
                                "category_name": post.category.name,
                                "category_id": post.category.id,
                            }
                        )
            else:
                print("skip ", n )
