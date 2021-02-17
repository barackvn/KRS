# -*- coding: utf-8 -*-
##########################################################################
# 2010-2017 Webkul.
#
# NOTICE OF LICENSE
#
# All right is reserved,
# Please go through this link for complete license : https://store.webkul.com/license.html
#
# DISCLAIMER
#
# Do not edit or add to this file if you wish to upgrade this module to newer
# versions in the future. If you wish to customize this module for your
# needs please refer to https://store.webkul.com/customisation-guidelines/ for more information.
#
# @Author        : Webkul Software Pvt. Ltd. (<support@webkul.com>)
# @Copyright (c) : 2010-2017 Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# @License       : https://store.webkul.com/license.html
#
##########################################################################

from odoo import api, fields, models, _
import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = 'website'

    @api.model
    def get_preorder_config_settings_values(self):
        """ this function retrn all configuration value for website Preorder module."""
        irmodule_obj = self.env['ir.module.module']
        result = irmodule_obj.sudo().search(
            [('name', 'in', ['website_preorder']), ('state', 'in', ['installed'])])

        res = super(Website,self).get_preorder_config_settings_values()
        if result:
            preorder_config_values = self.env['website.preorder.config.settings'].sudo(
            ).search([('is_active', '=', True)], limit=1)
            if preorder_config_values:
                res.update({'preorder_for_seller':preorder_config_values.preorder_for_seller,})
        return res

    @api.model
    def get_pre_order(self, product):
        res = super(Website,self).get_pre_order(product)
        active_id = self.get_preorder_config_settings_values()
        if active_id and not active_id.get('preorder_for_seller',False) and product.marketplace_seller_id:
            return False
        return res
