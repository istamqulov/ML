from admirarchy.utils import AdjacencyList
from django.contrib import admin
from django.core import serializers
from django.http import HttpResponse
from django.utils.html import format_html
from admirarchy.toolbox import HierarchicalModelAdmin
from dissercat.models import Post, Category


def export_as_json(modeladmin, request, queryset):
    response = HttpResponse(content_type="application/json")
    serializers.serialize("json", queryset, stream=response)
    return response


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_filter = [('category', admin.RelatedOnlyFieldListFilter), 'fetched']
    list_display = [
        'name',
        'author',
        'year',
        'created',
        'updated',
    ]

    search_fields = ['name', 'author']

    actions = [export_as_json]


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



