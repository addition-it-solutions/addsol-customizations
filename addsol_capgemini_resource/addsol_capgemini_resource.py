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


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
