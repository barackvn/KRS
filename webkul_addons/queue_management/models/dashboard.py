# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   "License URL : <https://store.webkul.com/license.html/>"
#
##########################################################################

from odoo import api, fields, models, _

import logging
_logger = logging.getLogger(__name__)


class QMSDashboard(models.Model):
    _name = 'qms.dashboard'
    _description = "Dashboard"


    @api.model
    def action_qms_dashboard_redirect(self):
        _logger.info("test---------------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:%r",self.env.user.has_group('queue_management.group_queue_manager'))
        if self.env.user.has_group('queue_management.group_queue_manager'):
            _logger.info("test---------------------------------@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@:%r",self.env.ref('queue_management.qms_backend_dashboard').read()[0])
            
            return self.env.ref('queue_management.qms_backend_dashboard').read()[0]
        return {
            'type': 'ir.actions.client',
            'name': 'Queue Management',
            'tag': 'reload',
            'params': {'menu_id': self.env.ref('queue_management.menu_queue_counters').id},
        }