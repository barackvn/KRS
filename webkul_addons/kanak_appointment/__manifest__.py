# -*- coding: utf-8 -*-
# Copyright (C) Kanak Infosystems LLP.

{
    'name': 'Kanak Calendar Appointment',
    'version': '1.0',
    'summary': 'This module is used to book appointment offered by a company on its e-commerce platform online in odoo.',
    'description': """
Kanak Calendar Appointment
    This module is used to book appointment offered by a company on its e-commerce platform online in odoo.
===========================
    """,
    'license': 'OPL-1',
    'author': 'Kanak Infosystems LLP.',
    'website': 'https://www.kanakinfosystems.com',
    'images': ['static/description/banner.gif'],
    'category': 'website',
    'depends': ['website', 'mail', 'calendar', 'contacts', 'pragtech_odoo_hangout_meeting_integration'],
    'data': [
        'data/appointment_data.xml',
        'views/res_partner.xml',
        'views/calendar_view.xml',
        'views/appointment_template.xml',
        'views/calendar_asset.xml',
        'security/ir.model.access.csv',
        'security/ir_rule.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
    'price': 149,
    'currency': 'EUR',
    'live_test_url': 'https://youtu.be/D1igSOPAebE',
}
