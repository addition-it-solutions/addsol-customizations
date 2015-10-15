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

{
    'name': 'Ticketing System  - Addsol',
    'version': '1.0',
    'author': 'Addition IT Solutions Pvt. Ltd.',
    'category': 'Human Resources',
    'summary': 'Employee Ticketing',
    'website': 'https://www.aitspl.com',
    'description': """
Ticketing system by Addition IT Solutions
====================================
Contact:
    * website: www.aitspl.com
    * email: info@aitspl.com    

Functionality:
* Employee raises a ticket to complain regarding his login.
* Admin handles the tickets and resolves the issues.
    
""",
    'images': [],
    'depends': ['hr_addsol', 'hr_gamification'],
    'data': [
        'security/ir.model.access.csv',
        'hr_addsol_ticket_data.xml',
        'hr_addsol_ticket_view.xml',
     ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: