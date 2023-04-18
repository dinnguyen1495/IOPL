from import_export import resources, fields
from .models import Book


class BookResource(resources.ModelResource):
    book_id = fields.Field(column_name='ID', attribute='book_id')
    type = fields.Field(column_name='Type', attribute='type')
    field = fields.Field(column_name='Field', attribute='field')
    authors = fields.Field(column_name='Authors', attribute='authors')
    title = fields.Field(column_name='Title', attribute='title')
    publisher = fields.Field(column_name='Publisher', attribute='publisher')
    year = fields.Field(column_name='Year of publication', attribute='year')
    edition = fields.Field(column_name='Edition', attribute='edition')
    isbn = fields.Field(column_name='ISBN', attribute='isbn')
    inventory_number = fields.Field(column_name='Inventory number', attribute='inventory_number')
    units = fields.Field(column_name='Units', attribute='units')

    class Meta:
        model = Book
        import_id_fields = ('book_id',)
        exclude = ('id',)
        skip_unchanged = True
        fields = ('ID', 'Type', 'Field', 'Authors', 'Title', 'Publisher', 'Year of publication', 'Edition', 'ISBN',
                  'Inventory number', 'Units',)

    def skip_row(self, instance, original, row, import_validation_errors=None):
        return row["ID"] == '' or row["ISBN"] == '' or row["Year of publication"] == ''

    def before_import_row(self, row, row_number=None, **kwargs):
        return super(BookResource, self).import_row(row, row, row_number, **kwargs)
