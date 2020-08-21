# -*- coding: utf-8 -*-
 
from odoo import models, fields, api, _


class AccountAsset(models.Model):
    _inherit = 'account.asset.asset'
    _rec_name = 'info_asset_name_seq'
    
    state = fields.Selection([('draft', 'Purchased'), ('open', 'In Use'), ('close', 'Disposed')], 'Status', required=True, copy=False, default='draft',
        help="When an asset is created, the status is 'Draft'.\n"
            "If the asset is confirmed, the status goes in 'Running' and the depreciation lines can be posted in the accounting.\n"
            "You can manually close an asset when the depreciation is over. If the last line of depreciation is posted, the asset automatically goes in that status.")
    
    info_asset_class = fields.Selection([
        ('devices', 'Devices'),
        ('software', 'Software Licenses'),
        ('site', 'Site'),
        ('department', 'Department'),
        ('employee', 'Employee'),
        ('business', 'Business Services'),
        ('information', 'Information'),
        ],string = "Asset class")
    info_asset_name_seq = fields.Char()
    info_asset_group_id = fields.Many2one('account.asset.group', string = "Asset Group")
    info_asset_classification_id = fields.Many2one('account.asset.classification', string = "Asset Classification")
#     info_asset_related_ci_ids = fields.One2many('account.asset.classification', string="Related CI")
    info_asset_account_cia_category_id = fields.Many2one('account.asset.cia.category', string = "Asset CIA Category")
    info_asset_personal_data = fields.Boolean(string = "Personal Data")
    info_asset_sensitive_data = fields.Boolean(string = "Sensitive Customer Data")
    info_asset_missing = fields.Boolean(string = "Missing")
    info_asset_managed_id = fields.Many2one('res.users', string = "Managed by")
    info_asset_owner_id = fields.Many2one('hr.employee', string = "Owned by")
    info_asset_drp_days = fields.Integer('Data Retention Period (Days)')
    
    
#     Cia valuation tab fields
    Info_asset_cia_confidentiality = fields.Integer('Confidentiality')
    Info_asset_cia_integrity = fields.Integer('Integrity')
    Info_asset_cia_availability = fields.Integer('Availability')
    info_asset_cia_total_value = fields.Integer('Total CIA Impact Value')
    
    @api.onchange('info_asset_account_cia_category_id')
    def onchange_cia_category(self):
        self.Info_asset_cia_confidentiality = self.info_asset_account_cia_category_id.info_asset_cia_confidentiality_id.info_asset_cia_impact_value
        self.Info_asset_cia_integrity = self.info_asset_account_cia_category_id.info_asset_cia_integrity_id.info_asset_cia_impact_value
        self.Info_asset_cia_availability = self.info_asset_account_cia_category_id.info_asset_cia_availability_id.info_asset_cia_impact_value
        self.info_asset_cia_total_value = self.info_asset_account_cia_category_id.info_asset_cia_total_value

    @api.model
    def create(self, vals):
        vals['info_asset_name_seq'] = self.env['ir.sequence'].next_by_code('account.asset.asset') or _('New')
        if 'info_asset_account_cia_category_id' in vals and vals['info_asset_account_cia_category_id']:
            cia_category_obj = self.env['account.asset.cia.category'].browse(vals['info_asset_account_cia_category_id'])
            vals['Info_asset_cia_confidentiality'] = cia_category_obj.info_asset_cia_confidentiality_id.info_asset_cia_impact_value
            vals['Info_asset_cia_integrity'] = cia_category_obj.info_asset_cia_integrity_id.info_asset_cia_impact_value
            vals['Info_asset_cia_availability'] = cia_category_obj.info_asset_cia_availability_id.info_asset_cia_impact_value
            vals['info_asset_cia_total_value'] = cia_category_obj.info_asset_cia_total_value
        return super(AccountAsset, self).create(vals)

    def write(self, vals):
        if 'info_asset_account_cia_category_id' in vals and vals['info_asset_account_cia_category_id']:
            cia_category_obj = self.env['account.asset.cia.category'].browse(vals['info_asset_account_cia_category_id'])
            vals['Info_asset_cia_confidentiality'] = cia_category_obj.info_asset_cia_confidentiality_id.info_asset_cia_impact_value
            vals['Info_asset_cia_integrity'] = cia_category_obj.info_asset_cia_integrity_id.info_asset_cia_impact_value
            vals['Info_asset_cia_availability'] = cia_category_obj.info_asset_cia_availability_id.info_asset_cia_impact_value
            vals['info_asset_cia_total_value'] = cia_category_obj.info_asset_cia_total_value
        return super(AccountAsset, self).write(vals)
        
    
