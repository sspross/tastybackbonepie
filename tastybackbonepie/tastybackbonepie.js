(function($, _, Backbone){

    window.TastyBackbonePieTable = function(element, options) {
        this.$element = element;
        this.url = null;
        this.uid = null;
        this.fields = null;
        this.additionalHtmlFields = [];
        this.hasPaginationTop = true;
        this.hasPaginationBottom = true;
        this.legendHtml = '';
        this.defaultFilters = {};
        this.paginationTemplate = '\
                <div class="pagination pagination-small"> \
                    <ul> \
                        <li<% if (meta.previous == null) { %> class="disabled"<% } %>><a href="#" class="previous-<%= id %>">«</a></li> \
                        <% for (var i=0, len=Math.ceil(meta.total_count / meta.limit); i < len; i++) { %> \
                            <li<% if (meta.offset / meta.limit == i) { %> class="active"<% } %>><a href="#" class="page-<%= id %>" data-offset="<%= meta.limit * i  %>"><%= i + 1 %></a></li> \
                        <% } %> \
                        <li<% if (meta.next == null) { %> class="disabled"<% } %>><a href="#" class="next-<%= id %>">»</a></li> \
                    </ul> \
                </div> \
            ';
        this.tableTemplate = '\
                <div id="alert-<%= id %>"></div> \
                <table class="table table-bordered table-striped table-hover"> \
                    <tr> \
                        <% _.each(fields, function(field) { %> \
                            <th> \
                                <% if (field.order_by) { %> \
                                    <a href="#" class="orderBy-<%= id %>" data-order_by="<% if (order_by == field.order_by) { %><%= order_direction %><% } %><%= field.order_by %>"> \
                                <% } %> \
                                <%= field.label %> \
                                <% if (field.order_by) { %> \
                                    </a> \
                                <% } %> \
                            </th> \
                        <% }) %> \
                        <% _.each(additional_html_fields, function(additional_html_field) { %> \
                            <th></th> \
                        <% }) %> \
                    </tr> \
                    <% _.each(entries, function(entry) { %> \
                        <tr> \
                            <% _.each(fields, function(field) { %> \
                                <td> \
                                    <% if (field.template) { %> \
                                        <%= _.template(field.template, {entry: entry}) %> \
                                    <% } else { %> \
                                        <%= entry.get(field.key) %> \
                                    <% } %> \
                                </td> \
                            <% }) %> \
                            <% _.each(additional_html_fields, function(additional_html_field) { %> \
                                <td><%= _.template(additional_html_field, {entry: entry}) %></td> \
                            <% }) %> \
                        </tr> \
                    <% }) %> \
                </table> \
            ';
        this.errorTemplate = '<div class="alert alert-warning hidden"><%= message %></div>';
        for (var key in options) {
            this[key] = options[key];
        }
        this.table = this.createTable();
        this.table.render();
        return this.table;
    };

    window.TastyBackbonePieTable.prototype = {
        createTable: function() {
            var self = this;
            this.tableTemplate = (this.hasPaginationTop ? this.paginationTemplate : '') + 
                                 (this.tableTemplate) + 
                                 (this.legendHtml ? this.legendHtml : '') + 
                                 (this.hasPaginationBottom ? this.paginationTemplate : '');
            this.collection = Backbone.Tastypie.Collection.extend({
                urlRoot: self.url
            });
            this.view = Backbone.View.extend({
                el: self.$element,
                al: '#alert-' + self.uid,
                entries: new self.collection(),
                parameters: self.defaultFilters,
                order_direction: '',
                getFetchOptions: function(){
                    var that = this;
                    return {
                        success: function(entries){
                            var e = $.Event('fetched', {
                                entries: entries.models
                            });
                            that.$el.trigger(e);
                            var t = _.template(self.tableTemplate, {
                                id: self.uid,
                                fields: self.fields, 
                                additional_html_fields: self.additionalHtmlFields,
                                entries: entries.models, 
                                meta: entries.meta,
                                order_by: that.parameters.order_by, 
                                order_direction: that.order_direction
                            });
                            that.$el.html(t);
                        },
                        error: function(model, response){
                            var json = JSON.parse(response.responseText);
                            var message = json.error || json.error_message || 'Error';
                            var t = _.template(self.errorTemplate, {message: message});
                            $(that.al).html(t);
                        }
                    };
                },
                events: {},
                render: function(){
                    _.extend(this.entries.filters, this.parameters);
                    this.entries.fetch(this.getFetchOptions());
                },
                loadPrevious: function(event){
                    event.preventDefault();
                    if (this.entries.meta.previous !== null) {
                        _.extend(this.entries.filters, this.parameters);
                        this.entries.fetchPrevious(this.getFetchOptions());
                    }
                },
                loadNext: function(event){
                    event.preventDefault();
                    if (this.entries.meta.next !== null) {
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
                    };
                    _.extend(this.parameters, parameters);
                    if (this.order_direction != '-') {
                        this.order_direction = '-';
                    }
                    this.render();
                },
                extendParameters: function(parameters){
                    _.extend(this.parameters, parameters);
                },
                setParameter: function(key, value){
                    this.parameters[key] = value;
                },
                removeParameter: function(key){
                    delete this.parameters[key];
                    delete this.entries.filters[key];
                }
            });
            this.view.prototype.events['click .previous-' + this.uid] = 'loadPrevious';
            this.view.prototype.events['click .next-' + this.uid] = 'loadNext';
            this.view.prototype.events['click .page-' + this.uid] = 'loadPage';
            this.view.prototype.events['click .orderBy-' + this.uid] = 'orderBy';
            return new this.view();
        }
    };

})(window.jQuery, window._, window.Backbone);