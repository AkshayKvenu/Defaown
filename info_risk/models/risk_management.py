# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class InfoRiskAssessment(models.Model):
    _name = 'info.risk.assessment'
    
    name = fields.Char("Name")
    state = fields.Selection([('draft', ' Draft'),('done', 'Done')], "State", default='draft')
    control_standard_ids = fields.Many2many('info.control.standard',string='Control Standard')
    risk_appetite_id = fields.Many2one('info.risk.appetite',string='Risk Appetite')
    asset_asset_id = fields.Many2one('account.asset.asset',string='Assets')
    info_asset_class = fields.Selection([
        ('devices', 'Devices'),
        ('software', 'Software Licenses'),
        ('site', 'Site'),
        ('department', 'Department'),
        ('employee', 'Employee'),
        ('business', 'Business Services'),
        ('information', 'Information'),
        ],string = "Asset class")
    seperate_threat_vulnerability = fields.Boolean(string = "Pick Threat and Vulnerability separately?")
    scenarios_id = fields.Many2one('info.risk.scenarios',string='Risk Scenarios')
    threat_id = fields.Many2one('info.risk.threat',string='Threats')
    vulnerability_id = fields.Many2one('info.risk.vulnerability',string='Vulnerabilities')
    owner_id = fields.Many2one('res.users',string='Risk Owner')


    def open_appetite(self):
#         context = dict(self.env.context or {})
#         context['default_apetite_id'] = self.id
        return {
            'name': _('Appetite'),
            'view_type': 'form',
            'view_mode': 'form',
            'res_model': 'info.risk.appetite',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'res_id':self.risk_appetite_id.id,
#             'domain': [('id', '=', self.risk_appetite_id.id)]
            }
    
    html_view = fields.Html('HTML View')
    
    @api.onchange('risk_appetite_id')
    def compute_html(self):
        print('aaaaaaaaaaaaa',self.risk_appetite_id)
        if self.risk_appetite_id:
            print('pppppppppppp',self.risk_appetite_id)
            self.html_view = self.risk_appetite_id.html_view
    
    
    def action_done(self):
        if self.state == 'draft':
            self.write({'state':'done'})
            if self.risk_appetite_id:
                self.risk_appetite_id.is_assessment = True
    
    def action_draft(self):
        if self.state == 'done':
            self.write({'state':'draft'})
            if self.risk_appetite_id:
                self.risk_appetite_id.is_assessment = False

    def compute_calculation(self, likelihood, impact, calculation):
        if calculation == 'add':
            return likelihood + impact
        elif calculation == 'add1':
            return likelihood + impact -1
        elif calculation == 'multiple':
            return likelihood * impact
    
    
##############################     I
#nitial Risk Menu

    likelihood_score = fields.Integer(string='Likelihood Score',default=1)
    likelihood_ids = fields.Many2many('info.risk.assesment.likelihood', string='Likelihood Context')
    impact_score = fields.Integer(string='Impact Score',default=1)
    impact_ids = fields.Many2many('info.risk.assesment.impact', string='Impact Context')
    initial_risk_score = fields.Integer(string='Initial Risk Score')
    
    html_likelihood_view = fields.Html()
    
#     @api.onchange('html_view')
#     def compute_html_likelihood(self):
#         if self.html_view:
#             self.html_likelihood_view = self.html_view
    
    def compute_hover_grid(self, likelihood, impact, calculation, likelihood_score, impact_score ,criteria_ids):
        col_likelihood = [i for i in range(1,likelihood+1)]
        row_impact = [i for i in range(1,impact+1)]
        row_impact.reverse()
        
        tbody = ''
        for line in row_impact:
            row = ''
            for item in col_likelihood:
                if calculation == 'add':
                    cell_val = line+item
                elif calculation == 'add1':
                    cell_val = line+item-1
                elif calculation == 'multiple':
                    cell_val = line*item
