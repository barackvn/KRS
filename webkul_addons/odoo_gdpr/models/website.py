from odoo import api, models, _
import logging
_logger = logging.getLogger(__name__)

class Website(models.Model):
    _inherit = "website"

    @api.model
    def footerGdprData(self):
        gdpr_footer_data = self.env["odoo.gdpr"].sudo().search([],limit=1)
        return gdpr_footer_data
