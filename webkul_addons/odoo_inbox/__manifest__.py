# -*- coding: utf-8 -*-

{
    'name': 'Mailbox (Odoo Inbox)',
    'category': 'Website',
    'author': 'Kanak Infosystems LLP.',
    'support': 'info@kanakinfosystems.com',
    'summary': 'This module is used to send or receive mail through the recipient, user can do the following types of message-send message, inbox message, starred or unstarred message, etc.',
    'version': '2.1',
    'description':
        """
Mailbox (Odoo Inbox)
====================
        """,
    'depends': ['website', 'mail', 'contacts'],
    'data': [
        'data/data.xml',
        'security/ir.model.access.csv',
        'views/template.xml',
        'views/mail_message.xml',
        'views/res_users_views.xml',
    ],
    'images': ['static/description/banner.gif'],
    'installable': True,
    'license': 'OPL-1',
    'bootstrap': True,  # load translations for login screen
    'application': True,
    'price': 250,
    'currency': 'EUR',
}
