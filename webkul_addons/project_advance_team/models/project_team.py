# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2016-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# License URL :<https://store.webkul.com/license.html/>
##########################################################################

from odoo import api, fields, models, exceptions, _
from odoo.exceptions import UserError, ValidationError


class ProjectTaskType(models.Model):
    _inherit = 'project.task.type'
    _description = 'Task Stage'
    _order = 'sequence, id'


    def _check_unique_name(self):
        """ verifies unique name. """
        for stage in self:
            if stage_ids := self.search(
                [('name', 'ilike', stage.name), ('id', '!=', stage.id)]
            ):
                raise ValidationError(_('Name must be Unique.'))

    @api.model
    def create(self, vals):
        name = str(vals.get('name')).strip()
        vals.update({'name': name})
        res = super(ProjectTaskType, self).create(vals)
        res._check_unique_name()
        return res

    def unlink(self):
        for obj in self:
            if obj.name.lower() in ["done", "cancel", "cancelled"]:
                raise UserError(_(
                    "You are not allowed to Delete the 'Done' and 'Cancel' Stage."))
        return super(ProjectTaskType, self).unlink()

    def write(self, vals):
        if vals.get('name'):
            for obj in self:
                if vals.get('name') != obj.name:
                    if obj.name.lower() in ["done", "cancel", "cancelled"]:
                        raise UserError(_(
                            "You are not allowed to modify the 'Done' and 'Cancel' Stage."))
                    obj._check_unique_name()
                    name = vals.get('name').strip()
                    vals.update({'name': name})
        return super(ProjectTaskType, self).write(vals)


class ProjectStageGroup(models.Model):

    _name = "project.stage.group"
    _description = "Project Stages Group"

    name = fields.Char(string="Name", required=True)
    stages_ids = fields.Many2many(
        'project.task.type', 'project_group_type_rel',
        'group_id', 'type_id', string='Tasks Stages')
    default = fields.Boolean(string="Use as Default", help="")
    sequence = fields.Integer(string="Sequence", default=1)


class ProjectProject(models.Model):

    _inherit = 'project.project'
    _order = "write_date desc"

    @api.model
    def get_default_stage(self):
        return self.env['project.task.type'].search(
            [('fold', '=', False)]).ids or False

    @api.model
    def get_default_stage_group(self):
        return self.env['project.stage.group'].search(
            [('default', '=', True)], limit=1).id or False

    wk_team_id = fields.Many2one(
        comodel_name="wk.team", string="Team",
        help="Default team of this project", tracking=True,)
    wk_extra_team_ids = fields.Many2many(
        "wk.team", "project_teams", "project_id", "team_id",
        string="Extra Teams",
        help="You may add extra team which will also be involved in this \
        project", tracking=True,)
    members = fields.Many2many('res.users', 'project_members', 'project_id',
                               'user_id', 'Extra Members', help="""Project's
                               members are users who can have an access to
                               the tasks related to this project.""",
                               tracking=True,)
    type_ids = fields.Many2many('project.task.type', 'project_task_type_rel',
                                'project_id', 'type_id', string='Tasks Stages',
                                tracking=True,)
    stage_group_id = fields.Many2one(
        'project.stage.group', string="Stage Group",
        default=get_default_stage_group, tracking=True,)

    def _get_many2many_track_visibility_names(self, values):
        return ', '.join([k.name for k in values])

    @api.onchange('stage_group_id')
    def onchange_stage_group_id(self):
        if self.stage_group_id:
            self.type_ids = [(6, 0, self.stage_group_id.stages_ids.ids)]
        else:
            self.type_ids = False

    def write(self, vals):
        old_members = self._get_many2many_track_visibility_names(self.members)
        old_teams = self._get_many2many_track_visibility_names(
            self.wk_extra_team_ids)
        res = super(ProjectProject, self).write(vals)
        new_members = self._get_many2many_track_visibility_names(self.members)
        new_teams = self._get_many2many_track_visibility_names(
            self.wk_extra_team_ids)
        if not self.wk_team_id and not self.wk_extra_team_ids and not self.members:
            raise UserError(
                _("Oops!!! you haven't configured any team or extra members for this project. So please do it otherwise you won't be able to assign any task of this project to your team members."))
        if vals.get('stage_group_id'):
            self.type_ids = [(6, 0, self.stage_group_id.stages_ids.ids)]
        if old_members != new_members:
            self.message_post(body=f"<b>Members:</b> {old_members} &#8594; {new_members}")
        if old_teams != new_teams:
            self.message_post(body=f"<b>Extra Teams:</b> {old_teams} &#8594; {new_teams}")

        return res

    @api.model
    def create(self, vals):
        if not vals.get("wk_team_id") and not vals.get("wk_extra_team_ids") and not vals.get("members"):
            raise UserError(
                _("Oops!!! you haven't configured any team or extra members for this project. So please do it otherwise you won't be able to assign any task of this project to your team members."))
        res = super(ProjectProject, self).create(vals)
        if not res.type_ids:
            res.type_ids = [(6, 0, res.stage_group_id.stages_ids.ids)]
        return res