#                 cell_val = line+item-1
                color_pick = 'black'
                for criteria in criteria_ids:
                    if criteria.score_min <= cell_val <= criteria.score_max:
                        color_pick = criteria.color
                if likelihood_score == item and impact_score == line:
                    row += '<td style="border-right:1px solid black;background-color:%s;text-align:center;width:50px;height:50px">%s</td>' % (color_pick, cell_val)
                else:
                    row += '<td style="border-right:1px solid black;background-color:%s;text-align:center;width:50px;height:50px;opacity: 0.3;">%s</td>' % (color_pick, cell_val)
            tbody += '<tr style="border-bottom:1px solid black">%s</tr>' % row
        tbody = '<tbody>%s</tbody>' % tbody
        return '<div class="col-xs-12"><div class="col-xs-1"><strong>Impact</strong></div><div class="col-xs-10"><table style="border:1px solid black">%s</table></div></div><div class="col-xs-2 col-xs-offset-1" style="margin-top:10px;margin-bottom:10px"><strong style="padding-left:17px">Likelihood</strong></div>' % (tbody)
        
    
    @api.onchange('impact_score','likelihood_score','risk_appetite_id')
    def onchange_hover_grid(self):
        if self.likelihood_score and self.impact_score:
            if self.risk_appetite_id:
                calculation = self.risk_appetite_id.calculation
                self.initial_risk_score = self.compute_calculation(self.likelihood_score, self.impact_score, calculation)
    
        likelihood = int(self.risk_appetite_id.likelihood_score)
        impact = int(self.risk_appetite_id.impact_score)
        calculation = self.risk_appetite_id.calculation
        likelihood_score = self.likelihood_score
        impact_score = self.impact_score
        criteria_ids = self.risk_appetite_id.criteria_ids
        self.html_likelihood_view = self.compute_hover_grid(likelihood, impact, calculation, likelihood_score, impact_score ,criteria_ids)
        
    
    @api.onchange('impact_score','risk_appetite_id')
    def compute_impact_id(self):
        if self.impact_score and self.risk_appetite_id:
            dict_value = []
            obj = self.env['info.risk.impact'].search([('apetite_id','=',self.risk_appetite_id.id)])
            for rec in obj:
                if self.impact_score > int(rec.range):
                    raise UserError(_('Impact score should be in the range of Risk Appetite.'))
                    
                for lines in rec.impact_ids:
                    if int(lines.name) == self.impact_score:
                        context={
                            'name':rec.name,
                            'description':lines.description
                            }
                        dict_value.append(context)
            self.impact_ids = False
            self.impact_ids =[(0, 0, l) for l in dict_value]
    
    @api.onchange('likelihood_score','risk_appetite_id')
    def compute_likelihood_id(self):
        if self.likelihood_score and self.risk_appetite_id:
            dict_value = []
            obj = self.env['info.risk.likelihood'].search([('apetite_id','=',self.risk_appetite_id.id)])
            for rec in obj:
                if self.likelihood_score > int(rec.range) :
                    raise UserError(_('Likelihood score should be in the range of Risk Appetite.'))
                if self.likelihood_score == 0:
                    raise UserError(_('Likelihood score should be in the range of Risk Appetite.'))
                for lines in rec.likelihood_ids:
                    if int(lines.name) == self.likelihood_score:
                        context={
                            'name':rec.name,
                            'description':lines.description
                            }
                        dict_value.append(context)
            self.likelihood_ids = False
            self.likelihood_ids =[(0, 0, l) for l in dict_value]
                        
    
#     @api.onchange('likelihood_score','impact_score','risk_appetite_id')
#     def compute_initial_risk(self):
#         if self.likelihood_score and self.impact_score:
#             if self.risk_appetite_id:
#                 calculation = self.risk_appetite_id.calculation
#                 self.initial_risk_score = self.compute_calculation(self.likelihood_score, self.impact_score, calculation)
#     
#     
    
############################     
#Risk Treatment Menu

    response_id = fields.Many2one('info.risk.response',string='Risk Response')
    response_name = fields.Char()
    response_description = fields.Char("Description")
    justification = fields.Text("Justification")
    
    @api.onchange('response_id')
    def compute_response(self):
        if self.response_id:
            self.response_name = self.response_id.name
            self.response_description = self.response_id.description
#     initial_risk_id = fields.Many2one('info.risk.appetite.criteria',string='Initial Risk Score')
#     residual_risk_id = fields.Many2one('info.risk.appetite.criteria',string='Residual Risk Score')
    
#############################     
#Controls Menu

#     control_standard_ids = fields.Many2one('info.control.standard',string='Control Standard')
    control_control_ids = fields.Many2many('info.control.control',string='Controls')
    
