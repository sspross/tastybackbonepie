from django.template.loader import render_to_string


class TastyBackbonePieTableHelper(object):
    uid = ''
    root_url = ''
    fields = []
    additional_html_fields = []
    html_template = 'tastybackbonepie/ajax_table.html'
    js_template = 'tastybackbonepie/ajax_table.js'
    default_filters = []

    def render_html(self):
        return render_to_string(self.html_template, {
            'id': self.uid,
            'fields': self.fields,
            'additional_html_fields': self.additional_html_fields,
        })

    def render_js(self):
        return render_to_string(self.js_template, {
            'id': self.uid,
            'fields': self.fields,
            'root_url': self.root_url,
            'default_filters': self.default_filters,
        })
