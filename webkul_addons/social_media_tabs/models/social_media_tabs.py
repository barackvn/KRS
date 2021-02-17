import logging
from odoo import api, fields, models, _
from odoo import tools
from odoo.exceptions import UserError
from odoo.tools import float_is_zero, float_compare, DEFAULT_SERVER_DATETIME_FORMAT
_logger = logging.getLogger(__name__)
import urllib.request
import importlib.util

class SocialMediaTabs(models.Model):
	_name = 'social.media.tabs'
	_order = 'tab_sequence'
	_description = 'Social Media Tabs'

	def _redirect_uri(self):
		base_url = self.env['ir.config_parameter'].sudo().get_param('web.base.url')
		redirect_uri = '%s/instagram/code/'%(base_url)
		return redirect_uri

	icon = fields.Binary('Icon',help='icon for the tab',required=True)
	media_type = fields.Selection([('custom','Custom Tab'),('social_tab','Social Tab')], 'Media Type' ,required=True)
	custom_html = fields.Html('Custom Your Html')
	custom_tab_name = fields.Char('Custom Tab Name')
	social_tab = fields.Selection([('facebook','Facebook'),('youtube','Youtube'),('flickr','Flickr'),('pinterest','Pinterest'),('vimeo','Vimeo'),('tumblr','Tumblr'),('twitter','Twitter'),('instagram','Instagram')], 'Social Tabs')
	tab_sequence = fields.Integer('Sequence', required=True, default=1, help="The tabs will be displayed in this sequence in website")
	color = fields.Char("Color", help="Hex color codes")
	title = fields.Char('Title', help="Title of the social media")
	folow = fields.Char('Follow', help="eg = Follow on Facebook")
	logo = fields.Binary('Logo', help="the logo of the page that will be displayed on the top of the header.")
	limit = fields.Integer('Limit', help="Number of records", default=10)
	publish = fields.Boolean('Publish')

	#Credentials for facebook
	facebook_id = fields.Char('Facebook Id')

	#You tube Credentials
	yt_api_key = fields.Char('Youtube Api key',help="youtube api key")
	yt_channel_id = fields.Char('Youtube Channel Id',help="youtube channel id")
	yt_user_id = fields.Char('Youtube User Id',help="youtube user id")
	yt_show_subscribe = fields.Boolean('Show Subscribe', help="an subscribe iframe will be displayed")

	#Flickr Credentials
	flickr_id = fields.Char('Flickr ID' , help="id of the flickr account")

	#Pintrest Credentials
	pinterest_id = fields.Char('Pintrest Id',help="id of the pintrest account")

	#Vimeo Credentials
	vimeo_id = fields.Char('Vimeo Id')
	vimeo_token = fields.Char('Token')
	vimeo_client_id = fields.Char('Client Id')
	vimeo_client_secret = fields.Char('Client Secret')

	#Tumblr Credentials
	tumblr_id = fields.Char('Tumblr Id')

	#Stumbleupon Credentials
	stumbleupon_id = fields.Char('Stumbleupon Id')

	#Credentials for google plus
	google_id = fields.Char('Google Id', help="page id of google plus")
	google_api_key = fields.Char('Google Api Key', help="api key for google plus account")

	#Credentials for Twitter
	twiter_user_id = fields.Char('Twitter User Id', help="User id for the twitter.")

	#Credentials for Instagram
	instagram_user = fields.Char('Instagram User')
	instagram_client_id = fields.Char('Instagram Client Id')
	instagram_client_secret = fields.Char('Instagram Client Secret')
	instagram_access_token = fields.Char('Instagram Access Token')
	url = fields.Char('Url', help="Please hit this url to process further")

	def generate_code(self):
		instagram_redirect_url = self._redirect_uri()
		return {
			"type": "ir.actions.act_url",
			"url": 'https://api.instagram.com/oauth/authorize?client_id=%s&redirect_uri=%s&scope=user_profile,user_media&response_type=code'%(self.instagram_client_id, instagram_redirect_url),
			"target": "self",
		}

	@api.onchange('social_tab')
	def _set_defaults(self):
		if self.social_tab:
			self.title = self.social_tab.capitalize()
			self.folow = 'Follow On ' + self.social_tab.capitalize()
	
	def publish_button(self):
		self.ensure_one()
		return self.write({'publish': not self.publish})

	@api.model
	def create(self, vals):
		if vals.get('social_tab') == 'vimeo':
			spec = importlib.util.find_spec('vimeo')
			if spec is None:
				raise UserError(_('Please install python library PyVimeo'))
		return super(SocialMediaTabs, self).create(vals)

	def write(self, vals):
		for tab in self:
			if tab.social_tab == 'vimeo':
				spec = importlib.util.find_spec('vimeo')
				if spec is None:
					raise UserError(_('Please install python library PyVimeo'))
		return super(SocialMediaTabs, self).write(vals)

class website(models.Model):
	_inherit = 'website'

	tab_ids = fields.Many2many(comodel_name="social.media.tabs", string='Social Tabs')
	tabs_position = fields.Selection([('left','Left'),('right','Right')], string='Tab Position', default="left")
	tab_event = fields.Selection([('hover','Mouse Hover'),('click','Mouse Click'),('fixed','Fixed')], required=True, default="click")
	quote = fields.Char(string="Quote", default="Follow Us")
	color = fields.Char(string="Background Color", default="#800080")