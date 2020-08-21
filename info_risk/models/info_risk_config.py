# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class InfoRiskLikelihood(models.Model):
    _name = 'info.risk.likelihood'
#     _description = 'info_risk.info_risk'

    name = fields.Char("Name")
    is_general = fields.Boolean('General', default=False)
    def _compute_range(self):
        obj = self.search([('name','=','General')],limit=1)
        if obj:
            return obj.range
        
    range = fields.Selection([('3', "3"), ('4', "4"), ('5', "5"), ('6', "6"), ('7', "7")], string='Range',default=_compute_range)
    
    default_range = fields.Char()
    

    @api.model
    def create(self, vals):    
        num = 1
        for rec in vals['likelihood_ids']:
            if len(rec)>=2 and rec[2] and rec[1]!= False:
                rec[2]['name'] = num
                num +=1
        return super(InfoRiskLikelihood, self).create(vals)   

    def write(self, vals):    
        num = 1
        if 'likelihood_ids' in vals and vals['likelihood_ids']:
            for rec in vals['likelihood_ids']:
                if len(rec)>=2 and rec[2] and rec[1]!= False:
                    rec[2]['name'] = num
                    num +=1
        return super(InfoRiskLikelihood, self).write(vals)   

    
    def unlink(self):
        for type in self:
            if type.is_general:
                raise UserError(_('You cannot delete default likelihood.'))
        return super(InfoRiskLikelihood, self).unlink()
    
    def _compute_likelihood(self):
        obj = self.search([('name','=','General')],limit=1)
        if obj:
            list_values = []
            for rec in obj.likelihood_ids:
                values=({
                        'name' : rec.name,
                        'description' : ''})
                list_values.append((0, False,values))
            return list_values
        
    apetite_id = fields.Many2one('info.risk.appetite', string='Appetite')
    likelihood_ids = fields.Many2many('info.risk.likelihood.context',relation = 'likelihood_id',string='Context', default=_compute_likelihood)
    default_ids = fields.Many2many('info.risk.likelihood.context',relation = 'default_likelihood_id')

# ,'likelihood_id'
    @api.model
    def action_open_base_document_wizard(self, action_ref=None):
        if not action_ref:
            action_ref = 'info_risk.action_view_likelihood_wizard'
        return self.env.ref(action_ref).read()[0]  
    
    def set_draft(self): 
        self.range = False
        self.likelihood_ids = False
        self.range = self.default_range
        dict_value=[]
        values=[]
        i=1
        for rec in self.default_ids:
            lines={'name' : i,
                    'description' : rec.description}
            dict_value.append(lines)
            i+=1
        self.likelihood_ids =[(0, 0, l) for l in dict_value]

class InfoRiskLikelihoodContext(models.Model):
    _name = 'info.risk.likelihood.context'
#     _description = 'info_risk.info_risk'

    name = fields.Char("Score")
    description = fields.Char("Descripiton")
    likelihood_id = fields.Many2one('info.risk.likelihood')
    default_likelihood_id = fields.Many2one('info.risk.likelihood')


###################################   IMPACT      ######################################

class InfoRiskImpact(models.Model):
    _name = 'info.risk.impact'
#     _description = 'info_risk.info_risk'


    name = fields.Char("Name")
    is_general = fields.Boolean('General', default=False)
    
    def _compute_range(self):
        obj = self.search([('name','=','General')],limit=1)
        if obj:
            return obj.range
    range = fields.Selection([('3', "3"), ('4', "4"), ('5', "5"), ('6', "6"), ('7', "7")], string='Range',default=_compute_range)
        
    default_range = fields.Char()
    
    def _compute_impact(self):
        obj = self.search([('name','=','General')],limit=1)
        if obj:
            list_values = []
            for rec in obj.impact_ids:
                values=({
                        'name' : rec.name,
                        'description' : ''})
                list_values.append((0, False,values))
            return list_values
       
    
    def set_draft(self): 
        self.impact_ids = False
        self.range = self.default_range 
