# -*- coding: utf-8 -*-
from odoo import models, fields

class MaintenanceEquipment(models.Model):
    _inherit = 'maintenance.equipment'

    room_id = fields.Many2one('hotel.room', string='Phòng đặt thiết bị', index=True,
                              help='Phòng khách sạn được trang bị thiết bị này')
