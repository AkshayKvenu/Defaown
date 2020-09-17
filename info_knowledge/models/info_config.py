# -*- coding: utf-8 -*-


from odoo import models, fields, api, _
from odoo.exceptions import UserError


class InfoKnowledgeTags(models.Model):
    _name = 'info.knowledge.tags'
    
    name = fields.Char('Name')