from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("main/", include("main.urls")),  # Убедитесь, что этот путь прописан правильно
]
