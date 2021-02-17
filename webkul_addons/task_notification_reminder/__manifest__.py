# -*- coding: utf-8 -*-
##########################################################################
# Author      : Webkul Software Pvt. Ltd. (<https://webkul.com/>)
# Copyright(c): 2017-Present Webkul Software Pvt. Ltd.
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
    'name': 'Task Notification Reminder',
    'summary': 'This module is used to send mail the deadline notification mail according to their setting.',
    'category': 'Project Management',
    'version': '1.0.0',
    'sequence': 1,
    'author': "Webkul Software Pvt. Ltd.",
    "license":  "Other proprietary",
    'website': 'https://store.webkul.com/Odoo-Task-Notification-Reminder.html',
    'description': """This module is used to send mail the deadline notification mail according to their setting.""",
    "live_test_url":  "http://odoodemo.webkul.com/?module=task_notification_reminder",
    'depends': [
        'project',
        'project_advance_team'
        ],
    'css': [
        'static/src/css/mail.css',
        ],
    'data': [
            'edi/notification_cron.xml',
            'edi/cron_mail_template.xml',
            'views/wk_notification_setting_view.xml',
            'security/ir.model.access.csv',
            'security/wk_notification_setting_security.xml',
    ],
    "images":  ['static/description/Banner.png'],
    "application":  True,
    "installable":  True,
    "auto_install":  False,
    "price":  45,
    "currency":  "EUR",
    "pre_init_hook":  "pre_init_check",
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
