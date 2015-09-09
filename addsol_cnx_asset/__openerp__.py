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
    'name': 'Assets for CNX - Addsol',
    'version': '1.0',
    'author': 'Addition IT Solutions Pvt. Ltd.',
    'category': 'Accounting & Finance',
    'summary': 'Assets Customization for CNX',
    'website': 'https://www.aitspl.com',
    'description': """
Account Assets by Addition IT Solutions
=======================================
Contact:
    * website: www.aitspl.com
    * email: info@aitspl.com    
Features:
---------
    * Depreciation calculation is divided into months according to fiscal year
    * Monthly journal entries are made for each asset

""",
    'images': [],
    'depends': ['account_asset'],
    'data': ['addsol_cnx_asset_data.xml',
             'addsol_cnx_asset_report.xml',
             'wizard/wizard_far_additions_view.xml',
             'views/report_faradditions.xml',
             ],
    'demo': [],
    'test': [],
    'installable': True,
    'auto_install': False,
}
# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4: