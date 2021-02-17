from odoo import models,fields,api,_
import logging
_logger = logging.getLogger(__name__)

class CommtypeDescWizard(models.TransientModel):
    _name = "commtype.desc.wizard"
    _desc = "Commission Type Description"

    desc = fields.Text(string="Commission Type")
