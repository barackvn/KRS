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
from odoo import api, models

class TaskTimesheetReport(models.AbstractModel):
    _name = 'report.project_timesheet_reports.task_timesheet_report'
    _description = "Task Timesheet Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        tasks = self.env['project.task'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'project.task',
            'docs': tasks,
            'data': data,
        }

class ProjectTaskTimesheetReport(models.AbstractModel):
    _name = 'report.project_timesheet_reports.project_task_timesheet_report'
    _description = "Project Task Timesheet Report"

    @api.model
    def _get_report_values(self, docids, data=None):
        tasks = self.env['project.project'].browse(docids)

        return {
            'doc_ids': docids,
            'doc_model': 'project.project',
            'docs': tasks,
            'data': data,
        }

class ReportProjectTimesheet(models.AbstractModel):
    _name = 'report.project_timesheet_reports.report_project_timesheet'
    _description = "Report Project Timesheet"

    def get_project_timesheet(self, projects, from_date,end_date):
        res = {}
        for project in projects:
            res.setdefault(project.id, [])
            timesheet_ids = self.env['account.analytic.line'].search([('project_id','=',project.id),('date','>=',from_date),('date','<=',end_date)])
            res[project.id].append({
                        'timesheet_ids': timesheet_ids,
                    })
        return res

    @api.model
    def _get_report_values(self, docids, data=None):
        projects = self.env['project.project'].browse(docids)
        return {
            'doc_ids': docids,
            'doc_model': 'project.project',
            'docs': projects,
            'data': data,
            'timesheets':self.get_project_timesheet(projects,self._context.get('from_date'),self._context.get('to_date'))
        }
