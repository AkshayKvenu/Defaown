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
#     manager = fields.Many2one('hr.employee','Manager')
    publish_workflow = fields.Selection([('instant', ' Knowledge instant publish'),
                                         ('approval', 'Knowledge approval publish')],
                                         "Publish Workflow")
    retir_flow = fields.Selection([('instant', ' Knowledge instant retire'),
                                   ('approval', 'Knowledge approval retire')],
                                    "Retire Workflow")
    is_active = fields.Boolean('Active')
    q_a = fields.Boolean('Enable social questions and answers')
    desc = fields.Text('Description')
    set_default = fields.Boolean('Set default knowledge field values')
    related_cmdb_ids = fields.Many2many('info.cmdb.classes',string='Related CI')
    knowledge_ids = fields.Many2many('info.knowledge.knowledge',string='Knowledge')
    category_ids = fields.Many2many('info.knowledge.category',string='Knowledge category')
    read_group_ids = fields.Many2many('res.groups', relation='read_group_id', string='Can read')
    contibute_groups_ids = fields.Many2many('res.groups', relation='contibute_groups_id', string='Can contribute')
    
    _sql_constraints = [
            ('title_uniq', 'unique(title)', 'Title must be unique per Base!'),
        ]
    
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
    
    
    
class InfoKnowledge(models.Model):
    _name = 'info.knowledge.knowledge'
    _rec_name = 'number'

    number = fields.Char('Number')
    state = fields.Selection([('draft', ' Draft'),
                              ('review', 'Review'),
                              ('published', 'Published'),
                              ('published', 'Published'),
                              ('retirement', 'Pending Retirement'),
                              ('retired', 'Retired')],
                              "State", default='draft')
    parent_id = fields.Many2one('info.knowledge.knowledge','Parent')
    knowledge_base = fields.Many2one('info.knowledge.base','Knowledge base')
    language_id = fields.Many2one('res.lang','Language')
        
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
#     inspect_file = fields.Binary('Attachment', attachment=True)  
    
    @api.model
    def create(self, vals):
        vals['number'] = self.env['ir.sequence'].next_by_code('info.knowledge.knowledge') or _('New')
        return super(InfoKnowledge, self).create(vals)
    
    

    
    
    
    
    
