from django.urls import path
from .views import index, book_list, book_detail, old_catalog

app_name = "dot"

urlpatterns = [
    path("", index, name="home"),
    path("books/", book_list, name="book_list"),
    path("books/<int:id>/", book_detail, name="book_detail"),
    path("catalog/", old_catalog, name="old_catalog")
]
