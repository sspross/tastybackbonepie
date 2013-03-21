!function($){

    "use strict"; // jshint ;_;

    /* TastyBackbonePie PUBLIC CLASS DEFINITION
     * ======================================== */

    var TastyBackbonePie = function (element, options) {
        this.$element = $(element)
        this.options = $.extend({}, $.fn.tastybackbonepie.defaults, options)
        this.uid = this.options.uid || this.uid
        this.urlRoot = this.options.urlRoot || this.urlRoot
        this.fields = this.options.fields || this.fields
        this.additionalFields = this.options.additionalFields || this.additionalFields
        this.defaultParameters = this.options.defaultParameters || this.defaultParameters
        this.template = this.options.template || this.template
        this.templateError = this.options.templateError || this.templateError
        this.collection = Backbone.Tastypie.Collection.extend({
            urlRoot: this.urlRoot
        });
        this.view = Backbone.View.extend({
            el: this.$element,
            al: '#alert-' + this.uid,
            entries: new this.collection(),
            parameters: this.defaultParameters || {},
            order_direction: '',
            getFetchOptions: function(){
                var that = this;
                return {
                    success: function(entries){
                        var t = _.template(template, {
                            id: this.uid,
                            fields: this.fields, 
                            additional_html_fields: this.additional_html_fields,
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
                        var t = _.template(template_error, {message: message});
                        $(that.al).html(t);
                    }
                }
            },
            events: {},
            render: function(){
                _.extend(this.entries.filters, this.parameters);
                this.entries.fetch(this.getFetchOptions());
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
    }

    /* TastyBackbonePie TEMPLATE DEFINITIONS
     * ===================================== */

	var PAGINATION_PARTIAL = ' \
    		<ul> \
    			<li<% if (meta.previous == null) { %> class="disabled"<% } %>><a href="#" class="previous-<%= id %>">«</a></li> \
    			<% for (var i=0, len=Math.ceil(meta.total_count / meta.limit); i < len; i++) { %> \
    			    <li<% if (meta.offset / meta.limit == i) { %> class="active"<% } %>><a href="#" class="page-<%= id %>" data-offset="<%= meta.limit * i  %>"><%= i + 1 %></a></li> \
    			<% } %> \
    			<li<% if (meta.next == null) { %> class="disabled"<% } %>><a href="#" class="next-<%= id %>">»</a></li> \
    		</ul> \
    	',
	    HTML_TEMPLATE = '\
    		<div class="pagination pagination-small"> \
    		' + PAGINATION_PARTIAL + ' \
    		</div> \
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
    	    <div class="pagination pagination-small"> \
    		' + PAGINATION_PARTIAL + ' \
    		</div> \
	    ',
        ERROR_TEMPLATE = '\
            <div class="alert alert-warning hidden"><%= message %></div> \
        ';

    TastyBackbonePie.prototype = {

        constructor: TastyBackbonePie,



	$.fn.renderTastyBackbonePieTable = function(this) {
        
        var element = this,
            template = settings.tpl_pagination || HTML_TEMPLATE,
            template_error = settings.template_error || ERROR_TEMPLATE;

        
        
        

        element.view.prototype.events['click .previous-' + settings.uid] = 'loadPrevious';
        element.view.prototype.events['click .next-' + settings.uid] = 'loadNext';
        element.view.prototype.events['click .page-' + settings.uid] = 'loadPage';
        element.view.prototype.events['click .orderBy-' + settings.uid] = 'orderBy';
        
        element.table = new element.view();
        element.table.render();
        
        return element.table;

	};
})( jQuery );