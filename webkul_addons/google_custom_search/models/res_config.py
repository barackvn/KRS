# -*- coding: utf-8 -*-
##########################################################################
#
#   Copyright (c) 2015-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#   See LICENSE file for full copyright and licensing details.
#   License URL : <https://store.webkul.com/license.html/>
#
##########################################################################
import urllib.request
import logging
_logger = logging.getLogger(__name__)

from odoo import api, fields, models



class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    cse_unique_id = fields.Char(
        string="Search Engine Unique Id",
        help="""Uniqu search engine id create on google custom search engine control panel""")
    cse_enable = fields.Boolean(
        string="Enable Custom Search Engine")
    cse_records_perpage = fields.Char(
        string="No. of Records per page")
    cse_image_search = fields.Boolean(
        string="Enable Image Search",
        help="""If yes image search will also be listed."""
        """ To work this also enable it in the custom search cantrol panel""")
    cse_order_sorting = fields.Boolean(
        string="Enable Search Result Sorting",
        help="""Enable the sorting of result by relevance, date.""")
    cse_auto_complete = fields.Boolean(
        string="Enable Auto Complete",
        help="It will auto complete searchin new search bar")
    cse_open_new_tab = fields.Boolean(
        string="Open Link in New Tab")
    cse_file = fields.Binary('CSE file')
    cse_filename = fields.Char("CSE file")
    # cse_history = fields.Boolean(
    #     string="Enable History",
    #     help="""Enables history management for the browse""")

    def set_values(self):
        super(ResConfigSettings, self).set_values()
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_unique_id", self.cse_unique_id
        )
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_enable", self.cse_enable
        )
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_records_perpage", self.cse_records_perpage
        )
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_image_search", self.cse_image_search
        )
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_order_sorting", self.cse_order_sorting
        )
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_auto_complete", self.cse_auto_complete
        )
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_open_new_tab", self.cse_open_new_tab
        )
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_file", self.cse_file
        )
        IrConfigPrmtr.set_param(
            "google_custom_search.cse_filename", self.cse_filename
        )
        # IrConfigPrmtr.set_param(
        #     "google_custom_search.cse_history", self.cse_history
        # )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res = super(ResConfigSettings, self).get_values()
        IrConfigPrmtr = self.env['ir.config_parameter'].sudo()
        cseUniqId = IrConfigPrmtr.get_param('google_custom_search.cse_unique_id')
        cseEnable = IrConfigPrmtr.get_param('google_custom_search.cse_enable')
        cseRecPage = IrConfigPrmtr.get_param('google_custom_search.cse_records_perpage')
        cseImgSrch = IrConfigPrmtr.get_param('google_custom_search.cse_image_search')
        cseOrderSort = IrConfigPrmtr.get_param('google_custom_search.cse_order_sorting')
        cseAutoComplt = IrConfigPrmtr.get_param('google_custom_search.cse_auto_complete')
        cseNewTab = IrConfigPrmtr.get_param('google_custom_search.cse_open_new_tab')
        cseFile = IrConfigPrmtr.get_param('google_custom_search.cse_file')
        cseFileName = IrConfigPrmtr.get_param('google_custom_search.cse_filename')
        # SalesPrsn = IrConfigPrmtr.get_param('google_custom_search.cse_history')
        res.update({
            'cse_unique_id': cseUniqId,
            'cse_enable': cseEnable,
            'cse_records_perpage': cseRecPage,
            'cse_image_search': cseImgSrch,
            'cse_order_sorting': cseOrderSort,
            'cse_auto_complete': cseAutoComplt,
            'cse_open_new_tab': cseNewTab,
            'cse_file': cseFile,
            'cse_filename': cseFileName,
            # 'cse_history': salesTeam,
        })
        return res

    def download_file(self):
        self.ensure_one()
        self.env['generate.cse.files'].prepare_tags()
        return self.download_cse_file()


    @api.model
    def download_cse_file(self):
        return {
            'type': 'ir.actions.act_url',
            'url': '/gce/download_files',
            'target': 'self',
        }

    @api.model
    def _cse_demo_setting(self):
        vals = {
            'cse_unique_id': '009424951233066005773:rdtz1mvmxhi',
            'cse_enable': True,
            'cse_image_search': True,
            'cse_order_sorting': True,
            'cse_auto_complete': True,
            'cse_open_new_tab': True,
        }
        defaultSetObj = self.sudo().create(vals)
        defaultSetObj.execute()
        return True
