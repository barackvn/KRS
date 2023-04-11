# -*- coding: utf-8 -*-
#################################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# License URL : https://store.webkul.com/license.html/
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

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)

class MassUploadStatus(models.TransientModel):
    _name = 'mass.upload.status'

    passed_rec = fields.Integer()
    message = fields.Text()

    def view_history(self):
        res_model = False
        view_id = False
        if self._context.get('active_model') == 'mass.inventory.upload':
            view_id = self.sudo().env.ref('marketplace_mass_upload.inventory_mass_upload_form_view').read()[0]['id']
            res_model = 'mass.inventory.upload'

        if self._context.get('active_model') == 'mass.product.upload':
            view_id = self.sudo().env.ref('marketplace_mass_upload.product_mass_upload_form_view').read()[0]['id']
            res_model = 'mass.product.upload'

        return {
            'type': 'ir.actions.act_window',
            'res_model': res_model,
            'view_mode': 'form',
            'context': {'mass_upload_view': True},
            'view_id': view_id,
            'res_id': self._context.get('active_id'),
        }
