from django.urls import path
from .views import BookListView, search_book, admin_view_books, admin_view_borrowers


urlpatterns = [
    path("", BookListView.as_view(), name="book_list"),
    path("search/", search_book, name="search_book"),
    path("books/", admin_view_books, name="admin_view_books"),
    path("borrowers/", admin_view_borrowers, name="admin_view_borrowers"),
]
