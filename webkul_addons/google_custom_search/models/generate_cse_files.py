# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################

import xml.etree.ElementTree as ET
import base64

from odoo import api, fields, models
from odoo.modules.module import get_module_path as moduleDirPath


class GenerateCseFiles(models.TransientModel):
    _name = 'generate.cse.files'
    _description = "Generate CSE Files"

    def create_xml_file(self, data):
        dirPath = moduleDirPath('google_custom_search')
        dirPath += '/static/description/cse.xml'
        ET.ElementTree(data).write(dirPath,
                                  encoding="UTF-8", xml_declaration=True)
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        fileOutput = ''
        with open(dirPath, "rb") as xmlFile:
            fileOutput = xmlFile.read()
        gentextfile = base64.b64encode(fileOutput)
        IrConfigPrmtr.set_param('google_custom_search.cse_file', gentextfile)
        res = IrConfigPrmtr.set_param('google_custom_search.cse_filename', 'cse.xml')


    def prepare_tags(self):
        configSudo = self.env['ir.config_parameter'].sudo()
        cseEngnId = configSudo.get_param(
            'google_custom_search.cse_unique_id'
        )
        creator, cseId = cseEngnId.split(':')
        topDict = {
            'id': cseId,
            'creator': creator,
            'language': "en",
            'encoding': "UTF-8",
            'enable_suggest': "true",
        }
        top = ET.Element('CustomSearchEngine', topDict)
        title = ET.SubElement(top, 'Title')
        title.text = "Odoo CSE"
        context = ET.SubElement(top, 'Context')
        backgroundLabels = ET.SubElement(context, 'BackgroundLabels')
        cseDundle = f'_cse_{cseId}'
        labelDict = {
            'name': cseDundle,
            'mode': "FILTER",
        }
        ET.SubElement(backgroundLabels, 'Label', labelDict)
        cseExludeDunder = f'_cse_exclude_{cseId}'
        labelDict = {
            'name': cseExludeDunder,
            'mode': "ELIMINATE",
        }
        ET.SubElement(backgroundLabels, 'Label', labelDict)
        lookFeelDict = {
            'nonprofit': "false",
            'element_layout': "5",
            'theme': "7",
            'custom_theme': "true",
            'text_font': "Arial, sans-serif",
            'url_length': "full",
            'element_branding': "show",
            'enable_cse_thumbnail': "true",
            'promotion_url_length': "full",
            'ads_layout': "1",
        }
        lookFeel = ET.SubElement(top, 'LookAndFeel', lookFeelDict)
        ET.SubElement(lookFeel, 'Logo')
        colorsDict = {
            'url': "#008000",
            'background': "#FFFFFF",
            'border': "#FFFFFF",
            'title': "#0000CC",
            'text': "#000000",
            'visited': "#0000CC",
            'title_hover': "#0000CC",
            'title_active': "#0000CC",
        }
        ET.SubElement(lookFeel, 'Colors', colorsDict)
        promotDict = {
            'title_color': "#0000CC",
            'title_visited_color': "#0000CC",
            'url_color': "#008000",
            'background_color': "#FFFFFF",
            'border_color': "#336699",
            'snippet_color': "#000000",
            'title_hover_color': "#0000CC",
            'title_active_color': "#0000CC",
        }
        ET.SubElement(lookFeel, 'Promotions',  promotDict)
        searchControlDict = {
            'input_border_color': "#D9D9D9",
            'button_border_color': "#666666",
            'button_background_color': "#CECECE",
            'tab_border_color': "#E9E9E9",
            'tab_background_color': "#E9E9E9",
            'tab_selected_border_color': "#FF9900",
            'tab_selected_background_color': "#FFFFFF",
        }
        ET.SubElement(lookFeel, 'SearchControls', searchControlDict)
        resultDict = {
            'border_color': "#FFFFFF",
            'border_hover_color': "#FFFFFF",
            'background_color': "#FFFFFF",
            'background_hover_color': "#FFFFFF",
            'ads_background_color': "#fff7f5",
            'ads_border_color': "#FFFFFF",
        }
        ET.SubElement(lookFeel, 'Results', resultDict)
        ET.SubElement(top, 'AdSense')
        ET.SubElement(top, 'EnterpriseAccount')
        if enableImgSearch := configSudo.get_param(
            'google_custom_search.cse_image_search'
        ):
            ET.SubElement(top, 'ImageSearchSettings', enable="true")
        if autoComplete := configSudo.get_param(
            'google_custom_search.cse_auto_complete'
        ):
            ET.SubElement(top, 'autocomplete_settings')
        if orderSoritng := configSudo.get_param(
            'google_custom_search.cse_order_sorting'
        ):
            ET.SubElement(top, 'sort_by_keys', label="Relevance", key="")
            ET.SubElement(top, 'sort_by_keys', label="Date", key="date")
        self.create_xml_file(top)
