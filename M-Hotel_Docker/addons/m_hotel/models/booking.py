# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta

class MHotelBooking(models.Model):
    _name = 'm.hotel.booking'
    _description = 'Đặt phòng khách sạn M-Hotel'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc'

    name = fields.Char(string='Mã đặt phòng', required=True, copy=False, readonly=True, default=lambda self: _('Mới'))
    partner_id = fields.Many2one('res.partner', string='Khách hàng', required=True, tracking=True)
    phone = fields.Char(related='partner_id.phone', string='Số điện thoại', readonly=True)
    email = fields.Char(related='partner_id.email', string='Email', readonly=True)
    
    hotel_id = fields.Many2one('m.hotel', string='Cơ sở / Chi nhánh', required=True, default=lambda self: self.env['m.hotel'].search([], limit=1))
    room_id = fields.Many2one('m.hotel.room', string='Phòng lưu trú', required=True, tracking=True, domain="[('hotel_id', '=', hotel_id)]")
    room_type_id = fields.Many2one(related='room_id.room_type_id', string='Hạng phòng', readonly=True, store=True)

    rent_type = fields.Selection([
        ('night', 'Thuê theo đêm / ngày (Check-in 14h - Check-out 12h)'),
        ('hour', 'Thuê theo giờ (Nghỉ nhanh block 1 - 5 tiếng)')
    ], string='Hình thức thuê', default='night', required=True, tracking=True)

    # Khoảng thời gian cho thuê theo đêm
    check_in = fields.Datetime(string='Thời gian nhận phòng', required=True, default=fields.Datetime.now, tracking=True)
    check_out = fields.Datetime(string='Thời gian trả phòng', required=True, default=lambda self: fields.Datetime.now() + timedelta(days=1), tracking=True)
    
    # Cho thuê theo giờ
    hours_duration = fields.Integer(string='Số giờ thuê (theo giờ)', default=2)
    hour_date = fields.Date(string='Ngày thuê theo giờ', default=fields.Date.context_today)
    hour_start = fields.Float(string='Giờ bắt đầu (VD: 8.0 = 08:00)', default=10.0)
    hour_end = fields.Float(string='Giờ kết thúc', compute='_compute_hour_end', store=True)
    
    # Tính toán chi phí
    nights_count = fields.Integer(string='Số đêm lưu trú', compute='_compute_nights_and_total', store=True)
    unit_price = fields.Float(string='Đơn giá áp dụng (VNĐ)', compute='_compute_nights_and_total', store=True)
    deposit_amount = fields.Float(string='Tiền cọc đã thanh toán (VNĐ)', default=0.0)
    total_amount = fields.Float(string='Tổng tiền thanh toán (VNĐ)', compute='_compute_nights_and_total', store=True, tracking=True)

    status = fields.Selection([
        ('draft', 'Dự thảo'),
        ('confirmed', 'Đã xác nhận'),
        ('occupied', 'Đang lưu trú'),
        ('completed', 'Đã trả phòng'),
        ('cancelled', 'Đã hủy')
    ], string='Trạng thái đơn', default='confirmed', tracking=True)

    note = fields.Text(string='Ghi chú yêu cầu của khách')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Mới')) == _('Mới'):
                vals['name'] = self.env['ir.sequence'].next_by_code('m.hotel.booking') or f"BK-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return super(MHotelBooking, self).create(vals_list)

    @api.depends('hour_start', 'hours_duration')
    def _compute_hour_end(self):
        for rec in self:
            duration = rec.hours_duration if rec.hours_duration > 0 else 1
            rec.hour_end = rec.hour_start + duration

    @api.depends('rent_type', 'check_in', 'check_out', 'hours_duration', 'room_id')
    def _compute_nights_and_total(self):
        for rec in self:
            if not rec.room_id or not rec.room_type_id:
                rec.nights_count = 0
                rec.unit_price = 0.0
                rec.total_amount = 0.0
                continue

            if rec.rent_type == 'hour':
                duration = rec.hours_duration if rec.hours_duration > 0 else 1
                rec.nights_count = 0
                rec.unit_price = rec.room_type_id.price_hour
                rec.total_amount = duration * rec.room_type_id.price_hour
            else:
                if rec.check_in and rec.check_out:
                    d1 = fields.Date.to_date(rec.check_in)
                    d2 = fields.Date.to_date(rec.check_out)
                    diff_days = (d2 - d1).days if d2 and d1 else 1
                    diff_days = max(diff_days, 1)
                    rec.nights_count = diff_days
                    rec.unit_price = rec.room_type_id.price_night
                    rec.total_amount = diff_days * rec.room_type_id.price_night
                else:
                    rec.nights_count = 1
                    rec.unit_price = rec.room_type_id.price_night
                    rec.total_amount = rec.room_type_id.price_night

    @api.constrains('check_in', 'check_out', 'rent_type', 'room_id', 'status', 'hour_date', 'hour_start', 'hour_end')
    def _check_booking_validity(self):
        for rec in self:
            if rec.status == 'cancelled':
                continue

            # 1. Kiểm tra phòng bảo trì
            if rec.room_id.status == 'maintenance':
                raise ValidationError(_("Phòng %s đang bảo trì kỹ thuật, không thể nhận đặt phòng!") % rec.room_id.name)

            # 2. Kiểm tra logic ngày nhận/trả đối với thuê theo đêm
            if rec.rent_type == 'night':
                if rec.check_out <= rec.check_in:
                    raise ValidationError(_("Ngày/giờ trả phòng phải sau ngày nhận phòng!"))

                # Chống trùng lặp theo quy tắc: existing_start < requested_end AND existing_end > requested_start
                domain = [
                    ('id', '!=', rec.id),
                    ('room_id', '=', rec.room_id.id),
                    ('status', 'in', ['confirmed', 'occupied']),
                    ('check_in', '<', rec.check_out),
                    ('check_out', '>', rec.check_in)
                ]
                conflict = self.search(domain, limit=1)
                if conflict:
                    raise ValidationError(_(
                        "Trùng lịch đặt phòng! Phòng %s đã được đặt bởi khách [%s] trong khoảng thời gian từ %s đến %s!"
                    ) % (rec.room_id.name, conflict.partner_id.name, conflict.check_in, conflict.check_out))

            # 3. Chống trùng lặp đối với thuê theo giờ
            elif rec.rent_type == 'hour':
                if rec.hour_start < 0 or rec.hour_start > 24 or rec.hours_duration <= 0:
                    raise ValidationError(_("Khung giờ thuê không hợp lệ!"))

                # Kiểm tra trùng với booking thuê theo giờ khác cùng ngày
                domain_hour = [
                    ('id', '!=', rec.id),
                    ('room_id', '=', rec.room_id.id),
                    ('rent_type', '=', 'hour'),
                    ('status', 'in', ['confirmed', 'occupied']),
                    ('hour_date', '=', rec.hour_date),
                    ('hour_start', '<', rec.hour_end),
                    ('hour_end', '>', rec.hour_start)
                ]
                conflict_hour = self.search(domain_hour, limit=1)
                if conflict_hour:
                    raise ValidationError(_(
                        "Trùng lịch theo giờ! Phòng %s đã có khách [%s] thuê từ %.1fh đến %.1fh vào ngày %s!"
                    ) % (rec.room_id.name, conflict_hour.partner_id.name, conflict_hour.hour_start, conflict_hour.hour_end, rec.hour_date))

    # --- NGHIỆP VỤ NÚT BẤM (BUTTON ACTIONS) ---
    def action_confirm(self):
        for rec in self:
            rec.status = 'confirmed'
            if rec.room_id.status == 'available':
                rec.room_id.status = 'confirmed'

    def action_check_in(self):
        for rec in self:
            if rec.status == 'cancelled':
                raise ValidationError(_("Không thể Check-in cho đơn đặt phòng đã bị Hủy!"))
            rec.status = 'occupied'
            rec.room_id.status = 'occupied'

    def action_check_out(self):
        for rec in self:
            if rec.status != 'occupied':
                raise ValidationError(_("Chỉ có thể Check-out cho khách đang lưu trú!"))
            rec.status = 'completed'
            rec.room_id.status = 'cleaning'
            # Tự động tạo sự vụ Buồng phòng cần dọn
            self.env['m.hotel.service.request'].create({
                'name': f"Dọn phòng sau khi khách {rec.partner_id.name} trả phòng",
                'room_id': rec.room_id.id,
                'request_type': 'housekeeping',
                'priority': 'high',
                'note': f"Khách vừa check-out từ đơn {rec.name}. Cần vệ sinh thay ga gối trước lượt khách tiếp theo."
            })

    def action_cancel(self):
        for rec in self:
            rec.status = 'cancelled'
            if rec.room_id.status == 'confirmed':
                rec.room_id.status = 'available'

    # --- RPC API CHO TIMELINE & CALENDAR PMS ---
    @api.model
    def get_calendar_data(self, start_date, end_date, hotel_id=None):
        domain = [
            ('status', '!=', 'cancelled'),
            '|',
            '&', ('rent_type', '=', 'night'), '&', ('check_in', '<=', end_date), ('check_out', '>=', start_date),
            '&', ('rent_type', '=', 'hour'), '&', ('hour_date', '<=', end_date), ('hour_date', '>=', start_date)
        ]
        if hotel_id:
            domain.append(('hotel_id', '=', hotel_id))

        bookings = self.search(domain)
        result = []
        for b in bookings:
            result.append({
                'id': b.id,
                'name': b.name,
                'partner': b.partner_id.name,
                'phone': b.phone,
                'room_id': b.room_id.id,
                'room_number': b.room_id.name,
                'rent_type': b.rent_type,
                'check_in': fields.Datetime.to_string(b.check_in),
                'check_out': fields.Datetime.to_string(b.check_out),
                'hour_date': str(b.hour_date) if b.hour_date else False,
                'hour_start': b.hour_start,
                'hour_end': b.hour_end,
                'total_amount': b.total_amount,
                'status': b.status
            })
        return result

    @api.model
    def get_day_summary(self, target_date, hotel_id=None):
        room_domain = []
        if hotel_id:
            room_domain.append(('hotel_id', '=', hotel_id))
        rooms = self.env['m.hotel.room'].search(room_domain)
        
        day_bookings = self.get_calendar_data(target_date, target_date, hotel_id)
        booked_room_ids = {b['room_id'] for b in day_bookings}

        total_rooms = len(rooms)
        booked_rooms = len(booked_room_ids)
        maintenance_rooms = len(rooms.filtered(lambda r: r.status in ['maintenance', 'cleaning']))
        available_rooms = max(0, total_rooms - booked_rooms - maintenance_rooms)

        return {
            'date': target_date,
            'total_rooms': total_rooms,
            'booked_rooms': booked_rooms,
            'available_rooms': available_rooms,
            'maintenance_rooms': maintenance_rooms,
            'bookings': day_bookings
        }