#         self.impact_ids = self.default_ids
        dict_value=[]
        values=[]
        i=1
        for rec in self.default_ids:
            lines={'name' : i,
                    'description' : rec.description}
            dict_value.append(lines)
            i+=1
        self.impact_ids =[(0, 0, l) for l in dict_value]
        
        
    @api.model
    def create(self, vals):    
        num = 1
        for rec in vals['impact_ids']:
            if len(rec)>=2 and rec[2] and rec[1]!= False:
                rec[2]['name'] = num
                num +=1
        return super(InfoRiskImpact, self).create(vals)  

    def write(self, vals):    
        num = 1
        if 'impact_ids' in vals and vals['impact_ids']:
            for rec in vals['impact_ids']:
                if len(rec)>=2 and rec[2] and rec[1]!= False:
                    rec[2]['name'] = num
                    num +=1
        return super(InfoRiskImpact, self).write(vals) 

    
    def unlink(self):
        for type in self:
            if type.is_general:
                raise UserError(_('You cannot delete default impact.'))
        return super(InfoRiskImpact, self).unlink()
     
    
    apetite_id = fields.Many2one('info.risk.appetite', string='Appetite')
    
    impact_ids = fields.Many2many('info.risk.impact.context',relation = 'impact_id',string='Context', default=_compute_impact)
    
    default_ids = fields.Many2many('info.risk.impact.context',relation = 'default_id')


    @api.model
    def action_open_base_document_wizard(self, action_ref=None):
        if not action_ref:
            action_ref = 'info_risk.action_view_impact_wizard'
        return self.env.ref(action_ref).read()[0]
    

class InfoRiskImpactContext(models.Model):
    _name = 'info.risk.impact.context'
#     _description = 'info_risk.info_risk'

    name = fields.Char("Score")
    description = fields.Char("Descripiton")
    impact_id = fields.Many2one('info.risk.impact')
    default_id = fields.Many2one('info.risk.impact')
    
    
class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    likelihood_range = fields.Selection([('3', "3"), ('4', "4"), ('5', "5"), ('6', "6"), ('7', "7")], string='Likelihood Range', default='3')

    impact_range = fields.Selection([('3', "3"), ('4', "4"), ('5', "5"), ('6', "6"), ('7', "7")], string='Impact Range', default='3')
    
    risk_calculation = fields.Selection([('add', "[Impact] + [Likelihood]"),('add1', "[Impact] + [Likelihood] - 1"),('multiple', "[Impact] x [Likelihood]")],
                                         string="Risk Calculation", default='add1')
    
    
    def compute_is_appetite(self):
        res = self.env['info.risk.appetite'].search_count([]) or 0 
        if res > 0:
            return True
    
    is_appetite = fields.Boolean("Is Appetite", default=compute_is_appetite)
    
    
    
    
    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        field_likelihood = self.env['ir.config_parameter'].sudo().get_param('info_risk.likelihood_range')
        field_impact = self.env['ir.config_parameter'].sudo().get_param('info_risk.impact_range')
        field_calculation = self.env['ir.config_parameter'].sudo().get_param('info_risk.risk_calculation')
        res.update(
            {'likelihood_range': field_likelihood,
             'impact_range': field_impact,
             'risk_calculation': field_calculation,}
            
        )
        return res
 
    def set_values(self):
        super(ResConfigSettings, self).set_values()
        param = self.env['ir.config_parameter'].sudo()
 
        field_likelihood = self.likelihood_range 
        field_impact = self.impact_range 
        field_calculation = self.risk_calculation 
#         and self.terms_sale_config.ids or False
        
        param.set_param('info_risk.likelihood_range', field_likelihood)
        param.set_param('info_risk.impact_range', field_impact)
        param.set_param('info_risk.risk_calculation', field_calculation)
        
        
        
        
        
    