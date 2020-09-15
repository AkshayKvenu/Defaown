# -*- coding: utf-8 -*-
import base64

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
from odoo.modules.module import get_resource_path
from bs4 import BeautifulSoup



class InfoKnowledgeTags(models.Model):
    _name = 'info.knowledge.tags'
    
    name = fields.Char('Name')
    
    _sql_constraints = [
            ('title_uniq', 'unique(name)', 'Name must be unique!'),
        ]
    
    
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
    active = fields.Boolean(default=True)
    desc = fields.Text('Description')
    related_asset_ids = fields.Many2many('account.asset.asset',string='Related CI')
    knowledge_ids = fields.One2many('info.knowledge.knowledge','knowledge_base_id', string='Knowledge Article')
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
            rec.category_ids = [(6, 0, self.category_ids.ids)]
            print("qqqqqqqqqqqqqqqqq",self.read_group_ids)
            for i in self.read_group_ids:
                print("Ssssssssssssssssssssss",i.users)
#                 users = approver_group.users.
                
                
    def action_draft(self):
        self.write({'state':'draft'})
        for rec in self.knowledge_ids:
            rec.is_instant_publish = False
            rec.is_instant_retire = False
            rec.category_ids = False
    
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
    _rec_name = 'user_id'
 
    user_id = fields.Many2one('res.users','User', default=lambda self: self.env.user)
    rating_comment = fields.Text('Comment')    
    article_id = fields.Many2one('info.knowledge.knowledge',)
    rating_image = fields.Binary('Image', compute='_compute_rating_image')
    rating_text = fields.Selection([
    ('0', 'No Rating yet'),
    ('1', 'Highly dissatisfied'),
    ('2', 'dissatisfied'),
    ('3', 'Not satisfied'),
    ('4', 'Satisfied'),
    ('5', 'Highly Satisfied')], string='Rating')


    
    def unlink(self):
        for type in self:
            if type.user_id != self.env.user:
                raise UserError(_('You can delete only your rating.'))
        return super(InfoKnowledgeRating, self).unlink()
    
    
    @api.depends('rating_text')
    def _compute_rating_image(self):
        # Due to some new widgets, we may have ratings different from 0/1/5/10 (e.g. slide.channel review)
        # Let us have some custom rounding while finding a better solution for images.
        for rating in self:
            rating_for_img = 0
            if rating.rating_text == '5':
                rating_for_img = 10
            elif rating.rating_text == '3':
                rating_for_img = 5
            elif rating.rating_text == '1':
                rating_for_img = 1
            try:
                image_path = get_resource_path('info_knowledge', 'static/src/img', 'rating_%s.png' % rating_for_img)
                rating.rating_image = base64.b64encode(open(image_path, 'rb').read())
            except (IOError, OSError):
                rating.rating_image = False
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
    tags_ids = fields.Many2many('info.knowledge.tags')
    category_ids = fields.Many2many('info.knowledge.category',string='Knowledge category')
    language_id = fields.Many2one('res.lang','Language')
    is_template = fields.Boolean('Is it a template', default=False) 
    is_instant_publish = fields.Boolean( default=False)   
    is_instant_retire = fields.Boolean( default=False)   
    template_id = fields.Many2one('info.knowledge.knowledge','Template')
    
    flag = fields.Integer(compute='compute_flag')
    flag_form = fields.Integer(compute='compute_flag_form')
    flag2 = fields.Integer('Views')
    user_count_ids = fields.One2many('info.knowledge.users','knowledge_users_id')
    rating_count = fields.Integer(compute='_compute_rating_count')
    
    def _compute_rating_count(self):
        for rat in self:
            res = self.env['info.knowledge.rating'].search_count([('article_id', '=', rat.id)])
            rat.rating_count = res or 0
    
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
    
    is_rating = fields.Boolean( default=False) 
    review_rating = fields.Integer(default=0)   
    
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
#         print("wwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwwww",self.env.user.id,self.id)
#         print("ddddddddddddddddddddddddddddddddddddd",self._context)
        rating_obj = self.env['info.knowledge.rating'].search([('user_id','=',self.env.user.id),('article_id','=',self.id)],limit=1)
        if rating_obj:
            self.is_rating = True
        else:
            self.is_rating = False
        print("QQQQQQQQQQQQQQQQQQQQQQQQ",self._context)
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
        print("aaaaaaaaaaaaaaa")
        for record in self:
            record.flag += 1
            context = dict(self.env.context or {})
#             context['abc_text']=''
            print("selfffffffffffffffffffffff111111111111",context)
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
            rating_obj = self.env['info.knowledge.rating'].search([('article_id','=',record.id)])
            a=0
            b=0
#             print("tttttttttttttttttt",rating_obj)
            for rating in rating_obj:
#                 print("1111111111111111111111",rating.rating_text)
                if rating.rating_text != '0':
                    a += int(rating.rating_text)
                    b +=1
            if b>0:
                record.review_rating = a/b
            else :
                record.review_rating = 0
            
#     
    published = fields.Date('Published')
    valid_to = fields.Date('Valid to')

    short_desc = fields.Char('Short description')
    article = fields.Html('Article body')
    article_text = fields.Text('Article text')
    
    workflow = fields.Selection([('draft', ' Draft'),('review', 'In Review'),('published', 'Published')], "Workflow", default='draft')
    link = fields.Binary('Attachment link', attachment=True)
    disp = fields.Boolean('Display attachments')  
    user_id = fields.Many2one('res.users','Owner', default=lambda self: self.env.user)
#     inspect_file = fields.Binary('Attachment', attachment=True)  

#     @api.onchange('knowledge_base_id')
#     def onchange_knowledge_base(self):
#         print("sssssssssssssssssssssssssssssssssssssssssssssssssss")


    @api.onchange('article')
    def get_article_text(self):
        if self.article:
            soup = BeautifulSoup(self.article)
            article = soup.get_text('\n')
            text = article
            a = 0
            for i in range(len(article)):
                if article[i] == "\n":
                    print("AaaaaaAAaAAaAAAAaAaaaaaAaAaAAAAAAAAAaaaAAAaaaaaAAaaaaAAaaaAAAaaaAAaaaAAaaaAAa")
                    print(a)
                    a +=1
                    if a > 3:
                        text =  article[0:i] +'............'
                        break
            self.article_text = text
#             with open(self.article, "r") as f:
#                 for line in f.readlines():
#                     print("!!!!!!!!!!!!!!!!!!!",line)
#          
        
        
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
    
    
