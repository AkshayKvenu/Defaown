# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError



class InfoRiskResponseTypes(models.Model):
    _name = 'info.risk.response'
#     _description = 'info_risk.info_risk'
    name = fields.Char("Types")
    description = fields.Text("Descripiton")
    default_description = fields.Text("Default Descripiton")

    @api.model
    def create(self, vals):    
        vals['default_description'] = vals['description']
        return super(InfoRiskResponseTypes, self).create(vals)  
    
    def set_draft(self): 
        if self.default_description:
            self.description = self.default_description
            
   

    

class InfoRiskAppetite(models.Model):
    _name = 'info.risk.appetite'
    
    name = fields.Char("Name")
    state = fields.Selection([('draft', ' Draft'),('approve', 'Approved')], "State", default='draft')
    is_assessment = fields.Boolean(default=False)

    color = fields.Char(
            string="Color",
            help="Choose your color"
                )
    
    
    
    
    likelihood_count = fields.Integer(compute='_likelihood_count', string="likelihood")
    
    def _likelihood_count(self):
        for asset in self:
            res = self.env['info.risk.likelihood'].search_count([('apetite_id', '=', self.id)])
            asset.likelihood_count = res or 0
            
    impact_count = fields.Integer(compute='_impact_count', string="likelihood")
    
    def _impact_count(self):
        for asset in self:
            res = self.env['info.risk.impact'].search_count([('apetite_id', '=', self.id)])
            asset.impact_count = res or 0


    def open_likelihood(self):
        context = dict(self.env.context or {})
        context['default_apetite_id'] = self.id
        return {
            'name': _('Likelihood'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.risk.likelihood',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context':context,
            'domain': [('apetite_id', '=', self.id)]
            }


    def open_impact(self):
        context = dict(self.env.context or {})
        context['default_apetite_id'] = self.id
        return {
            'name': _('Impact'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.risk.impact',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context':context,
            'domain': [('apetite_id', '=', self.id)]
            }
        
        
        
    def compute_impact(self):
        if self.impact_score:
            likeli = []
            
            if self.impact_score == '3':
                def_val=['Low','Medium','High']
                for i in range(int(self.impact_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            elif self.impact_score == '4':
                def_val=['Very Low','Low','High','Very High']
                for i in range(int(self.impact_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            elif self.impact_score == '5':
                def_val=['Very Low','Low','Medium','High','Very High']
                for i in range(int(self.impact_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            elif self.impact_score == '6':
                def_val=['Negligible','Very Low','Low','High','Very High','Critical']
                for i in range(int(self.impact_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            elif self.impact_score == '7':
                def_val=['Negligible','Very Low','Low','Medium','High','Very High','Critical']
                for i in range(int(self.impact_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            
        dict_value=[]
        values=[]
        list_ = []
        if self.impact_score == '3':
            def_val_c=['Minimal amount of critical data exposed','Extensive amount of non-sensitive data disclosed','Extensive amount of sensitive data disclosed']
            def_val_i=['Minimal amount of data seriously corrupt','Extensive amount of data slightly corrupt','Extensive amount of data partly corrupt']
            def_val_a=['Secondary services extensively interrupted','Primary services minimally interrupted','Primary services partly interrupted']
        elif self.impact_score == '4':
            def_val_c=['Minimal amount of sensitive data exposed','Minimal amount of critical data exposed','Extensive amount of sensitive data disclosed',
                       'Extensive amount of critical data disclosed']
            def_val_i=['Minimal amount of data partly corrupt','Minimal amount of data seriously corrupt','Extensive amount of data partly corrupt',
                       'Extensive amount of data seriously corrupt']
            def_val_a=['Secondary services partly interrupted','Secondary services extensively','Primary services partly ','Primary services extensively']
        elif self.impact_score == '5':
            def_val_c=['Minimal amount of sensitive data exposed','Minimal amount of critical data exposed','Extensive amount of non-sensitive data disclosed',
                       'Extensive amount of sensitive data disclosed','Extensive amount of critical data disclosed']
            def_val_i=['Minimal amount of data partly corrupt','Minimal amount of data seriously corrupt','Extensive amount of data slightly corrupt',
                       'Extensive amount of data partly corrupt','Extensive amount of data seriously corrupt']
            def_val_a=['Secondary services partly interrupted','Secondary services extensively interrupted','Primary services minimally interrupted',
                       'Primary services partly interrupted','Primary services extensively interrupted']
        elif self.impact_score == '6':
            def_val_c=['Minimal amount of non-sensitive data disclosed','Minimal amount of sensitive data exposed','Minimal amount of critical data exposed',
                       'Extensive amount of sensitive data disclosed','Extensive amount of critical data disclosed','All data disclosed']
            def_val_i=['Minimal amount of data slightly corrupt','Minimal amount of data partly corrupt','Minimal amount of data seriously corrupt',
                       'Extensive amount of data partly corrupt','Extensive amount of data seriously corrupt','All data corrupt']
            def_val_a=['Secondary services minimally','Secondary services partly','Secondary services extensively','Primary services partly interrupted',
                       'Primary services extensively ','All systems lost']
        elif self.impact_score == '7':
            def_val_c=['Minimal amount of non-sensitive data disclosed','Minimal amount of sensitive data exposed','Minimal amount of critical data exposed','Extensive amount of non-sensitive data disclosed',
                       'Extensive amount of sensitive data disclosed','Extensive amount of critical data disclosed','All data disclosed']
            def_val_i=['Minimal amount of data slightly corrupt','Minimal amount of data partly corrupt','Minimal amount of data seriously corrupt',
                       'Extensive amount of data slightly corrupt','Extensive amount of data partly corrupt','Extensive amount of data seriously corrupt','All data corrupt']
            def_val_a=['Secondary services minimally interrupted','Secondary services partly interrupted','Secondary services extensively interrupted',
                       'Primary services minimally interrupted','Primary services partly interrupted','Primary services extensively interrupted','All systems lost']
            
            
        context_li={
            'name':'General',
            'range':self.impact_score,
            'default_range':self.impact_score,
            'is_general':True,
            'apetite_id':self.id,
            'impact_ids':[(0, 0, l) for l in likeli],
            'default_ids':[(0, 0, l) for l in likeli]
            
            }
        obj = self.env['info.risk.impact'].search([('apetite_id','=',self.id)])
        for rec in obj:
            obj.is_general = False
        self.env['info.risk.impact'].search([('apetite_id','=',self.id)]).unlink()
        obj = self.env['info.risk.impact'].create(context_li)
        
        
        lines_C = {}
        lines_I = {}
        lines_A = {}
        
        values_C = []
        values_I = []
        values_A = []
        
        
        for i in range(int(self.impact_score)):
            lines_C={'name' : str(i+1),
                    'description' : def_val_c[i]}
            values_C.append(lines_C)
            lines_I={'name' : str(i+1),
                    'description' : def_val_i[i]}
            values_I.append(lines_I)
            lines_A={'name' : str(i+1),
                    'description' : def_val_a[i]}
            values_A.append(lines_A)
            
        context_C={
            'name':'Confidentiality',
            'range':self.impact_score,
            'default_range':self.impact_score,
            'is_general':True,
            'apetite_id':self.id,
            'impact_ids':[(0, 0, l) for l in values_C],
            'default_ids':[(0, 0, l) for l in values_C]
            
            }
        self.env['info.risk.impact'].create(context_C)
            
        context_I={
            'name':'Integrity',
            'range':self.impact_score,
            'default_range':self.impact_score,
            'is_general':True,
            'apetite_id':self.id,
            'impact_ids':[(0, 0, l) for l in values_I],
            'default_ids':[(0, 0, l) for l in values_I]
            
            }
        self.env['info.risk.impact'].create(context_I)
            
        context_A={
            'name':'Availability',
            'range':self.impact_score,
            'default_range':self.impact_score,
            'is_general':True,
            'apetite_id':self.id,
            'impact_ids':[(0, 0, l) for l in values_A],
            'default_ids':[(0, 0, l) for l in values_A]
            
            }
        self.env['info.risk.impact'].create(context_A)
#         self.env.company.onboarding_state_impact = 'done'

    def compute_likelihood(self):
#         print("sssssss",self.number)
        if self.likelihood_score:
#             self.likelihood_ids = False
            likeli = []
            
            if self.likelihood_score == '3':
                def_val=['Unlikely','Plausible','Likely']
                for i in range(int(self.likelihood_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            elif self.likelihood_score == '4':
                def_val=['Highly unlikely','Unlikely','Likely','Highly Likely']
                for i in range(int(self.likelihood_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            elif self.likelihood_score == '5':
                def_val=['Highly unlikely','Unlikely','Plausible','Likely','Highly Likely']
                for i in range(int(self.likelihood_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            elif self.likelihood_score == '6':
                def_val=['Almost Impossible','Highly unlikely','Unlikely','Likely','Highly Likely','Almost Certain']
                for i in range(int(self.likelihood_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
                    
            elif self.likelihood_score == '7':
                def_val=['Almost Impossible','Highly unlikely','Unlikely','Plausible','Likely','Highly Likely','Almost Certain']
                for i in range(int(self.likelihood_score)):
                    lines={
                        'name' : str(i+1),
                        'description' : def_val[i]}
                    likeli.append(lines)
            context_li={
            'name':'General',
            'range':self.likelihood_score,
            'default_range':self.likelihood_score,
            'is_general':True,
            'apetite_id':self.id,
            'likelihood_ids':[(0, 0, l) for l in likeli],
            'default_ids':[(0, 0, l) for l in likeli] 
            }        
            obj = self.env['info.risk.likelihood'].search([('apetite_id','=',self.id)])
            for rec in obj:
                obj.is_general = False
            self.env['info.risk.likelihood'].search([('apetite_id','=',self.id)]).unlink()
            self.env['info.risk.likelihood'].create(context_li)
            
    def action_validate(self): 
        if self.state == 'draft':
            self.write({'state':'approve'})
            self.compute_likelihood()
            self.compute_impact()
            
    
    def action_draft(self): 
        if self.state == 'approve':
            self.write({'state':'draft'})
            
    def _compute_max(self, calculation, likelihood, impact):
#         calculation = self.calculation
#         likelihood = self.likelihood_score
#         impact = self.impact_score
        if likelihood and impact:
            if calculation == 'add':
                return int(likelihood) + int(impact)
            elif calculation == 'add1':
                return int(likelihood) + int(impact) -1
            elif calculation == 'multiple':
                return int(likelihood) * int(impact)
                
    
    def _compute_min(self, calculation):
        if calculation == 'add':
            return 2
        elif calculation == 'add1':
            return 1
        elif calculation == 'multiple':
            return 1
        
        
    def _compute_criteria(self):
        calculation = self.calculation
        likelihood = int(self.likelihood_score)
        impact = int(self.impact_score)
        list2 = []
        list3 = []
        list_score = []
        if calculation == 'add':
            max = likelihood+impact
            range_A = round(max/3)
            list1 = [2,range_A]
            list2 = [range_A+1,range_A+2]
            list3 = [range_A+3,max]
            list_score = [list1,list2,list3]
        elif calculation == 'add1':
            max = likelihood+impact-1
            range_A = round(max/3)
            list1 = [1,range_A]
            list2 = [range_A+1,range_A+2]
            list3 = [range_A+3,max]
            list_score = [list1,list2,list3]
        elif calculation == 'multiple':
            abc=[x*y for x in range(1,likelihood+1)for y in range(1,impact+1)]
            max = likelihood*impact
            range_A = round(max/3)
            sort_list = list(set(abc))
            final_list = sorted(abc)
            a=0
            b=0
            c=0
            d=0
            if range_A in final_list:
                a=range_A
            else:
                for x in range(len(final_list)):
                    if range_A < final_list[x]:
                        a = final_list[x-1]
                        b = final_list[x]
                        break
                    
#             if b==0:
            if a+1 in final_list:
                b=a+1
            else:
                for x in range(len(final_list)):
                    if a+1 < final_list[x]:
                        b = final_list[x]
                        break
                        
                        
            if b+1 in final_list:
                c = b+1
            else:
                for x in range(len(final_list)):
                    if b+1 < final_list[x]:
                        c = final_list[x]
                        break
                    
            if c+1 in final_list:
                d = c+1
            else:
                for x in range(len(final_list)):
                    if c+1 < final_list[x]:
                        d = final_list[x]
                        break
                    
            list1 = [1,a]
            list2 = [b,c]
            list3 = [d,max]
            list_score = [list1,list2,list3]
        
        list_name=['Acceptable','Border line','Unacceptable']
        color_list=['rgba(133,235,154,1)','rgba(196,196,205,1)','rgba(252,135,135,1)']
        likeli = []
        for i in range(len(list_name)):
            lines={
                'name' : list_name[i],
                'is_default': True,
                'score_min': list_score[i][0],
                'score_max': list_score[i][1],
                'color': color_list[i] }
            likeli.append(lines)
            obj = self.env['info.risk.appetite.criteria'].create(likeli)
            
        return obj
    
    def compute_likelihood_score(self):   
        return self.env['ir.config_parameter'].sudo().get_param('info_risk.likelihood_range') or '3'
    
    def compute_impact_score(self):   
        return self.env['ir.config_parameter'].sudo().get_param('info_risk.impact_range') or '3'
    
    def compute_calcutation(self):   
        return self.env['ir.config_parameter'].sudo().get_param('info_risk.risk_calculation')
    
    @api.onchange('likelihood_score','impact_score','calculation')
    def compute_min_max_score(self):
        if self.likelihood_score and self.impact_score:
            if self.calculation:
                self.score_min =self._compute_min(self.calculation)
                self.score_max =self._compute_max(self.calculation, self.likelihood_score, self.impact_score)
                if self.criteria_ids:
                    for rec in self.criteria_ids:
                        rec.is_default =False
                        rec.appetite_id = False
                    self.criteria_ids = False
                if self.default_criteria_ids:
                    for rec in self.default_criteria_ids:
                        rec.is_default =False
                        rec.appetite_id = False
                    self.default_criteria_ids = False
                self.criteria_ids = self._compute_criteria()
                self.default_criteria_ids = self._compute_criteria()
                
                
                
    
    likelihood_score = fields.Selection([('3', "3"), ('4', "4"), ('5', "5"), ('6', "6"), ('7', "7")], default=compute_likelihood_score, string='Likelihood')
    impact_score = fields.Selection([('3', "3"), ('4', "4"), ('5', "5"), ('6', "6"), ('7', "7")], default=compute_impact_score, string='Impact')
    calculation = fields.Selection([('add', "[Impact] + [Likelihood]"),('add1', "[Impact] + [Likelihood] - 1"),('multiple', "[Impact] x [Likelihood]")],
                                      string='Risk Calculation', default=compute_calcutation)
    score_min = fields.Integer("Score Min")
    score_max = fields.Integer("Score Max")
#     likelihood_ids = fields.One2many('info.risk.appetite.criteria','appetite_id',string='Criteria')
    criteria_ids = fields.One2many('info.risk.appetite.criteria','appetite_id',string='Criteria')
    default_criteria_ids = fields.One2many('info.risk.appetite.criteria','default_appetite_id')
    
    html_view = fields.Html('HTML View',compute="_create_html_view")
#     risk_criteria_ids = fields.One2many('risk.criteria', 'relation_id', string="Risk Criterias")
            
    @api.depends('criteria_ids','criteria_ids.color')
    def _create_html_view(self):
        likelihood = int(self.likelihood_score)
        impact = int(self.impact_score)
        col_likelihood = [i for i in range(1,likelihood+1)]
        row_impact = [i for i in range(1,impact+1)]
        row_impact.reverse()
        
        tbody = ''
        for line in row_impact:
            row = ''
            for item in col_likelihood:
                if self.calculation == 'add':
                    cell_val = line+item
                elif self.calculation == 'add1':
                    cell_val = line+item-1
                elif self.calculation == 'multiple':
                    cell_val = line*item
#                 cell_val = line+item-1
                color_pick = 'black'
                for criteria in self.criteria_ids:
                    if criteria.score_min <= cell_val <= criteria.score_max:
                        color_pick = criteria.color
                row += '<td style="border-right:1px solid black;background-color:%s;text-align:center;width:50px;height:50px">%s</td>' % (color_pick, cell_val)
            tbody += '<tr style="border-bottom:1px solid black">%s</tr>' % row
        tbody = '<tbody>%s</tbody>' % tbody
        self.html_view = '<div class="col-xs-12"><div class="col-xs-1"><strong>Impact</strong></div><div class="col-xs-10"><table style="border:1px solid black">%s</table></div></div><div class="col-xs-2 col-xs-offset-1" style="margin-top:10px;margin-bottom:10px"><strong style="padding-left:17px">Likelihood</strong></div>' % (tbody)
        

    def unlink(self):
        for type in self:
            res = self.env['info.risk.assessment'].search_count([('risk_appetite_id','=',type.id)])
            if res > 0:
                raise UserError(_('You cannot delete an Appetite that is already used.'))
        return super(InfoRiskAppetite, self).unlink()
    
    
    @api.model
    def create(self, vals):  
#         if 'likelihood_score' in vals and 'impact_score' in vals and 'calculation' in vals: 
        vals['score_min'] = self._compute_min(self.compute_calcutation())
        vals['score_max'] = self._compute_max(self.compute_calcutation(), vals['likelihood_score'], vals['impact_score'])
        return super(InfoRiskAppetite, self).create(vals) 

    def write(self, vals):    
        likelihood = self.likelihood_score
        impact = self.impact_score
        calculation =  self.calculation
        if 'likelihood_score' in vals and vals['likelihood_score']:
            likelihood = vals['likelihood_score']
        if 'impact_score' in vals and vals['impact_score']:
            impact = vals['impact_score']
        if 'calculation' in vals and vals['calculation']:
            calculation = vals['calculation']
        vals['score_min'] = self._compute_min(calculation)
        vals['score_max'] = self._compute_max(calculation,likelihood,impact)
        return super(InfoRiskAppetite, self).write(vals)    
    
    
    def set_draft(self): 
        self.criteria_ids =False
        likeli =[]
        for rec in self.default_criteria_ids:
            lines={
                'name' : rec.name,
                'is_default': True,
                'score_min': rec.score_min,
                'score_max': rec.score_max,
                'color': rec.color }
            likeli.append(lines)
        self.criteria_ids =[(0, 0, l) for l in likeli]
#             obj = self.env['info.risk.appetite.criteria'].create(likeli)
            
    @api.constrains('criteria_ids')
    def lines_validation(self):
        if self.likelihood_score and self.impact_score:
            if self.calculation:
                score_min =self._compute_min(self.calculation)
                score_max =self._compute_max(self.calculation, self.likelihood_score, self.impact_score)
        num = 0
        for rec in self.criteria_ids:
            if rec.is_default:
                num +=1
            if rec.score_max < rec.score_min:
                raise UserError(_('Score max should be greater than score min.'))
            if rec.score_max <= 0:
                raise UserError(_('Score max should be greater than 0.'))
            if rec.score_min <= 0:
                raise UserError(_('Score min should be greater than 0.'))
            if score_min > rec.score_min:
                raise UserError(_('Score min of %s should be greater than default score min.') % (rec.name,))
            if score_max < rec.score_max:
                raise UserError(_('Score max of %s should be lesser than default score max.') % (rec.name,))
            for lines in self.criteria_ids:
                if rec.id != lines.id:
                    range_line = list(range(lines.score_min,lines.score_max+1))
                    if rec.score_max in range_line:
                        raise UserError(_('Range cannot be overlapped.'))
        if num != 3 and self.criteria_ids:
            raise UserError(_('You cannot delete default criteria.'))
            
                

class InfoRiskAppetiteCriteria(models.Model):
    _name = 'info.risk.appetite.criteria'
    
    name = fields.Char("Name")
#     colour = fields.Char("Colour")
    score_min = fields.Integer("Score Min")
    score_max = fields.Integer("Score Max")
    description = fields.Char("Descripiton")
    is_default = fields.Boolean(default=False)
    appetite_id = fields.Many2one('info.risk.appetite')
    default_appetite_id = fields.Many2one('info.risk.appetite')
    color = fields.Char(
            string="Color",
            help="Choose your color"
                )
    
    

class ResCompany(models.Model):
    _inherit = 'res.company'
    
    
    sale_quotation_onboarding_state = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done"), ('closed', "Closed")], string="State of the sale onboarding panel", default='not_done')
    onboarding_state_impact = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done"), ('closed', "Closed")], string="State of the impact onboarding panel", default='not_done')
    
    onboarding_state_scenarios = fields.Selection([('not_done', "Not done"), ('just_done', "Just done"), ('done', "Done"), ('closed', "Closed")], string="State of the scenerio onboarding panel", default='not_done')
    
    @api.model
    def action_close_sale_quotation_onboarding(self):
        """ Mark the onboarding panel as closed. """
        self.env.company.sale_quotation_onboarding_state = 'closed'
        
    @api.model
    def action_close_impact_onboarding(self):
        """ Mark the onboarding panel as closed. """
        self.env.company.onboarding_state_impact = 'closed'
        
    @api.model
    def action_close_scenarios_onboarding(self):
        """ Mark the onboarding panel as closed. """
        self.env.company.onboarding_state_scenarios = 'closed'
    
    