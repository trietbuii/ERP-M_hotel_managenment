# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HotelRoomType(models.Model):
    _name = 'hotel.room.type'
    _description = 'Hạng Phòng Khách Sạn'
    _order = 'base_price_night asc, name asc'

    name = fields.Char(string='Tên hạng phòng', required=True, translate=True)
    code = fields.Char(string='Mã hạng phòng', required=True, size=10)
    company_id = fields.Many2one('res.company', string='Cơ sở / Chi nhánh', default=lambda self: self.env.company)
    
    capacity = fields.Integer(string='Sức chứa chuẩn (người)', default=2, required=True)
    extra_capacity = fields.Integer(string='Sức chứa tối đa thêm (người)', default=1)
    bed_type = fields.Selection([
        ('single', '1 Giường đơn'),
        ('double', '1 Giường đôi lớn'),
        ('twin', '2 Giường đơn'),
        ('double_2', '2 Giường đôi'),
        ('triple', '3 Giường (đơn hoặc đôi)'),
        ('dorm', '6 Giường (đơn hoặc tầng)'),
        ('queen', '1 Giường Queen'),
        ('king', '1 Giường King'),
    ], string='Loại giường', default='double', required=True)
    
    base_price_night = fields.Float(string='Giá tiêu chuẩn theo đêm (VNĐ)', digits=(16, 0), required=True, default=500000.0)
    base_price_hour = fields.Float(string='Giá tiêu chuẩn theo giờ (VNĐ)', digits=(16, 0), required=True, default=150000.0)
    
    amenities = fields.Text(string='Tiện ích nổi bật')
    description = fields.Text(string='Mô tả chi tiết')
    active = fields.Boolean(string='Còn áp dụng', default=True)

    room_ids = fields.One2many('hotel.room', 'room_type_id', string='Danh sách phòng')
    room_count = fields.Integer(string='Số lượng phòng', compute='_compute_room_count', store=True)
    rate_ids = fields.One2many('hotel.room.rate', 'room_type_id', string='Bảng giá theo mùa')

    _code_company_uniq = models.Constraint(
        'unique(code, company_id)',
        'Mã hạng phòng phải là duy nhất cho mỗi chi nhánh!'
    )

    @api.depends('room_ids')
    def _compute_room_count(self):
        for record in self:
            record.room_count = len(record.room_ids)
