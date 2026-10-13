# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class MHotelServiceRequest(models.Model):
    _name = 'm.hotel.service.request'
    _description = 'Yêu cầu sự vụ, Buồng phòng & Bảo trì M-Hotel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Nội dung công việc / Sự vụ', required=True, tracking=True)
    room_id = fields.Many2one('m.hotel.room', string='Phòng phát sinh', required=True, tracking=True)
    request_type = fields.Selection([
        ('housekeeping', 'Buồng phòng & Vệ sinh (Housekeeping)'),
        ('maintenance', 'Sửa chữa & Bảo trì kỹ thuật (Maintenance)'),
        ('guest_service', 'Yêu cầu phục vụ tiện ích của khách')
    ], string='Phân loại sự vụ', default='housekeeping', required=True, tracking=True)
    
    user_id = fields.Many2one('res.users', string='Nhân viên phụ trách', default=lambda self: self.env.user, tracking=True)
    priority = fields.Selection([
        ('low', 'Thấp'),
        ('medium', 'Bình thường'),
        ('high', 'Ưu tiên cao'),
        ('urgent', 'Khẩn cấp')
    ], string='Mức độ ưu tiên', default='medium')

    status = fields.Selection([
        ('new', 'Mới tiếp nhận'),
        ('in_progress', 'Đang xử lý / Đang dọn'),
        ('done', 'Đã hoàn tất'),
        ('cancelled', 'Đã hủy')
    ], string='Tiến độ xử lý', default='new', tracking=True)

    note = fields.Text(string='Ghi chú chi tiết')

    def action_start(self):
        for rec in self:
            rec.status = 'in_progress'
            if rec.request_type == 'housekeeping':
                rec.room_id.status = 'cleaning'
            elif rec.request_type == 'maintenance':
                rec.room_id.status = 'maintenance'

    def action_done(self):
        for rec in self:
            rec.status = 'done'
            # Sau khi buồng phòng dọn xong hoặc kỹ thuật sửa xong, phòng chuyển về Sẵn sàng
            if rec.room_id.status in ['cleaning', 'maintenance']:
                rec.room_id.status = 'available'
