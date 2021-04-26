import json

from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from lxml import etree
import re
import requests, json
from base64 import b64encode
import base64
import datetime

from requests.auth import HTTPBasicAuth


class CommunicationEwms(models.Model):
    _inherit = 'stock.picking'


    def send_xml_pre_advice(self):

            # base_url = 'http://devewms.distrimedia.be:8080'
            # headers = {
            #     "key": "SOAPAction",
            #     "value": "CreateOrder",
            #     "type": "text"
            # }
            # # attrs = {
            # #     'id': "comprobante",
            # #     'version': "1.0.0"
            # # }
            PreAdvice = etree.Element("PreAdvice")
            etree.SubElement(PreAdvice, 'Reference').text = str(self.pre_advice_name) or ''
            etree.SubElement(PreAdvice, 'DateExpected').text = self.arrival_date.strftime("%Y%m%d")
            etree.SubElement(PreAdvice, 'Supplier').text = str(self.partner_id.id) or ''
            etree.SubElement(PreAdvice, 'Modus').text = 'D'
            for line in self.move_ids_without_package:
                PreAdviceLine = etree.SubElement(PreAdvice, 'PreAdviceLine')
                etree.SubElement(PreAdviceLine, 'ProductID').text = str(line.product_id.id) or ''
                etree.SubElement(PreAdviceLine, 'Pieces').text = str(line.product_uom_qty) or ''
                etree.SubElement(PreAdviceLine, 'DueDate').text = self.arrival_date.strftime("%Y%m%d")
                Product = etree.SubElement(PreAdviceLine,'Product')
                etree.SubElement(Product, 'EAN').text = str(line.product_id.default_code) or ''
                etree.SubElement(Product, 'ExternalRef').text = str(line.product_id.name) or ''
                etree.SubElement(Product, 'Description1').text = str(line.product_id.name) or ''
                etree.SubElement(Product, 'NbrDaysNoDeliveryForDueDate').text = '60'
                etree.SubElement(Product, 'UseDueDate').text = '1'
                etree.SubElement(Product, 'Quantity_Full_Box').text = '1'
                etree.SubElement(Product, 'Quantity_Fullx_Pallet').text = '40'
            return PreAdvice

    def export_pre_advice(self):
        # data = base64.encodestring(self.get_export_xml())
        base_url = 'http://devewms.distrimedia.be:8080'
        headers = {
            # "key": "",
            "SOAPAction": "CreatePreAdvice",
            # "type": "text",
            "Content-Type": "text/xml;charset=UTF-8",
        }
        data = self.get_export_xml()
        xml_data = data.decode("utf-8")
        datas = """<soap:Envelope xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xmlns:xsd="http://www.w3.org/2001/XMLSchema" xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/">
                            <soap:Body>
                            <WebshopCode>99</WebshopCode>
                            <SoapPassword>Cst78!*KevS</SoapPassword>  
                            %s                    
                            </soap:Body>
                            </soap:Envelope>""" % (xml_data)

        # filename = self.get_export_xml_filename()
        # wizard = self.env['communication.export.file'].create({'file_export': datas, 'filename': filename})
        # # wizard.file_export = datas
        # # wizard.filename = filename
        #
        # model_data_obj = self.env['ir.model.data']
        # view_rec = model_data_obj.get_object_reference(
        #     'ewms_connection',
        #     'wizard_dati_iva_export_file_exit'
        # )
        # view_id = view_rec and view_rec[1] or False
        #
        # return {
        #     'view_type': 'form',
        #     'view_id': [view_id],
        #     'view_mode': 'form',
        #     'res_model': 'communication.export.file',
        #     'res_id': wizard.id,
        #     'type': 'ir.actions.act_window',
        #     'target': 'current',
        # }
        print(datas)
        response = requests.post(base_url, headers=headers, data=datas)
        text_msgs = response.content.decode("utf-8")
        print(text_msgs)

    def get_export_xml_filename(self):
        self.ensure_one()
        filename = 'Pre Advice.{ext}'.format(
            ext='xml',
        )
        return filename


    def get_export_xml(self):
        data_in = self.send_xml_pre_advice()
        xml_string = etree.tostring(
            data_in, encoding='UTF-8', method='xml', pretty_print=True)
        return xml_string
