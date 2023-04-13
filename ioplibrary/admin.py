from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from .models import Book


class BookTable(admin.TabularInline):
    model = Book


class BookAdmin(admin.ModelAdmin):
    model = Book
    exclude = ('book_id',)
    search_fields = ('book_id', 'title', 'authors', 'type', 'field', 'year', 'isbn', 'inventory_number')
    list_display = ('title', 'authors', 'field', 'isbn', 'inventory_number')

    def clean_title(self):
        title = self.clean_title['title']
        if Book.objects.filter(title=title).exists():
            raise forms.ValidationError("A book with the same title is already exists")
        return title

    def clean_isbn(self):
        title = self.clean_title['isbn']
        if Book.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError("A book with the same isbn is already exists")
        return title

    def save_model(self, request, obj, form, change):
        if not change:
            obj.book_id = Book.objects.count() + 100
        obj.inventory_number = f"{obj.book_id} {obj.location.split()[0]} {obj.type} {obj.year}"
        obj.save()


# Register your models here.
admin.site.register(Book, BookAdmin)
admin.site.unregister(Group)
