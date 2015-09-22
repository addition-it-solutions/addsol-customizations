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
import time
from openerp.osv import osv
from openerp.report import report_sxw
from report_far_common import report_far_common

class report_depreciation_schedule(report_sxw.rml_parse, report_far_common):
    _name = 'report.depn.schedule'
    
    def set_context(self, objects, data, ids, report_type=None):
        asset_categ_obj = self.pool.get('account.asset.category')
        ctx = self.context.copy()
        ctx['fiscalyear'] = data['form']['fiscalyear_id']
        ctx['period_from'] = data['form']['period_from']
        ctx['period_to'] = data['form']['period_to']
        data['form'].update({'state': 'open'})
        self.context.update(ctx)
        if (data['model'] == 'ir.ui.menu'):
            new_ids = asset_categ_obj.search(self.cr, self.uid, [])
            objects = asset_categ_obj.browse(self.cr, self.uid, new_ids)
        return super(report_depreciation_schedule, self).set_context(objects, data, new_ids, report_type=report_type)
    
    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(report_depreciation_schedule, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_fiscalyear': self._get_fiscalyear,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_assets': self._get_assets,
            'get_depreciations': self._get_depreciations,
            'get_depreciated_amount': self._get_depreciated_amount,
            'sum_assets': self._sum_assets,
            'current_depreciation_amount': self._current_depreciation_amount,
            'total_depreciated_amount': self._total_depreciated_amount,
            'total_current_depreciation': self._total_current_depreciation,
        })
        self.context = context

    def _sum_assets(self, category):
        addition = 0.0
        data = {'form': self.context}
        assets = self._get_assets(category, data)
        for asset in assets:
            addition += asset.purchase_value
        return addition

    def _get_depreciations(self, asset):
        depn_obj = self.pool.get('account.asset.depreciation.line')
        period_obj = self.pool.get('account.period')
        cr = self.cr
        uid = self.uid
        context = self.context
        res = []
        period_from = period_to = False
        if context.get('period_from', False):
            period_from = context['period_from']
        if context.get('period_to', False):
            period_to = context['period_to']
        if period_from and period_to:
            start_date = period_obj.browse(cr, uid, period_from).date_start
            end_date = period_obj.browse(cr, uid, period_to).date_stop
        domain = [('depreciation_date','>=',start_date), 
                  ('depreciation_date','<=',end_date),
                  ('asset_id','=',asset.id),
                  ('parent_state','=','open'),
                  ('move_check','=',True)]
        depn_ids = depn_obj.search(cr, uid, domain)
        for depn in depn_obj.browse(cr, uid, depn_ids):
            res.append(depn)
        return res
        
    def _get_depreciated_amount(self, asset):
        addition = 0.0
        depreciations = self._get_depreciations(asset)
        for depn in depreciations:
            if depn.sequence == len(depreciations):
                addition = depn.depreciated_value + depn.amount
        return addition
    
    def _current_depreciation_amount(self, asset):
        current_depn = 0.0
        depreciations = self._get_depreciations(asset)
        for depn in depreciations:
            if depn.sequence == len(depreciations):
                current_depn = depn.amount
        return current_depn
    
    def _total_depreciated_amount(self, category, data):
        total_depn = 0.0
        assets = self._get_assets(category, data)
        for asset in assets:
            total_depn += self._get_depreciated_amount(asset)
        return total_depn
    
    def _total_current_depreciation(self, category, data):
        total_depn = 0.0
        assets = self._get_assets(category, data)
        for asset in assets:
            total_depn += self._current_depreciation_amount(asset)
        return total_depn

class report_depn_schedule(osv.AbstractModel):
    _name = 'report.addsol_cnx_asset.report_depn_schedule'
    _inherit = 'report.abstract_report'
    _template = 'addsol_cnx_asset.report_depn_schedule'
    _wrapped_report_class = report_depreciation_schedule

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: