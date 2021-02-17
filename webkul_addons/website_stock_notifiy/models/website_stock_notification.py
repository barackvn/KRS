# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################
import logging

from odoo import api, fields, models, _
from odoo.exceptions import UserError

_logger = logging.getLogger(__name__)


class WebsiteStockNotify(models.Model):
    _name = "website.stock.notify"
    _inherit = ['mail.thread']
    _description = "Website Stock Notify"
    _order = 'create_date desc'

    @api.depends('wk_product')
    def _get_product_image_url(self):
        for record in self:
            if not record.product_image_url:
                image_url = self.env['website'].sudo().image_url(
                    record.wk_product, 'image_1920')
                record.product_image_url = image_url

    name = fields.Char(string='Name')
    email = fields.Char(string='Email')
    wk_user = fields.Many2one('res.users', string='User', track_visibility='always')
    wk_product = fields.Many2one('product.product', string='Product')
    wk_pageURL = fields.Char(string='PageURl')
    state = fields.Selection([('draft', 'Draft'),
                              ('cancel', 'Cancel'),
                              ('done', 'Done')
                              ], string='Status', default="draft", track_visibility='onchange')
    product_image_url = fields.Char(compute='_get_product_image_url', string="Product Image URL", store=True)

    @api.model
    def get_notification_config_settings_values(self):
        """ this function retrn all configuration value for website stock notify module."""

        res = {}
        stock_notify_config_values = self.env['website.notifiy.config.settings'].sudo(
        ).search([('is_active', '=', True)], limit=1)
        if stock_notify_config_values:
            res = {
                'wk_cron_confirm': stock_notify_config_values.wk_cron_confirm,
                'wk_cron_shedular': stock_notify_config_values.wk_cron_shedular,
                'wk_email_template': stock_notify_config_values.wk_email_template,
            }
        return res

    @api.model
    def create_stock_notify_record(self, product_id, email=False, user_id=False, pageURL=False, customer_name=None):
        if product_id:
            if not customer_name:
                customer_name = self.env['res.users'].browse(user_id).partner_id.name

            self.create({'name': customer_name,
                         'email': email,
                         'wk_product': product_id,
                         'wk_user': user_id,
                         'wk_pageURL': pageURL,
                         })
        return True

    
    def action_button_cancel(self):
        for current_record in self:
            current_record.state = 'cancel'
        return True

    
    def action_button_resend(self):
        for current_record in self:
            current_record.state = 'draft'
        return True

    @api.model
    def create_wizard(self):
        partial_id = self.env['wk.wizard.message'].create({'text': 'Mail has been sent Successfully!!!'})
        return {'name': "Message",
                'view_mode': 'form',
                'view_id': False,
                'res_model': 'wk.wizard.message',
                'res_id': partial_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
                }

    @api.model
    def send_email_cron(self):
        website_obj = self.env['website']
        config_vals = self.get_notification_config_settings_values()
        stock_config_vals = website_obj.get_config_settings_values()
        stock_location_id = stock_config_vals.get('wk_stock_location')
        wk_stock_type, mail_template, quantities = stock_config_vals.get('wk_stock_type'), config_vals.get('wk_email_template'), 0

        if self._context.get('active_ids'):
            self_obj = self.browse(self._context.get('active_ids', []))
        else:
            if config_vals.get('wk_cron_confirm'):
                self_obj = self.search([])
            else:
                self_obj = False

        if self_obj and mail_template:
            for obj in self_obj:
                if stock_config_vals.get('wk_warehouse_type') == 'specific':
                    product_obj = obj.with_context(location = int(stock_location_id)).wk_product
                else:
                    product_obj = obj.wk_product
                quantities = website_obj.get_product_stock_qty(product_obj, wk_stock_type)

                if quantities > 0:
                    if self._context.get('active_ids'):
                        if obj.state == 'draft':
                            mail_confirmed = mail_template.send_mail(obj.id, True)

                            if mail_confirmed:
                                obj.state = 'done'
                                return self.create_wizard()

                        elif self_obj.state == 'cancel':
                            raise UserError(_('Mail cannot be send, you have cancelled it!!'))
                        else:
                            raise UserError(_('Mail has alerady been sent!!'))
                    else:
                        if obj.state != 'done':
                            mail_confirmed = mail_template.send_mail(obj.id, True)

                            if mail_confirmed:
                                obj.state = 'done'
                            _logger.warning("Notify mail Send to the customer")
                        else:
                            _logger.warning("Notify mail already send to the customer.")
                else:
                    if self._context.get('active_ids'):
                        raise UserError(_('The quantity of the Product is less than zero, email cannot be send!!!'))
