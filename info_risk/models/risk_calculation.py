# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class InfoRiskCalculation(models.Model):
    _name = 'info.risk.calculation'

#     name = fields.Char("Name")
    name = fields.Selection([('add', "[Impact] + [Likelihood]"),('add1', "[Impact] + [Likelihood] - 1"),('multiple', "[Impact] x [Likelihood]")], string="Risk")
    
    impact_score = fields.Integer("Impact Score")
    likelihood_score = fields.Integer("Likelihood Score")
    risk_score = fields.Integer("Risk Score")
    
    @api.onchange('impact_score','likelihood_score','name')
    def compute_risk_score(self):
        if self.impact_score and self.risk_score:
            if self.name == 'add':
                self.risk_score = self.impact_score + self.likelihood_score
            elif self.name == 'add1':
                self.risk_score = self.impact_score + self.likelihood_score-1
            elif self.name == 'multiple':
                self.risk_score = self.impact_score * self.likelihood_score
        
     
    def write(self, vals):
#         vals['info_asset_name_seq'] = self.env['ir.sequence'].next_by_code('account.asset.asset') or _('New')
        like_score = self.likelihood_score
        imp_score = self.impact_score
        risk = self.name
        if 'impact_score' in vals and vals['impact_score']:
            imp_score = vals['impact_score']
        if 'likelihood_score' in vals and vals['likelihood_score']:
            like_score = vals['likelihood_score']
        if 'likelihood_score' in vals and 'impact_score' in vals:
            like_score = vals['likelihood_score']
            imp_score = vals['impact_score']
        if 'name' in vals and vals['name']:
            risk = vals['name']
            
        if risk == 'add':
            vals['risk_score'] = imp_score + like_score
        elif risk == 'add1':
            vals['risk_score'] = imp_score + like_score - 1
        elif risk == 'multiple':
            vals['risk_score'] = imp_score * like_score
        return super(InfoRiskCalculation, self).write(vals)

    @api.model
    def create(self, vals):
        if 'impact_score' in vals and 'likelihood_score' in vals:
            if vals['name'] == 'add':
                vals['risk_score'] = vals['impact_score'] + vals['likelihood_score']
            elif vals['name'] == 'add1':
                vals['risk_score'] = vals['impact_score'] + vals['likelihood_score'] - 1
            elif vals['name'] == 'multiple':
                vals['risk_score'] = vals['impact_score'] * vals['likelihood_score']
        return super(InfoRiskCalculation, self).create(vals)     
      