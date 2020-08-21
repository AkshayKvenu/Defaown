# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CmdbBusinessServices(models.Model):
    _name = 'info.cmdb.business.services'
#     _rec_name = 'group_name'
#     _description = 'info_cmdb.info_cmdb'

    name = fields.Char('Name')
    ci_business_services_class_id = fields.Many2one('info.cmdb.classes', string="CI Class")
    business_critical = fields.Selection([('1', 'most critical'),
                                           ('2', 'somewhat critical'),
                                           ('3', 'less critical'),
                                           ('4', 'not critical)')],
                                         string="Business Criticality")
    used_for = fields.Selection([('production', 'Production'),
                                           ('staging', 'Staging'),
                                           ('qa', 'QA'),
                                           ('test', 'Test'),
                                           ('development', 'Development'),
                                           ('demonstration', 'Demonstration'),
                                           ('training', 'Training'),
                                           ('disaster', 'Disaster Recovery')],
                                         string="Used for")
    service_classification = fields.Selection([('business', 'Business Service'),
                                           ('technical', 'Technical Service'),
                                           ('application', 'Application Service')],
                                         string="Service classification")
#     ci_soft_licenses_contract_no = fields.Many2one('contract.contract', string="Contract Number")
    ci_soft_licenses_business_owener_id = fields.Many2one('hr.employee', string="Business Owne")
    ci_soft_licenses_description = fields.Char("Description")
    ci_soft_licenses_key = fields.Char("License Key")