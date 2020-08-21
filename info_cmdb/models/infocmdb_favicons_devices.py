# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class CmdbApplications(models.Model):
    _name = 'info.cmdb.applications'
    _rec_name = 'ci_device_id'
#     _description = 'info_cmdb.info_cmdb'

    ci_device_id = fields.Many2one('info.cmdb.devices', string="Device ID")
    ci_application_id = fields.Integer('Application ID')
#     ci_application_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_application_type = fields.Char('Application Type')
    ci_application_state = fields.Char('Application State')
    ci_application_status = fields.Char('Application Status')
    ci_application_instance = fields.Char('Application Instance')
    
    
class CmdbVM(models.Model):
    _name = 'info.cmdb.vm'
    _rec_name = 'ci_device_id'
#     _description = 'info_cmdb.info_cmdb'

    ci_device_id = fields.Many2one('info.cmdb.devices', string="Device ID")
    ci_vm_id = fields.Integer('VM ID')
#     ci_application_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_vm_type = fields.Char('VM Type')
    ci_vm_display_name = fields.Char('VM Display Name')
    ci_vm_guest_os = fields.Char('VM Guest OS')
    ci_vm_memory_size = fields.Integer('VM Memory Size')
    ci_vm_cpu = fields.Integer('VM CPU')
    
#     
class CmdbProcessors(models.Model):
    _name = 'info.cmdb.processors'
#     _rec_name = 'ci_device_id'
#     _description = 'info_cmdb.info_cmdb'
 
    ci_device_id = fields.Many2one('info.cmdb.devices', string="Device ID")
    ci_processors_id = fields.Integer('Processor ID')
#     ci_application_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_processors_index = fields.Char('Processor Index')
    ci_processors_descr = fields.Char('Processor Description')
    
#     
class CmdbMemory(models.Model):
    _name = 'info.cmdb.memory'
#     _rec_name = 'ci_device_id'
#     _description = 'info_cmdb.info_cmdb'
 
    ci_device_id = fields.Many2one('info.cmdb.devices', string="Device ID")
    ci_memory_id = fields.Integer('Memory ID')
#     ci_application_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_mempool_index = fields.Char('Memory Index')
    ci_mempool_descr = fields.Char('Memory Description')
    ci_mempool_total = fields.Char('Memory Total')
    
    
#     
class CmdbStorages(models.Model):
    _name = 'info.cmdb.storages'
    _rec_name = 'ci_device_id'
#     _description = 'info_cmdb.info_cmdb'
 
    ci_device_id = fields.Many2one('info.cmdb.devices', string="Device ID")
    ci_storages_id = fields.Integer('Storage ID')
#     ci_application_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_storages_index = fields.Char('Storage Index')
    ci_storages_type = fields.Char('Storage Type')
    ci_storages_descr = fields.Char('Storage Description')
    ci_storages_size = fields.Char('Storage Size')
    
#     
class CmdbSensors(models.Model):
    _name = 'info.cmdb.sensors'
    _rec_name = 'ci_device_id'
#     _description = 'info_cmdb.info_cmdb'
 
    ci_device_id = fields.Many2one('info.cmdb.devices', string="Device ID")
    ci_sensors_id = fields.Integer('Sensor ID')
#     ci_application_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_sensors_class = fields.Char('Sensor Class')
    ci_sensors_index = fields.Char('Sensor Index')
    ci_sensors_type = fields.Char('Sensor Type')
    
# #     
class CmdbVlans(models.Model):
    _name = 'info.cmdb.vlans'
    _rec_name = 'ci_device_id'
#     _description = 'info_cmdb.info_cmdb'
  
    ci_device_id = fields.Many2one('info.cmdb.devices', string="Device ID")
    ci_vlans_id = fields.Integer('VLAN ID')
#     ci_application_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_vlans_vlan = fields.Char('VLAN')
    ci_vlans_domain = fields.Char('VLAN Domain')
    ci_vlans_name = fields.Char('VLAN Name')
    ci_vlans_type = fields.Char('VLAN Type')
    
# #     
class CmdbInterfaces(models.Model):
    _name = 'info.cmdb.interfaces'
    _rec_name = 'ci_device_id'
#     _description = 'info_cmdb.info_cmdb'
  
    ci_device_id = fields.Many2one('info.cmdb.devices', string="Device ID")
    ci_interfaces_id = fields.Integer('Interface ID')
#     ci_application_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_interfaces_name = fields.Char('Interface Name')
    ci_interfaces_descr = fields.Char('Interface Description')
    ci_interfaces_index = fields.Integer('Interface index')
    ci_interfaces_type = fields.Char('Interface Type')
    ci_interfaces_phys_address = fields.Char('Interface Physical Address')
    
    
