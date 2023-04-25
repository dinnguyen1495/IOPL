from django.views.generic import ListView
from .models import Book, Field, Holder
from django.http import JsonResponse


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['field_list'] = Field.objects.all()
        context['holders'] = reversed(Holder.objects.all())
        context['book_columns'] = ["Title", "Publisher", "Year", "Edition", "ISBN"]
        return context


def search_book(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    filtered_books = []

    if request.method == "GET" and is_ajax:
        query = request.GET['query']
        field = request.GET['field']
        column = request.GET['column']

        queryset = Book.objects.all()
        if query == "":
            if field != 'All':
                queryset = Book.objects.filter(field__field_name=field)

        if query != "":
            if field != 'All':
                queryset = Book.objects.filter(field__field_name=field)

            query_dict = {
                "title": queryset.filter(title__contains=query),
                "authors": queryset.filter(authors__contains=query),
                "publisher": queryset.filter(publisher__contains=query),
                "year": queryset.filter(year__contains=query),
                "edition": queryset.filter(edition__contains=query)
            }

            if column == 'all':
                queryset = query_dict["title"] | query_dict["authors"] | query_dict["publisher"] | query_dict["year"] \
                           | query_dict["edition"]
            else:
                queryset = query_dict[column]

        for book in queryset:
            book_info = {
                "title": book.title,
                "authors": book.authors,
                "publisher": book.publisher,
                "field": book.field.field_name,
                "year": book.year,
                "edition": book.edition,
                "available": book.get_availability(),
                "cover": book.cover.url
            }
            filtered_books.append(book_info)

        return JsonResponse({'books': filtered_books})
    return JsonResponse({'error': 'Something is wrong!'})