class Task(models.Model):

    _inherit = "project.task"
    _order = "write_date desc"

    @api.model
    def get_user_domin(self):
        users = [self._uid]
        if self.project_id:
            if self.project_id.user_id:
                users.append(self.project_id.user_id.id)
            if self.project_id.members:
                users += self.project_id.members.ids
            if self.project_id.sudo().wk_team_id:
                users.append(self.project_id.sudo().wk_team_id.manager.id)
                users += self.project_id.sudo().wk_team_id.members.ids
            if self.project_id.sudo().wk_extra_team_ids:
                for team_id in self.project_id.sudo().wk_extra_team_ids:
                    users.append(team_id.manager.id)
                    users += team_id.members.ids
        return list(set(users))

    @api.model
    def get_default_stage_group(self):
        return (
            self.env['project.stage.group']
            .search([('default', '=', True), ('stages_ids', '!=', False)], limit=1)
            .id
            or self.env['project.stage.group']
            .search([('stages_ids', '!=', False)], limit=1)
            .id
        )

    @api.onchange('project_id')
    def _onchange_project(self):
        users = self.get_user_domin()
        if self.project_id:
            self.partner_id = self.project_id.partner_id
            self.stage_id = self.stage_find(
                self.project_id.id, [('fold', '=', False)])
            self.stage_group_id = self.project_id.stage_group_id or False
            self.user_id = False
            return {'domain': {
                'stage_id': [('id', 'in', self.project_id.type_ids.ids)],
                'user_id': [('id', 'in', users)]}}
        else:
            self.user_id = self._uid
            if self.stage_group_id.stages_ids:
                self.stage_id = self.stage_group_id.stages_ids.ids[0]
                return {'domain': {
                    'stage_id': [
                        ('id', 'in', self.stage_group_id.stages_ids.ids)],
                    'user_id': [('id', 'in', users)]}}
            return {'domain': {'user_id': [('id', 'in', users)]}}

    @api.onchange('stage_group_id')
    def onchange_stage_group_id(self):
        if not self.project_id and self.stage_group_id:
            if self.stage_group_id.stages_ids:
                self.stage_id = self.stage_group_id.stages_ids.ids[0]
                return {'domain': {
                    'stage_id': [
                        ('id', 'in', self.stage_group_id.stages_ids.ids)]}}
        elif not self.project_id:
            self.stage_id = False
            return {'domain': {'stage_id': [('id', 'in', [])]}}
        elif self.stage_group_id:
            if self.project_id.stage_group_id:
                self.stage_group_id = self.project_id.stage_group_id
                self.stage_id = self.project_id.type_ids.ids[0]
                return {'domain': {
                    'stage_id': [
                        ('id', 'in', self.project_id.type_ids.ids)]}}
            else:
                self.stage_id = self.stage_group_id.stages_ids.ids[0]
                return {'domain': {
                    'stage_id': [
                        ('id', 'in', self.stage_group_id.stages_ids.ids)]}}

    @api.onchange('user_id')
    def _onchange_user(self):
        users = self.get_user_domin()
        return {'domain': {'user_id': [('id', 'in', users)]}}

    @api.depends('project_id')
    def task_user_domain(self):
        for obj in self:
            obj.user_ids = [(6, 0, obj.sudo().get_user_domin())]

    stage_group_id = fields.Many2one(
        'project.stage.group', string="Stage Group",
        default=get_default_stage_group)
    user_id = fields.Many2one(
        'res.users', string='Assigned to', domain="[('id', 'in', user_ids)]",
        default=lambda self: self.env.uid,
        index=True, tracking=True,
        help="You'll only assign this task to project team and extra members. \
        so if you're not able to see any members then please configure the \
        team and members for particular project.")
    user_ids = fields.Many2many(
        "res.users", 'task_id', 'user_id',
        compute="task_user_domain", string="Task Users")
