from django.urls import path
from . import views

urlpatterns = [
    path('v1/women/', views.WomenListAPIView.as_view(), name='api-women-list'),
]