# -*- coding: utf-8 -*-
from odoo import fields, models


class MessageTag(models.Model):
    _name = "message.tag"
    _description = "Message Tag"

    name = fields.Char(string='Tag Name')
    user_id = fields.Many2one('res.users', 'Owner', default=lambda self: self.env.user)
    partner_id = fields.Many2one('res.partner', string='Responsible', related='user_id.partner_id', readonly=True)
