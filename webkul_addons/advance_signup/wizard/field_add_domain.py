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

from odoo import models,fields,api,_
from lxml import etree

class FieldAddDomain(models.TransientModel):
    _name ="field.add.domain"
    _description = "Field Add Domain"

    domain = fields.Char("Domain")

    @api.model
    def fields_view_get(self, view_id=None, view_type='form', toolbar=False, submenu=False):
        res = super(FieldAddDomain, self).fields_view_get(
            view_id=view_id, view_type=view_type, toolbar=toolbar, submenu=submenu)
        obj_relation = self._context.get("obj_relation")
        doc = etree.XML(res['arch'])
        for node in doc.xpath("//field[@name='domain']"):
            node.set('options', "{'model': %r}" % obj_relation)
        res['arch'] = etree.tostring(doc)
        return res

    def button_add_domain(self):
        obj = self.env['adv.signup.fields'].browse(self._context.get('active_ids'))
        for record in obj:
            record.field_domain =  self.domain
        return True
