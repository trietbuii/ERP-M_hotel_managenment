# -*- coding: utf-8 -*-
from odoo import models, fields, api

class MHotelRoom(models.Model):
    _name = 'm.hotel.room'
    _description = 'Phòng nghỉ khách sạn M-Hotel'
    _order = 'name asc'

    name = fields.Char(string='Số phòng', required=True)
    hotel_id = fields.Many2one('m.hotel', string='Cơ sở / Chi nhánh', required=True)
    room_type_id = fields.Many2one('m.hotel.room.type', string='Hạng phòng', required=True)
    floor = fields.Integer(string='Tầng', default=1)
    status = fields.Selection([
        ('available', 'Trống / Sẵn sàng'),
        ('confirmed', 'Đã đặt trước'),
        ('occupied', 'Đang lưu trú'),
        ('cleaning', 'Chờ dọn dẹp'),
        ('maintenance', 'Đang bảo trì')
    ], string='Trạng thái vận hành', default='available')
    
    price_night = fields.Float(related='room_type_id.price_night', string='Giá đêm (VNĐ)', store=True)
    price_hour = fields.Float(related='room_type_id.price_hour', string='Giá giờ (VNĐ)', store=True)
    capacity = fields.Integer(related='room_type_id.capacity', string='Sức chứa', store=True)
    
    booking_ids = fields.One2many('m.hotel.booking', 'room_id', string='Lịch đặt phòng')
    service_request_ids = fields.One2many('m.hotel.service.request', 'room_id', string='Lịch sử sự vụ / bảo trì')
    current_guest = fields.Char(string='Khách đang ở', compute='_compute_current_guest')
    active = fields.Boolean(string='Hoạt động', default=True)

    def _compute_current_guest(self):
        for room in self:
            current_booking = self.env['m.hotel.booking'].search([
                ('room_id', '=', room.id),
                ('status', '=', 'occupied')
            ], limit=1)
            room.current_guest = current_booking.partner_id.name if current_booking else False
