# -*- coding: utf-8 -*-
#################################################################################
# Author	  : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2015-Present Webkul Software Pvt. Ltd.
# All Rights Reserved.
#
#
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
#
# You should have received a copy of the License along with this program.
# If not, see <https://store.webkul.com/license.html/>
#################################################################################

from . import models
from . import controllers
def pre_init_check(cr):
	from odoo.service import common
	from odoo.exceptions import Warning
	versionInfo = common.exp_version()
	serverSerie =versionInfo.get('server_serie')
	if serverSerie!='13.0':
		raise Warning(f'Module support Odoo series 13.0, found {serverSerie}.')
	return True
