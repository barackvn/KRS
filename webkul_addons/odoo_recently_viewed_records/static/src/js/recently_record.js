odoo.define('odoo_recently_viewed_records.get_view_url', function (require) {
    "use strict";
    var FormRenderer = require('web.FormRenderer');
    var ajax = require('web.ajax');
    FormRenderer.include({
        _updateView: function(e) {
    //			inherit method to be able to display an alert if
    //			method called returns a string
                var self = this;
                this._super.apply(this, arguments);
                var name =  this.state.data.display_name;
                var url = window.location.href;    //this.$el.context.baseURI;
                var components = URI.parse(url);
                console.log(this.state.data)
                console.log(components)
                var query = URI.parseQuery(components['fragment']);
                var action = query['action']


                // var params = url.extract();
                console.log(query);
                ajax.jsonRpc("/recently/view/records", 'call', {'name':name,'url':url,'action':parseInt(action) || false,'record_id':this.state.data.id,'model':this.state.model}).then(
                    function(data) {
                        console.log(data['status'])
                        if (data['status']){
                            location.reload()
                        }
                        }

                    );
            },
        });
    
    })