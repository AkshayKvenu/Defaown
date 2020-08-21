# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CmdbGroup(models.Model):
    _name = 'info.cmdb.group'
    _rec_name = 'group_name'
#     _description = 'info_cmdb.info_cmdb'

    group_name = fields.Char("Group Name")
    ci_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    group_type = fields.Selection([('default', 'Default'), ('health', 'Health')], string="Group Type")
    configuration_item_id = fields.Many2one('info.cmdb.classes', string="Configuration item")
    
#     value = fields.Integer()
#     value2 = fields.Float(compute="_value_pc", store=True)
#     description = fields.Text()
#
#     @api.depends('value')
#     def _value_pc(self):
#         for record in self:
#             record.value2 = float(record.value) / 100