##########################     
#Residual Risk Menu

    res_likelihood_score = fields.Integer(string='Likelihood Score', default=1)
    res_likelihood_ids = fields.Many2many('info.risk.assesment.res.likelihood',string='Likelihood')
    res_impact_score = fields.Integer(string='Impact Score', default=1)
    res_impact_ids = fields.Many2many('info.risk.assesment.res.impact',string='Impact')
    residual_risk_score = fields.Integer(string='Residual Risk Score')
    
    html_residual_view = fields.Html()
        
    @api.onchange('res_impact_score','res_likelihood_score','risk_appetite_id')
    def onchange_hover_grid_residual(self):
        if self.res_likelihood_score and self.res_impact_score:
            if self.risk_appetite_id:
                calculation = self.risk_appetite_id.calculation
                self.residual_risk_score = self.compute_calculation(self.res_likelihood_score, self.res_impact_score, calculation)
        likelihood = int(self.risk_appetite_id.likelihood_score)
        impact = int(self.risk_appetite_id.impact_score)
        calculation = self.risk_appetite_id.calculation
        likelihood_score = self.res_likelihood_score
        impact_score = self.res_impact_score
        criteria_ids = self.risk_appetite_id.criteria_ids
        self.html_residual_view = self.compute_hover_grid(likelihood, impact, calculation, likelihood_score, impact_score ,criteria_ids)
    
    @api.onchange('res_impact_score','risk_appetite_id')
    def compute_res_impact_id(self):
        if self.res_impact_score and self.risk_appetite_id:
            dict_value = []
            obj = self.env['info.risk.impact'].search([('apetite_id','=',self.risk_appetite_id.id)])
            for rec in obj:
                if self.res_impact_score > int(rec.range) or self.res_impact_score == 0:
                    raise UserError(_('Impact score should be in the range of Risk Appetite.'))
                    
                for lines in rec.impact_ids:
                    if int(lines.name) == self.res_impact_score:
                        context={
                            'name':rec.name,
                            'description':lines.description
                            }
                        dict_value.append(context)
            self.res_impact_ids = False
            self.res_impact_ids =[(0, 0, l) for l in dict_value]
    
    @api.onchange('res_likelihood_score','risk_appetite_id')
    def compute_res_likelihood_id(self):
        if self.res_likelihood_score and self.risk_appetite_id:
            dict_value = []
            obj = self.env['info.risk.likelihood'].search([('apetite_id','=',self.risk_appetite_id.id)])
            for rec in obj:
                if self.res_likelihood_score > int(rec.range) :
                    raise UserError(_('Likelihood score should be in the range of Risk Appetite.'))
                if self.res_likelihood_score == 0:
                    raise UserError(_('Likelihood score should be in the range of Risk Appetite.'))
                for lines in rec.likelihood_ids:
                    if int(lines.name) == self.likelihood_score:
                        context={
                            'name':rec.name,
                            'description':lines.description
                            }
                        dict_value.append(context)
            self.res_likelihood_ids = False
            self.res_likelihood_ids =[(0, 0, l) for l in dict_value]
                        
        
    
#     @api.onchange('res_likelihood_score','res_impact_score')
#     def compute_residual_risk(self):
#         if self.res_likelihood_score and self.res_impact_score:
#             if self.risk_appetite_id:
#                 calculation = self.risk_appetite_id.calculation
#                 self.residual_risk_score = self.compute_calculation(self.res_likelihood_score, self.res_impact_score, calculation)
#     
    
    
    
############################
            
    @api.constrains('res_likelihood_score','res_impact_score','likelihood_score','impact_score','response_name')
    def score_validation(self):
        if self.response_name in ['Amend/Treat','Share/Transfer']:
            if self.likelihood_score and self.res_likelihood_score:
                if self.res_likelihood_score > self.likelihood_score:
                    raise UserError(_('Residual likelihood score should be less than Initial likehood score.'))
            if self.impact_score and self.res_impact_score:
                if self.res_impact_score > self.impact_score:
                    raise UserError(_('Residual impact score should be less than Initial impact score.'))
                

    @api.model
    def create(self, vals):   
        if 'risk_appetite_id' in vals:
            appetite_obj = self.env['info.risk.appetite'].browse(vals['risk_appetite_id'])
            calculation = appetite_obj.calculation 
            vals['html_view'] = appetite_obj.html_view
