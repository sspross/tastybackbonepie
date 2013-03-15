from django.views.generic import TemplateView

from tastybackbonepie.helpers import TastyBackbonePieTableHelper


class BookTable(TastyBackbonePieTableHelper):
    uid = 'book_table'
    root_url = '/api/v1/book/'
    fields = [
        {
            'key': 'name',
            'label': 'Name',
        },
    ]


class TestView(TemplateView):
    template_name = 'test.html'

    def get_context_data(self, **kwargs):
        context = super(TestView, self).get_context_data(**kwargs)
        context['book_table'] = BookTable()
        return context
