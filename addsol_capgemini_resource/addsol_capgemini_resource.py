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

from openerp import models, fields, api, _

class resource_skill(models.Model):
    _name = 'resource.skill'
    _description = "Resource skill"
    
    name = fields.Char("Skill Name", required=True, size=200)

class resource_level(models.Model):
    _name = 'resource.level'
    _description = "Resource level"
    
    name = fields.Char("Level Name", required=True, size=200)

class resource_request(models.Model):
    _name = 'resource.request'
    _description = "Resource Requests"
    
    name = fields.Char('Request', required=True)
    project_id = fields.Many2one('project.project','Project')
    manager_id = fields.Many2one('hr.employee', 'Project Manager')
    parent_id = fields.Many2one('resource.request','Parent Request')
    request_line_ids = fields.One2many('resource.request.lines','request_id', 'Request Lines')
    type = fields.Selection([('new','New'), 
                              ('extension','Extension'), 
                              ('terminate','Termination')],
                             'Type', default='new')
    resource_ids = fields.Many2many('hr.employee','employee_id','request_id', 'Assigned Resources')
    state = fields.Selection([('new','New'),
                               ('submit','Waiting for Approval'),
                               ('approve','Approved'),
                               ('reject','Rejected'),
                               ('assign','Assigned'),
                               ('close','Closed')], 'State')

    @api.model
    def submit_request(self):
        return True
    
    @api.model
    def assign_resources(self):
        return True
    
    @api.model
    def approve_request(self):
        return True
    
    @api.model
    def reject_request(self):
        return True
    
    @api.model
    def close_request(self):
        return True
 
class resource_request_lines(models.Model):
    _name = 'resource.request.lines'
    _description = "Request Lines"

    name = fields.Char('Request Line', required=True)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date')
    request_id = fields.Many2one('resource.request','Request')
    req_type = fields.Selection(related='request_id.type', selection=[('new','New'), 
                              ('extension','Extension'), 
                              ('terminate','Termination')], string="Type", readonly=True)
    skill_id = fields.Many2one('resource.skill', 'Skill')
    level_id = fields.Many2one('resource.level', 'Level')
    no_of_resources = fields.Integer('No. of Resources')
    billability_start_date = fields.Date('Billability Start Date')
    billability_end_date = fields.Date('Billability End Date')
    reason = fields.Char('Reason for Termination')
    resource_id = fields.Many2one('hr.employee','Resource')

class addsol_resorce(models.Model):
    _inherit = 'hr.employee'
    
    skill_set = fields.One2many('resource.skill.set','resource','Skill Set',required=True)
    billable_start_date= fields.Date('Billable Start Date')
    billable_end_date= fields.Date('Billable End Date')
    on_bench= fields.Boolean('On Bench')
    project= fields.Many2one('project.project','Project',required=True)
    resume= fields.Binary('Resume',required=True)

class resource_skil_set(models.Model):
    _name = 'resource.skill.set'
    _description = "Resource skill set"
    
    resource= fields.Many2one('hr.employee','Resource',required=True)
    skill= fields.Many2one('resource.skill','Skill',required=True)
    level= fields.Many2one('resource.level','Level',required=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
