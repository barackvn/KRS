import base64
from odoo import api, fields, models, exceptions, _


class ComExportFile(models.TransientModel):
    _name = "communication.export.file"
    _description = "Export XML of invoices data communication"

    file_export = fields.Binary('File', readonly=True)
    filename = fields.Char()
    name = fields.Char('File Name', readonly=True, default='invoice_data.xml')


    def export(self):

        comunicazione_ids = self._context.get('active_ids')
        if not comunicazione_ids:
            raise exceptions.UserError(
                _('No communication selected')
            )
        if len(comunicazione_ids) > 1:
            raise exceptions.UserError(
                _('You can only export one communication')
            )

        for wizard in self:
            for comunicazione in self.env['stock.picking'].browse(comunicazione_ids):
                out = base64.encodestring(comunicazione.get_export_xml())
                filename = comunicazione.get_export_xml_filename()
                wizard.file_export = out
                wizard.filename = filename
            model_data_obj = self.env['ir.model.data']
            view_rec = model_data_obj.get_object_reference(
                'ewms_connection',
                'wizard_dati_iva_export_file_exit'
            )
            view_id = view_rec and view_rec[1] or False

            return {
                'view_type': 'form',
                'view_id': [view_id],
                'view_mode': 'form',
                'res_model': 'communication.export.file',
                'res_id': wizard.id,
                'type': 'ir.actions.act_window',
                'target': 'current',
            }