#             vals['html_likelihood_view'] = vals['html_view']
            vals['html_likelihood_view'] = self.compute_hover_grid(int(appetite_obj.likelihood_score), int(appetite_obj.impact_score), calculation, vals['likelihood_score'], vals['impact_score'], appetite_obj.criteria_ids)
        
            vals['html_residual_view'] = self.compute_hover_grid(int(appetite_obj.likelihood_score), int(appetite_obj.impact_score), calculation, vals['res_likelihood_score'], vals['res_impact_score'], appetite_obj.criteria_ids)
        
       
            
            if 'likelihood_score' in vals:
                dict_value = []
                obj = self.env['info.risk.likelihood'].search([('apetite_id','=',vals['risk_appetite_id'])])
                for rec in obj:
                    for lines in rec.likelihood_ids:
                        if int(lines.name) == vals['likelihood_score']:
                            context={
                                'name':rec.name,
                                'description':lines.description
                                }
                            dict_value.append(context)
                vals['likelihood_ids'] =[(0, 0, l) for l in dict_value]
            
            if 'res_likelihood_score' in vals:
                dict_value = []
                obj = self.env['info.risk.likelihood'].search([('apetite_id','=',vals['risk_appetite_id'])])
                for rec in obj:
                    for lines in rec.likelihood_ids:
                        if int(lines.name) == vals['res_likelihood_score']:
                            context={
                                'name':rec.name,
                                'description':lines.description
                                }
                            dict_value.append(context)
                vals['res_likelihood_ids'] =[(0, 0, l) for l in dict_value]
                
            if 'impact_score' in vals:
                dict_value = []
                obj = self.env['info.risk.impact'].search([('apetite_id','=',vals['risk_appetite_id'])])
                for rec in obj:
                    for lines in rec.impact_ids:
                        if int(lines.name) == vals['impact_score']:
                            context={
                                'name':rec.name,
                                'description':lines.description
                                }
                            dict_value.append(context)
                vals['impact_ids'] =[(0, 0, l) for l in dict_value]
                
            if 'res_impact_score' in vals:
                dict_value = []
                obj = self.env['info.risk.impact'].search([('apetite_id','=',vals['risk_appetite_id'])])
                for rec in obj:
                    for lines in rec.impact_ids:
                        if int(lines.name) == vals['res_impact_score']:
                            context={
                                'name':rec.name,
                                'description':lines.description
                                }
                            dict_value.append(context)
                vals['res_impact_ids'] =[(0, 0, l) for l in dict_value]
            
            if 'likelihood_score' in vals and 'impact_score' in vals:
                vals['initial_risk_score'] = self.compute_calculation(vals['likelihood_score'], vals['impact_score'], calculation)
            
            if 'res_likelihood_score' in vals and 'res_impact_score' in vals:
                vals['residual_risk_score'] = self.compute_calculation(vals['res_likelihood_score'], vals['res_impact_score'], calculation)
            
            if 'response_id' in vals:
                response_obj = self.env['info.risk.response'].browse(vals['response_id'])
                vals['response_description'] = response_obj.description
            
        return super(InfoRiskAssessment, self).create(vals)   
        
     
    def write(self, vals):
        likelihood_score = self.likelihood_score
        impact_score = self.impact_score
        res_likelihood_score = self.res_likelihood_score
        res_impact_score = self.res_impact_score
        calculation = self.risk_appetite_id.calculation
        appetite = self.risk_appetite_id.id
