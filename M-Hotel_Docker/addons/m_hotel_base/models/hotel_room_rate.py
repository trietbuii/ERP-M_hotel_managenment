# -*- coding: utf-8 -*-
from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HotelRoomRate(models.Model):
    _name = 'hotel.room.rate'
    _description = 'Bảng Giá Phòng Theo Mùa & Dịp Lễ'
    _order = 'start_date desc, name asc'

    name = fields.Char(string='Tên biểu giá', required=True)
    room_type_id = fields.Many2one('hotel.room.type', string='Hạng phòng', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Cơ sở', default=lambda self: self.env.company)
    
    rate_type = fields.Selection([
        ('season', 'Mùa cao điểm / Lễ hội'),
        ('weekend', 'Cuối tuần (Thứ 6 - CN)'),
        ('holiday', 'Dịp Lễ / Tết'),
        ('promo', 'Chương trình khuyến mãi'),
    ], string='Phân loại biểu giá', default='season', required=True)

    start_date = fields.Date(string='Ngày bắt đầu', required=True)
    end_date = fields.Date(string='Ngày kết thúc', required=True)

    price_night = fields.Float(string='Giá thuê theo đêm (VNĐ)', required=True, digits=(16, 0))
    price_hour = fields.Float(string='Giá thuê theo giờ (VNĐ)', required=True, digits=(16, 0))
    active = fields.Boolean(string='Kích hoạt', default=True)

    @api.constrains('start_date', 'end_date')
    def _check_dates(self):
        for rec in self:
            if rec.start_date and rec.end_date and rec.start_date > rec.end_date:
                raise ValidationError("Ngày bắt đầu không được lớn hơn ngày kết thúc!")
