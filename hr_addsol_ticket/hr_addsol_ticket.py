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

from openerp import models, fields, api, _
from datetime import datetime

class hr_addsol_ticket(models.Model):
    _name = "hr.addsol.ticket"
    _description = "Ticket"
    _rec_name = 'employee_id'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _track = {
        'state': {
            'hr_addsol_ticket.mt_ticket_confirmed': lambda self, cr, uid, obj, ctx=None: obj.state == 'confirm',
            'hr_addsol_ticket.mt_ticket_resolved': lambda self, cr, uid, obj, ctx=None: obj.state == 'validate',
        },
    }

    problem_desc = fields.Text("Description")
    employee_id = fields.Many2one('hr.employee', "Employee", required=True, track_visibility='always')
    ticket_date = fields.Datetime("Date", required=True, track_visibility='always')
    state = fields.Selection([('draft', 'To Submit'), ('cancel', 'Cancelled'),('confirm', 'To Resolve'), ('validate', 'Resolved'), ('refuse', 'Refused')], 'Status', readonly=True)
    resolved_date = fields.Datetime("Resolved Date")
    
    @api.cr_uid_ids_context
    def _employee_get(self, cr, uid, context=None):
        emp_id = context.get('default_employee_id', False)
        if emp_id:
            return emp_id
        ids = self.pool.get('hr.employee').search(cr, uid, [('user_id', '=', uid)], context=context)
        if ids:
            return ids[0]
        return False
    
    _defaults = {
        'employee_id' : _employee_get,
        'state' : 'draft',
        'ticket_date' : datetime.now(),
     }
    
    @api.one
    def request_send(self):
        self.write({'state': 'confirm'})
        return True
    
    @api.one
    def request_approve(self):
        self.write({'state': 'validate','resolved_date':datetime.now()})
        return True
    
    @api.one
    def refuse(self):
        self.write({'state': 'refuse'})
        return True
    
    @api.one
    def reset(self):
        self.write({'state': 'cancel'})
        return True
    
    @api.cr_uid_ids_context
    def create(self, cr, uid, vals, context=None):
        ctx = dict(context or {}, mail_create_nolog=True)
        new_id = super(hr_addsol_ticket,self).create(cr, uid, vals, context=ctx)
        self.message_post(cr, uid, [new_id], body="Ticket created", context=ctx)
        return new_id

