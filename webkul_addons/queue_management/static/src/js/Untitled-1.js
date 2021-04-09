odoo.define('queue_management.backend.dashboard', function (require) {
    'use strict';

    var AbstractAction = require('web.AbstractAction');
    var ajax = require('web.ajax');
    var core = require('web.core');
    var Dialog = require('web.Dialog');
    var field_utils = require('web.field_utils');
    var session = require('web.session');
    var time = require('web.time');
    var web_client = require('web.web_client');
    
    var _t = core._t;
    var QWeb = core.qweb;
    
    var DATE_FORMAT = time.getLangDateFormat();
    var COLORS = ["#1f77b4", "#aec7e8"];
    var FORMAT_OPTIONS = {
        // allow to decide if utils.human_number should be used
        humanReadable: function (value) {
            return Math.abs(value) >= 1000;
        },
        // with the choices below, 1236 is represented by 1.24k
        minDigits: 1,
        decimals: 2,
        // avoid comma separators for thousands in numbers when human_number is used
        formatterCallback: function (str) {
            return str;
        },
    };

    var Dashboard = AbstractAction.extend({
        hasControlPanel: true,
        contentTemplate: 'queue_management.QMSDashboardMain',
        jsLibs: [
            '/web/static/lib/Chart/Chart.js',
        ],
        events: {
            'click .js_link_analytics_settings': 'on_link_analytics_settings',
            'click .o_dashboard_action': 'on_dashboard_action',
            'click .o_dashboard_action_form': 'on_dashboard_action_form',
        },

        init: function (parent, context) {
            this._super(parent, context);

            this.date_range = 'week';  // possible values : 'week', 'month', year'
            this.date_from = moment().subtract(1, 'week');
            this.date_to = moment();

            this.dashboards_templates = [
                'queue_management.dashboard_qms',
            ];
            this.chartIds = {};
            this.graphs = [
            { 'name': 'qms', 'type': 'line' }, 
            { 'name': 'qms', 'type': 'pie' }
        ]
        },

        willStart: function () {
            var self = this;
            return Promise.all([ajax.loadLibs(this), this._super()]).then(function () {
                return self.fetch_data();
            });
        },

        on_attach_callback: function () {
            this._isInDom = true;
            this.render_graphs();
            this._super.apply(this, arguments);
        },
        on_detach_callback: function () {
            this._isInDom = false;
            this._super.apply(this, arguments);
        },

        start: function () {
            var self = this;
            return this._super().then(function () {
                self.update_cp();
                self.render_dashboards();
                self.render_graphs();
                // self.$el.parent().addClass('oe_background_grey');
            });
        },

        /**
         * Fetches dashboard data
         */
        fetch_data: function () {
            var self = this;
            return this._rpc({
                route: '/queue_management/fetch_dashboard_data',
                params: {
                    dateFrom: this.date_from.year() + '-' + (this.date_from.month() + 1) + '-' + this.date_from.date(),
                    dateTo: this.date_to.year() + '-' + (this.date_to.month() + 1) + '-' + this.date_to.date(),
                },
            }).done(function (result) {
                self.data = result;
                self.dashboards_data = result.dashboards;
                self.tokens = result.tokens;
            });
        },

        render_dashboards: function () {
            var self = this;
            _.each(this.dashboards_templates, function (template) {
                self.$('.o_qms_dashboard_content').append(QWeb.render(template, { widget: self }));
            });
        },

        render_graph: function (divToDisplay, chartValues) {
            divToDisplay = divToDisplay + " svg";

            var self = this;
            nv.addGraph(function () {
                var chart = nv.models.lineChart()
                    .x(function (d) { return self.getDate(d); })
                    .y(function (d) { return self.getValue(d); })
                    .forceY([0]);
                chart
                    .useInteractiveGuideline(true)
                    .showLegend(false)
                    .showYAxis(true)
                    .showXAxis(true);

                var tick_values = self.getPrunedTickValues(chartValues[0].values, 5);

                chart.xAxis
                    .tickFormat(function (d) { return d3.time.format("%m/%d/%y")(new Date(d)); })
                    .tickValues(_.map(tick_values, function (d) { return self.getDate(d); }))
                    .rotateLabels(-45);

                chart.yAxis
                    .tickFormat(d3.format('.02f'));

                var svg = d3.select(divToDisplay);
                svg
                    .datum(chartValues)
                    .call(chart);

                nv.utils.windowResize(chart.update);
                return chart;
            });
        },

        render_pi_graph: function name(divToDisplay, chartValues) {
            divToDisplay = divToDisplay  + " svg";
            console.log(divToDisplay);
            console.log(chartValues);
            var data = [];
            nv.addGraph(function () {
                var chart = nv.models.pieChart()
                    .x(function (d) { return d.labels; })
                    .y(function (d) { return d.value; })
                    .labelType('percent')
                    .showLabels(true);

                d3.select(divToDisplay).datum(chartValues).transition(300).call(chart);
                return chart;
            });

        },

        render_graphs: function () {
            var self = this;
            _.each(this.graphs, function (e) {
                if (e.type == 'line') {
                    self.render_graph('#o_graph_' + e.name, self.dashboards_data[e.name].graph);
                } else if (e.type == 'pie') {
                    self.render_pi_graph('.o_graph_pi_' + e.name, self.dashboards_data[e.name].pi_graph);
                }
            });
        },

        on_date_range_button: function (date_range) {
            if (date_range === 'week') {
                this.date_range = 'week';
                this.date_from = moment().subtract(1, 'weeks');
            } else if (date_range === 'month') {
                this.date_range = 'month';
                this.date_from = moment().subtract(1, 'months');
            } else if (date_range === 'year') {
                this.date_range = 'year';
                this.date_from = moment().subtract(1, 'years');
            } else {
                console.log('Unknown date range. Choose between [week, month, year]');
                return;
            }

            var self = this;
            Promise.all([this.fetch_data()]).then(function () {
                self.$('.o_qms_dashboard_content').empty();
                self.render_dashboards();
                self.render_graphs();
            });

        },

        on_reverse_breadcrumb: function () {
            web_client.do_push_state({});
            this.update_cp();
        },

        on_dashboard_action: function (ev) {
            ev.preventDefault();
            var $action = $(ev.currentTarget);
            var nameAttr = $action.attr('name');
            var actionExtra = $action.data('extra');
            var actionLeft = document.getElementById('token_left').value;
            var additionalContext = {};
            var tokenList = true;
            if (actionExtra === 'td_queue') {
                additionalContext = { search_default_tdqueue: true,
                search_default_today : true};
            } else if (actionExtra === 'served') {
                additionalContext = { search_default_served: true,
                    search_default_today: true };
            } else if (actionExtra === 'cancel') {
                additionalContext = { search_default_cancel: true,
                    search_default_today: true };
            } else if (actionExtra === 'left') {
                additionalContext = {
                    search_default_draft: true,
                    search_default_today: true };
            } else if (actionExtra === 'all_token') {
                additionalContext = {};
            } else if (actionExtra === 'all_served') {
                additionalContext = {search_default_served: true};
            } else if (actionExtra === 'all_cancel') {
                additionalContext = {search_default_cancel: true};
            } else if (actionExtra === 'cu_session') {
                additionalContext = { search_default_open_sessions: true };
            } else if (actionExtra === 'to_counter') {
                additionalContext = {};
            } else {
                tokenList = false;
            }

            if (tokenList) {
                if (actionLeft && actionExtra === 'left' && actionLeft === '0') {
                    this.trigger_up('show_effect', {
                        type: 'rainbow_man',
                        message: _t('Congratulations, your queue is empty!'),
                        click_close: false,
                    });
                } else {
                    this.do_action(nameAttr, { 
                        additional_context: additionalContext,
                        on_reverse_breadcrumb: this.on_reverse_breadcrumb });
                }
            } else {
                if (this.date_range === 'week') {
                    additionalContext = { search_default_week: true };
                } else if (this.date_range === 'month') {
                    additionalContext = { search_default_month: true };
                } else if (this.date_range === 'year') {
                    additionalContext = { search_default_year: true };
                }
                this.do_action($action.attr('name'), {
                    additional_context: additionalContext,
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb
                });
            }
        },

        on_line_pie_action : function (ev) {
            ev.preventDefault();
            var graphType = $(ev.currentTarget).data('extra');
            var line = document.getElementById("o_graph_qms");
            var lineButton = document.getElementById("line_button");
            var pie = document.getElementById("o_graph_pi");
            var pieButton = document.getElementById("pi_button");
            if (graphType === 'pie') {
                line.style.display = 'none';
                lineButton.classList.remove('active');
                pie.style.display = 'initial';
                pieButton.classList.add('active');
            } else if (graphType === 'line') {
                line.style.display = 'initial';
                lineButton.classList.add('active');
                pie.style.display = 'none';
                pieButton.classList.remove('active');
            }
        },

        on_top_dept: function (ev) {
            ev.preventDefault();

            var deptid = $(ev.currentTarget).data('deptartmentId');
            this.do_action({
                type: 'ir.actions.act_window',
                res_model: 'department.department',
                res_id: deptid,
                views: [[false, 'form']],
                target: 'current',
            }, {
                    on_reverse_breadcrumb: this.on_reverse_breadcrumb,
                });
        },

        update_cp: function () {
            var self = this;
            if (!this.$searchview) {
                this.$searchview = $(QWeb.render("queue_management.DateRangeButtons", {
                    widget: this,
                }));
                this.$searchview.click('button.js_date_range', function (ev) {
                    self.on_date_range_button($(ev.target).data('date'));
                    $(this).find('button.js_date_range.active').removeClass('active');
                    $(ev.target).addClass('active');
                });
            }
            this.updateControlPanel({
                cp_content: {
                    $searchview: this.$searchview,
                },
                // breadcrumbs: this.getParent().get_breadcrumbs(),
            });
        },
        formatValue: function (value) {
            var formatter = field_utils.format.float;
            var formatedValue = formatter(value, undefined, FORMAT_OPTIONS);
            return formatedValue;
        },
        getDate: function (d) { return new Date(d[0]); },
        getValue: function (d) { return d[1]; },
        getPrunedTickValues: function (ticks, nb_desired_ticks) {
            var nb_values = ticks.length;
            var keep_one_of = Math.max(1, Math.floor(nb_values / nb_desired_ticks));

            return _.filter(ticks, function (d, i) {
                return i % keep_one_of === 0;
            });
        },

    });
    core.action_registry.add('qms_backend_dashboard', Dashboard);

    return Dashboard;
});
