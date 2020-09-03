# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class ProductProduct(models.Model):
    _inherit = 'product.product'
    
    knowledge_base_id = fields.Many2one('info.knowledge.base')

class ResGroups(models.Model):
    _inherit = 'res.groups'
    
    read_group_id = fields.Many2one('info.knowledge.base')
    contibute_groups_id = fields.Many2one('info.knowledge.base')
 


class InfoKnowledgeBase(models.Model):
    _name = 'info.knowledge.base'
    _rec_name = 'number'
    
    
    
    number = fields.Char('Number')
    title = fields.Char('Title')
    valid_art = fields.Date('Article Validity')
    icon_image = fields.Image('Icon')
    owner = fields.Many2one('hr.employee','Owner')
    state = fields.Selection([('draft', ' Draft'),
                              ('done', 'Done')],
                              "State", default='draft')
#     manager = fields.Many2one('hr.employee','Manager')
    publish_workflow = fields.Selection([('instant', ' Knowledge Instant Publish'),
                                         ('approval', 'Knowledge Approval Publish')],
                                         "Publish Workflow")
    retir_flow = fields.Selection([('instant', ' Knowledge Instant Retire'),
                                   ('approval', 'Knowledge Approval Retire')],
                                    "Retire Workflow")
    is_active = fields.Boolean('Active')
    q_a = fields.Boolean('Enable social questions and answers')
    desc = fields.Text('Description')
    set_default = fields.Boolean('Set default knowledge field values')
    related_cmdb_ids = fields.Many2many('info.cmdb.classes',string='Related CI')
    knowledge_ids = fields.One2many('info.knowledge.knowledge','knowledge_base_id', string='Knowledge')
    category_ids = fields.Many2many('info.knowledge.category',string='Knowledge category')
    read_group_ids = fields.Many2many('res.groups', relation='read_group_id', string='Can read')
    contibute_groups_ids = fields.Many2many('res.groups', relation='contibute_groups_id', string='Can contribute')
    
    _sql_constraints = [
            ('title_uniq', 'unique(title)', 'Title must be unique per Base!'),
        ]
    
                
        
    def action_done(self):
        self.write({'state':'done'})
        for rec in self.knowledge_ids:
            if self.publish_workflow == 'instant':
                rec.is_instant_publish = True
            else:
                rec.is_instant_publish = False
                
            if self.retir_flow == 'instant':
                rec.is_instant_retire = True
            else:
                rec.is_instant_retire = False
                
                
    def action_draft(self):
        self.write({'state':'draft'})
        for rec in self.knowledge_ids:
            rec.is_instant_publish = False
            rec.is_instant_retire = False
    
    @api.onchange('knowledge_ids','publish_workflow')
    def set_knwoledge_article(self):
        if self.publish_workflow == 'instant':
            for rec in self.knowledge_ids:
                rec.is_template = True
                
        
    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('info.knowledge.base') or _('New')
        return super(InfoKnowledgeBase, self).create(vals)
    


class InfoKnowledgeCategory(models.Model):
    _name = 'info.knowledge.category'
    
    name = fields.Char('Name')
    patent_id = fields.Many2one('info.knowledge.category','Parent')
    desc = fields.Text('Description')
    
    knowledge_base_id = fields.Many2one('info.knowledge.base','Parent')
    

class InfoKnowledgeResUserCount(models.Model):
    _name = 'info.knowledge.users'
    
#     name = fields.Char('Name')
    user_id = fields.Many2one('res.users','User')
    count = fields.Integer('Count')
    is_like = fields.Boolean( default=False) 
    is_dislike = fields.Boolean( default=False)  
    knowledge_users_id = fields.Many2one('info.knowledge.knowledge')
       
    
#     
class InfoKnowledgeRating(models.Model):  
    _name = 'info.knowledge.rating'
    _rec_name = 'article_id'
 
    user_id = fields.Many2one('res.users','User', default=lambda self: self.env.user)
    rating_comment = fields.Text('Comment')    
    article_id = fields.Many2one('info.knowledge.knowledge',)
#     rating_image = fields.Binary('Image', compute='_compute_rating_image')
    rating_text = fields.Selection([
        ('satisfied', 'Satisfied'),
        ('not_satisfied', 'Not satisfied'),
        ('highly_dissatisfied', 'Highly dissatisfied'),
        ('no_rating', 'No Rating yet')], string='Rating')
#     
#     
    
