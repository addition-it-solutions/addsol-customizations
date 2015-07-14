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
    
    def _manager_get(self):
        ids = self.env['hr.employee'].search([('user_id', '=', self._uid)])
        if ids:
            return ids[0]
        return False
    
    
    name = fields.Char('Request', required=True, default=lambda self: self.env['ir.sequence'].get('resource.request.number'))
    manager_id = fields.Many2one('hr.employee', 'Project Manager', required=True, default=_manager_get)
    project_id = fields.Many2one('project.project','Project', required=True)
    parent_id = fields.Many2one('resource.request','Parent Request')
    request_line_ids = fields.One2many('resource.request.lines','request_id', 'Request Lines')
    type = fields.Selection([('new','New'), 
                              ('extension','Extension'), 
                              ('terminate','Termination')],
                             'Type', default='new', required=True)
    resource_ids = fields.Many2many('hr.employee', string='Assigned Resources')
    state = fields.Selection([('new','New'),
                               ('submit','Waiting for Approval'),
                               ('approve','Approved'),
                               ('reject','Rejected'),
                               ('assign','Assigned'),
                               ('close','Closed')], 'State', default='new')
    
    @api.multi
    def submit_request(self):
        return self.write({'state': 'submit'})
    
    @api.multi
    def assign_resources(self):
        return self.write({'state': 'assign'})
    
    @api.multi
    def approve_request(self):
        return self.write({'state': 'approve'})
    
    @api.multi
    def reject_request(self):
        return self.write({'state': 'reject'})
    
    @api.multi
    def close_request(self):
        return self.write({'state': 'close'})
    
 
class resource_request_lines(models.Model):
    _name = 'resource.request.lines'
    _description = "Request Lines"
    _rec_name = 'sequence'

    @api.one
    def _progress_rate(self):
        self._cr.execute("""
            SELECT resource_request_lines.id, count(resource_request_lines.no_of_resources),resource_request_lines.no_of_resources
            FROM public.hr_employee_resource_request_rel, public.resource_request, public.resource_request_lines, public.resource_skill_set
            WHERE hr_employee_resource_request_rel.hr_employee_id = resource_skill_set.resource AND
                resource_request.id = resource_request_lines.request_id AND
                resource_request.id = hr_employee_resource_request_rel.resource_request_id AND
                resource_request_lines.skill_id = resource_skill_set.skill AND
                resource_request_lines.level_id = resource_skill_set.level AND
                resource_request_lines.id = %s
            Group By resource_request_lines.id
          """%self.ids[0])
        for id, count , no_of_res in self._cr.fetchall():
            if count == no_of_res:
                self.progress = 100.0
            else:
                self.progress = float(count)/float(no_of_res)*100

    sequence = fields.Integer('Sequence', default=5)
    start_date = fields.Date('Start Date')
    end_date = fields.Date('End Date', required=True)
    request_id = fields.Many2one('resource.request','Request')
    req_type = fields.Selection(related='request_id.type', selection=[('new','New'), 
                              ('extension','Extension'), 
                              ('terminate','Termination')], string="Type", readonly=True)
    skill_id = fields.Many2one('resource.skill', 'Skill')
    level_id = fields.Many2one('resource.level', 'Level')
    no_of_resources = fields.Integer('No. of Resources')
    billability_start_date = fields.Date('Billability Start Date')
    billability_end_date = fields.Date('Billability End Date')
    reason = fields.Text('Reason for Termination')
    resource_id = fields.Many2one('hr.employee','Resource')
    progress = fields.Float(compute='_progress_rate', string='Progress')


class addsol_resource(models.Model):
    _inherit = 'hr.employee'
    
    skill_set = fields.One2many('resource.skill.set','resource','Skill Set',required=True)
    billable_start_date= fields.Date('Billable Start Date')
    billable_end_date= fields.Date('Billable End Date')
    on_bench= fields.Boolean('On Bench')
    project= fields.Many2one('project.project','Project')
    resume= fields.Binary('Resume')

class resource_skil_set(models.Model):
    _name = 'resource.skill.set'
    _description = "Resource skill set"
    
    resource= fields.Many2one('hr.employee','Resource',required=True)
    skill= fields.Many2one('resource.skill','Skill',required=True)
    level= fields.Many2one('resource.level','Level',required=True)

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
