from rest_framework import serializers
from .models import Category, Women

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class WomenSerializer(serializers.ModelSerializer):
    cat_name = serializers.CharField(source='cat.name', read_only=True)
    
    class Meta:
        model = Women
        fields = ['id', 'title', 'content', 'cat', 'cat_name', 'time_create', 'is_published']