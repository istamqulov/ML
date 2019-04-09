from django.db import models

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=255)
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)
    fetched = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name


class Post(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey(to=Category, on_delete=models.CASCADE)
    author = models.CharField(max_length=255)
    url = models.CharField(max_length=255)
    year = models.IntegerField(blank=True, null=True)
    head = models.TextField(default="")
    introduction = models.TextField(default="")
    close = models.TextField(default="")
    content = models.TextField(default="")
    biblio = models.TextField(default="")

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    fetched = models.BooleanField(default=False)
#     moved = models.BooleanField(default=False)

    

