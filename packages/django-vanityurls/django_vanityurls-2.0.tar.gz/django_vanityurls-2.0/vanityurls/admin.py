from django.contrib import admin

from .models import Category, VanityUrl


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):

    list_display = ['name']


@admin.register(VanityUrl)
class VanityUrlAdmin(admin.ModelAdmin):

    list_display = ['vanity_url', 'target', 'code', 'category']
    list_filter = ['code', 'category']
    show_facets = admin.ShowFacets.ALWAYS
    empty_value_display = 'Unassigned'
