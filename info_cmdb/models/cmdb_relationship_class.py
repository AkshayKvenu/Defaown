# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CmdbRelationshipClass(models.Model):
    _name = 'info.cmdb.relationship.class'
    _rec_name = 'base_class'
#     _description = 'info_cmdb.info_cmdb'
# 
    base_class = fields.Many2one('info.cmdb.classes', string="Base Class")
    relation_type = fields.Many2one('info.cmdb.classes', string="Relationship Type")
    dependent_class = fields.Many2one('info.cmdb.classes', string="Dependent Class")
#     group_type = fields.Selection([('default', 'Default'), ('health', 'Health')],"Group Type")
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
