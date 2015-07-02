# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2015-2016 Addition IT Solutions Pvt. Ltd. (<http://www.aitspl.com>).
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from datetime import datetime, timedelta

from openerp.tools import DEFAULT_SERVER_DATETIME_FORMAT
from openerp import models, fields, api, _

def refresh_db_job(cr):
    cr.execute("select tablename from pg_tables where schemaname = 'public' and tablename ilike 'hr_%'")
    now = datetime.now().strftime(DEFAULT_SERVER_DATETIME_FORMAT)
    prev_day = (datetime.now() + timedelta(hours=-24)).strftime(DEFAULT_SERVER_DATETIME_FORMAT)
    
    for table in cr.fetchall():
        cr.execute("delete from %s where create_date > '%s' and create_date < '%s'"% (str(table[0]), prev_day, now))
    return now

class refresh_db(models.Model):
    _name = 'refresh.db'

    name = fields.Datetime('Refreshed On:')

    @api.model
    def refresh_db_daily(self):
        dt = refresh_db_job(self._cr)
        self.create({'name': dt})

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:

