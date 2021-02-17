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

from odoo import api, fields, models, _
from odoo.exceptions import UserError
from datetime import datetime,  timedelta
import logging
_logger = logging.getLogger(__name__)


class Survey(models.Model):
    """ Settings for a multi-page/multi-question survey.
        Each survey can have one or more attached pages, and each page can display
        one or more questions.
    """

    _inherit = 'survey.survey'

    @api.depends('enable_scheduler','enable_follow','days','schedule_date')
    def _get_followup_date(self):
        for obj in self:
            obj.followup_date = False
            if obj.enable_scheduler and obj.enable_follow and obj.schedule_date:
                if not obj.followup_date and obj.days :
                    obj.followup_date =obj.schedule_date + timedelta(days=obj.days)
                elif obj.repeative == 'repetively':
                    obj.followup_date = obj.followup_date + timedelta(days=obj.days)
                else:
                    obj.followup_date = obj.schedule_date  + timedelta(days=obj.days)

    enable_scheduler = fields.Boolean(string="Enable cron job for this survey", copy=False)
    schedule_date = fields.Date('Scheduled Date', default=fields.Date.context_today, help="Date on which survey has been sent",track_visibility='onchange', copy=False)
    cron_status = fields.Selection([('in-progress','In-Progress'),('done','Done')], string="Cron Status", default="in-progress", copy=False)
    access_mode = fields.Selection([
        ('public', 'Anyone with the link'),
        ('token', 'Invited people only')], string='Access Mode',
        default='token', required=True)
    partner_ids = fields.Many2many('res.partner', 'survey_mail_partner_rel',
                                   'wizard_id', 'partner_id', string='Existing contacts', copy=False)
    emails = fields.Text(string='Additional emails', help="This list of emails of recipients will not be converted in contacts. Emails must be separated by commas, semicolons or newline.")
    enable_follow = fields.Boolean(string="Enable Follow-up", help="Cron will send followup mail, who has not yet answered. Followup will not work for closed survey.", copy=False)
    repeative = fields.Selection([('one-time','Once'),('repetively','Repeatedly')], string="Follow-up Type", copy=False, default="one-time")
    days = fields.Integer(string="Follow-up After", copy=False, default=1)
    followup_date = fields.Date('Follow-up Date', compute="_get_followup_date", store=True)
    authorised_user_ids = fields.Many2many('res.users','survey_authorised_users','survey_id','user_id',string="Authorised Users")

    @api.constrains('days')
    def _check_days(self):
        if self.days < 0:
            raise ValidationError(_('Days must be greater than or equals to zero'))

    @api.constrains('schedule_date')
    def schedule_date_in_the_past(self):
        for obj in self:
            if obj.schedule_date:
                d1 = obj.schedule_date
                d2 = datetime.today().date()
                if (d1 - d2).days < 0:
                    raise ValidationError(_('The Scheduled Date always be of future.'))
        return True

    @api.model
    def survey_send_cron(self):
        surveys = self.search(
            [('enable_scheduler', '=', 'True'), ('schedule_date', '=', fields.Date.today()),('cron_status', '!=', 'done'),('state','!=','closed')])
        for survey in surveys:
            survey.send_survey()
            survey.cron_status = 'done'
        followup_surveys = self.search(
            [('enable_scheduler', '=', 'True'), ('followup_date', '=', fields.Date.today()),('cron_status', '=', 'done'),('state','!=','closed'),('enable_follow','=',True)])
        for followup_survey in followup_surveys:
            followup_survey.send_follow_survey()
            if followup_survey.repeative == 'repetively':
                followup_survey.followup_date = followup_survey.followup_date + timedelta(days=followup_survey.days)
            else:
                followup_survey.followup_date = False
        return True

    def send_follow_survey(self):
        for survey in self:
            followup_history = self.env['survey.followup.history'].search(
            [('survey_id', '=', survey.id), ('followup_date', '=', fields.Date.today())])
            if not followup_history:
                followup_history = self.env['survey.followup.history'].create(
                    {'name': survey.title + ' (' + survey.followup_date.strftime('%m/%d/%Y') + ')', 'survey_id': survey.id, 'followup_date': fields.Date.today()})
            for user_input in survey.user_input_ids:
                if user_input.state != 'done' and user_input.input_type == 'link':
                    if user_input.id not in followup_history.user_input_ids.ids:
                        fields_get = self.env['survey.invite'].fields_get()
                        composed_survey = user_input.action_resend()
                        vals = self.env['survey.invite'].with_context(
                        composed_survey.get('context')).default_get(fields_get)
                        wizard = self.env['survey.invite'].with_context(composed_survey.get('context')).create(vals)
                        wizard.action_invite()
                        followup_history.user_input_ids = [(4, user_input.id)]


    def send_survey(self):
        for survey in self:
            local_context = {
                'default_public': survey.access_mode,
                'default_emails': survey.emails,
                'default_partner_ids': survey.partner_ids,
            }
            fields_get = self.env['survey.invite'].fields_get()
            composed_survey = survey.with_context(local_context).action_send_survey()
            vals = self.env['survey.invite'].with_context(
                composed_survey.get('context')).default_get(fields_get)
            wizard = self.env['survey.invite'].create(vals)
            wizard.action_invite()
        return True


class SurveyFollowUpHistory(models.Model):

    _name = "survey.followup.history"
    _description = "Survey Follow-Up History"

    name = fields.Char(string="Name")
    survey_id = fields.Many2one('survey.survey', string="Survey", required=True)
    followup_date = fields.Date(string="Follow-up Date", required=True)
    user_input_ids = fields.Many2many(
        'survey.user_input', 'followup_survey_input', 'followup_id', 'input_id', string='Sent Follow Ups')

