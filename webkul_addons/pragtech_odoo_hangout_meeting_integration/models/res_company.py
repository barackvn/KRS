# -*- coding: utf-8 -*-
import json
import logging
from datetime import datetime
import requests
import base64
from dateutil.parser import parse as duparse
from odoo import api, fields, models
from odoo.exceptions import Warning

_logger = logging.getLogger(__name__)


class ResCompany(models.Model):
    _inherit = "res.company"

  
    client_id = fields.Char("Client Id",help="The client ID you obtain from the google developer console.")
    client_secret = fields.Char("Client Secret",help="The client Secret key you obtain from the google developer console.")
    redirect_uri = fields.Char("Authorized redirect URIs",help="",default="http://localhost:8069/get_auth_code")
    outgoing_server_mail_id = fields.Many2one("ir.mail_server",string="Outgoing mail server")