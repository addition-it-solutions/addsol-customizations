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


class profitability_report(models.Model):
    _name = "profitability.report"
    _description = ""
    _auto = False
    
    salesperson = fields.Char("Salesperson")
    income = fields.Float("Income")
    expense = fields.Float("Expenses")
    profit = fields.Float("Profit")


    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'profitability_report')
        cr.execute("""
            CREATE view profitability_report as
                SELECT 
                    res.id as id, 
                    res.name as salesperson, 
                    sum(Invoice_Total) as income , 
                    sum(expense_amount) as expense , 
                    (sum(Invoice_Total) - sum(expense_amount)) as profit
                FROM
                    ( SELECT id as res ,salesperson,Invoice_Total,NULL::float as expense_amount
                        FROM (
                            SELECT res.id, res.name as salesperson,sum(inv.amount_total) as Invoice_Total
                            FROM resource_resource res 
                                JOIN account_invoice inv ON inv.user_id = res.user_id
                            GROUP BY res.id, res.name ) invoice
                     UNION ALL
                     SELECT id ,salesperson,NULL::float as Invoice_Total , expense_amount
                     FROM (
                        SELECT res.id, res.name as salesperson, sum(exp.amount) as expense_amount
                        FROM resource_resource res 
                            JOIN hr_employee empl ON empl.resource_id = res.id 
                            JOIN hr_expense_expense exp ON empl.id = exp.employee_id
                        GROUP BY res.id,res.name) expense
                    ) results
                    JOIN resource_resource res ON res.id = results.res
                GROUP BY res.name,res.id
        """)
