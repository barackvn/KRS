# -*- coding: utf-8 -*-
#################################################################################
# Author : Webkul Software Pvt. Ltd. (<https://webkul.com/>:wink:
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
# If not, see <https://store.webkul.com/license.html/>;
#################################################################################
from odoo import models, fields,api,_
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
from odoo.service.db import exp_duplicate_database,check_db_management_enabled, list_dbs, _drop_conn, exp_drop,exp_restore,dump_db,restore_db

from odoo import SUPERUSER_ID
from odoo.exceptions import AccessDenied
import odoo.release
import odoo.sql_db
import odoo.tools
from odoo.sql_db import db_connect
from odoo.tools import pycompat
from contextlib import closing
from odoo import tools
import threading
import psycopg2
import psycopg2.extensions
from odoo.http import request
import random
CUSTOM_QUERY = """UPDATE %s SET %s = '%s';"""
def random_Char():
    # the token has an entropy of about 120 bits (6 bits/char * 20 chars)
    chars = '7894561230ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789'
    return ''.join(random.SystemRandom().choice(chars) for _ in range(20))

def random_Bool():
    return random.choice([True, False])

def _getFormatedValue(model_name,field_name,field_type,state,fixed_value=False):
    make_query = False
    if state == "random":
        make_query = CUSTOM_QUERY%(model_name,field_name,random_Char(5))
    elif state == 'fixed':
        make_query = CUSTOM_QUERY%(model_name,field_name,fixed_value)
    elif state == 'clear':
        make_query = CUSTOM_QUERY%(model_name,field_name," ")
    return make_query

MESSAGE = _("<div> <b>Operation :</b> %s </br><b>Status :</b> %s </br> <b>Message : </b> %s </div>")
QUERY_MSG = _("Operation : %s ,\nStatus : %s ,\nMessage : %s ,\nRow affected : %s ")
AFTER_QUERY_EXECUTE_MSG = _("There is %s query executed on database name (%s), \n Successfull Queries : %s, \n Failed Queries : %s \n check the query history in 'Query Responses history menu'")

class InheritResPartner(models.Model):
    _inherit = "res.partner"

    def rpc_compute_display_name(self):
        partners = self.search([])
        partners._compute_display_name()
        return True

