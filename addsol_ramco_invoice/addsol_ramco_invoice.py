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

class addsol_ramco_invoice(models.Model):
    _inherit = 'account.invoice'
    

    nxt_number = fields.Integer(string='Next Number')
    order_detail = fields.Char("Your Order Details")
    freight_paid_topay = fields.Char("Freight Paid / To Pay")
    excisable_commodity_id = fields.Many2one('ramco.excisable.commodity',"Excisable Commodity")
    tariff_sub_heading_id = fields.Many2one('ramco.tariff.heading',"Tariff Sub Heading No.")
    exemption_notification_no = fields.Char("Exemption Notification No.")
    debit_entry_txt = fields.Char("Debit Entry Text")
    time_of_issue = fields.Char("Time of Issue")
    time_of_removal = fields.Char("Time of Removal")
    dispatch_through = fields.Char("Dispatch Through")
    dispatch_to = fields.Char("Dispatch To")
    l_r_details = fields.Char("LR Details")
    vehicle_no = fields.Char("Vehicle No")

    @api.multi
    def action_number(self):
        # This is code generate invoice number from ir.sequence object  
        previous_id = self.search([('id','not in',self.ids),('state', '=', 'draft')],limit=1,order='id DESC')
        sequence_obj = self.env['ir.sequence'].browse(self.journal_id.sequence_id.id)
        if previous_id:
            new_number = previous_id.journal_id.sequence_id.number_next
        else:
            new_number = self.journal_id.sequence_id.number_next
            
        new_inv_number = sequence_obj.next_by_id(self.journal_id.sequence_id.id)
        self.write({'number': new_inv_number,'nxt_number':new_number})
        #self.write({'number': new_inv_number,'internal_number':new_inv_number})
        return True
    
    @api.multi
    def unlink(self):
        # This is code delete the invoice & update next_number of ir.sequence object
        for inv_id in self.browse(self.ids):
            seq_id = inv_id.journal_id.sequence_id.id
            sequence_obj = self.env['ir.sequence'].browse(seq_id)
            sequence_obj.write({'number_next': inv_id.nxt_number})
        return super(addsol_ramco_invoice, self).unlink()
    
    
class ramco_account_invoice_line(models.Model):
    _inherit = 'account.invoice.line'
    
    sr_no = fields.Integer("Sr. No")
    bundles_no_desc = fields.Char("Bundles No & descriprion")


class ramco_excisable_commodity(models.Model):
    _name = 'ramco.excisable.commodity'
    _description = "Excisable Commodity"
    
    name = fields.Char("name", required=True, size=500)

class ramco_tariff_heading(models.Model):
    _name = 'ramco.tariff.heading'
    _description = "Tariff Sub Heading No."
    
    name = fields.Char("Tariff Sub Heading Number", required=True, size=200)
    
class addsol_ramco_res_partner(models.Model):
    _inherit = 'res.partner'
    
    ecc_no = fields.Char("Ecc No")
    division = fields.Char("Division")
    range = fields.Char("Range")
    commissionerate = fields.Char("Commissionerate")
    supplier_code_no = fields.Char("Supplier Code No.")
    
class addsol_invoice_tax(models.Model):
    _inherit = 'account.invoice.tax'
    
    @api.v8
    def compute(self,invoice):
        # This function is calculate tax & update tax_categ field of account.invoice.tax object which is used to print total of un-taxed amount & base_amount of VAT
        res = super(addsol_invoice_tax, self).compute(invoice)
        dict=[]
        dict = res.values()
        for val in res.values():
            tax_name = val.get('name')
            tax_id = self.env['account.tax'].search([('name', '=', tax_name)])
            for tax_ids in tax_id:
                tax = self.env['account.tax'].browse(tax_ids.id)
                category = tax.tax_categ
                frm = tax.is_form
                val['tax_categ'] = category
                val['is_form'] =  frm
        return res
        

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
