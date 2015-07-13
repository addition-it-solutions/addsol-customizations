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
        'resource_ids' : fields.many2many('hr.employee', string='Assigned Resources'),
    }
    
    def default_get(self, cr, uid, fields, context=None):
        if context is None:
            context = {}
        result = super(assign_resources, self).default_get(cr, uid, fields, context=context)
        if not result.get('resource_ids'):
            result['resource_ids'] = []
        request_obj = self.pool.get('resource.request')
        resource_skills_obj = self.pool.get('resource.skill.set')
        resource_obj = self.pool.get('hr.employee')
        record_id = context.get('active_id',False)
        if record_id:
            requests = request_obj.browse(cr, uid, record_id, context)
            resource_ids = []
            for line in requests.request_line_ids:
                if line.skill_id and line.level_id:
                    resource_skill_ids = resource_skills_obj.search(cr, uid, [('skill','=',line.skill_id.id),('level','=',line.level_id.id)])
                    resource_ids.extend([res.resource.id for res in resource_skills_obj.browse(cr, uid, resource_skill_ids, context) if res.resource.id not in resource_ids])
                if resource_ids:
                    for res in resource_obj.browse(cr, uid, resource_ids, context):
                        if res.billable_end_date >= line.billability_start_date and not res.on_bench:
                            index = resource_ids.index(res.id)
                            resource_ids.pop(index)
                    if 'resource_ids' in fields and resource_ids:
                        result.update({'resource_ids': resource_ids})
        return result
    
    def assign(self, cr, uid, ids, context=None):
        request_obj = self.pool.get('resource.request')
        resource_skills_obj = self.pool.get('resource.skill.set')
        resource_obj = self.pool.get('hr.employee')
        record_id = context.get('active_id',False)
        if record_id:
            for assign_id in self.browse(cr, uid, ids):
                request_lines = request_obj.browse(cr, uid, record_id, context).request_line_ids
                res_ids = [res.id for res in assign_id.resource_ids]
                skill_ids = resource_skills_obj.search(cr, uid, [('resource','in',res_ids)])
                for line in request_lines:
                    for resource in resource_skills_obj.browse(cr, uid, skill_ids, context):
                        if line.skill_id.id == resource.skill.id and line.level_id.id == resource.level.id:
                            resource_obj.write(cr, uid, resource.resource.id, {'billable_start_date': line.billability_start_date,
                                                                      'billable_end_date': line.billability_end_date,
                                                                      'project': line.request_id.project_id.id,
                                                                      'on_bench': False})
                
                request_obj.write(cr, uid, record_id, {'resource_ids': [(4, res_id) for res_id in res_ids],'state':'assign'},context=context)

        return True

