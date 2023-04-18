from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime
from django.utils import timezone

from .validators import CommaSeparatedStringValidator, ISBNValidator, YearValidator


# Create your models here.
class Book(models.Model):
    class TruePositiveIntegerField(models.PositiveIntegerField):
        def formfield(self, **kwargs):
            return super().formfield(
                **{
                    "min_value": 1,
                    **kwargs,
                }
            )

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
    field = models.CharField(
        "Field",
        max_length=200,
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
    year = models.PositiveIntegerField(
        "Year of publication",
        validators=[YearValidator],
        default=datetime.date.today().year,
    )
    edition = models.PositiveIntegerField(
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
        editable=False,
        unique=True,
    )
    units = models.PositiveIntegerField(
        "Units",
        default=0,
    )

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)


class Holder(models.Model):
    name = models.CharField(max_length=200)
    date = models.DateField(default=datetime.date.today())
    borrowed_book = models.ForeignKey("Book", on_delete=models.CASCADE)

    def __str__(self):
        return self.name
