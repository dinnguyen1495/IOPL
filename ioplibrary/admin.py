from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .models import Book, Holder, Field
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


class BookAdmin(ImportExportModelAdmin):
    model = Book
    search_fields = ('book_id', 'type', 'authors', 'field__field_name', 'title', 'publisher', 'year', 'edition', 'isbn',
                     'inventory_number', 'holder__borrower_name', 'holder__borrowed_date')
    list_display = ('title', 'authors', 'field', 'isbn', 'inventory_number', 'holders', 'date', 'display_cover')
    readonly_fields = ('display_cover',)
    inlines = (HolderInLine,)
    resource_class = BookResource

    def clean_title(self):
        title = self.clean_title['title']
        if Book.objects.filter(title=title).exists():
            raise forms.ValidationError("A book with the same title is already exists")
        return title

    def clean_isbn(self):
        title = self.clean_title['isbn'].replace("-", "")
        if Book.objects.filter(isbn=isbn).exists():
            raise forms.ValidationError("A book with the same isbn is already exists")
        return title

    def save_model(self, request, obj, form, change):
        def get_type(type_name):
            return 'BO' if type_name == 'Book' else 'TH'

        def get_cover(isbn):
            pass

        if not change:
            if Book.objects.count() == 0:
                obj.book_id = 101
            else:
                obj.book_id = Book.objects.filter().order_by('book_id').last().book_id + 1
            obj.inventory_number = f"{obj.book_id} CSST {get_type(obj.type)} {obj.year}"
        obj.save()
        return super(BookAdmin, self).save_model(request, obj, form, change)

    def holders(self, obj):
        result = ""
        for holder in Holder.objects.filter(borrowed_book=obj):
            result += f"{holder.borrower_name}\n"
        return result

    def date(self, obj):
        result = ""
        for holder in Holder.objects.filter(borrowed_book=obj):
            result += f"{holder.borrowed_date}\n"
        return result

    def get_exclude(self, request, obj=None):
        exclude = ['book_id', 'id']
        if obj is None:
            exclude += ["inventory_number"]
        return tuple(set(exclude))

    def get_import_formats(self):
        formats = (
            base_formats.XLSX,
            base_formats.XLS,
            base_formats.CSV,
            base_formats.ODS,
        )
        return [f for f in formats if f().can_export()]

    def get_export_formats(self):
        formats = (
            base_formats.XLSX,
            base_formats.XLS,
            base_formats.CSV,
            base_formats.ODS,
        )
        return [f for f in formats if f().can_export()]


class HolderAdmin(admin.ModelAdmin):
    model = Holder
    search_fields = ('borrower_name', 'borrowed_date', 'borrowed_book')
    list_display = ('borrower_name', 'borrowed_date', 'borrowed_book')


# Register your models here.
admin.site.unregister(Group)
admin.site.register(Book, BookAdmin)
admin.site.register(Holder, HolderAdmin)
admin.site.register(Field)
