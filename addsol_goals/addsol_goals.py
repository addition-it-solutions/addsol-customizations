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
    
class addsol_goals(models.Model):
    _name = 'addsol.goals'
    
    goal_partner_id = fields.Many2one('res.partner',"Goals")
    product_id = fields.Many2one('product.product', "Product", required=True)
    quantity = fields.Float("Quantity", required=True)


class addsol_res_partner(models.Model):
    _inherit = 'res.partner'
    
    start_date = fields.Date("Start Date")
    end_date = fields.Date("End Date")
    goal_ids = fields.One2many('addsol.goals', 'goal_partner_id')
    salesperson = fields.Boolean("Is a salesperson?")
    
    @api.one
    @api.constrains('id','start_date','end_date')
    def _check_periodicity_dates(self):
        """ This constraint is used for can not assign same period """
        for periodic_ids in self.browse(self.ids):

            domain =[
                 ('start_date', '=', periodic_ids.start_date),
                 ('end_date', '=', periodic_ids.end_date),
            ]
            if 'id' == periodic_ids.id:
                no_repeat_date = self.search_count(domain)
                if no_repeat_date > 1:
                    raise Warning(_('Can not assign same period'))
        return True
    
    

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
