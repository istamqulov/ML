from admirarchy.utils import AdjacencyList
from django.contrib import admin
from django.utils.html import format_html
from admirarchy.toolbox import HierarchicalModelAdmin
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
class CategoryAdmin(HierarchicalModelAdmin):
    hierarchy = AdjacencyList('parent')

    list_filter = [('parent', admin.RelatedOnlyFieldListFilter),]

    list_display = [
        'name',
        'parent',
        'url',
        'get_posts'
    ]

    def get_posts(self, obj):
        return format_html(
            """<a href='/admin/dissercat/post/?category_id={}'>{}</a>""",
            str(obj.id),
            str(obj.post_set.count())
        )



