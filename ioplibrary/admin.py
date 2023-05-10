from django.contrib import admin
from django import forms
from django.contrib.auth.models import Group
from django.utils.html import mark_safe
from django.utils.translation import gettext_lazy
from django.contrib.auth.models import User
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.utils.translation import gettext as _
from import_export.admin import ImportExportModelAdmin
from import_export.formats import base_formats

from .models import Book, Borrower, Field
from .resources import BookResource


class CustomAdminSite(admin.AdminSite):
    site_title = gettext_lazy("IOP")


class BookTable(admin.TabularInline):
    model = Book


class BorrwerInLine(admin.TabularInline):
    model = Borrower
    extra = 0

    def get_max_num(self, request, obj=None, **kwargs):
        if obj is not None:
            self.max_num = obj.units
        return super(BorrwerInLine, self).get_max_num(request, obj, **kwargs)


class BookAdmin(ImportExportModelAdmin):
    model = Book
    search_fields = (
        "book_id",
        "type",
        "title",
        "authors",
        "field__field_name",
        "publisher",
        "year",
        "edition",
        "isbn",
        "inventory_number",
        "borrower__borrower_name",
        "borrower__borrowed_date",
    )
    list_display = (
        "display_cover",
        "title",
        "get_authors",
        "field",
        "isbn",
        "inventory_number",
        "get_borrowers",
        "get_date",
    )
    list_display_links = (
        "display_cover",
        "title",
    )
    readonly_fields = ("display_cover",)
    inlines = (BorrwerInLine,)
    show_close_button = True
    resource_class = BookResource

    def get_exclude(self, request, obj=None):
        exclude = ["book_id", "id"]
        if obj is None:
            exclude += ["inventory_number"]
        return tuple(set(exclude))

    def save_model(self, request, obj, form, change):
        def get_type(type_name):
            return "BO" if type_name == "Book" else "TH"

        if not change:
            if Book.objects.count() == 0:
                obj.book_id = 101
            else:
                obj.book_id = (
                    Book.objects.filter().order_by("book_id").last().book_id + 1
                )
            obj.inventory_number = f"{obj.book_id} CSST {get_type(obj.type)} {obj.year}"
        obj.save()
        return super(BookAdmin, self).save_model(request, obj, form, change)

    def get_form(self, request, obj=None, **kwargs):
        kwargs["widgets"] = {
            "title": forms.Textarea(attrs={"cols": 35, "rows": 4}),
            "authors": forms.Textarea(attrs={"cols": 35, "rows": 3}),
        }
        return super().get_form(request, obj, **kwargs)

    def get_authors(self, obj):
        result = ""
        for author in obj.authors.split(", "):
            result += f"{author},<br>"
        return mark_safe(result[:-5])

    get_authors.short_description = "Authors"

    def get_borrowers(self, obj):
        result = ""
        for borrower in Borrower.objects.filter(borrowed_book=obj):
            result += f"{borrower.borrower_name}<br>"
        return mark_safe(result[:-4])

    get_borrowers.short_description = "Borrowers"

    def get_date(self, obj):
        result = ""
        for borrower in Borrower.objects.filter(borrowed_book=obj):
            result += f"{borrower.borrowed_date.strftime('%d.%m.%Y')}<br>"
        return mark_safe(result[:-4])

    get_date.short_description = "Borrowed Date"

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


class BorrowerAdmin(admin.ModelAdmin):
    model = Borrower
    search_fields = ("borrower_name", "borrowed_date", "borrowed_book")
    list_display = (
        "borrowed_book",
        "get_inventory_number",
        "get_borrower_name",
        "get_borrowed_date",
    )

    def get_inventory_number(self, obj):
        return obj.borrowed_book.inventory_number

    get_inventory_number.short_description = "Inventory Number"

    def get_borrower_name(self, obj):
        return obj.borrower_name

    get_borrower_name.short_description = "Borrower's Name"

    def get_borrowed_date(self, obj):
        return obj.borrowed_date.strftime("%d.%m.%Y")

    get_borrowed_date.short_description = "Borrowed Date"


# Register your models here.
admin_site = CustomAdminSite()
admin_site.register(User)
admin_site.register(Book, BookAdmin)
admin_site.register(Borrower, BorrowerAdmin)
admin_site.register(Field)
