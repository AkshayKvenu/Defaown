# -*- coding: utf-8 -*-
 
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class AccountGroup(models.Model):
    _name = 'account.asset.group'
    
    name = fields.Char(string = "Name")
    description = fields.Char(string = "Description")


class AccountClassification(models.Model):
    _name = 'account.asset.classification'
    
    name = fields.Char(string = "Name")
    sensitivity = fields.Char(string = "Sensitivity")
    guide_lines = fields.Text(string = "Guide Lines")
    

class AccountCiaCategory(models.Model):
    _name = 'account.asset.cia.category'
    
    name = fields.Char(string="Asset CIA Category Name")
    info_asset_cia_confidentiality_id = fields.Many2one('account.asset.cia.impact', string="Confidentiality")
    info_asset_cia_integrity_id = fields.Many2one('account.asset.cia.impact', string="Integrity")
    info_asset_cia_availability_id = fields.Many2one('account.asset.cia.impact', string="Availability")
    info_asset_cia_total_value = fields.Integer(string="Total CIA Impact Value")
    
    @api.model
    def create(self,vals):
        line = super(AccountCiaCategory, self).create(vals)
        line.info_asset_cia_total_value = line.info_asset_cia_confidentiality_id.info_asset_cia_impact_value + line.info_asset_cia_integrity_id.info_asset_cia_impact_value + line.info_asset_cia_availability_id.info_asset_cia_impact_value
        return line
    
    @api.onchange('info_asset_cia_confidentiality_id', 'info_asset_cia_integrity_id','info_asset_cia_availability_id')
    def onchange_total_value_compute(self):
        self.info_asset_cia_total_value = self.info_asset_cia_confidentiality_id.info_asset_cia_impact_value + self.info_asset_cia_integrity_id.info_asset_cia_impact_value + self.info_asset_cia_availability_id.info_asset_cia_impact_value
    
    def write(self, vals):
        impact_obj = self.env['account.asset.cia.impact']
        confidentiality = impact_obj.browse(vals['info_asset_cia_confidentiality_id']) if 'info_asset_cia_confidentiality_id' in vals and vals['info_asset_cia_confidentiality_id'] else self.info_asset_cia_confidentiality_id
        integrity = impact_obj.browse(vals['info_asset_cia_integrity_id']) if 'info_asset_cia_integrity_id' in vals and vals['info_asset_cia_integrity_id'] else self.info_asset_cia_integrity_id
        availability = impact_obj.browse(vals['info_asset_cia_availability_id']) if 'info_asset_cia_availability_id' in vals and vals['info_asset_cia_availability_id'] else self.info_asset_cia_availability_id
        vals['info_asset_cia_total_value'] = confidentiality.info_asset_cia_impact_value + integrity.info_asset_cia_impact_value + availability.info_asset_cia_impact_value
        res = super(AccountCiaCategory, self).write(vals)
        return res
    
    

class AccountCiaImpact(models.Model):
    _name = 'account.asset.cia.impact'
    _rec_name = 'info_asset_cia_impact_rate'
    
    name = fields.Char()
    info_asset_cia_impact_rate = fields.Char(string = "Name")
    info_asset_cia_impact_value = fields.Integer(string = "Value")
    info_asset_cia_impact_label  = fields.Char(string = "Label")
    
    @api.constrains('info_asset_cia_impact_rate', 'info_asset_cia_impact_label')
    def name_label_validation(self):
        cia_name_obj = self.search([('info_asset_cia_impact_rate', '=', self.info_asset_cia_impact_rate),('id', '!=', self.id)])
        cia_label_obj = self.search([('info_asset_cia_impact_label', '=', self.info_asset_cia_impact_label),('id', '!=', self.id)])
        if cia_name_obj:
            raise UserError(_("Name cannot be duplicated."))
            
        if cia_label_obj:
            raise UserError(_("label cannot be duplicated."))
        
    @api.constrains('info_asset_cia_impact_value')
    def name_label_validation(self):
        if self.info_asset_cia_impact_value <= 0:
            raise UserError(_("Value should be greater than zero."))
            
    
    @api.model
    def create(self, vals):
        vals['name'] = vals['info_asset_cia_impact_rate']+"["+vals['info_asset_cia_impact_label']+"]"
        return super(AccountCiaImpact, self).create(vals)
        
    
    
    
    