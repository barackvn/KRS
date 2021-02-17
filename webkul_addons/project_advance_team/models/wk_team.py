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

from odoo import api, fields, models, tools, _
from odoo.exceptions import ValidationError
from odoo.osv import expression

class WkTeam(models.Model):

    _name = 'wk.team'
    _inherit = ['mail.thread']
    _description = "Team"

    name = fields.Char(
        string="Name", required=True, tracking=True)
    active = fields.Boolean(
        string="Active", default=True, tracking=True)
    description = fields.Text(
        string="Description", tracking=True)
    members = fields.Many2many(
        'res.users', 'team_members', 'team_id',
        'user_id', 'Members',
        help="""A group of people with a full set of complementary skills \
        required to complete a job.""", tracking=True)
    manager = fields.Many2one(
        comodel_name="res.users", string='Manager', required=True,
        default=lambda self: self.env.uid, tracking=True)
    project_ids = fields.One2many(
        "project.project", 'wk_team_id', string="Projects")
    project_count = fields.Integer(string="count", compute="get_count", store=True)
    parent_id = fields.Many2one(
        'wk.team', 'Parent Team', index=True, ondelete='cascade',
        tracking=True)
    child_ids = fields.One2many(
        'wk.team', 'parent_id', 'Child Teams', tracking=True)
    department_id = fields.Many2one(
        'hr.department', string="Department", compute="get_department_id",
        store=True, tracking=True)

    @api.depends('manager')
    def get_department_id(self):
        for obj in self:
            if obj.manager and obj.manager.sudo().employee_ids and obj.manager.sudo().employee_ids[0].department_id:
                obj.department_id = obj.manager.sudo(
                ).employee_ids[0].department_id.id
            else:
                obj.department_id = False

    @api.constrains('parent_id')
    def _check_team_recursion(self):
        if not self._check_recursion():
            raise ValidationError(
                _('Error ! You cannot create recursive teams.'))
        return True

    def _recursive_search_of_teams(self):
        """
        @return: returns a list of tuple (id, sequence) which are all
         the children of the passed rule_ids
        """
        members_list = []
        for team in self.filtered(lambda team: team.child_ids):
            members_list += team.child_ids._recursive_search_of_teams()
        return [
            team.members.ids + [
                team.manager.id] for team in self] + members_list

    def name_get(self):
        def get_names(team):
            """ Return the list [team.name, team.parent_id.name, ...] """
            res = []
            while team:
                res.append(team.name)
                team = team.parent_id
            return res

        return [(
            team.id, " / ".join(reversed(get_names(team)))) for team in self]

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        if not args:
            args = []
        if name:
            # Be sure name_search is symmetric to name_get
            team_names = name.split(' / ')
            parents = list(team_names)
            child = parents.pop()
            domain = [('name', operator, child)]
            if parents:
                names_ids = self.name_search(
                    ' / '.join(parents), args=args,
                    operator='ilike', limit=limit)
                team_ids = [name_id[0] for name_id in names_ids]
                if operator in expression.NEGATIVE_TERM_OPERATORS:
                    teams = self.search([('id', 'not in', team_ids)])
                    domain = expression.OR(
                        [[('parent_id', 'in', teams.ids)], domain])
                else:
                    domain = expression.AND(
                        [[('parent_id', 'in', team_ids)], domain])
                for i in range(1, len(team_names)):
                    domain = [
                        [('name', operator, ' / '.join(
                            team_names[-1 - i:]))], domain]
                    if operator in expression.NEGATIVE_TERM_OPERATORS:
                        domain = expression.AND(domain)
                    else:
                        domain = expression.OR(domain)
            teams = self.search(expression.AND([domain, args]), limit=limit)
        else:
            teams = self.search(args, limit=limit)
        return teams.name_get()

    def check_access_rule(self, operation):
        action = self.env['ir.model.data'].xmlid_to_object(
            'project_advance_team.wk_team_view')
        if self._context.get(
            'params') and action.id == self._context.get(
                'params').get('action'):
            if self._uid in self.members:
                return super(WkTeam, self.sudo()).check_access_rule(operation)
        return super(WkTeam, self).check_access_rule(operation)

    def read(self, fields=None, load='_classic_read'):
        self.check_access_rule('read')
        res = super(WkTeam, self).read(fields, load)
        return res

    def get_count(self):
        for record in self:
            record.project_count = len(record.project_ids)

    def projects_action(self):
        projects = self.mapped('project_ids')
        result = {
            "type": "ir.actions.act_window",
            "res_model": "project.project",
            "views": [[False, "tree"], [False, "form"]],
            "domain": [["id", "in", projects.ids]],
            "context": {"create": False},
            "name": "Projects",
        }
        if len(projects) == 1:
            result['views'] = [(False, "form")]
            result['res_id'] = projects.id
        return result