#         response_id = self.risk_appetite_id.id
        if 'risk_appetite_id' in vals:
            calculation = self.env['info.risk.appetite'].browse(vals['risk_appetite_id']).calculation
            vals['html_view'] = self.env['info.risk.appetite'].browse(vals['risk_appetite_id']).html_view
            vals['html_likelihood_view'] = vals['html_view']
            appetite = vals['risk_appetite_id']
            
        if 'likelihood_score' in vals and vals['likelihood_score']:
            likelihood_score = vals['likelihood_score']
        if 'impact_score' in vals and vals['impact_score']:
            impact_score = vals['impact_score']
        vals['initial_risk_score'] = self.compute_calculation(likelihood_score, impact_score, calculation)
            
        if 'res_likelihood_score' in vals and vals['res_likelihood_score']:
            res_likelihood_score = vals['res_likelihood_score']
        if 'res_impact_score' in vals and vals['res_impact_score']:
            res_impact_score = vals['res_impact_score']
        vals['residual_risk_score'] = self.compute_calculation(res_likelihood_score, res_impact_score, calculation)
        
        if  'risk_appetite_id' in vals or 'likelihood_score' in vals:
            dict_value = []
            obj = self.env['info.risk.likelihood'].search([('apetite_id','=',appetite)])
            for rec in obj:
                for lines in rec.likelihood_ids:
                    if int(lines.name) == likelihood_score:
                        context={
                            'name':rec.name,
                            'description':lines.description
                            }
                        dict_value.append(context)
            self.likelihood_ids = False
            vals['likelihood_ids'] =[(0, 0, l) for l in dict_value]
        
        if  'risk_appetite_id' in vals or 'res_likelihood_score' in vals:
            dict_value = []
            obj = self.env['info.risk.likelihood'].search([('apetite_id','=',appetite)])
            for rec in obj:
                for lines in rec.likelihood_ids:
                    if int(lines.name) == res_likelihood_score:
                        context={
                            'name':rec.name,
                            'description':lines.description
                            }
                        dict_value.append(context)
            self.res_likelihood_ids = False
            vals['res_likelihood_ids'] =[(0, 0, l) for l in dict_value]
        
        if  'risk_appetite_id' in vals or 'impact_score' in vals:
            dict_value = []
            obj = self.env['info.risk.impact'].search([('apetite_id','=',appetite)])
            for rec in obj:
                for lines in rec.impact_ids:
                    if int(lines.name) == impact_score:
                        context={
                            'name':rec.name,
                            'description':lines.description
                            }
                        dict_value.append(context)
            self.impact_ids = False
            vals['impact_ids'] =[(0, 0, l) for l in dict_value]
        
        if  'risk_appetite_id' in vals or 'res_impact_score' in vals:
            dict_value = []
            obj = self.env['info.risk.impact'].search([('apetite_id','=',appetite)])
            for rec in obj:
                for lines in rec.impact_ids:
                    if int(lines.name) == res_impact_score:
                        context={
                            'name':rec.name,
                            'description':lines.description
                            }
                        dict_value.append(context)
            self.res_impact_ids = False
            vals['res_impact_ids'] =[(0, 0, l) for l in dict_value]
            
        print("qqqqqqqqqqqqqqqqq1111111111",vals)
        if 'response_id' in vals:
            print("qqqqqqqqqqqqqqqqq2222222",vals)
            response_obj = self.env['info.risk.response'].browse(vals['response_id'])
            print("qqqqqqqqqqqqqqqqq333333",response_obj,response_obj.description)
            vals['response_description'] = response_obj.description
            
            
        appetite_obj = self.env['info.risk.appetite'].browse(appetite)
        vals['html_likelihood_view'] = self.compute_hover_grid(int(appetite_obj.likelihood_score), int(appetite_obj.impact_score), appetite_obj.calculation, likelihood_score, impact_score, appetite_obj.criteria_ids)
        
        vals['html_residual_view'] = self.compute_hover_grid(int(appetite_obj.likelihood_score), int(appetite_obj.impact_score), appetite_obj.calculation, res_likelihood_score, res_impact_score, appetite_obj.criteria_ids)
        
            
            
        return super(InfoRiskAssessment, self).write(vals)  
    
    

   
class InfoRiskAssesmentLikelihood(models.Model):
    _name = 'info.risk.assesment.likelihood'
     
    name = fields.Char("Name")
    description = fields.Char("Description")
#     assessment_id = fields.Many2one('info.risk.assesment')
   
class InfoRiskAssesmentImpact(models.Model):
    _name = 'info.risk.assesment.impact'
     
    name = fields.Char("Name")
    description = fields.Char("Description")
#     assessment_id = fields.Many2one('info.risk.assesment')
   
class InfoRiskAssesmentResLikelihood(models.Model):
    _name = 'info.risk.assesment.res.likelihood'
     
    name = fields.Char("Name")
    description = fields.Char("Description")
#     assessment_id = fields.Many2one('info.risk.assesment')
   
class InfoRiskAssesmentResImpact(models.Model):
    _name = 'info.risk.assesment.res.impact'
     
    name = fields.Char("Name")
    description = fields.Char("Description")
#     assessment_id = fields.Many2one('info.risk.assesment')


class InfoRiskReview(models.Model):
    _name = 'info.risk.review'
     
    name = fields.Many2one('info.risk.assessment',string="Name")
    description = fields.Char("Description")
#     assessment_id = fields.Many2one('info.risk.assesment')
    
    
    
    
    
    
    
