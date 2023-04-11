# -*- coding: utf-8 -*-
###############################################################################
#
# Copyright (c) 2017-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
###############################################################################

from odoo import models, fields, api
import logging
_logger = logging.getLogger(__name__)


class TodoList(models.Model):
    _name = "todo.list"
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "Manage Todo Lists"
    _order = 'create_date desc'

    STATES = [
        ('draft', 'New'),
        ('pending', 'Pending'),
        ('done', 'Done'),
        ('cancel', 'Cancelled')
    ]

    FOLDED_STATES = [
        'cancel',
    ]

    active = fields.Boolean(default=True)
    name = fields.Char(
        string="Name", required=True, tracking=True)
    scheduled_date = fields.Date(
        string="Scheduled Date", tracking=True)
    project_id = fields.Many2one(
        'project.project', string="Project", tracking=True)
    state = fields.Selection(
        STATES, string="Status", default="draft", tracking=True)
    color = fields.Integer(string='Color Index')
    priority = fields.Selection([
        ('0', 'Normal'),
        ('1', 'High')
    ], default='0', index=True, tracking=True)
    description = fields.Html(string='Description')
    task_id = fields.Many2one("project.task", string="Related Task")

    def _read_group_fill_results(
            self, domain, groupby, remaining_groupbys, aggregated_fields,
            count_field, read_group_result, read_group_order=None):
        """
        The method seems to support grouping using m2o fields only,
        while we want to group by a simple status field.
        Hence the code below - it replaces simple status values
        with (value, name) tuples.
        """
        new_read_group_result = []
        if groupby == 'state':
            states = [result.get('state') for result in read_group_result]
            for state in self.STATES:
                if state[0] not in states:
                    read_group_result.append(
                        {'__count': 0, 'color': False,
                            'state': state[0], '__domain': [
                                (u'state', '=', state[0])]})
            for state in self.STATES:
                for result in read_group_result:
                    if result['state'] in self.FOLDED_STATES:
                        result['__fold'] = True
                    if state[0] == result.get('state'):
                        new_read_group_result.append(result)

        return super(TodoList, self)._read_group_fill_results(
            domain, groupby, remaining_groupbys, aggregated_fields,
            count_field, new_read_group_result, read_group_order
        )

    def mark_as_cancel(self):
        for obj in self:
            if obj.state != 'done':
                obj.state = 'cancel'

    def mark_as_pending(self):
        for obj in self:
            if obj.state == 'draft':
                obj.state = 'pending'

    def set_as_draft(self):
        for obj in self:
            if obj.state == 'cancel':
                obj.state = 'draft'

    def mark_as_done(self):
        for obj in self:
            if obj.state == 'pending':
                obj.state = 'done'

    def open_create_task(self):
        self.ensure_one()
        action = self.env.ref('odoo_todo_list.open_create_task').read()[0]
        context = self._context.copy()
        context.update({
            'default_project_id':self.project_id.id if self.project_id else False,
            'default_name':self.name,
            'default_description':self.description,
            'active_todo':self.id
         })
        action['context'] = context
        return action


class Project(models.Model):
    _inherit = "project.project"

    todos = fields.One2many('todo.list', 'project_id', string="Todo Lists")
    todo_count = fields.Integer(compute='_compute_todo_count')
    todo_ids = fields.One2many(
        'todo.list', 'project_id', string="Todo's",
        domain=[('state', '!=', 'done')])
    label_todo = fields.Char(
        string='Use Issues as', help="Customize the todo label, for example to \
        call them cases.", default="Todo's")
    todo_needaction_count = fields.Integer(
        compute="_todo_needaction_count")

    def _compute_todo_count(self):
        for project in self:
            project.todo_count = self.env['todo.list'].search_count([
                ('project_id', '=', project.id), ('state', '!=', 'done')])

    def _todo_needaction_count(self):
        todo_data = self.env['todo.list'].read_group([
            ('project_id', 'in', self.ids), ('message_needaction', '=', True)
            ], ['project_id'], ['project_id'])
        result = {
            data['project_id'][0]: data['project_id_count'] for data in todo_data
        }
        for project in self:
            project.todo_needaction_count = int(result.get(project.id, 0))

    def write(self, vals):
        res = super(Project, self).write(vals)
        if 'active' in vals:
            # archiving/unarchiving a project does it on its issues, too
            todos = self.with_context(active_test=False).mapped('todo_ids')
            todos.write({'active': vals['active']})
        return res

class Task(models.Model):
    _inherit = "project.task"

    @api.model
    def create(self, vals):
        res = super(Task, self).create(vals)
        if self._context.get('active_todo') and self._context.get(
                'active_model') == 'todo.list':
            active_todo = self.env[self._context.get(
                'active_model')].browse(self._context.get('active_todo'))
            active_todo.task_id = res.id
            active_todo.state = 'done'
        return res
