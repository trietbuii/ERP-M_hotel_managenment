# -*- coding: utf-8 -*-
from odoo import models

class HotelBooking(models.Model):
    _inherit = 'hotel.booking'

    def _auto_create_housekeeping_task(self):
        """Tự động sinh nhiệm vụ dọn phòng khi trả phòng"""
        for rec in self:
            self.env['hotel.housekeeping.task'].create({
                'room_id': rec.room_id.id,
                'task_type': 'checkout_clean',
                'booking_id': rec.id,
                'priority': '2',
                'notes': f"Dọn buồng phòng sau khi khách {rec.partner_id.name} làm thủ tục trả phòng (Đơn {rec.name})."
            })
