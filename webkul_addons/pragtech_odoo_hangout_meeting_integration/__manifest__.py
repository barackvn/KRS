{
    'name': 'Odoo Google meet Integration', # 'Odoo Google Hangout Integration',
    'version': '14.0.1',
    'author': 'Pragmatic TechSoft Pvt Ltd.',
    'website': 'http://www.pragtech.co.in',
    'category': 'Other',
    'depends': ['calendar'],
    'summary': 'Odoo Join a Google Meetings Connector odoo Google Hangout Connector odoo Hangout integration',
    'description': '''
Odoo Join a Google Meetings Connector
=====================================
This app adds the feature of creating Meetings in Odoo calendar with Google Hangouts. This app also adds the features of create meeting as
 google calendar events directly from odoo. Calendar meetings in Odoo will automatically be linked into Google Calendar Events.
 When the user clicks the phone icon, the user will redirect to join a meeting page and enter the Meeting code, then join.
 Now you do not need to separately sign in to google calendar. Everything happens through Odoo. It is completely secure.

 Features
 --------
    * Multi Company Support
    * Multi User’s Support
    * Works with Community and Enterprise Odoo Edition
    * Connect to Google Hangout Meeting directly from Odoo
    * Backed by our 3 months bugs free support

''',
    'data': [
        'views/res_company_view.xml',
        'views/res_users_view.xml',
        'views/meeting_view.xml',
        'templates/mail_data.xml',
    ],
    'images': ['static/description/google-hangout-meeting-integration-gif.gif'],
    'live_test_url': 'https://www.pragtech.co.in/company/proposal-form.html?id=103&name=odoo-google-hangout-meeting-integration',
    'currency': 'USD',
    'license': 'OPL-1',
    'price': 49.00,
    'installable': True,
    'application': True,
    'auto_install': False,
}
