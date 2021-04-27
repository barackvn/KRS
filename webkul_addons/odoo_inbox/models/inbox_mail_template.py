# -*- coding: utf-8 -*-
from odoo import _, api, fields, models


class InbxoMailTemplate(models.Model):
    _name = 'inbox.mail.template'
    _description = "Inbox mail template"
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(string='Name')
