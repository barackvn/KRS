# -*- coding: utf-8 -*-
from odoo import fields, models


class MessageFolder(models.Model):
    _name = "message.folder"
    _description = "Message Folder"

    name = fields.Char(string='Folder Name')
    user_id = fields.Many2one('res.users', 'Owner', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Responsible', related='user_id.partner_id', readonly=True)
