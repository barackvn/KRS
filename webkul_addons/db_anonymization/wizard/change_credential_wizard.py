# -*- coding: utf-8 -*-
################################################################################
#
#   Copyright (c) 2016-Present Webkul Software Pvt. Ltd. (<https://webkul.com/>)
#
################################################################################
from odoo import api, fields, models, _ , SUPERUSER_ID
import odoo.sql_db
import odoo.tools
from odoo.sql_db import db_connect
import logging
_logger = logging.getLogger(__name__)
from odoo.exceptions import UserError
from odoo.exceptions import Warning
import threading

QUERY_MSG = _("Operation : %s ,\nStatus : %s ,\nMessage : %s ,\nRow affected : %s ")

class ChangeCredentialWizard(models.TransientModel):
    _name = "change.credential.wizard"

    user_name = fields.Char(string='Clone DB User Name')
    user_password = fields.Char(string='Clone DB User Password')
    database_backup_id = fields.Many2one('database.backup',string='Database Backup Id',required=True)


    def action_change_credential(self):
        status = False
        msg = False
        operation = "Reset Users Password"
        alter_user_id = self.isUserExist(self.user_name,self.user_password)
        if alter_user_id:
            db_name = self.database_backup_id.clone_db_name
            db = odoo.sql_db.db_connect(db_name)
            threading.current_thread().dbname = db_name
            cr = db.cursor()
            try:
                cr.execute("UPDATE res_users SET password = '%s' WHERE id = %s"%(self.user_password,alter_user_id))
                cr.commit()
                row_affected = cr.rowcount
                status = "success"
                msg = "Opeartion Successfull."
            except Exception as e:
                _logger.exception('Unexpected exception while processing anonymization job %r', e)
                status = "failure"
                msg = "Exception occurs : "
                msg += str(e)
            finally:
                cr.close()
            if status == "success":
                raise UserError(_("Password Updated Successfully. For User '%s'"%self.user_name))
            else:
                raise UserError(_("Something went wrong.."))
        else:
            raise UserError(_(" UserName doesn't Exist. Please enter the correct user."))



    def isUserExist(self,user_name,user_password):
        result = False
        db_name = self.database_backup_id.clone_db_name
        db = odoo.sql_db.db_connect(db_name)
        threading.current_thread().dbname = db_name
        cr = db.cursor()
        try:
            cr.execute("SELECT id from res_users where login = '%s'"%user_name)
            data = cr.fetchone()
            if not data:
                result = False
            else:
                result = data[0]
        except Exception as e:
            _logger.exception('Unexpected exception while processing anonymization job %r', e)
            _logger.info('< EXCEPTION : Unexpected exception while processing anonymization job %r >', e)
            result = False
        finally:
            cr.close()
        return result
