# -*- coding: utf-8 -*-
from odoo import models, fields, _

class HotelRoom(models.Model):
    _inherit = 'hotel.room'

    equipment_ids = fields.One2many('maintenance.equipment', 'room_id', string='Thiết bị trong phòng')
    equipment_count = fields.Integer(string='Số lượng thiết bị', compute='_compute_maintenance_counts')
    
    maintenance_ids = fields.One2many('maintenance.request', 'room_id', string='Lịch sử bảo trì')
    maintenance_count = fields.Integer(string='Số lần bảo trì', compute='_compute_maintenance_counts')

    def _compute_maintenance_counts(self):
        for rec in self:
            rec.equipment_count = len(rec.equipment_ids)
            rec.maintenance_count = len(rec.maintenance_ids)

    def action_view_equipments(self):
        self.ensure_one()
        return {
            'name': _('Thiết Bị Phòng %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.equipment',
            'view_mode': 'kanban,list,form',
            'domain': [('room_id', '=', self.id)],
            'context': {'default_room_id': self.id},
        }

    def action_view_maintenances(self):
        self.ensure_one()
        return {
            'name': _('Yêu Cầu Sửa Chữa Phòng %s') % self.name,
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'view_mode': 'kanban,list,form',
            'domain': [('room_id', '=', self.id)],
            'context': {'default_room_id': self.id},
        }
