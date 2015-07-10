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


#from openerp import models, fields, api, _
from openerp.osv import fields, osv
from openerp.tools.translate import _


class assign_resources(osv.osv_memory):
    _name = 'assign.resources'
    _description = "Assign Resources for Project"
    
    _columns = {
        'resource_ids' : fields.many2many('hr.employee','res_request_employee_rel','employee_id','request_id', 'Assigned Resources'),
    }
    
    def assign(self, cr, uid, ids, context=None):
        resource_obj = self.pool.get('resource.request')
        for assign_ids in self.browse(cr, uid, ids):
            if assign_ids:
                resource_obj.write(cr, uid, context['active_id'],{'resource_ids': assign_ids,'state':'assign'},context=context)
                
        return True
    
    
