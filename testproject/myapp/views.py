from django.views.generic import TemplateView

from tastybackbonepie.helpers import TastyBackbonePieTableHelper


class BookTable(TastyBackbonePieTableHelper):
    uid = 'book_table'
    root_url = '/api/v1/book/'
    fields = [
        {
            'key': 'id',
            'label': '#',
        },
        {
            'key': 'name',
            'label': 'Name',
            'order_by': 'name',
        },
        {
            'key': 'added',
            'label': 'Added at',
            'order_by': 'added',
        },
        {
            'key': 'read',
            'label': 'Read',
            'template': '<% if (entry.get(\'read\') == true) { %>x<% } %>',
            'order_by': 'read',
        },
    ]
    additional_html_fields = [
        '<a class="btn btn-mini" href="#" data-id="<%= entry.get(\'id\') %>"><i class="icon-trash"></i></a>',
    ]


class TestView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context['book_table'] = BookTable()
        return context
