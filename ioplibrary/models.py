from django.db import models
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
import datetime
from os.path import exists

from .validators import CommaSeparatedStringValidator, ISBNValidator, YearValidator
from .constants import *
from .query_cover import *


# Create your models here.
class Field(models.Model):
    field_name = models.CharField(
        "Field's name",
        max_length=20,
    )

    def __str__(self):
        return self.field_name


def get_default_field():
    fields = ["Physics", "Mechanics", "Nanotechnology", "Mathematics", "Programming"]
    default_field = None
    for name in fields:
        field, _ = Field.objects.get_or_create(field_name=name)
        field.save()
        if default_field is None:
            default_field = field
    return default_field


class TruePositiveIntegerField(models.PositiveIntegerField):
    def formfield(self, **kwargs):
        return super().formfield(
            **{
                "min_value": 1,
                **kwargs,
            }
        )


class Book(models.Model):
    class TypeOfMaterial(models.TextChoices):
        BOOK = "Book", _("Book")
        THESIS = "Thesis", _("Thesis")

    book_id = models.PositiveIntegerField(
        "ID",
        primary_key=True,
        unique=True,
        default=0
    )
    type = models.CharField(
        "Type",
        max_length=10,
        choices=TypeOfMaterial.choices,
        default=TypeOfMaterial.BOOK,
    )
    field = models.ForeignKey(
        "Field",
        default=get_default_field,
        null=True,
        on_delete=models.SET_NULL,
    )
    authors = models.CharField(
        "Authors",
        max_length=200,
        validators=[CommaSeparatedStringValidator],
    )
    title = models.CharField(
        "Title",
        max_length=200,
        unique=True,
    )
    publisher = models.CharField(
        "Publisher",
        max_length=200,
        null=True,
    )
    year = TruePositiveIntegerField(
        "Year of publication",
        validators=[YearValidator],
        default=datetime.date.today().year,
    )
    edition = TruePositiveIntegerField(
        "Edition",
        default=1,
    )
    isbn = models.CharField(
        "ISBN",
        max_length=20,
        validators=[ISBNValidator],
        null=True,
    )
    inventory_number = models.CharField(
        "Inventory number",
        max_length=200,
        default="",
        editable=True,
        unique=True,
    )
    units = TruePositiveIntegerField(
        "Units",
        default=1,
    )
    cover = models.ImageField(
        "Cover's Path",
        upload_to=f"{COVERS_DIR}",
        blank=True,
        null=True,
        default=f'{COVERS_DIR}/unavailable.jpg'
    )
    cover_url = models.CharField(
        max_length=2000,
        default="",
        editable=False
    )

    def __str__(self):
        return self.title

    def display_cover(self):
        return mark_safe(f'<img src="{self.cover.url}" width="150" />')
    display_cover.short_description = "Cover's Preview"
    display_cover.allow_tags = True

    def get_availability(self) -> int:
        return self.units - Holder.objects.filter(borrowed_book=self).count()

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        self.isbn = self.isbn.strip()
        self.title = self.title.strip()
        self.authors = self.authors.strip()
        self.publisher = self.publisher.strip()
        self.inventory_number = self.inventory_number.strip()

        if self.cover == f"{COVERS_DIR}/unavailable.jpg":
            if exists(f"./media/{COVERS_DIR}/{self.isbn}.jpg"):
                self.cover = f"{COVERS_DIR}/{self.isbn}.jpg"
            else: 
                if self.cover_url == "":
                    if self.publisher != "LUH":
                        self.cover_url = get_cover_gg(self.title, self.authors)
                    else:
                        self.cover_url = get_cover_luh(self.title)
                else:
                    self.cover = save_cover(self.cover_url, self.isbn)
                print()

        return super(Book, self).save(force_insert, force_update, using, update_fields)


class Holder(models.Model):
    borrower_name = models.CharField(
        "Name",
        max_length=200,
        unique=True,
    )
    borrowed_date = models.DateField(
        "Date",
        default=datetime.date.today(),
    )
    borrowed_book = models.ForeignKey(
        "Book",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return ""
