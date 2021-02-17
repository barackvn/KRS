odoo.define('website_product_brands.tour', function(require) {
"use strict";
  var base = require('web_editor.base');
  var core = require('web.core');
  var tour = require('web_tour.tour');
  var _t = core._t;
  var options =  {
      test: true,
      url: "/web",
      rainbowMan: false,
      wait_for: base.ready(),
  };

  var seo_steps = [tour.STEPS.SHOW_APPS_MENU_ITEM, {
      trigger: '.o_app[data-menu-xmlid="website.menu_website_configuration"], .oe_menu_toggler[data-menu-xmlid="website.menu_website_configuration"]',

  }, {
      trigger: '.oe_menu_leaf[data-menu-xmlid="website_product_brands.menu_product_brand_config"]',
  }, {
      trigger: '.oe_kanban_global_click',
      extra_trigger: '.o_kanban_ungrouped',

  }, {
    trigger: '.o_form_button_edit',
    extra_trigger: '.o_form_view',
  }, {
      trigger: ".o_field_many2manytags input",
      extra_trigger: ".o_form_view",
      position: "top",
  }, {
      trigger: ".ui-menu-item > a",
      auto: true,
      in_modal: false,
  }, {
   trigger: '.o_form_button_save',
   extra_trigger: '.o_form_view',
 }, {
      trigger: '.o_app[data-menu-xmlid="website.menu_website_configuration"], .oe_menu_toggler[data-menu-xmlid="website.menu_website_configuration"]',

  }, {
      trigger: '.oe_menu_leaf[data-menu-xmlid="website_sale.menu_catalog_products"]',
  }, {
      trigger: '.o_facet_remove',
  }, {
      trigger: '.o_searchview input',
      position: "top",
  }, {
      trigger: "ul.o_searchview_autocomplete > li",
  },  {
      trigger: '.o_kanban_record:eq(0)',
  }, {
      trigger: '.o_form_button_edit',
      extra_trigger: '.o_form_view',
  }, {
      trigger: 'div[name="product_brand_id"] input',
      extra_trigger: '.o_form_view',
  },
];

tour.register('brands_tour', options ,seo_steps);

});
