# -*- coding: utf-8 -*-
from odoo import models, fields

class MHotelRoomType(models.Model):
    _name = 'm.hotel.room.type'
    _description = 'Hạng phòng khách sạn M-Hotel'
    _order = 'price_night asc'

    name = fields.Char(string='Tên hạng phòng', required=True)
    code = fields.Char(string='Mã hạng phòng', required=True)
    price_night = fields.Float(string='Đơn giá theo đêm (VNĐ)', required=True, default=800000.0)
    price_hour = fields.Float(string='Đơn giá theo giờ (VNĐ)', required=True, default=200000.0)
    capacity = fields.Integer(string='Sức chứa tối đa (người)', default=2)
    bed_count = fields.Integer(string='Số giường ngủ', default=1)
    description = fields.Text(string='Mô tả tiện nghi')
    amenities = fields.Char(string='Tiện ích (Wifi, Ban công, Tivi 4K...)')
    active = fields.Boolean(string='Hoạt động', default=True)
    room_ids = fields.One2many('m.hotel.room', 'room_type_id', string='Các phòng thuộc hạng')
