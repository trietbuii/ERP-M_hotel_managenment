# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError

class HotelRoomSearchWizard(models.TransientModel):
    _name = 'hotel.room.search.wizard'
    _description = 'Wizard Tìm Phòng Trống Nhanh'

    company_id = fields.Many2one('res.company', string='Cơ sở / Chi nhánh', default=lambda self: self.env.company, required=True)
    room_type_id = fields.Many2one('hotel.room.type', string='Hạng phòng mong muốn')
    rent_type = fields.Selection([
        ('night', 'Thuê theo đêm'),
        ('hour', 'Thuê theo giờ'),
    ], string='Hình thức thuê', default='night', required=True)

    check_in = fields.Datetime(string='Ngày nhận phòng', default=fields.Datetime.now)
    check_out = fields.Datetime(string='Ngày trả phòng')
    
    hour_date = fields.Date(string='Ngày thuê giờ', default=fields.Date.context_today)
    hour_start = fields.Float(string='Giờ bắt đầu', default=14.0)
    hours_duration = fields.Integer(string='Số giờ thuê', default=2)

    available_room_ids = fields.Many2many('hotel.room', string='Các phòng đang trống khả dụng')
    selected_room_id = fields.Many2one('hotel.room', string='Chọn phòng để đặt ngay')

    def action_search_rooms(self):
        self.ensure_one()
        # Lấy tất cả các phòng thỏa mãn điều kiện cơ sở và hạng phòng
        room_domain = [
            ('company_id', '=', self.company_id.id),
            ('status', 'not in', ['maintenance', 'out_of_service'])
        ]
        if self.room_type_id:
            room_domain.append(('room_type_id', '=', self.room_type_id.id))
        
        all_rooms = self.env['hotel.room'].search(room_domain)
        
        # Lọc bỏ các phòng bị trùng lịch
        busy_room_ids = set()
        booking_domain = [
            ('company_id', '=', self.company_id.id),
            ('state', 'in', ['confirmed', 'check_in', 'check_out', 'invoiced']),
            ('room_id', 'in', all_rooms.ids)
        ]
        active_bookings = self.env['hotel.booking'].search(booking_domain)
        
        if self.rent_type == 'night':
            if not self.check_in or not self.check_out:
                raise UserError(_("Vui lòng nhập đầy đủ ngày nhận và trả phòng!"))
            for b in active_bookings:
                if b.rent_type == 'night' and b.check_in and b.check_out:
                    if self.check_in < b.check_out and self.check_out > b.check_in:
                        busy_room_ids.add(b.room_id.id)
        else:
            hour_end = (self.hour_start or 0.0) + (self.hours_duration or 0)
            for b in active_bookings:
                if b.rent_type == 'hour' and b.hour_date == self.hour_date:
                    if self.hour_start < b.hour_end and hour_end > b.hour_start:
                        busy_room_ids.add(b.room_id.id)

        available_rooms = all_rooms.filtered(lambda r: r.id not in busy_room_ids)
        self.available_room_ids = [(6, 0, available_rooms.ids)]
        
        # Mở lại popup hiển thị kết quả
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.room.search.wizard',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }

    def action_book_room(self):
        self.ensure_one()
        if not self.selected_room_id:
            raise UserError(_("Vui lòng chọn 1 phòng trong danh sách phòng trống bên dưới!"))
        
        vals = {
            'company_id': self.company_id.id,
            'room_id': self.selected_room_id.id,
            'rent_type': self.rent_type,
        }
        if self.rent_type == 'night':
            vals.update({
                'check_in': self.check_in,
                'check_out': self.check_out,
            })
        else:
            vals.update({
                'hour_date': self.hour_date,
                'hour_start': self.hour_start,
                'hours_duration': self.hours_duration,
            })
        
        booking = self.env['hotel.booking'].create(vals)
        return {
            'name': _('Phiếu Đặt Phòng Mới'),
            'type': 'ir.actions.act_window',
            'res_model': 'hotel.booking',
            'res_id': booking.id,
            'view_mode': 'form',
            'target': 'current',
        }