class DatabaseBackup(models.Model):
    _name = "database.backup"

    def _getDefaultDbName(self):
        return self._cr.dbname
    def _getDefaultCompany(self):
        return 1

    def _getDefaultCloneDbName(self):
        return f'an_db({fields.datetime.now().strftime("%Y-%m-%d_%H:%M")})'

    def _getDefaultPgHost(self):
        return tools.config['db_host'] or 'localhost'

    def _getDefaultPgPort(self):
        return tools.config['db_port'] or 5432

    def _getDefaultPgUser(self):
        return tools.config['db_user'] or 'postgres'

    def _getDefaultPgPassword(self):
        return tools.config['db_password'] or 'postgres'

    def _getMAilTemplate(self):
        return self.env.ref('db_anonymization.send_credential_email_email').id

    def show_msg_wizard(self,msg):
            partial_id = self.env['wk.wizard.message'].create({'text': msg})
            return {
                'name': "Message",
                'view_mode': 'form',
                'view_id': False,
                'view_type': 'form',
                'res_model': 'wk.wizard.message',
                'res_id': partial_id.id,
                'type': 'ir.actions.act_window',
                'nodestroy': True,
                'target': 'new',
            }

    name = fields.Char(string="Backup Name",required=True)
    conn_error_msg = fields.Text(string="Connection Message")
    state = fields.Selection([
        ("draft","Draft"),
        ("connection","DB Connection Successfull"),
        ("ready","Clone Database Ready"),
        ("error","Error"),
    ],string="State",default="draft")
    current_db_name = fields.Char(string="Current DB Name",default=_getDefaultDbName,readonly=True)
    postgres_host = fields.Char(string="Postgres Host",default=_getDefaultPgHost)
    postgres_port = fields.Integer(string="Postgres Port",default=_getDefaultPgPort)
    postgres_user = fields.Char(string="Postgres User",default=_getDefaultPgUser)
    postgres_passowrd = fields.Char(string="Postgres Password",default=_getDefaultPgPassword)
    clone_db_name = fields.Char(string="Clone DB Name",default=_getDefaultCloneDbName)
    is_fake_created = fields.Boolean("Is Faked Record")
    is_execute_anonymise = fields.Boolean("Is Anonymize Executed")
    credential_mail_id = fields.Many2one('mail.template',string="Mail Template",
                                          default=_getMAilTemplate,readonly=True)
    emails = fields.Text(string="Emails")
    company_id = fields.Many2one('res.company',string="Company",default=_getDefaultCompany,readonly=True)
    mail_subject = fields.Char(string="Subject",required="1",readonly=False,related="credential_mail_id.subject")
    body_text = fields.Html(related='credential_mail_id.body_html',string="Mail Body",readonly=False,required="1")
    attachment_ids = fields.Many2many(related='credential_mail_id.attachment_ids',string="Attachments",readonly=False)
    clone_db_login = fields.Char(string="CloneDB Login",required=True)
    clone_db_passowrd = fields.Char(string="CloneDB Password",required=True)

    def action_create_fakerecord(self):
        res_id = self.env['fake.contact.wizard'].create({"database_backup_id": self.id})
        return {
				'type'      : 'ir.actions.act_window',
				'name'      : 'Fake Records Creation',
				'view_type' : 'form',
				'view_mode' : 'form',
				'res_model' : 'fake.contact.wizard',
                'res_id'    : res_id.id,
				'target'    : 'new',
			}
        # self.is_fake_created= True

    def action_check_connection(self):
        if not self.is_fake_created:
            raise UserError(_("Before check database connection. Click on Create Fake Record button."))
        operation = "On creating Connection to Postgres DB."
        msg = ""
        status = ""
        try:
            dbConnection = psycopg2.connect(
                                    host=self.postgres_host,
                                    port=self.postgres_port,
                                    database=self.current_db_name,
                                    user=self.postgres_user,
                                    password=self.postgres_passowrd)
            self.state = 'connection'
            status = 'success'
            msg = "Postgres Connection Successfull Created. "

        except Exception as e:
            _logger.info("< EXCEPTION : POSTGRES %r >",e)
            status = 'failure'
            msg = str(e)
            self.state = 'error'
        self.conn_error_msg = msg
        return self.show_msg_wizard(MESSAGE%(operation,status,msg))

    def action_create_backup(self):
        db_original_name = self.current_db_name
        db_name = self.clone_db_name
        operation = f"Cloning of Database ({db_original_name})"
        status = "Success"
        msg = ""
        if db_name in list_dbs():
            self.state = 'ready'
            _logger.info(_("< MESSAGE : You already create a dublictae Database. >"))
            msg = _("Database (%s) Backup is created successfully of name %s.")%(self.current_db_name,self.clone_db_name)
            self.conn_error_msg = msg
            return self.show_msg_wizard(MESSAGE%(operation,status,msg))
        else:

            try:
                status = exp_duplicate_database(db_original_name, db_name)
                # in function "exp_duplicate_database" all the cursor is closed and commit and server lost the connection.
                # so the updation of DB not occur
            except Exception as e:
                _logger.info("< Duplicate Database Exception: %r >", e)



    def check_resote_db_exist(self):
        db_original_name = self.current_db_name
        db_name = self.clone_db_name
        operation = f"Cloning of Database ({db_original_name})"
        status = "Success"
        msg = ""
        if self.clone_db_name in list_dbs():
            self.state = 'ready'
            msg = _("Database (%s) Backup is created successfully of name %s.")%(self.current_db_name,self.clone_db_name)
            self.conn_error_msg = msg
            return
        else:
            status = 'failure'
            msg = _("Clone Database (%s) not Found. Click on Create Backup Button.")%db_name
            self.conn_error_msg = msg
            return self.show_msg_wizard(MESSAGE%(operation,status,msg))



    def action_execute_query(self):
        queries_all = self.env['anonymize.query'].sudo().search([])
        if not queries_all:
            raise UserError(_("There is no 'Query' found in Query List menu. Please write down the Query which you want to execute in clone Database."))
        if self.is_execute_anonymise:
            return self.show_msg_wizard("Query already executed.")

        qHitoryObj = self.env['query.history'].sudo()
        db_name = self.clone_db_name
        db = odoo.sql_db.db_connect(db_name)
        threading.current_thread().dbname = db_name
        success_query = 0
        fail_query = 0
        for query in queries_all:
            query_history = qHitoryObj.search(
                [
                    ('anonymize_query_id', '=', query.id),
                    ('database_backup_id', '=', self.id),
                ],
                limit=1,
            ) or qHitoryObj.create(
                {'anonymize_query_id': query.id, 'database_backup_id': self.id}
            )
            cr = db.cursor()
            operation = query.name
            status = "failure"
            row_affected = 0
            msg = ""
            make_query = False
            try:
                if query.query_type == 'custom':
                    make_query = _getFormatedValue(model_name=query.model_id.model.replace(".","_"),
                                                   field_name= query.field_id.name,
                                                   field_type=query.field_ttype,
                                                   state=query.state,
                                                   fixed_value=query.fixed_text
                                                    )
                elif query.query_type == 'raw':
                    make_query = query.database_query
                if make_query:
                    self.is_execute_anonymise = True
                    cr.execute(make_query)
                    cr.commit()
                    row_affected = cr.rowcount
                    status = 'success'
                    msg = "Opeartion Successfull. "
                    success_query +=1
                else:
                    status = 'failed'
                    msg = "No Query Found Opeartion Fail. "
                    fail_query +=1
            except Exception as e:
                _logger.exception('Unexpected exception while processing anonymization job %r', e)
                msg = str(e)
                fail_query +=1
            finally:
                cr.close()
            query_history.query_response = QUERY_MSG%(operation,status,msg,row_affected)
        self.action_uninstall_module()
        return self.show_msg_wizard(AFTER_QUERY_EXECUTE_MSG%(str(len(queries_all)),db_name,success_query,fail_query))

    def action_change_clone_db_password(self):
        res_id = self.env['change.credential.wizard'].create({"database_backup_id": self.id})
        return {
				'type'      : 'ir.actions.act_window',
				'name'      : 'Credential Configuration',
				'view_type' : 'form',
				'view_mode' : 'form',
				'res_model' : 'change.credential.wizard',
                'res_id'    : res_id.id,
				'target'    : 'new',
			}

    def action_credential_mail(self):
        if not self.emails:
            raise UserError(_("Please Enter the Recipent Email Address for Sending Email."))
        result = self.env['mail.template'].browse(self.credential_mail_id.id).send_mail(self.id)

    def action_uninstall_module(self):
        db_name = self.clone_db_name
        db = odoo.sql_db.db_connect(db_name)
        threading.current_thread().dbname = db_name
        try:
            cr0 = db.cursor()
            cr0.execute(
                f"UPDATE res_users SET login='{self.clone_db_login}',password='{self.clone_db_passowrd}' WHERE id = 2;"
            )

            cr0.commit()
            affect = cr0.rowcount
            _logger.info("****** CHANGE ADMIN CREDENTIAL OF CLONE DATABASE *******")
        except Exception as e:
            _logger.exception('Unexpected exception while changing admin credential %r', e)
        finally:
            cr0.close()
        module = self.env['ir.module.module'].search([('name','=','db_anonymization')],limit=1)
        base_url = request and request.httprequest.url_root or self.env['ir.config_parameter'].sudo().get_param('web.base.url')
        url = base_url[:-1]
        db = self.clone_db_name
        username = self.clone_db_login
        password = self.clone_db_passowrd
        import xmlrpc.client
        common = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/common')
        uid = common.authenticate(db, username, password, {})
        models = xmlrpc.client.ServerProxy(f'{url}/xmlrpc/2/object')
        # Cannot call private functions remotely like _compute_display_name. Created a non private method and then made the xmlrpc call to that
        models.execute_kw(db, uid, password,'res.partner', 'rpc_compute_display_name',[SUPERUSER_ID])
        ret = models.execute_kw(db, uid, password,'ir.module.module', 'button_immediate_uninstall',[[module.id]])

        _logger.info("***** UNINSTALLING ANONYMIZATION MODULE FROM CLONE DATABASE ****")
