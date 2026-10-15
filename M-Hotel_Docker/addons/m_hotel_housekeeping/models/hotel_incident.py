# -*- coding: utf-8 -*-
from odoo import models, fields, api, _

class HotelIncident(models.Model):
    _name = 'hotel.incident'
    _description = 'Sự Cố & Hư Hỏng Buồng Phòng'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Mã sự cố', required=True, copy=False, readonly=True,
                       default=lambda self: _('Mới'), tracking=True)
    title = fields.Char(string='Tiêu đề sự cố', required=True, tracking=True)
    room_id = fields.Many2one('hotel.room', string='Phòng xảy ra sự cố', required=True, tracking=True)
    company_id = fields.Many2one('res.company', string='Cơ sở', related='room_id.company_id', store=True, readonly=True)
    user_id = fields.Many2one('res.users', string='Người ghi nhận', default=lambda self: self.env.user, tracking=True)
    
    severity = fields.Selection([
        ('low', 'Mức độ nhẹ (Khách vẫn có thể ở)'),
        ('medium', 'Trung bình (Cần sửa chữa trong ngày)'),
        ('critical', 'Nghiêm trọng (Không thể cho thuê - Khóa phòng)'),
    ], string='Mức độ nghiêm trọng', default='medium', required=True, tracking=True)

    block_room = fields.Boolean(string='Khóa phòng (Không đón khách)', default=False, tracking=True,
                                help='Nếu tích chọn, trạng thái phòng sẽ tự động chuyển sang Bảo trì / Khóa tạm thời')
    
    state = fields.Selection([
        ('reported', 'Mới tiếp nhận'),
        ('in_progress', 'Đang xử lý'),
        ('resolved', 'Đã khắc phục'),
        ('cancel', 'Hủy'),
    ], string='Trạng thái', default='reported', tracking=True, required=True)

    description = fields.Text(string='Mô tả chi tiết sự cố / hư hỏng')
    resolution_note = fields.Text(string='Biện pháp & Kết quả khắc phục')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Mới')) == _('Mới'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hotel.incident') or _('Mới')
        records = super().create(vals_list)
        for rec in records:
            if rec.block_room and rec.state in ['reported', 'in_progress']:
                rec.room_id.write({'status': 'maintenance'})
        return records

    def write(self, vals):
        res = super().write(vals)
        for rec in self:
            if rec.block_room and rec.state in ['reported', 'in_progress']:
                rec.room_id.write({'status': 'maintenance'})
            elif rec.state == 'resolved' and rec.room_id.status in ['maintenance', 'out_of_service']:
                rec.room_id.write({'status': 'cleaning'})
        return res

    def action_start(self):
        self.write({'state': 'in_progress'})

    def action_resolve(self):
        self.write({'state': 'resolved'})

    def action_cancel(self):
        self.write({'state': 'cancel'})
