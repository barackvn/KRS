# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################


from odoo import _, api, fields, models


class QueueMessageWizard(models.TransientModel):
    _name = "queue.message.wizard"

    text = fields.Text(string='Message', readonly=True, translate=True)
