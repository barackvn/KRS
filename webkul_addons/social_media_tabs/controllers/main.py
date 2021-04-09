# -*- coding: utf-8 -*-
#################################################################################
#
# Copyright (c) 2018-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
# See LICENSE file for full copyright and licensing details.
#################################################################################
from odoo import http, _
from odoo.http import request
from odoo.http import Response
from odoo.exceptions import UserError
from odoo.addons.website_sale.controllers.main import WebsiteSale
import json
import pprint
import logging
import requests

_logger = logging.getLogger(__name__)
pp = pprint.PrettyPrinter(indent=4)

class SocialTabs(http.Controller):

	def _get_vimeo_data(self, vimeoId, token, clientID, clientSecret):
		try:
			import vimeo
		except:
			raise UserError(_('Please install python library PyVimeo'))
		v = vimeo.VimeoClient(
			token=token,
			key=clientID,
			secret=clientSecret
		)
		videos = v.get('https://api.vimeo.com/me/videos')
		if videos.status_code == 200:
			return videos.json()
		else:
			assert 'Something went wrong!!!'

	def _get_flickr_data(self, flicker_id):
		lang = 'en-us'
		cq = flicker_id.split('/')
		fd = 'groups_pool' if len(cq) > 1 else 'photos_public'
		url = 'http://api.flickr.com/services/feeds/' + fd + '.gne'
		response = requests.get(url, params = {'id': flicker_id,'lang': lang,'format': 'json'})
		data = False
		if response.status_code == 200:
		# response.content[15:-1] => Remove Extra bytes string form the byte response
			data = json.loads(response.content.decode('utf8')[15:-1])
		return data

	@http.route(['/instagram/code/'], type='http', auth="public", website=True, csrf=False)
	def instagram_code(self, **kw):
		if kw.get('code', False):
			instagram_id = request.env['social.media.tabs'].search([('social_tab','=','instagram')], limit=1)
			action = request.env.ref('social_media_tabs.action_media_tabs')
			if instagram_id:
				code = kw.get('code')
				client_id = instagram_id.instagram_client_id
				client_secret = instagram_id.instagram_client_secret
				base_url = request.env['ir.config_parameter'].sudo().get_param('web.base.url')
				redirect_uri = '%s/instagram/code/'%(base_url)
				token_url = 'https://api.instagram.com/oauth/access_token'
				data = {
					'client_id': client_id,
					'client_secret': client_secret,
					'redirect_uri': redirect_uri,
					'grant_type': 'authorization_code',
					'code': code,
				}
				response = requests.post(url = token_url, data = data)
				if response.status_code == 200:
					access_token = response.json().get('access_token', False)
					if access_token:
						long_lived_token_url = 'https://graph.instagram.com/access_token'
						data = {
							'grant_type': 'ig_exchange_token',
							'client_secret': client_secret,
							'access_token': access_token,
						}		
						response = requests.get(url = long_lived_token_url, params = data)
						long_lived_access_token = response.json().get('access_token', False)
						if instagram_id:
							instagram_id.instagram_access_token = long_lived_access_token
				else:
					_logger.info('Something went wrong!!! {} {}'.format(response.status_code, (response.json())))
		return request.redirect('/web#id={}&action={}&model=social.media.tabs&view_type=form'.format(instagram_id.id, action.id))

	def _get_instagram_data(self, token):
		media_url = 'https://graph.instagram.com/me/media?fields=id,caption,media_url,timestamp&access_token=%s'%(token)
		response = requests.get(url = media_url) 

		data = response.json().get('data', False)
		if data:
			feeds = []
			for post in data:
				data_dict = {}
				node_url = 'https://graph.instagram.com/%s?fields=id,media_type,media_url,caption,timestamp&access_token=%s'%(post.get('id'), token)
				node_data = requests.get(url = node_url)
				data_dict.update(
					node_data.json()
				)
				feeds.append(data_dict)
			return feeds
		return False

	@http.route('/socialTabs/url', type='json', auth='public', website=True)
	def social_tabs_url(self, tab_id=False):
		tab_obj = request.env['social.media.tabs'].sudo().browse(int(tab_id))
		values = {}
		if tab_obj:
			values['type'] = tab_obj.media_type,
			if tab_obj.media_type == 'social_tab':
				values['limit'] = tab_obj.limit
				if tab_obj.social_tab:
					values['social_tab'] = tab_obj.social_tab
					if str(tab_obj.social_tab) == 'twitter':
						values['twiter_user_id'] = str(tab_obj.twiter_user_id),
					if  tab_obj.social_tab in  ['facebook','fblike']:
						values['url'] = 'https://graph.facebook.com/' + tab_obj.facebook_id,
						# values['fb_token'] = tab_obj.fb_token,
						values['fb_id'] = tab_obj.facebook_id,
					if tab_obj.social_tab == 'youtube':
						values['api_key'] = tab_obj.yt_api_key,
						values['channel_id'] = tab_obj.yt_channel_id,
						values['user_id'] = tab_obj.yt_user_id,
						values['subscribe'] = tab_obj.yt_show_subscribe,
					if tab_obj.social_tab == 'flickr':
						values['flickr_data'] = self._get_flickr_data(tab_obj.flickr_id)
					if tab_obj.social_tab == 'pinterest':
						values['pinterest_id'] = tab_obj.pinterest_id,
					if tab_obj.social_tab == 'vimeo':
						#Python lib fro vimeo
						vimeoID = tab_obj.vimeo_id
						token = tab_obj.vimeo_token
						clientID = tab_obj.vimeo_client_id
						clientSecret = tab_obj.vimeo_client_secret
						values.update({
							'vimeo_data': self._get_vimeo_data(vimeoID, token, clientID, clientSecret)
						})
					if tab_obj.social_tab == 'tumblr':
						values['tumblr_id'] = tab_obj.tumblr_id,
					if tab_obj.social_tab == 'stumbleupon':
						values['stumbleupon_id'] = tab_obj.stumbleupon_id,
					if tab_obj.social_tab == 'google':
						values['google_id'] = tab_obj.google_id,
						values['google_api_key'] = tab_obj.google_api_key,
					if tab_obj.social_tab == 'instagram':
						token = tab_obj.instagram_access_token
						values.update({
							'instagram_data': self._get_instagram_data(token)
						})
			else:
				values['custom_html'] =  tab_obj.custom_html
		return values