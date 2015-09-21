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

#from openerp.osv import fields, osv
from openerp import models, fields, api, _
from openerp import tools


class party_ledger_report(models.Model):
    _name = "party.ledger.report"
    _description = ""
    _auto = False
    
    party = fields.Char("Party Name")
    invoice_amount = fields.Float("Invoice Amount")
    refund_amount = fields.Float("Refund Amount")
    payment_amount = fields.Float("Payment Amount")
    balance_amount = fields.Float("Balance Amount")

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'party_ledger_report')
        cr.execute("""
            CREATE view party_ledger_report as
              SELECT 
                  subq.id as id, 
                  subq.party as party, 
                  (subq.Invoice_Amount) as invoice_amount,
                  (subq.Refund_Amount) as refund_amount, 
                  (subq.Payment_Amount) as payment_amount, 
                  (COALESCE(subq.Invoice_Amount,0) - COALESCE(subq.Refund_Amount,0) - COALESCE(subq.Payment_Amount,0)) as balance_amount
              FROM (
                    SELECT part.id as id, part.name as party,
                        (SELECT sum(a.amount_Total)FROM account_invoice a 
                            WHERE a.type = 'out_invoice' AND a.partner_id = part.id GROUP BY a.partner_id) as invoice_amount,
                        (SELECT sum(b.amount_Total)  FROM account_invoice b 
                            WHERE b.type = 'out_refund' AND b.partner_id = part.id GROUP BY b.partner_id) as refund_amount,
                        (SELECT sum(acnt.amount) FROM account_voucher acnt 
                            WHERE acnt.partner_id = part.id) as payment_amount
                    FROM res_partner part
                WHERE customer = True AND active = True
                ) subq
        """)
