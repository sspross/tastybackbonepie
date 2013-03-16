var TastybackbonepieCollection{{ id }} = Backbone.Tastypie.Collection.extend({
    urlRoot: "{{ root_url }}",
});

var TastybackbonepieTable{{ id }} = Backbone.View.extend({
    el: '#tastybackbonepie-table-{{ id }}',
    tt: '#tastybackbonepie-table-template-{{ id }}',
    al: '#tastybackbonepie-table-alert-{{ id }}',
    entries: new TastybackbonepieCollection{{ id }}(),
    parameters: {
        {% for default_filter in default_filters %}
            {{ default_filter.key }}: '{{ default_filter.value }}'{% if not forloop.last %},{% endif %}
        {% endfor %}
    },
    order_direction: '',
    getFetchOptions: function(){
        var that = this;
        return {
            success: function(entries){
                var t = _.template($(that.tt).html(), {entries: entries.models, meta: entries.meta, order_by: that.parameters.order_by, order_direction: that.order_direction});
                that.$el.html(t);
            },
            error: function(model, response){
                if (response.status != 400) {
                    $(that.al).html(JSON.parse(response.responseText).error_message);
                    $(that.al).removeClass('hidden');
                }
            }
        }
    },
    render: function(){
        _.extend(this.entries.filters, this.parameters);
        this.entries.fetch(this.getFetchOptions());
    },
    events: {
        'click .previous-{{ id }}': 'loadPrevious',
        'click .next-{{ id }}': 'loadNext',
        'click .page-{{ id }}': 'loadPage',
        'click .orderBy-{{ id }}': 'orderBy'
    },
    loadPrevious: function(event){
        event.preventDefault();
        if (this.entries.meta.previous != null) {
            _.extend(this.entries.filters, this.parameters);
            this.entries.fetchPrevious(this.getFetchOptions());
        }
    },
    loadNext: function(event){
        event.preventDefault();
        if (this.entries.meta.next != null) {
            _.extend(this.entries.filters, this.parameters);
            this.entries.fetchNext(this.getFetchOptions());
        }
    },
    loadPage: function(event){
        event.preventDefault();
        _.extend(this.entries.filters, this.parameters);
        var fetchOptions = this.getFetchOptions();
        fetchOptions.offset = $(event.currentTarget).attr('data-offset');
        this.entries.fetchOffset(fetchOptions);
    },
    orderBy: function(event){
        event.preventDefault();
        var parameters = {
            'order_by': $(event.currentTarget).attr('data-order_by')
        }
        _.extend(this.parameters, parameters);
        if (this.order_direction != '-') {
            this.order_direction = '-';
        }
        this.render();
    }
});

var {{ id }} = new TastybackbonepieTable{{ id }}();
{{ id }}.render();