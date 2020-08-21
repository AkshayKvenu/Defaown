# -*- coding: utf-8 -*-

from odoo import models, fields, api, _


class InfoCmdbDevices(models.Model):
    _name = 'info.cmdb.devices'
    _rec_name = 'ci_device_hostname'
#     _description = 'info_cmdb.info_cmdb'

#     image_1920 = fields.Image("Image", compute='_compute_image_1920', inverse='_set_image_1920')
    ci_image_medium = fields.Image()
    ci_device_asset_ok = fields.Boolean("Is it an Asset?", default=True)
    ci_device_class = fields.Many2one('info.cmdb.classes', string="CI Class")
    ci_device_hostname = fields.Char('Host Name')
    ci_device_sys_name = fields.Char('Sys Name')
    state = fields.Selection([('in_use', ' in Use'),('in_repair', 'in Repair'),('retired', 'Retired')], "State", default='in_use')
#     General Informations tab
    ci_device_group_id = fields.Many2one('info.cmdb.group', string="CI Group")
    ci_location_id = fields.Many2one('stock.location', string="Location")
    ci_device_sys_descr = fields.Text('System Description')
    ci_device_hardware = fields.Text('Vendor/Hardware')
    ci_device_serial = fields.Text('Serial')
    ci_device_type = fields.Text('Type')
    ci_device_os = fields.Char('Operating System')
    ci_device_version = fields.Char('Version')
#     Discovery Probe Tab
    ci_device_last_discovered = fields.Date('Last Discovered')
    ci_device_last_pinged = fields.Date('Last Pinged')
    ci_device_last_polled = fields.Date('Last Pooled')
    
    def action_repair(self):
        self.write({"state":'in_repair'})
        
    def action_retire(self): 
        self.write({"state":'retired'})
        
    def action_in_use(self):   
        self.write({"state":'in_use'})
    
    applications_count = fields.Integer("Applications", compute='compute_applications_count')
    def compute_applications_count(self):
        for rec in self:
            res = self.env['info.cmdb.applications'].search_count([('ci_device_id', '=', rec.id)])
            rec.applications_count = res or 0
    
    vm_count = fields.Integer("VM", compute='compute_vm_count')
    def compute_vm_count(self):
        for rec in self:
            res = self.env['info.cmdb.vm'].search_count([('ci_device_id', '=', rec.id)])
            rec.vm_count = res or 0
    
    processors_count = fields.Integer("Processors", compute='compute_processors_count')
    def compute_processors_count(self):
        for rec in self:
            res = self.env['info.cmdb.processors'].search_count([('ci_device_id', '=', rec.id)])
            rec.processors_count = res or 0
    
    memory_count = fields.Integer("Memory", compute='compute_memory_count')
    def compute_memory_count(self):
        for rec in self:
            res = self.env['info.cmdb.memory'].search_count([('ci_device_id', '=', rec.id)])
            rec.memory_count = res or 0
    
    storages_count = fields.Integer("Storages", compute='compute_storages_count')
    def compute_storages_count(self):
        for rec in self:
            res = self.env['info.cmdb.storages'].search_count([('ci_device_id', '=', rec.id)])
            rec.storages_count = res or 0
    
    sensors_count = fields.Integer("Sensors", compute='compute_sensors_count')
    def compute_sensors_count(self):
        for rec in self:
            res = self.env['info.cmdb.sensors'].search_count([('ci_device_id', '=', rec.id)])
            rec.sensors_count = res or 0
    
    vlans_count = fields.Integer("Vlans", compute='compute_vlans_count')
    def compute_vlans_count(self):
        for rec in self:
            res = self.env['info.cmdb.vlans'].search_count([('ci_device_id', '=', rec.id)])
            rec.vlans_count = res or 0
    
    
    interfaces_count = fields.Integer("Interfaces", compute='compute_interfaces_count')
    def compute_interfaces_count(self):
        for rec in self:
            res = self.env['info.cmdb.interfaces'].search_count([('ci_device_id', '=', rec.id)])
            rec.interfaces_count = res or 0

    def open_applications(self):
        context = dict(self.env.context or {})
        context['default_ci_device_id'] = self.id
        return {
            'name': _('Applications'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.cmdb.applications',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('ci_device_id', '=', self.id)],
                }

    def open_vm(self):
        context = dict(self.env.context or {})
        context['default_ci_device_id'] = self.id
        return {
            'name': _('VM'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.cmdb.vm',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('ci_device_id', '=', self.id)],
                }

    def open_processors(self):
        context = dict(self.env.context or {})
        context['default_ci_device_id'] = self.id
        return {
            'name': _('Processors'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.cmdb.processors',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('ci_device_id', '=', self.id)],
                }

    def open_memory(self):
        context = dict(self.env.context or {})
        context['default_ci_device_id'] = self.id
        return {
            'name': _('Memory'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.cmdb.memory',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('ci_device_id', '=', self.id)],
                }

    def open_storages(self):
        context = dict(self.env.context or {})
        context['default_ci_device_id'] = self.id
        return {
            'name': _('Storages'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.cmdb.storages',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('ci_device_id', '=', self.id)],
                }

    def open_sensors(self):
        context = dict(self.env.context or {})
        context['default_ci_device_id'] = self.id
        return {
            'name': _('Sensors'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.cmdb.sensors',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('ci_device_id', '=', self.id)],
                }

    def open_vlans(self):
        context = dict(self.env.context or {})
        context['default_ci_device_id'] = self.id
        return {
            'name': _('Vlans'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.cmdb.vlans',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('ci_device_id', '=', self.id)],
                }

    def open_interfaces(self):
        context = dict(self.env.context or {})
        context['default_ci_device_id'] = self.id
        return {
            'name': _('Interfaces'),
            'view_type': 'form',
            'view_mode': 'tree,form',
            'res_model': 'info.cmdb.interfaces',
            'view_id': False,
            'type': 'ir.actions.act_window',
            'context': context,
            'domain': [('ci_device_id', '=', self.id)],
                }
        