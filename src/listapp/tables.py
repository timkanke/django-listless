from django_tables2 import Column, tables, TemplateColumn
from .models import Item


class ItemList(tables.Table):

    class Meta:
        model = Item
        template_name = 'django_tables2/bootstrap5.html'
        attrs = {'class': 'table table-sm'}
        fields = ['id',
                  'author',
                  'title',
                  'publish',
                  ]

    review = TemplateColumn(template_name='listapp/tables/view_item.html', orderable=False)
