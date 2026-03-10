from django.contrib import admin
from .models import Category, Women

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')
    search_fields = ('name',)

@admin.register(Women)
class WomenAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'cat', 'time_create', 'is_published')
    list_filter = ('cat', 'is_published')
    search_fields = ('title', 'content')
    readonly_fields = ('time_create', 'time_update')