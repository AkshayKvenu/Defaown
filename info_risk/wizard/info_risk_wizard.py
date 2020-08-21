# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InfoRiskScenarioWizard(models.TransientModel):
    _name = "info.risk.scenario.wizard"
    
    vulnerability_id = fields.Many2one('info.risk.vulnerability', string='Vulnerability')
    
    def compute(self):
        threat_obj = self.vulnerability_id.threat_ids
        if not threat_obj:
            raise UserError(_("No related threat found for %s.") % (self.vulnerability_id.name,))
            
        for rec in threat_obj:
            self.env['info.risk.scenarios'].create({
                'vulnerability_id':self.vulnerability_id.id,
                'threat_id':rec.id
                })
    

class InfoRiskWizard(models.TransientModel):
    _name = "info.risk.wizard"
    
    name = fields.Char("Name")
    number = fields.Selection([('3', "3"), ('4', "4"), ('5', "5"), ('6', "6"), ('7', "7")], default='3', string='Number')
    
    likelihood_ids = fields.Many2many('info.risk.likelihood.context', string='Likelihood')
    
    @api.onchange('number')
    def compute_likelihood(self):
#         print("sssssss",self.number)
        if self.number:
            self.likelihood_ids = False
            likeli = []
            
            if self.number == '3':
                print("sssssss", self.number)
                def_val = ['Unlikely', 'Plausible', 'Likely']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            elif self.number == '4':
                def_val = ['Highly unlikely', 'Unlikely', 'Likely', 'Highly Likely']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            elif self.number == '5':
                def_val = ['Highly unlikely', 'Unlikely', 'Plausible', 'Likely', 'Highly Likely']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            elif self.number == '6':
                def_val = ['Almost Impossible', 'Highly unlikely', 'Unlikely', 'Likely', 'Highly Likely', 'Almost Certain']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            elif self.number == '7':
                def_val = ['Almost Impossible', 'Highly unlikely', 'Unlikely', 'Plausible', 'Likely', 'Highly Likely', 'Almost Certain']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            self.likelihood_ids = likeli
            
    def compute(self):
        dict_value = []
        values = []
        for lines in self.likelihood_ids:
            values.append(lines.description)
#         self.env['info.risk.likelihood'].search([]).unlink()
        for i in range(len(values)):
            lines = {'name' : str(i + 1),
                    'description' : values[i]}
            dict_value.append(lines)
        context_li = {
            'name':'General',
            'range':self.number,
            'default_range':self.number,
            'is_general':True,
            'likelihood_ids':[(0, 0, l) for l in dict_value],
            'default_ids':[(0, 0, l) for l in dict_value]
            
            }
        obj = self.env['info.risk.likelihood'].search([])
        for rec in obj:
            obj.is_general = False
        self.env['info.risk.likelihood'].search([]).unlink()
        self.env['info.risk.likelihood'].create(context_li)
        self.env.company.sale_quotation_onboarding_state = 'done'


class InfoRiskImpactWizard(models.TransientModel):
    _name = "info.risk.impact.wizard"
    
    name = fields.Char("Name")
    number = fields.Selection([('3', "3"), ('4', "4"), ('5', "5"), ('6', "6"), ('7', "7")], default='3', string='Number')
    
    Impact_ids = fields.Many2many('info.risk.impact.context', string='Impact')
    
    @api.onchange('number')
    def compute_impact(self):
#         print("sssssss",self.number)
        if self.number:
            self.Impact_ids = False
            likeli = []
            
            if self.number == '3':
                print("sssssss", self.number)
                def_val = ['Low', 'Medium', 'High']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            elif self.number == '4':
                def_val = ['Very Low', 'Low', 'High', 'Very High']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            elif self.number == '5':
                def_val = ['Very Low', 'Low', 'Medium', 'High', 'Very High']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            elif self.number == '6':
                def_val = ['Negligible', 'Very Low', 'Low', 'High', 'Very High', 'Critical']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            elif self.number == '7':
                def_val = ['Negligible', 'Very Low', 'Low', 'Medium', 'High', 'Very High', 'Critical']
                for i in range(int(self.number)):
                    lines = {
                        'name' : str(i + 1),
                        'description' : def_val[i]}
                    likeli.append((0, False, lines))
                    
            self.Impact_ids = likeli
            
    def compute(self):
        dict_value = []
        values = []
        for lines in self.Impact_ids:
            values.append(lines.description)
