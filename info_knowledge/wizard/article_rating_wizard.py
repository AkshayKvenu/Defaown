# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError

AVAILABLE_PRIORITIES = [
    ('0', 'No Rating yet'),
    ('1', 'Highly dissatisfied'),
    ('2', 'dissatisfied'),
    ('3', 'Not satisfied'),
    ('4', 'Satisfied'),
    ('5', 'Highly Satisfied'),
]



class InfoRatingWizard(models.Model):  
    _name = 'info.rating.wizard'


    def compute_rating_(self):
        active_id = self.env.context.get('active_id')
        rating_obj = self.env['info.knowledge.rating'].search([('user_id','=',self.env.user.id),('article_id','=',active_id)],limit=1)
        return rating_obj or False
        
    def compute_comment(self):
        rating = self.compute_rating_()
        if rating:
            return rating.rating_comment
        else:
            return False
    
    def compute_text(self):
        rating = self.compute_rating_()
        if rating:
            return rating.rating_text
        else:
            return False
        
    rating_comments = fields.Text('Comment',default=compute_comment)    
#     rating_image = fields.Binary('Image', compute='_compute_rating_image')
#     priority = fields.Selection(AVAILABLE_PRIORITIES, string='Priority', index=True, default=AVAILABLE_PRIORITIES[0][0])
    rating_text = fields.Selection( AVAILABLE_PRIORITIES, string='Rating',default=compute_text)
    
    
        
    def compute(self):
        rating_obj = self.compute_rating_()
        if rating_obj:
           rating_obj.rating_comment = self.rating_comments
           rating_obj.rating_text = self.rating_text 
        else:
            self.env['info.knowledge.rating'].create({
                                                    'rating_comment':self.rating_comments,
                                                    'rating_text': self.rating_text,
                                                    'article_id':self.env.context.get('active_id'),
                                                    'user_id':self.env.user.id})