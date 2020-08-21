# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InfoRiskThreat(models.Model):
    _name = 'info.risk.threat'

    name = fields.Text("Name")
    description = fields.Text("Description")

class InfoRiskVulnerability(models.Model):
    _name = 'info.risk.vulnerability'

    name = fields.Char("Name")
    vulnerability_type_id = fields.Many2one('info.risk.vulnerability.type',string='Type of Vulnerability')
    description = fields.Text("Description")
    threat_ids = fields.Many2many('info.risk.threat',string='Related Threats')

class InfoRiskVulnerabilityType(models.Model):
    _name = 'info.risk.vulnerability.type'

    name = fields.Char("Name",requied=True)
    asset_class = fields.Selection([('devices', 'Devices'),
                ('software', 'Software Licenses'),
                ('company', 'Company'),
                ('site', 'Site'),
                ('department', 'Department'),
                ('cmployee', 'Employee'),
                ('contacts', 'Contacts'),
                ('working_schedule', 'Working Schedule'),
                ('business', 'Business Services')],
                "Asset class",requied=True)

class InfoRiskScenarios(models.Model):
    _name = 'info.risk.scenarios'

    name = fields.Char("Name")
    vulnerability_id = fields.Many2one('info.risk.vulnerability',string='Vulnerability')
    threat_id = fields.Many2one('info.risk.threat',string='Threat')

    @api.model
    def action_open_base_document_wizard(self, action_ref=None):
        if not action_ref:
            action_ref = 'info_risk.action_view_scenario_wizard'
        return self.env.ref(action_ref).read()[0]  
    
    
    @api.onchange('vulnerability_id','threat_id')
    def compute_name(self):
        if self.vulnerability_id and self.threat_id:
            self.name = self.vulnerability_id.name+' Exploited by '+self.threat_id.name

    @api.model
    def create(self, vals):    
        if 'vulnerability_id' in vals and 'threat_id' in vals:
            vulnerable= self.env['info.risk.vulnerability'].browse(vals['vulnerability_id'])
            threat= self.env['info.risk.threat'].browse(vals['threat_id'])
            vals['name'] = vulnerable.name +' Exploited by '+ threat.name
        if self.env['info.risk.scenarios'].search([('vulnerability_id','=',vulnerable.id),('threat_id','=',threat.id)]):
            raise UserError(_("Same Vulnerability and threat already found"))
        return super(InfoRiskScenarios, self).create(vals)   
        
     
    def write(self, vals):
        vulnerable = self.vulnerability_id.name
        threat = self.threat_id.name
        if 'vulnerability_id' in vals and vals['vulnerability_id']:
            vulnerable= self.env['info.risk.vulnerability'].browse(vals['vulnerability_id']).name
        if 'threat_id' in vals and vals['threat_id']:
            threat= self.env['info.risk.threat'].browse(vals['threat_id']).name
            
        vals['name'] = vulnerable +' Exploited by '+ threat
        return super(InfoRiskScenarios, self).write(vals)   
        
            