class InfoKnowledge(models.Model):
    _name = 'info.knowledge.knowledge'
    _rec_name = 'number'

    number = fields.Char('Number')
    state = fields.Selection([('draft', ' Draft'),
                              ('review', 'Review'),
                              ('published', 'Published'),
                              ('retirement', 'Pending Retirement'),
                              ('retired', 'Retired')],
                              "State", default='draft')
    parent_id = fields.Many2one('info.knowledge.knowledge','Parent')
    knowledge_base_id = fields.Many2one('info.knowledge.base','Knowledge base')
    language_id = fields.Many2one('res.lang','Language')
    is_template = fields.Boolean('Is it a template', default=False) 
    is_instant_publish = fields.Boolean( default=False)   
    is_instant_retire = fields.Boolean( default=False)   
    template_id = fields.Many2one('info.knowledge.knowledge','Template')
    
    flag = fields.Integer(compute='compute_flag')
    flag_form = fields.Integer(compute='compute_flag_form')
    flag2 = fields.Integer('Count')
    user_count_ids = fields.One2many('info.knowledge.users','knowledge_users_id')
    
    def open_rating(self):
        return {
            'name': _('Rating'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.knowledge.rating',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'domain': [('article_id', '=', self.id)],
            }
    
#     @api.model
#     def rating_wizard(self, action_ref=None):
#         if not action_ref:
#             action_ref = 'info_knowledge.info_rating_wizard'
#         return self.env.ref(action_ref).read()[0] 
    
    def action_pass(self):
        pass
    
    is_like = fields.Boolean( default=False)  
    is_dislike = fields.Boolean( default=False)  
    like_count = fields.Integer('Like Count')  
    dislike_count = fields.Integer('Dislike Count')
    
    def action_like(self):
        self.is_like = True
        for rec in self.user_count_ids:
            if rec.user_id == self.env.user:
                rec.is_like = True
                rec.is_dislike = False
        self.is_dislike = False
    
    
    def action_dislike(self):
        self.is_like = False
        for rec in self.user_count_ids:
            if rec.user_id == self.env.user:
                rec.is_like = False
                rec.is_dislike = True
        self.is_dislike = True
    
    
    def compute_flag_form(self):
#         record.flag +=1
        self.flag2 += 1
        self.flag_form += 1
        user = self.env.user
        f=0
        for rec in self.user_count_ids:
            if rec.user_id == user:
                f=1
                rec.count += 1
#                 self.is_like = rec.is_like
#                 self.is_dislike = rec.is_dislike
        if f == 0:
            self.user_count_ids = [(0, 0,{'count':1,'user_id':user.id})]
        
    
    def compute_flag(self):
        for record in self:
            record.flag += 1
            print("selfffffffffffffffffffffff111111111111",self.env.user)
            user = self.env.user
#             f=0
            like = 0
            dislike = 0
            for rec in record.user_count_ids:
                if rec.is_like:
                    like += 1
                if rec.is_dislike:
                    dislike+= 1
                if rec.user_id == user:
#                     f=1
#                     rec.count += 1
                    record.is_like = rec.is_like
                    record.is_dislike = rec.is_dislike
            record.like_count = like
            record.dislike_count = dislike
#             if f == 0:
#                 record.user_count_ids = [(0, 0,{'count':1,'user_id':user.id})]
            print("selfffffffffffffffffffffff",record.flag)
#     @api.depends('knowledge_base_id','knowledge_base_id.publish_workflow')
#     def _compute_is_instant(self):
#         for rec in self:
#             print("sssssssssssssssssssssssssssssssssssssssssssssssssss")
#         if self.knowledge_base_id:
#             if self.knowledge_base_id.publish_workflow == 'instant':
#                 self.is_instant = True
        
#     @api.model
#     def _lang_get(self):
#         return self.env['res.lang'].get_installed()
#     
#     lang = fields.Selection(_lang_get, string='Language', default=lambda self: self.env.lang)
#     
    published = fields.Date('Published')
    valid_to = fields.Date('Valid to')

    short_desc = fields.Char('Short description')
    article = fields.Html('Article body')
    workflow = fields.Selection([('draft', ' Draft'),('review', 'In Review'),('published', 'Published')], "Workflow", default='draft')
    link = fields.Binary('Attachment link', attachment=True)
    disp = fields.Boolean('Display attachments')  
    user_id = fields.Many2one('res.users','Owner', default=lambda self: self.env.user)
#     inspect_file = fields.Binary('Attachment', attachment=True)  

#     @api.onchange('knowledge_base_id')
#     def onchange_knowledge_base(self):
#         print("sssssssssssssssssssssssssssssssssssssssssssssssssss")
    @api.onchange('template_id')
    def get_template_values(self):
        self.short_desc = self.template_id.short_desc or False
        self.parent_id = self.template_id.parent_id or False
        self.article = self.template_id.article or False
        
        
    def set_draft(self):
        self.write({'state':'draft'})
    
    def set_publish(self):
        self.write({'state':'published'})
    
    def set_pend_retire(self):
        self.write({'state':'retirement'})
    
    def set_retire(self):
        self.write({'state':'retired'})
    
    
        
    def set_review(self):
        if self.state == 'draft':
            self.write({'state':'review'})
    
    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('info.knowledge.knowledge') or _('New')
        return super(InfoKnowledge, self).create(vals)
    
    


class InfoKnowledgeFeedback(models.Model):
    _name = 'info.knowledge.feedback'
    _rec_name = 'created_date'
    
    
    article_id = fields.Many2one('info.knowledge.knowledge', string='Article')
    state = fields.Selection([('draft', ' Draft'),
                              ('done', 'Done')],
                              "State", default='draft')
    
    user_id = fields.Many2one('res.users','Owner', default=lambda self: self.env.user, readonly=True)
    created_date = fields.Date('Created Date', default=fields.Date.context_today, readonly=True)
    
    comment = fields.Text('Comments')
    work_notes = fields.Text('Work Notes')
    is_flagged = fields.Boolean('Flagged', default=False)   
    useful = fields.Selection([('yes', 'Yes'),
                              ('no', 'No')],
                              "Useful")
    
    
