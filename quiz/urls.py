from django.urls import path
from .views import cele

urlpatterns = [
    path("celery/", cele),
]