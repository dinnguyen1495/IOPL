from django.urls import path
from .views import BookListView, search_book


urlpatterns = [
    path('', BookListView.as_view(), name='book_list'),
    path('search/', search_book, name='search_book')
]
