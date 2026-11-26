# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    room_id = fields.Many2one('hotel.room', string='Phòng phát sinh sự cố', index=True)
    incident_id = fields.Many2one('hotel.incident', string='Phiếu sự cố buồng phòng liên quan')

    @api.onchange('equipment_id')
    def _onchange_equipment_id_room(self):
        if self.equipment_id and self.equipment_id.room_id:
            self.room_id = self.equipment_id.room_id
            self.company_id = self.equipment_id.room_id.company_id

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('equipment_id') and not vals.get('room_id'):
                equip = self.env['maintenance.equipment'].browse(vals['equipment_id'])
                if equip.room_id:
                    vals['room_id'] = equip.room_id.id
                    vals.setdefault('company_id', equip.room_id.company_id.id)
        return super().create(vals_list)
