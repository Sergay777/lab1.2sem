from django.shortcuts import render
from rest_framework import generics
from .models import Women
from .serializers import WomenSerializer

class WomenListAPIView(generics.ListAPIView):
    """Read-only API для списка статей"""
    queryset = Women.objects.filter(is_published=True).select_related('cat')
    serializer_class = WomenSerializer