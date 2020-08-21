# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CmdbClassCategory(models.Model):
    _name = 'info.cmdb.classes'
    _rec_name = 'class_name'
#     _description = 'info_cmdb.info_cmdb'

    class_name = fields.Char("Class Name")
    class_id = fields.Selection([('devices', 'Devices'),
                ('software', 'Software Licenses'),
                ('company', 'Company'),
                ('site', 'Site'),
                ('department', 'Department'),
                ('cmployee', 'Employee'),
                ('contacts', 'Contacts'),
                ('working_schedule', 'Working Schedule'),
                ('business', 'Business Services')],
                "CI Class ID")
    description = fields.Char("Description")
    icon = fields.Image("Icon")
    class_recommended_fields = fields.Char("Recommended Fields")
    
#  ......   Completeness tab .....
#     class_recommended_fields = fields.Many2one('info.cmdb.classes', string="Recommended Fields")
    
#  .......   Correctness tab .....
    class_orphan_relationship_types = fields.Many2many('info.cmdb.relationship.class',relation = 'relation_type', string="Orphan Relationship Rules")
#     class_staleness_effective_duration = fields.Many2one('info.cmdb.classes', string="Staleness Rule")

#   .......  Suggested Relationships .....
    class_suggested_relationships = fields.Many2many('info.cmdb.relationship.class',relation = 'base_class', string="Suggested Relationships")
#     
#     
# #   .......  Dependent Relationships .....
    class_dependent_relationships = fields.Many2many('info.cmdb.relationship.class',relation = 'dependent_class', string="Dependent Relationships")

    
    @api.onchange('class_id')
    def onchange_class_name(self):
        self.class_name = dict(self._fields['class_id'].selection).get(self.class_id)
        
    @api.model
    def create(self, vals):
        if 'class_id' in vals and vals['class_id']:
            vals['class_name'] = dict(self._fields['class_id'].selection).get(vals['class_id'])
        return super(CmdbClassCategory, self).create(vals)

    def write(self, vals):
        if 'class_id' in vals and vals['class_id']:
            vals['class_name'] = dict(self._fields['class_id'].selection).get(vals['class_id'])
        return super(CmdbClassCategory, self).write(vals)
        
    


