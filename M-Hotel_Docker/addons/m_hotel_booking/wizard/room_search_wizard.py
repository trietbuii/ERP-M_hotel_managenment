# -*- coding: utf-8 -*-
from datetime import timedelta
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
    check_out = fields.Datetime(string='Ngày trả phòng', default=lambda self: fields.Datetime.now() + timedelta(days=1))
    
    hour_date = fields.Date(string='Ngày thuê giờ', default=fields.Date.context_today)
    hour_start = fields.Float(string='Giờ bắt đầu', default=14.0)
    hours_duration = fields.Integer(string='Số giờ thuê', default=2)

    available_room_ids = fields.Many2many('hotel.room', string='Các phòng đang trống khả dụng')
    selected_room_id = fields.Many2one('hotel.room', string='Chọn phòng để đặt ngay')

    def action_search_rooms(self):
        self.ensure_one()
        Booking = self.env['hotel.booking']
        now = fields.Datetime.now()

        if self.rent_type == 'night':
            if not self.check_in or not self.check_out:
                raise UserError(_("Vui lòng nhập đầy đủ ngày nhận và trả phòng!"))
            if self.check_out <= self.check_in:
                raise UserError(_("Ngày giờ trả phòng phải lớn hơn ngày giờ nhận phòng!"))
            search_start, search_end = Booking._get_rent_interval(
                'night', self.check_in, self.check_out, False, False, False
            )
        else:
            if not self.hour_date or (self.hours_duration or 0) <= 0:
                raise UserError(_("Vui lòng nhập ngày thuê giờ và số giờ thuê lớn hơn 0!"))
            hour_end = (self.hour_start or 0.0) + self.hours_duration
            search_start, search_end = Booking._get_rent_interval(
                'hour', False, False, self.hour_date, self.hour_start, hour_end
            )

        # Lấy các phòng đang hoạt động (nếu nhận ngay/hôm nay thì loại luôn phòng Đang có khách)
        excluded_statuses = ['maintenance', 'out_of_service']
        if search_start <= now + timedelta(hours=1):
            excluded_statuses.append('occupied')

        room_domain = [
            ('company_id', '=', self.company_id.id),
            ('status', 'not in', excluded_statuses),
        ]
        if self.room_type_id:
            room_domain.append(('room_type_id', '=', self.room_type_id.id))

        all_rooms = self.env['hotel.room'].search(room_domain)

        # Lọc bỏ các phòng bị trùng lịch (kiểm tra chéo cả theo đêm & theo giờ)
        busy_room_ids = set()
        booking_domain = [
            ('company_id', '=', self.company_id.id),
            ('state', 'in', ['confirmed', 'check_in', 'check_out', 'invoiced']),
            ('room_id', 'in', all_rooms.ids)
        ]
        active_bookings = Booking.search(booking_domain)

        for b in active_bookings:
            b_start, b_end = Booking._get_rent_interval(
                b.rent_type, b.check_in, b.check_out, b.hour_date, b.hour_start, b.hour_end
            )
            if not b_start or not b_end:
                continue
            # Khách đang lưu trú chưa trả phòng thì vẫn chiếm phòng ít nhất tới thời điểm hiện tại
            if b.state == 'check_in':
                b_end = max(b_end, now + timedelta(minutes=1))
            if search_start < b_end and search_end > b_start:
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
        
        # Tìm khách hàng mặc định (ưu tiên Nguyễn Văn An hoặc khách hàng đầu tiên)
        default_partner = self.env['res.partner'].search([('name', 'ilike', 'Nguyễn Văn An')], limit=1)
        if not default_partner:
            default_partner = self.env['res.partner'].search([('id', '!=', self.env.ref('base.partner_admin').id)], limit=1) or self.env.user.partner_id

        vals = {
            'company_id': self.company_id.id,
            'partner_id': default_partner.id,
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
