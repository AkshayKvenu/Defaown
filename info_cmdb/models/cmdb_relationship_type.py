# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CmdbRelationshipClass(models.Model):
    _name = 'info.cmdb.relationship.type'
    _rec_name = 'relationship'
#     _description = 'info_cmdb.info_cmdb'

    relationship = fields.Char("Name")
    parent_descriptor = fields.Char("Parent Descriptor")
    child_descriptor = fields.Char("Child Descriptor")
    
    @api.onchange('parent_descriptor','child_descriptor')
    def onchange_relationship_(self):
        if self.parent_descriptor and self.child_descriptor:
            self.relationship = self.child_descriptor+"::"+self.parent_descriptor
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
