# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserErro


class InfoKnowledgeTags(models.Model):
    _name = 'info.knowledge.tags'
    
    name = fields.Char('Name')