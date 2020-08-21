# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CmdbSoftwateLicense(models.Model):
    _name = 'info.cmdb.software.licenses'
#     _rec_name = 'group_name'
#     _description = 'info_cmdb.info_cmdb'

    name = fields.Char('Software Licenses')
    ci_class_id = fields.Many2one('info.cmdb.classes', string="CI Class")
#     ci_soft_licenses_contract_no = fields.Many2one('contract.contract', string="Contract Number")
    ci_soft_licenses_business_owener_id = fields.Many2one('hr.employee', string="Business Owne")
    ci_soft_licenses_description = fields.Char("Description")
    ci_soft_licenses_key = fields.Char("License Key")