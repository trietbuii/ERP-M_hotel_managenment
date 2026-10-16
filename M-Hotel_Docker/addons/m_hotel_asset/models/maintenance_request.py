# -*- coding: utf-8 -*-
from odoo import models, fields

class MaintenanceRequest(models.Model):
    _inherit = 'maintenance.request'

    room_id = fields.Many2one('hotel.room', string='Phòng phát sinh sự cố', index=True)
    incident_id = fields.Many2one('hotel.incident', string='Phiếu sự cố buồng phòng liên quan')
