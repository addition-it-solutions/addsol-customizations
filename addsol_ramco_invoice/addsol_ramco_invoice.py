# -*- coding: utf-8 -*-
##############################################################################
#
#    OpenERP, Open Source Management Solution
#    Copyright (C) 2004-2010 Tiny SPRL (<http://tiny.be>).
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

class addsol_ramco_invoice(models.Model):
    _inherit = 'account.invoice'
    

    nxt_number = fields.Integer(string='Next Number')

    @api.multi
    def action_number(self):
        previous_id = self.search([('id','not in',self.ids),('state', '=', 'draft')],limit=1,order='id DESC')
        sequence_obj = self.env['ir.sequence'].browse(self.journal_id.sequence_id.id)
        if previous_id:
            new_number = previous_id.journal_id.sequence_id.number_next
            new_inv_number = sequence_obj.next_by_id(self.journal_id.sequence_id.id)
        else:
            new_number = self.journal_id.sequence_id.number_next
            new_inv_number = sequence_obj.next_by_id(self.journal_id.sequence_id.id)
            
        self.write({'number': new_inv_number,'nxt_number':new_number})
        #self.write({'number': new_inv_number,'internal_number':new_inv_number})
        return True
    
    @api.multi
    def unlink(self):
        for inv_id in self.browse(self.ids):
            seq_id = inv_id.journal_id.sequence_id.id
            sequence_obj = self.env['ir.sequence'].browse(seq_id)
            sequence_obj.write({'number_next': inv_id.nxt_number})
        return super(addsol_ramco_invoice, self).unlink()

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
