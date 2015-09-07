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


class top_product_reoprt(models.Model):
    _name = "top.product.report"
    _description = ""
    _auto = False
    
    name_template = fields.Char("Product Name")
    amount_total = fields.Float("Invoice Total")
    

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'top_product_reoprt')
        cr.execute("""
            CREATE view top_product_reoprt as
              SELECT 
                    product.id as id,
                    sum(invl.price_subtotal) as amount_total, 
                    product.name as name_template
              FROM account_invoice_line invl   
                  JOIN account_invoice inv ON invl.invoice_id = inv.id
                  JOIN product_template product ON product.id = invl.product_id
              WHERE inv.type ='out_invoice'
              GROUP BY 
                  product.name,product.id
              ORDER BY 
                  amount_total DESC
        """)
