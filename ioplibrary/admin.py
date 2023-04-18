from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin

from .models import Book, Holder
from .resources import BookResource


class BookTable(admin.TabularInline):
    model = Book


class HolderInLine(admin.TabularInline):
    model = Holder
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if obj is not None:
            self.max_num = obj.units
        return super(HolderInLine, self).get_max_num(request, obj, **kwargs)


class BookAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    model = Book
    exclude = ('book_id', 'id',)
    search_fields = ('book_id', 'type', 'field', 'authors', 'title', 'publisher', 'year', 'edition', 'isbn',
                     'inventory_number')
    list_display = ('title', 'authors', 'field', 'isbn', 'inventory_number', 'holders', 'date')
    inlines = (HolderInLine,)
    resource_class = BookResource

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
        def get_type(type_name):
            return 'BO' if type_name == 'Book' else 'TH'

        if not change:
            obj.book_id = Book.objects.count() + 100
        obj.inventory_number = f"{obj.book_id} CSST {get_type(obj.type)} {obj.year}"
        obj.save()

    def holders(self, obj):
        result = ""
        for borrower in Holder.objects.filter(borrowed_book=obj):
            result += f"{borrower.name}\n"
        return result

    def date(self, obj):
        result = ""
        for borrower in Holder.objects.filter(borrowed_book=obj):
            result += f"{borrower.date}\n"
        return result


class HolderAdmin(admin.ModelAdmin):
    model = Holder
    list_display = ('name', 'date', 'borrowed_book')


# Register your models here.
admin.site.unregister(Group)
admin.site.register(Book, BookAdmin)
admin.site.register(Holder, HolderAdmin)
