# -*- coding: utf-8 -*-
#################################################################################
#
#    Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################
from odoo import fields, models
from odoo import api

import logging
_logger = logging.getLogger(__name__)


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    website_odoo_login = fields.Boolean("Odoo Login")
    website_facebook_login = fields.Boolean("Facebook Login")
    facebook_client_id = fields.Char("Facebook App ID")
    show_ajax_form_always = fields.Boolean("Pop Up Ajax form if user not logged in, on every web page.")
    wk_block_ui = fields.Boolean("Don't allow user to close the Ajax Pop Up form without login.")

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        facebook_id = self.env.ref('auth_oauth.provider_facebook',False )
        odoo_id =  self.env.ref('auth_oauth.provider_openerp')
        IrDefault = self.env['ir.default'].sudo()
        show_ajax_form_always = IrDefault.get('res.config.settings', 'show_ajax_form_always')
        wk_block_ui = IrDefault.get('res.config.settings', 'wk_block_ui')
        website_odoo_login =IrDefault.get('res.config.settings', 'website_odoo_login')
        res.update(
            website_odoo_login = odoo_id.enabled,
            website_facebook_login =  facebook_id.enabled,
            facebook_client_id =  facebook_id.client_id,
            show_ajax_form_always =  show_ajax_form_always,
            wk_block_ui =  wk_block_ui
        )
        return res


    def set_values(self):
        super(ResConfigSettings, self).set_values()
        icp = self.env['ir.config_parameter']
        IrDefault = self.env['ir.default'].sudo()
        IrDefault.set('res.config.settings', 'website_odoo_login', self.website_odoo_login)
        IrDefault.set('res.config.settings', 'show_ajax_form_always', self.show_ajax_form_always)
        IrDefault.set('res.config.settings', 'wk_block_ui', self.wk_block_ui)
        facebook_id = self.env.ref('auth_oauth.provider_facebook', False)
        if facebook_id:
            facebook_id.write({
                'enabled': self.website_facebook_login,
                'client_id': self.facebook_client_id,
            })
        odoo_id = self.env.ref('auth_oauth.provider_openerp', False)
        if odoo_id:
            odoo_id.write({
                'enabled': self.website_odoo_login,
            })
