# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError


class InfoRatingWizard(models.Model):  
    _name = 'info.rating.wizard'

    rating_comments = fields.Text('Comment')    
#     rating_image = fields.Binary('Image', compute='_compute_rating_image')
    rating_text = fields.Selection([
        ('satisfied', 'Satisfied'),
        ('not_satisfied', 'Not satisfied'),
        ('highly_dissatisfied', 'Highly dissatisfied'),
        ('no_rating', 'No Rating yet')], string='Rating')
    
    
        
    def compute(self):
        active_id = self.env.context.get('active_id')
        print("AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",self.env.context.get('active_id'))
        rating_obj = self.env['info.knowledge.rating'].search([('user_id','=',self.env.user.id),('article_id','=',active_id)],limit=1)
        if rating_obj:
           rating_obj.rating_comment = self.rating_comments
           rating_obj.rating_text = self.rating_text 
        else:
            self.env['info.knowledge.rating'].create({
                                                    'rating_comment':self.rating_comments,
                                                    'rating_text': self.rating_text,
                                                    'article_id':active_id,
                                                    'user_id':self.env.user.id})