#         self.env['info.risk.likelihood'].search([]).unlink()
        list_ = []
        if self.number == '3':
            def_val_c = ['Minimal amount of critical data exposed', 'Extensive amount of non-sensitive data disclosed', 'Extensive amount of sensitive data disclosed']
            def_val_i = ['Minimal amount of data seriously corrupt', 'Extensive amount of data slightly corrupt', 'Extensive amount of data partly corrupt']
            def_val_a = ['Secondary services extensively interrupted', 'Primary services minimally interrupted', 'Primary services partly interrupted']
        elif self.number == '4':
            def_val_c = ['Minimal amount of sensitive data exposed', 'Minimal amount of critical data exposed', 'Extensive amount of sensitive data disclosed',
                       'Extensive amount of critical data disclosed']
            def_val_i = ['Minimal amount of data partly corrupt', 'Minimal amount of data seriously corrupt', 'Extensive amount of data partly corrupt',
                       'Extensive amount of data seriously corrupt']
            def_val_a = ['Secondary services partly interrupted', 'Secondary services extensively', 'Primary services partly ', 'Primary services extensively']
        elif self.number == '5':
            def_val_c = ['Minimal amount of sensitive data exposed', 'Minimal amount of critical data exposed', 'Extensive amount of non-sensitive data disclosed',
                       'Extensive amount of sensitive data disclosed', 'Extensive amount of critical data disclosed']
            def_val_i = ['Minimal amount of data partly corrupt', 'Minimal amount of data seriously corrupt', 'Extensive amount of data slightly corrupt',
                       'Extensive amount of data partly corrupt', 'Extensive amount of data seriously corrupt']
            def_val_a = ['Secondary services partly interrupted', 'Secondary services extensively interrupted', 'Primary services minimally interrupted',
                       'Primary services partly interrupted', 'Primary services extensively interrupted']
        elif self.number == '6':
            def_val_c = ['Minimal amount of non-sensitive data disclosed', 'Minimal amount of sensitive data exposed', 'Minimal amount of critical data exposed',
                       'Extensive amount of sensitive data disclosed', 'Extensive amount of critical data disclosed', 'All data disclosed']
            def_val_i = ['Minimal amount of data slightly corrupt', 'Minimal amount of data partly corrupt', 'Minimal amount of data seriously corrupt',
                       'Extensive amount of data partly corrupt', 'Extensive amount of data seriously corrupt', 'All data corrupt']
            def_val_a = ['Secondary services minimally', 'Secondary services partly', 'Secondary services extensively', 'Primary services partly interrupted',
                       'Primary services extensively ', 'All systems lost']
        elif self.number == '7':
            def_val_c = ['Minimal amount of non-sensitive data disclosed', 'Minimal amount of sensitive data exposed', 'Minimal amount of critical data exposed', 'Extensive amount of non-sensitive data disclosed',
                       'Extensive amount of sensitive data disclosed', 'Extensive amount of critical data disclosed', 'All data disclosed']
            def_val_i = ['Minimal amount of data slightly corrupt', 'Minimal amount of data partly corrupt', 'Minimal amount of data seriously corrupt',
                       'Extensive amount of data slightly corrupt', 'Extensive amount of data partly corrupt', 'Extensive amount of data seriously corrupt', 'All data corrupt']
            def_val_a = ['Secondary services minimally interrupted', 'Secondary services partly interrupted', 'Secondary services extensively interrupted',
                       'Primary services minimally interrupted', 'Primary services partly interrupted', 'Primary services extensively interrupted', 'All systems lost']
            
        for i in range(len(values)):
            lines = {'name' : str(i + 1),
                    'description' : values[i]}
            dict_value.append(lines)
            
        context_li = {
            'name':'General',
            'range':self.number,
            'default_range':self.number,
            'is_general':True,
            'impact_ids':[(0, 0, l) for l in dict_value],
            'default_ids':[(0, 0, l) for l in dict_value]
            
            }
        obj = self.env['info.risk.impact'].search([])
        for rec in obj:
            obj.is_general = False
        self.env['info.risk.impact'].search([]).unlink()
        obj = self.env['info.risk.impact'].create(context_li)
        
        lines_C = {}
        lines_I = {}
        lines_A = {}
        
        values_C = []
        values_I = []
        values_A = []
        
        for i in range(int(self.number)):
            lines_C = {'name' : str(i + 1),
                    'description' : def_val_c[i]}
            values_C.append(lines_C)
            lines_I = {'name' : str(i + 1),
                    'description' : def_val_i[i]}
            values_I.append(lines_I)
            lines_A = {'name' : str(i + 1),
                    'description' : def_val_a[i]}
            values_A.append(lines_A)
            
        context_C = {
            'name':'Confidentiality',
            'range':self.number,
            'default_range':self.number,
            'is_general':True,
            'impact_ids':[(0, 0, l) for l in values_C],
            'default_ids':[(0, 0, l) for l in values_C]
            
            }
#         print("aaaaaaaaaaaaaaaaaaaaaaaa",def_val_c,context_C)
        self.env['info.risk.impact'].create(context_C)
            
        context_I = {
            'name':'Integrity',
            'range':self.number,
            'default_range':self.number,
            'is_general':True,
            'impact_ids':[(0, 0, l) for l in values_I],
            'default_ids':[(0, 0, l) for l in values_I]
            
            }
        self.env['info.risk.impact'].create(context_I)
            
        context_A = {
            'name':'Availability',
            'range':self.number,
            'default_range':self.number,
            'is_general':True,
            'impact_ids':[(0, 0, l) for l in values_A],
            'default_ids':[(0, 0, l) for l in values_A]
            
            }
        self.env['info.risk.impact'].create(context_A)
        self.env.company.onboarding_state_impact = 'done'
