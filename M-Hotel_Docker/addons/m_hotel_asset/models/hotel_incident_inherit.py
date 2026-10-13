# -*- coding: utf-8 -*-
from odoo import models, fields, _

class HotelIncident(models.Model):
    _inherit = 'hotel.incident'

    maintenance_request_id = fields.Many2one('maintenance.request', string='Phiếu bảo trì Kỹ thuật', readonly=True)

    def action_create_maintenance_request(self):
        """Chuyển giao sự cố sang phân hệ Bảo trì (Maintenance)"""
        self.ensure_one()
        if self.maintenance_request_id:
            return self.action_view_maintenance_request()

        m_request = self.env['maintenance.request'].create({
            'name': f"[{self.room_id.name}] {self.title}",
            'room_id': self.room_id.id,
            'incident_id': self.id,
            'description': self.description or self.title,
            'priority': '3' if self.severity == 'critical' else ('2' if self.severity == 'medium' else '1'),
        })
        self.maintenance_request_id = m_request.id
        self.state = 'in_progress'
        return self.action_view_maintenance_request()

    def action_view_maintenance_request(self):
        self.ensure_one()
        return {
            'name': _('Phiếu Bảo Trì Kỹ Thuật'),
            'type': 'ir.actions.act_window',
            'res_model': 'maintenance.request',
            'view_mode': 'form',
            'res_id': self.maintenance_request_id.id,
            'target': 'current',
        }
