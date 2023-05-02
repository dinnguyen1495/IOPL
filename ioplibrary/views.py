from django.views.generic import ListView, UpdateView
from .models import Book, Field, Borrower
from django.http import JsonResponse


class BookListView(ListView):
    model = Book
    template_name = 'books/book_list.html'

    def get_context_data(self, *args, **kwargs):
        context = super(BookListView, self).get_context_data(*args, **kwargs)
        context['object_list'] = Book.objects.order_by("book_id")
        context['result_number'] = context['object_list'].count()
        context['types'] = ["Book", "Thesis"]
        context['field_list'] = Field.objects.all()
        context['borrowers'] = reversed(Borrower.objects.all())
        context['book_columns'] = ["Inventory Number", "Title", "Publisher", "ISBN", "Year"]
        return context


def search_book(request):
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest'
    filtered_books = []

    if request.method == "GET" and is_ajax:
        book_type = request.GET['book_type']
        query = request.GET['query']
        field = request.GET['field']
        column = request.GET['column']

        queryset = None
        if book_type != 'All':
            queryset = Book.objects.filter(type=book_type).order_by("-book_id")
        else:
            queryset = Book.objects.all()

        if query == "":
            if field != 'All':
                queryset = Book.objects.filter(field__field_name=field).order_by("-book_id")

        if field != 'All':
            queryset = Book.objects.filter(field__field_name=field).order_by("-book_id")

        query_dict = {
            "inventory number": queryset.filter(inventory_number__startswith=query),
            "title": queryset.filter(title__contains=query),
            "authors": queryset.filter(authors__contains=query),
            "publisher": queryset.filter(publisher__contains=query),
            "isbn": queryset.filter(isbn__startswith=query),
            "year": queryset.filter(year__startswith=query),
        }

        if column == 'all':
            queryset = query_dict["title"] | query_dict["authors"] | query_dict["publisher"] | query_dict["inventory number"] | \
                       query_dict["isbn"] | query_dict["year"]
        else:
            queryset = query_dict[column]

        for book in queryset:
            book_info = {
                "title": book.title,
                "authors": book.authors,
                "publisher": book.publisher,
                "type": book.type,
                "field": book.field.field_name,
                "year": book.year,
                "edition": book.edition,
                "isbn": book.isbn,
                "inventory_number": book.inventory_number,
                "units": book.units,
                "available": book.get_availability(),
                "cover": book.cover.url
            }
            filtered_books.append(book_info)

        return JsonResponse({"books": filtered_books, "result_number": len(filtered_books)})
    return JsonResponse({'error': 'Something is wrong!'})
