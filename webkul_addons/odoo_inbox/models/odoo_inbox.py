# -*- coding: utf-8 -*-

from odoo import models


class OdooInbox(models.AbstractModel):
    _name = 'odoo.inbox'
    _description = "Inbox"

    def set_done(self, message=None):
        message.message_label = 'done'

    def set_star(self, action=None, message=None):
        message.message_label = 'starred' if action == 'add' else 'inbox'

    def move_to_send(self, action=None, message=None):
        message.message_label = 'sent' if action == 'add' else 'inbox'

    def move_to_trash(self, message=None):
        message.message_label = 'trash'
