from django.contrib import admin

from dissercat.models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = [('category', admin.RelatedOnlyFieldListFilter), 'fetched']
    list_display = [
        'name',
        'author',
        "category",
        'updated',
    ]

    search_fields = ['name', 'author', "category__name"]


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    search_fields = ['name',]

    list_filter = [
        ('parent', admin.RelatedOnlyFieldListFilter),
    ]

    list_display = [
        'name',
        'parent',
        'url',
    ]

