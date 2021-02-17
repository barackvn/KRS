# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import fields,models,api,http
from odoo.tools.safe_eval import safe_eval
import logging
_logger = logging.getLogger(__name__)


class website(models.Model):
    """ this model make these fields avilable on front end template """
    _inherit='website'

    def wk_get_ajax_config(self):
        res =  self.env["res.config.settings"].sudo().get_values()
        res['social_enabled'] = (res.get('website_gmail_login')
            or res.get('website_facebook_login')
            or res.get('website_odoo_login'))
        auth_signup_uninvited = self.env['res.users']._get_signup_invitation_scope()
        res.update({'auth_signup_uninvited': auth_signup_uninvited})
        return res

    @api.model
    def wk_get_social_enabled(self):
        web_config_obj = self.wk_get_ajax_config()
        return web_config_obj['social_enabled']

    @api.model
    def get_db_list(self):
        return http.db_list()

    @api.model
    def get_wk_block_ui_info(self):
        web_config_obj = self.env["res.config.settings"].sudo().get_values()
        return web_config_obj.get("wk_block_ui")

    @api.model
    def get_enable_reset_password(self):
        return safe_eval(self.env['ir.config_parameter'].sudo().get_param('auth_signup.reset_password', 'False'))
