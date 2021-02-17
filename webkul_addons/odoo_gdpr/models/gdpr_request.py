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
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
from odoo import models, fields,api,_

# USER_FIELDS= ["name"]

PARTNER_FIELDS = ["name","street","street2","city","zip","company_name","email","phone"]
PARTNER_RELATED_FIELDS = ["state_id","country_id"]

# PARTNER_ADDRESS_FIELD =["child_ids"]

def GetWipedVals():
    vals={}
    for field in PARTNER_FIELDS:
        vals.update({field : "N/A"})
    for field in PARTNER_RELATED_FIELDS:
        vals.update({field : False})
    return vals

class OdooGdpr(models.Model):
    _name = "gdpr.request"

    name = fields.Char(string="Name",compute="_getname")
    partner_id = fields.Many2one('res.partner',String="Customer",required=True)
    operation_type = fields.Selection([('all',"All Objects"),("object","Specific Object")],default="all",required=True,String="Operation For",help="Request for specific model or all")
    object_id = fields.Many2one('gdpr.data.template', 'Object Name')
    action_type = fields.Selection([('download',"Download"),("delete","Delete")],String="Action Type",required=True,help="Request for download or delete action")
    state = fields.Selection([('pending',"Pending"),("cancel","Cancel"),("done","Done")],String="State",default="pending")
    created_on = fields.Datetime(String="Created On",default=lambda self: fields.Datetime.now(),readonly=True)
    website_action_type = fields.Char(string="Website Action ",compute="_getWebsite_action_type")
    attachment = fields.Binary(String="Attachment File")
    file_name = fields.Char('Filename')
    is_wiped = fields.Boolean(default=False,String="is Wipe")
    attach_id = fields.Many2one("ir.attachment",String="Attachment Id" )

    # @api.multi
    def write(self,vals):
        if vals.get("attachment"):
            for gdpr_request in self:
                if gdpr_request.attach_id:
                    gdpr_request.attach_id.unlink()

                attachmentValue = {
                    'name': vals.get('file_name', 'Details'),
                    'datas': vals.get("attachment"),
                    'res_model': gdpr_request._name,
                    'res_id': gdpr_request.id,
                    'type': 'binary',
                    'db_datas': 'Details',
                    'datas_fname': vals.get('file_name', 'Details'),
                    'res_name': gdpr_request.name,
                }
                attach_id = gdpr_request.env['ir.attachment'].create(attachmentValue)
            vals.update({"attach_id":attach_id.id})
        result=super(OdooGdpr,self).write(vals)
        return result

    @api.onchange('attachment')
    def _check_attachment(self):
        if not self.attachment:
            self.state = 'pending'


    def action_cancel(self):
        self.state = "cancel"

    def action_done_download(self):
        if self.attachment and self.action_type == "download":
            self.state = "done"
        else:
            raise UserError(_("Please attach the File before Mark As Done." ))

    def action_done_delete(self):
        if self.action_type == "delete" and self.is_wiped:
             self.state = "done"
        else:
            raise UserError(_("Please Wiped(Reset) all data before Mark As Wiped." ))


    def create_data(self):
        pass

    def _removeAddress(self):
        for address in self.partner_id.child_ids:
            # if address.type == "delivery":
            address.write(GetWipedVals())

    def wipe_data(self):
        if self.state in ["pending","cancel"]:
            result = 0
            if self.action_type == "delete":
                if self.operation_type == "all":
                    self.partner_id.write(GetWipedVals())
                    self._removeAddress()
                    result += 1
                elif self.operation_type == "object":
                    if self.object_id.type == "user":
                        self.partner_id.write(GetWipedVals())
                        result += 1
                    elif self.object_id.type == "address":
                        self._removeAddress()
                        result += 1
            if result > 0:
                self.is_wiped = True

    # @api.multi
    def _getname(self):
        for o in self:
            o.name = "All Object" if not o.object_id else o.object_id.name

    # @api.multi
    def _getWebsite_action_type(self):
        for o in self:
            o.website_action_type = "Request for DATA DOWNLOAD" if o.action_type == "download" else "Request for DATA REMOVAL"
