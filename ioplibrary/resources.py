from import_export import resources, fields, widgets
from .models import Book, Holder, Field
from .query_image import *


class BookResource(resources.ModelResource):
    book_id = fields.Field(
        column_name='ID',
        attribute='book_id'
    )
    type = fields.Field(
        column_name='Type',
        attribute='type'
    )
    field = fields.Field(
        column_name='Field',
        attribute='field',
        widget=widgets.ForeignKeyWidget(Field, 'field_name')
    )
    authors = fields.Field(
        column_name='Authors',
        attribute='authors'
    )
    title = fields.Field(
        column_name='Title',
        attribute='title'
    )
    publisher = fields.Field(
        column_name='Publisher',
        attribute='publisher'
    )
    year = fields.Field(
        column_name='Year of publication',
        attribute='year'
    )
    edition = fields.Field(
        column_name='Edition',
        attribute='edition')
    isbn = fields.Field(
        column_name='ISBN',
        attribute='isbn'
    )
    inventory_number = fields.Field(
        column_name='Inventory number',
        attribute='inventory_number'
    )
    units = fields.Field(
        column_name='Units',
        attribute='units'
    )

    class Meta:
        model = Book
        import_id_fields = ('book_id',)
        exclude = ('id',)
        skip_unchanged = True
        fields = ('ID', 'Type', 'Field', 'Authors', 'Title', 'Publisher', 'Year of publication', 'Edition', 'ISBN',
                  'Inventory number', 'Units')

    def skip_row(self, instance, original, row, import_validation_errors=None):
        return row["ID"] == '' or row["ISBN"] == '' or row["Year of publication"] == ''

    def save_instance(self, instance, is_create, using_transactions=True, dry_run=False):
        # if instance.cover_url == "":
        #     if instance.publisher == "LUH":
        #         instance.cover_url = get_cover_luh(instance.isbn)
        #     else:
        #         instance.cover_url = get_cover_ddg(title=instance.title, isbn=instance.isbn)
        return super(BookResource, self).save_instance(instance, is_create, using_transactions, dry_run)
