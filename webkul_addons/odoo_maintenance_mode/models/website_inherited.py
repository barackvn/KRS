# -*- coding: utf-8 -*-
#################################################################################
##    Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#    You should have received a copy of the License along with this program.
#    If not, see <https://store.webkul.com/license.html/>
#################################################################################

from odoo import api, fields, models, SUPERUSER_ID, _
from odoo.http import request
import logging
_logger = logging.getLogger(__name__)


class Website(models.Model):
	_inherit = "website"

	maintenance_mode = fields.Boolean(string="Maintenance Mode", help="Set it true during the maintenance mode")
	allowed_ips = fields.Char(string="Allowed IPs (comma separated)",help="Specify the IPs for whcih you want to allow the acess during the maintenance mode")
	maintenance_mode_id = fields.Many2one('maintenance.mode', string="Set messages")

	@api.model
	def odoo_maintainance_mode(self):
		# IrConfigParam = self.env['ir.config_parameter'].sudo()
		website = self.env['website'].get_current_website()
		maintenance_mode = website.sudo().maintenance_mode
		allowed_ips = website.sudo().allowed_ips
		wk_display_page = False
		is_sigin_clicked = False
		accessible_user = False
		context = dict(request.session.context)
		context['login_clicked'] = False
		request.session.context = context
		if maintenance_mode and allowed_ips:
			ip_list = list(allowed_ips.split(","))
			user_ip = request.httprequest.environ['REMOTE_ADDR']
			user_id = self.env['res.users'].browse(self._uid)
			if user_id.has_group('base.group_system'):
				accessible_user = True
			elif user_ip not in ip_list:
				if request.httprequest.path != '/web/login':
					wk_display_page = True
				else:
					is_sigin_clicked = True
					context['login_clicked'] = False
			else:
				accessible_user = True
		context['accessible_user'] = accessible_user
		return {'wk_display_page': wk_display_page, 'is_sigin_clicked': is_sigin_clicked, 'accessible_user': accessible_user}

	@api.model
	def get_config_id(self):
		# IrConfigParam = self.env['ir.config_parameter']
		website = self.env['website'].get_current_website()
		if (
			maintenance_mode_id := website.get_current_website()
			.sudo()
			.maintenance_mode_id
		):
			return self.env['maintenance.mode'].sudo().browse(int(maintenance_mode_id))

	@api.model
	def get_page_header_message(self):
		return obj.page_header if (obj := self.get_config_id()) else False

	@api.model
	def get_page_descriptitive_message(self):
		return obj.page_message if (obj := self.get_config_id()) else False

	@api.model
	def get_login_page_message(self):
		return obj.login_message if (obj := self.sudo().get_config_id()) else False

	@api.model
	def get_admin_message(self):
		return obj.admin_message if (obj := self.sudo().get_config_id()) else False

	@api.model
	def get_image(self):
		if obj := self.sudo().get_config_id():
			image = obj.image
			return obj
		return False

	@api.model
	def display_email_in_page(self):
		if obj := self.sudo().get_config_id():
			display_email_field = obj.display_email_field
			return display_email_field
		return False

	@api.model
	def display_admin_message(self):
		return obj.display_admin_mesage if (obj := self.get_config_id()) else False

	@api.model
	def display_invalid_email_msg(self):
		return obj.email_error_msg if (obj := self.get_config_id()) else False

	@api.model
	def display_valid_email_msg(self):
		return obj.email_valid_msg if (obj := self.get_config_id()) else False
	@api.model
	def get_notification_header(self):
		return obj.email_notif_title if (obj := self.get_config_id()) else False
	@api.model
	def display_exists_email_msg(self):
		return obj.email_exists if (obj := self.get_config_id()) else False
