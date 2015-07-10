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

class resource_skill(osv.osv):
    _name = 'resource.skill'
    _description = "Resource skill"
    
    _columns = {
        'name' : fields.char("Skill Name", required=True, size=200)
    }
    
    
class resource_level(osv.osv):
    _name = 'resource.level'
    _description = "Resource level"
    
    _columns = {
        'name' : fields.char("Level Name", required=True, size=200)
    }
    
class addsol_resorce(osv.osv):
    _inherit = 'hr.employee'
    
    _columns = {
        'skill_set' : fields.one2many('resource.skill.set','resource','Skill Set',required=True),
        'billable_start_date' : fields.date('Billable Start Date'),
        'billable_end_date' : fields.date('Billable End Date'),
        'on_bench' : fields.boolean('On Bench'),
        'project' : fields.many2one('project.project','Project',required=True),
        'resume' : fields.binary('Resume',required=True),
        
    }
    

class resource_skil_set(osv.osv):
    _name = 'resource.skill.set'
    _description = "Resource skill set"
    
    _columns = {
        'resource' : fields.many2one('hr.employee','Resource',required=True),
        'skill' : fields.many2one('resource.skill','Skill',required=True),
        'level' : fields.many2one('resource.level','Level',required=True),
    }

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
