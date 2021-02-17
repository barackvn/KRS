# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
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
##########################################################################

{
  'name'                 :  'Merge Purchase Order',
  'version'              :  '1.0.1',
  'category'             :  'Purchases',
  'author'               :  'Webkul Software Pvt. Ltd.',
  'website'              :  'https://store.webkul.com/Odoo-Merge-Purchase-Order.html',
  'sequence'             :  1,
  'summary'              :  'Join two or more Purchase quotations from the same vendor into a new single quotation.',
  'description'          :  """Merge Purchase Order """,
  "live_test_url"        :  "http://odoodemo.webkul.com/?module=merge_purchase_orders",
  'depends'              :  ['purchase'],
  'data'                 :  [
                              'data/data.xml',
                              'wizard/merge_po_wizard_view.xml',
                              'wizard/message_po_wizard_view.xml',
                              'views/purchase_views.xml',
                            ],
  "images"               :  ['static/description/Banner.png'],
  'application'          :  True,
  'installable'          :  True,
  'active'               :  False,
  "price"                :  35,
  "currency"             :  "EUR",
  'pre_init_hook'        :  'pre_init_check',
}
