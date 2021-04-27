# -*- coding: utf-8 -*-

import logging
from odoo import api, models
_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = "res.partner"

    @api.model
    def get_needaction_count(self):
        """ compute the number of needaction of the current user """
        if self.env.user.partner_id:
            self.env['mail.notification'].flush(['is_read', 'res_partner_id'])
            self.env.cr.execute("""
                SELECT count(*) as needaction_count
                FROM mail_message_res_partner_needaction_rel R
                LEFT JOIN mail_message msg ON (msg.id=R.mail_message_id)
                WHERE R.res_partner_id = %s AND (R.is_read = false OR R.is_read IS NULL) AND msg.message_type != 'email'""", (self.env.user.partner_id.id,))
            return self.env.cr.dictfetchall()[0].get('needaction_count')
        _logger.error('Call to needaction_count without partner_id')
        return 0

    @api.model
    def _notify_prepare_email_values(self, message):
        mail_values = super(ResPartner, self)._notify_prepare_email_values(message)
        cc_email_list = message.email_cc_ids.mapped('email')
        bcc_email_list = message.email_bcc_ids.mapped('email')
        cc_bcc = {
            'email_cc': ",".join(cc_email_list),
            'email_bcc': ",".join(bcc_email_list),
        }
        mail_values.update(cc_bcc)
        return mail_values
