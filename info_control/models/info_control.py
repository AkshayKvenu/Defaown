# -*- coding: utf-8 -*-

from odoo import models, fields, api, _
from odoo.exceptions import UserError, ValidationError
 
 
class InfoStandard(models.Model):
    _name = 'info.control.standard'
#     _description = 'info_control.info_control'
#     info_control_standard_id = fields.Integer('id')

    name = fields.Char('Standard Name')
    code = fields.Char('Standard Code')
    version = fields.Char('Standard Version')
    date = fields.Date('Standard Date')
    overview = fields.Char('Standard Overview')
    purpose = fields.Char('Standard Purpose')
    family_ids = fields.One2many('info.control.standard.family','info_control_standard_id',string='Standard Family')
    control_ids = fields.One2many('info.control.control','info_control_standard_id',string='Standard Controls')
 
 
class InfoControlStandardFamily(models.Model):
    _name = 'info.control.standard.family'
    
    name = fields.Char('Member Name')
    code = fields.Char('Member Code')
    brief = fields.Char('Member Brief')
    scope = fields.Char('Member Scope')
    purpose = fields.Char('Member Purpose')
    info_control_standard_id = fields.Many2one('info.control.standard',string='Info Standard Id')
 
 
class InfoControlControl(models.Model):
    _name = 'info.control.control'
#     _rec_name = 'clause_ref'
    
    name = fields.Char('Control Name')
    clause_ref = fields.Char('Control Clause ID')
    clause = fields.Char('Control Clause')
    category_id = fields.Many2one('info.control.category',string='Control Category ID')
    category_objective = fields.Char('Control Category Objective')
    control_ref = fields.Char('Control ID')
    brief = fields.Text('Control Brief')
    implementation_guide = fields.Text('Control Implementation Guide')
    control_document = fields.Char('Control Document')
    
    control_type_ids = fields.Many2many('info.control.type',string='Control Types')
 
    is_impact_confidentiality = fields.Boolean('Impact Confidentiality?')
    is_impact_integrity = fields.Boolean('Impact Integrity?')
    is_impact_availability = fields.Boolean('Impact Availability?')
    
    info_control_standard_id = fields.Many2one('info.control.standard',string='Info Standard Id')
 
 
class InfoControlCategory(models.Model):
    _name = 'info.control.category'
#     _rec_name = 'clause_ref'
    
    name = fields.Char('Control Category Name')
    objective = fields.Char('Control Category Objective')
 
 
class InfoControlType(models.Model):
    _name = 'info.control.type'
#     _rec_name = 'clause_ref'
    
    name = fields.Char('Control Type Name')
#     objective = fields.Char('Control Category Objective')

    
    def unlink(self):
        for type in self:
            control_obj = self.env['info.control.control'].search([('control_type_ids','=',type.id)])
            if control_obj:
                raise UserError(_('You cannot delete a type that is already used.'))
        return super(InfoControlType, self).unlink()

    
    


