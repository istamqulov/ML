from django.contrib import admin

from dissercat.models import Post, Category


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = [('category', admin.RelatedOnlyFieldListFilter), ]
    list_display = [
        'name',
        'author',
        'year',
        'created',
        'updated',
    ]

    search_fields = ['name', 'author']


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_filter = [('parent', admin.RelatedOnlyFieldListFilter),]

    list_display = [
        'name',
        'parent',
        'url',
    ]

