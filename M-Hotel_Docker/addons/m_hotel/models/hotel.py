# -*- coding: utf-8 -*-
from odoo import models, fields

class MHotel(models.Model):
    _name = 'm.hotel'
    _description = 'Cơ sở khách sạn M-Hotel'
    _order = 'name asc'

    name = fields.Char(string='Tên khách sạn / Chi nhánh', required=True)
    code = fields.Char(string='Mã cơ sở', required=True)
    address = fields.Text(string='Địa chỉ')
    phone = fields.Char(string='Số điện thoại hotline')
    email = fields.Char(string='Email liên hệ')
    active = fields.Boolean(string='Hoạt động', default=True)
    room_ids = fields.One2many('m.hotel.room', 'hotel_id', string='Danh sách phòng')
    room_count = fields.Integer(string='Tổng số phòng', compute='_compute_room_count')

    def _compute_room_count(self):
        for record in self:
            record.room_count = len(record.room_ids)
