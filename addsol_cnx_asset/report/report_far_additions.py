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

class report_far_additions(report_sxw.rml_parse, report_far_common):
    _name = 'report.far.additions'
    
    def set_context(self, objects, data, ids, report_type=None):
        asset_categ_obj = self.pool.get('account.asset.category')
        ctx = self.context.copy()
        ctx['fiscalyear'] = data['form']['fiscalyear_id']
        ctx['period_from'] = data['form']['period_from']
        ctx['period_to'] = data['form']['period_to']
        self.context.update(ctx)
        if (data['model'] == 'ir.ui.menu'):
            new_ids = asset_categ_obj.search(self.cr, self.uid, [])
            objects = asset_categ_obj.browse(self.cr, self.uid, new_ids)
        return super(report_far_additions, self).set_context(objects, data, new_ids, report_type=report_type)
    
    def __init__(self, cr, uid, name, context=None):
        if context is None:
            context = {}
        super(report_far_additions, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_fiscalyear': self._get_fiscalyear,
            'get_start_period': self.get_start_period,
            'get_end_period': self.get_end_period,
            'get_assets': self._get_assets,
            'sum_assets': self._sum_assets,
        })
        self.context = context

    def _get_assets(self, category):
        asset_obj = self.pool.get('account.asset.asset')
        period_obj = self.pool.get('account.period')
        fiscalyear_obj = self.pool.get('account.fiscalyear')
        cr = self.cr
        uid = self.uid
        res = []
        fiscalyear_id = self.context.get('fiscalyear_id',False)
        period_from = self.context.get('period_from',False)
        period_to = self.context.get('period_to',False)
        start_date = end_date = False
        if fiscalyear_id:
            start_date = fiscalyear_obj.browse(cr, uid, fiscalyear_id).date_start
            end_date = fiscalyear_obj.browse(cr, uid, fiscalyear_id).date_stop
        if period_from and period_to:
            start_date = period_obj.browse(cr, uid, period_from).date_start
            end_date = period_obj.browse(cr, uid, period_to).date_stop
        domain = [('purchase_date','>=',start_date), ('purchase_date','<=',end_date),('category_id','=',category.id),('state','!=','draft')]
        asset_ids = asset_obj.search(cr, uid, domain)
        for asset in asset_obj.browse(cr, uid, asset_ids):
            res.append(asset)
        return res
        
    def _sum_assets(self, category):
        addition = 0.0
        assets = self._get_assets(category)
        for asset in assets:
            addition += asset.purchase_value
        return addition

class report_faradditions(osv.AbstractModel):
    _name = 'report.addsol_cnx_asset.report_faradditions'
    _inherit = 'report.abstract_report'
    _template = 'addsol_cnx_asset.report_faradditions'
    _wrapped_report_class = report_far_additions

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: