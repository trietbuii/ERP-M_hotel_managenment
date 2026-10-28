# -*- coding: utf-8 -*-
from odoo import models, fields, api

class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Phòng Khách Sạn'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'company_id asc, floor asc, name asc'

    name = fields.Char(string='Số phòng', required=True, tracking=True)
    floor = fields.Char(string='Tầng', required=True, default='Tầng 1')
    room_type_id = fields.Many2one('hotel.room.type', string='Hạng phòng', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Cơ sở / Chi nhánh', default=lambda self: self.env.company, required=True)
    
    status = fields.Selection([
        ('available', 'Sẵn sàng'),
        ('reserved', 'Đã đặt trước'),
        ('occupied', 'Đang có khách'),
        ('cleaning', 'Cần dọn dẹp'),
        ('maintenance', 'Bảo trì / Sửa chữa'),
        ('out_of_service', 'Khóa tạm thời'),
    ], string='Trạng thái phòng', default='available', tracking=True, required=True)

    current_guest = fields.Char(string='Khách lưu trú hiện tại', tracking=True)
    
    price_night = fields.Float(string='Giá theo đêm (VNĐ)', digits=(16, 0), related='room_type_id.base_price_night', readonly=False, store=True)
    price_hour = fields.Float(string='Giá theo giờ (VNĐ)', digits=(16, 0), related='room_type_id.base_price_hour', readonly=False, store=True)
    
    note = fields.Text(string='Ghi chú đặc biệt')
    color = fields.Integer(string='Color Index', compute='_compute_color')
    active = fields.Boolean(string='Còn sử dụng', default=True)

    _name_company_uniq = models.Constraint(
        'unique(name, company_id)',
        'Số phòng phải là duy nhất tại mỗi cơ sở / chi nhánh!'
    )

    @api.depends('status')
    def _compute_color(self):
        color_map = {
            'available': 10,       # Green
            'reserved': 3,         # Yellow/Orange
            'occupied': 1,         # Red
            'cleaning': 4,         # Blue
            'maintenance': 2,      # Orange/Brown
            'out_of_service': 8,   # Dark/Gray
        }
        for rec in self:
            rec.color = color_map.get(rec.status, 0)

    def action_set_available(self):
        self.write({'status': 'available', 'current_guest': False})

    def action_set_cleaning(self):
        self.write({'status': 'cleaning'})

    def action_set_maintenance(self):
        self.write({'status': 'maintenance'})

    def action_set_out_of_service(self):
        self.write({'status': 'out_of_service'})
