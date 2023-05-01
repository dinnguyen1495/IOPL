from import_export import resources, fields, widgets
from .models import Book, Borrower, Field
from .query_cover import *


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
    borrowers = fields.Field(
        column_name='Borrowers',
        attribute='borrowers',
        widget=widgets.ManyToManyWidget(Borrower, field='borrower_name', separator=',')
    )
    borrowed_dates = fields.Field(
        column_name='Borrowed Dates',
        attribute='borrowed_dates',
        widget=widgets.ManyToManyWidget(Borrower, field='borrowed_date', separator=',')
    )

    class Meta:
        model = Book
        import_id_fields = ('book_id',)
        exclude = ('id',)
        skip_unchanged = True
        fields = ('ID', 'Type', 'Field', 'Authors', 'Title', 'Publisher', 'Year of publication', 'Edition', 'ISBN',
                  'Inventory number', 'Units', 'Borrowers', 'Borrowed Dates')

    def skip_row(self, instance, original, row, import_validation_errors=None):
        return row["ID"] == '' or row["ISBN"] == '' or row["Year of publication"] == ''

    def save_instance(self, instance, is_create, using_transactions=True, dry_run=False):
        # if instance.cover_url == "":
        #     if instance.publisher != "LUH":
        #         instance.cover_url = get_cover_gg(self.title, self.authors)
        #     else:
        #         instance.cover_url = get_cover_luh(self.title)
        self.before_save_instance(instance, using_transactions, dry_run)
        if self._meta.use_bulk:
            if is_create:
                self.create_instances.append(instance)
            else:
                self.update_instances.append(instance)
        else:
            if not using_transactions and dry_run:
                pass
            else:
                instance.save()
        self.after_save_instance(instance, using_transactions, dry_run)
        return super(BookResource, self).save_instance(instance, is_create, using_transactions, dry_run)
