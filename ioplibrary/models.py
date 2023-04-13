from django.db import models
from django.utils.translation import gettext_lazy as _
import datetime

from .validators import CommaSeparatedStringValidator, ISBNValidator, YearValidator


# Create your models here.
class Book(models.Model):
    class TypeOfMaterial(models.TextChoices):
        BOOK = "BO", _("Book")
        THESIS = "TH", _("Thesis")

    book_id = models.IntegerField("ID", primary_key=True, unique=True, default=0)
    title = models.CharField(max_length=200, unique=True)
    authors = models.CharField(
        max_length=200,
        validators=[CommaSeparatedStringValidator],
    )
    type = models.CharField(max_length=2, choices=TypeOfMaterial.choices, default=TypeOfMaterial.BOOK)
    field = models.CharField(max_length=200)
    year = models.IntegerField(validators=[YearValidator], default=datetime.date.today().year)
    edition = models.IntegerField(default=1)
    publisher = models.CharField(max_length=200)
    isbn = models.CharField("ISBN", max_length=200, validators=[ISBNValidator], unique=True)
    location = models.CharField(max_length=200, default="CSST Lib")
    quantity = models.IntegerField(default=1)
    inventory_number = models.CharField("Inventory number", max_length=200, default="", editable=False, unique=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        super(Book, self).save(*args, **kwargs)
