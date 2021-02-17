# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
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
##########################################################################
from odoo import api, models, fields
from odoo.exceptions import UserError

class ProjectTimesheetWizard(models.TransientModel):

    _name = 'project.timesheet.wizard'
    _description = "Project Timesheet Wizard"

    from_date = fields.Date(string='From Date', default=fields.Date.context_today, required=True)
    to_date = fields.Date(string='To Date', default=fields.Date.context_today, required=True)


    def action_sent_report(self):
        if self.from_date > self.to_date:
            raise UserError(_('From date must be smaller than To date'))
        template = self.env['ir.model.data'].xmlid_to_object(
                    'project_timesheet_reports.email_template_edi_timesheet')
        if template:
            template.with_context({'from_date':self.from_date,'to_date':self.to_date}).send_mail(self._context.get('active_id'), force_send=True)
