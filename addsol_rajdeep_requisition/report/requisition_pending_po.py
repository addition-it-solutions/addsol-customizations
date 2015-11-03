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

class requisition_pending_po(report_sxw.rml_parse):
    
    def set_context(self, objects, data, ids, report_type=None):
        req_obj = self.pool.get('purchase.requisition')
        new_ids = req_obj.search(self.cr, self.uid, [('state','!=','draft'),('purchase_ids','!=',[])])
        objects = req_obj.browse(self.cr, self.uid, new_ids)
        return super(requisition_pending_po, self).set_context(objects, data, new_ids, report_type=report_type)

    def __init__(self, cr, uid, name, context):
        super(requisition_pending_po, self).__init__(cr, uid, name, context=context)
        self.localcontext.update({
            'time': time,
            'get_lines': self._get_lines,
        })
    
    def _get_lines(self, req):
        result = []
        state_dict = {'cancel': 'Cancelled', 'open': 'Bid Selection', 'in_progress': 'Confirmed', 'draft': 'Draft', 'done': 'PO Created'}
        for po in req.purchase_ids:
            for poline in po.order_line:
                state = state_dict[po.requisition_id.state]
                result.append({
                               'prno': po.requisition_id.name,
                               'prdate': po.requisition_id.ordering_date,
                               'prstate': state,
                               'product': poline.product_id.name, 
                               'poqty': poline.product_qty,
                               'supplier': po.partner_id.name,
                               'po_state': po.state})
        for val in result:
            for line in req.line_ids:
                if val['product'] == line.product_id.name:
                    val.update({'remaining_qty': line.product_qty,
                                'prqty': line.product_qty})
                    if val['po_state'] == 'approved':
                        val.update({'remaining_qty': line.product_qty - val.get('poqty')})
        return result

class report_requisition_pending_po(osv.AbstractModel):
    _name = 'report.addsol_rajdeep_requisition.report_pendingpo'
    _inherit = 'report.abstract_report'
    _template = 'addsol_rajdeep_requisition.report_pendingpo'
    _wrapped_report_class = requisition_pending_po

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
