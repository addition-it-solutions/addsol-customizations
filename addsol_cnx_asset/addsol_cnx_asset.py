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
from datetime import datetime
from dateutil.relativedelta import relativedelta

from openerp.osv import osv

class addsol_account_asset(osv.osv):
    _inherit = 'account.asset.asset'
    
    def compute_depreciation_board(self, cr, uid, ids, context=None):
        depreciation_lin_obj = self.pool.get('account.asset.depreciation.line')
        currency_obj = self.pool.get('res.currency')
        for asset in self.browse(cr, uid, ids, context=context):
            if asset.value_residual == 0.0:
                continue
            posted_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_check', '=', True)],order='depreciation_date desc')
            old_depreciation_line_ids = depreciation_lin_obj.search(cr, uid, [('asset_id', '=', asset.id), ('move_id', '=', False)])
            if old_depreciation_line_ids:
                depreciation_lin_obj.unlink(cr, uid, old_depreciation_line_ids, context=context)

            amount_to_depr = residual_amount = asset.value_residual
            if asset.prorata:
                depreciation_date = datetime.strptime(self._get_last_depreciation_date(cr, uid, [asset.id], context)[asset.id], '%Y-%m-%d')
            else:
                purchase_date = datetime.strptime(asset.purchase_date, '%Y-%m-%d')
                #if we already have some previous validated entries, starting date isn't 1st January but last entry + method period
                if (len(posted_depreciation_line_ids)>0):
                    last_depreciation_date = datetime.strptime(depreciation_lin_obj.browse(cr,uid,posted_depreciation_line_ids[0],context=context).depreciation_date, '%Y-%m-%d')
                    depreciation_date = (last_depreciation_date+relativedelta(months=+asset.method_period))
                else:
                    # depreciation_date = start date of fiscal year or 1st January of purchase year
                    fiscal_date = self.pool.get('account.fiscalyear').search_read(cr, uid, [('date_start', '<=', purchase_date), ('date_stop', '>=', purchase_date)], ['date_start'], context=context)
                    if fiscal_date:
                        fis_date = datetime.strptime(fiscal_date[0]['date_start'], '%Y-%m-%d') 
                    depreciation_date = datetime(fis_date.year, fis_date.month, fis_date.day)
                    depn_start_date = datetime(purchase_date.year, purchase_date.month, purchase_date.day)
#                     else:
#                         depreciation_date = datetime(purchase_date.year, 1, 1)
            day = depreciation_date.day
            month = depreciation_date.month
            year = depreciation_date.year
            total_days = (year % 4) and 365 or 366

            undone_dotation_number = self._compute_board_undone_dotation_nb(cr, uid, asset, depreciation_date, total_days, context=context)
            if depn_start_date.month > fis_date.month:
                diff_month = (12 * depn_start_date.year + depn_start_date.month) - (12 * fis_date.year + fis_date.month)
            for x in range(len(posted_depreciation_line_ids), undone_dotation_number):
                new_vals = {}
                i = x + 1
                amount = self._compute_board_amount(cr, uid, asset, i, residual_amount, amount_to_depr, undone_dotation_number, posted_depreciation_line_ids, total_days, depreciation_date, context=context)
                residual_amount -= amount
                vals = {
                     'amount': amount,
                     'asset_id': asset.id,
                     'sequence': i,
                     'name': str(asset.id) +'/' + str(i),
                     'remaining_value': residual_amount,
                     'depreciated_value': (asset.purchase_value - asset.salvage_value) - (residual_amount + amount),
                     'depreciation_date': depreciation_date.strftime('%Y-%m-%d'),
                }
                if depn_start_date.month > fis_date.month:
                    if i == 1:
                        new_amount = ((asset.method_period - diff_month) * amount)/asset.method_period
                        new_dep_value = (asset.purchase_value - asset.salvage_value) - (residual_amount + new_amount)
                        residual_amount = residual_amount + new_dep_value
                        vals.update({'amount': new_amount, 'depreciation_date': depn_start_date.strftime('%Y-%m-%d'),
                                     'remaining_value': residual_amount})
                    if i == undone_dotation_number:
                        amount = amount_to_depr / (undone_dotation_number - len(posted_depreciation_line_ids))
                        new_residual_amount = amount - new_amount
                        dep_value = (asset.purchase_value - asset.salvage_value) - (new_residual_amount + amount)
                        vals.update({'remaining_value': new_residual_amount, 'depreciated_value': dep_value, 'amount': amount})
                        depn_end_date = depreciation_date + relativedelta(months=+asset.method_period)
                        new_vals.update({
                                    'amount': amount - new_amount,
                                     'asset_id': asset.id,
                                     'sequence': i + 1,
                                     'name': str(asset.id) +'/' + str(i + 1),
                                     'remaining_value': residual_amount,
                                     'depreciated_value': dep_value + amount,
                                     'depreciation_date': depn_end_date.strftime('%Y-%m-%d'),
                        })
                depreciation_lin_obj.create(cr, uid, vals, context=context)
                if new_vals:
                    depreciation_lin_obj.create(cr, uid, new_vals, context=context)
                # Considering Depr. Period as months
                depreciation_date = (datetime(year, month, day) + relativedelta(months=+asset.method_period))
                day = depreciation_date.day
                month = depreciation_date.month
                year = depreciation_date.year

        return True

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: