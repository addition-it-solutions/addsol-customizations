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

from openerp.osv import fields, osv
from openerp import tools


class demand_analysis_report(osv.osv):
    _name = "demand.analysis.report"
    _description = ""
    _auto = False
    _columns = {
        'request_id' : fields.many2one('resource.request', 'Request', readonly=True),
        'manager_id' : fields.many2one('hr.employee', 'Manager', readonly=True),
        'competancy' : fields.many2one('resource.competancy', readonly=True),
        'skill' : fields.many2one('resource.skill', readonly=True),
        'level' : fields.many2one('resource.level', readonly=True),
        'no_of_resources': fields.integer('No. of Resources', readonly=True),
        
    }

    def init(self, cr):
        tools.sql.drop_view_if_exists(cr, 'demand_analysis_report')
        cr.execute("""
            CREATE view demand_analysis_report as
              SELECT
                    l.id as id,
                    r.manager_id as manager_id,
                    l.request_id as request_id,
                    l.competancy_id as competancy,
                    l.skill_id as skill,
                    l.level_id as level,
                    l.no_of_resources as no_of_resources
              FROM  resource_request_lines l, resource_request r
                WHERE  r.id = l.request_id 
                GROUP BY
                    l.id ,
                    r.manager_id,
                    l.request_id,
                    l.competancy_id,
                    l.skill_id,
                    l.level_id,
                    l.no_of_resources
        """)
