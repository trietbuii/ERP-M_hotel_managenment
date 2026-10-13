# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HotelHousekeepingTask(models.Model):
    _name = 'hotel.housekeeping.task'
    _description = 'Nhiệm Vụ Buồng Phòng'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, date_deadline asc, id desc'

    name = fields.Char(string='Mã nhiệm vụ', required=True, copy=False, readonly=True,
                       default=lambda self: _('Mới'), tracking=True)
    
    room_id = fields.Many2one('hotel.room', string='Phòng', required=True, tracking=True)
    room_type_id = fields.Many2one('hotel.room.type', string='Hạng phòng', related='room_id.room_type_id', store=True)
    company_id = fields.Many2one('res.company', string='Cơ sở / Chi nhánh',
                                 related='room_id.company_id', store=True, readonly=True)
    
    task_type = fields.Selection([
        ('checkout_clean', 'Dọn phòng sau khi khách trả (Check-out)'),
        ('stayover_clean', 'Dọn phòng khách đang ở (Stay-over)'),
        ('deep_clean', 'Tổng vệ sinh định kỳ (Deep Clean)'),
        ('turndown', 'Chỉnh trang phòng buổi tối (Turn-down)'),
    ], string='Loại công việc', default='checkout_clean', required=True, tracking=True)

    priority = fields.Selection([
        ('0', 'Bình thường'),
        ('1', 'Ưu tiên'),
        ('2', 'Khẩn cấp / Khách chờ nhận'),
    ], string='Mức độ ưu tiên', default='1', tracking=True)

    user_id = fields.Many2one('res.users', string='Nhân viên dọn phòng', tracking=True)
    booking_id = fields.Many2one('hotel.booking', string='Đơn đặt phòng liên quan', readonly=True)
    
    state = fields.Selection([
        ('pending', 'Chờ xử lý'),
        ('in_progress', 'Đang dọn dẹp'),
        ('done', 'Đã sạch & Sẵn sàng'),
        ('cancel', 'Đã hủy'),
    ], string='Trạng thái', default='pending', tracking=True, required=True)

    date_deadline = fields.Datetime(string='Hạn hoàn thành', default=fields.Datetime.now)
    notes = fields.Text(string='Ghi chú buồng phòng')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Mới')) == _('Mới'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hotel.housekeeping.task') or _('Mới')
        return super().create(vals_list)

    def action_start(self):
        for rec in self:
            rec.write({'state': 'in_progress'})
            if rec.room_id.status != 'occupied':
                rec.room_id.write({'status': 'cleaning'})

    def action_complete(self):
        for rec in self:
            rec.write({'state': 'done'})
            # Nếu phòng không có khách đang ở thì chuyển về Sẵn sàng
            if rec.room_id.status != 'occupied':
                rec.room_id.write({'status': 'available'})
            
            # Kích hoạt hook trừ kho tiêu hao (m_hotel_inventory)
            if hasattr(rec, '_consume_room_supplies'):
                rec._consume_room_supplies()

    def action_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})
