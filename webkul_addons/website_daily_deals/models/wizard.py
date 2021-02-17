# -*- coding: utf-8 -*-
#################################################################################
##    Copyright (c) 2019-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import fields, models

class DealPricelistWarning(models.TransientModel):
    _name = 'deal.wizard.message'
    _description = 'Wizard that show warning if user try to apply deal pricelist on current website'
    msg = fields.Char(string='message', readonly=True)

    def change_pricelist_on_website(self):
        active_record = self.env[self._context['active_model']].browse([self._context['active_id']])
        # feature = self.env[self._context['active_model']].browse([self._context['feature_id']])
        partner = self.env.user.partner_id
        applied_pl  = active_record.deal_pricelist

        for pricelist in self.env["product.pricelist"].sudo().search([]):
            pricelist.sequence=16
        applied_pl.sequence = 1
        partner.property_product_pricelist = applied_pl
        return True
