# -*- coding: utf-8 -*-
from datetime import datetime, time, timedelta
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError, UserError

class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Phiếu Đặt Phòng Khách Sạn'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'create_date desc, id desc'

    name = fields.Char(string='Mã đặt phòng', required=True, copy=False, readonly=True,
                       default=lambda self: _('Mới'), tracking=True)
    
    partner_id = fields.Many2one('res.partner', string='Khách hàng', required=True, tracking=True)
    phone = fields.Char(string='Số điện thoại', related='partner_id.phone', readonly=False, store=True)
    email = fields.Char(string='Email', related='partner_id.email', readonly=False, store=True)
    id_card_number = fields.Char(string='CCCD / Hộ chiếu', related='partner_id.id_card_number', readonly=False)
    
    company_id = fields.Many2one('res.company', string='Cơ sở / Chi nhánh',
                                 default=lambda self: self.env.company, required=True)
    room_id = fields.Many2one('hotel.room', string='Phòng xếp chỗ', required=True, tracking=True)
    room_type_id = fields.Many2one('hotel.room.type', string='Hạng phòng',
                                  related='room_id.room_type_id', store=True, readonly=True)
    
    rent_type = fields.Selection([
        ('night', 'Thuê theo đêm'),
        ('hour', 'Thuê theo giờ'),
    ], string='Hình thức thuê', default='night', required=True, tracking=True)

    # Thuê theo đêm
    check_in = fields.Datetime(string='Ngày giờ nhận phòng', default=fields.Datetime.now, tracking=True)
    check_out = fields.Datetime(string='Ngày giờ trả phòng', default=lambda self: fields.Datetime.now() + timedelta(days=1), tracking=True)
    nights_count = fields.Integer(string='Số đêm', compute='_compute_duration', store=True)

    @api.onchange('check_in')
    def _onchange_check_in(self):
        if self.check_in:
            self.check_out = self.check_in + timedelta(days=1)

    # Thuê theo giờ
    hour_date = fields.Date(string='Ngày thuê giờ', default=fields.Date.context_today)
    hour_start = fields.Float(string='Giờ bắt đầu', default=14.0)
    hour_end = fields.Float(string='Giờ kết thúc', compute='_compute_hour_end', store=True)
    hours_duration = fields.Integer(string='Số giờ thuê', default=2)

    room_price = fields.Float(string='Đơn giá phòng (VNĐ)', compute='_compute_room_price', readonly=False, store=True)
    line_ids = fields.One2many('hotel.booking.line', 'booking_id', string='Dịch vụ & Minibar (Folio)')

    amount_room = fields.Float(string='Tiền phòng', compute='_compute_totals', store=True, tracking=True)
    amount_services = fields.Float(string='Tiền dịch vụ', compute='_compute_totals', store=True)
    amount_total = fields.Float(string='Tổng cộng', compute='_compute_totals', store=True, tracking=True)
    deposit_amount = fields.Float(string='Tiền đặt cọc', default=0.0, tracking=True)
    amount_residual = fields.Float(string='Còn lại thanh toán', compute='_compute_totals', store=True)

    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('confirmed', 'Đã xác nhận'),
        ('check_in', 'Đang lưu trú'),
        ('check_out', 'Đã trả phòng'),
        ('invoiced', 'Đã xuất hóa đơn'),
        ('cancel', 'Đã hủy'),
    ], string='Trạng thái', default='draft', tracking=True, required=True)

    invoice_id = fields.Many2one('account.move', string='Hóa đơn khách hàng', readonly=True, copy=False)
    invoice_count = fields.Integer(string='Số hóa đơn', compute='_compute_invoice_count')
    note = fields.Text(string='Ghi chú đặc biệt')

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('Mới')) == _('Mới'):
                vals['name'] = self.env['ir.sequence'].next_by_code('hotel.booking') or _('Mới')
        return super().create(vals_list)

    @api.depends('rent_type', 'check_in', 'check_out', 'hours_duration')
    def _compute_duration(self):
        for rec in self:
            if rec.rent_type == 'night' and rec.check_in and rec.check_out:
                diff = rec.check_out - rec.check_in
                nights = max(1, int(round(diff.total_seconds() / 86400.0)))
                rec.nights_count = nights
            else:
                rec.nights_count = 1

    @api.depends('hour_start', 'hours_duration')
    def _compute_hour_end(self):
        for rec in self:
            rec.hour_end = (rec.hour_start or 0.0) + (rec.hours_duration or 0)

    @api.depends('room_id', 'rent_type', 'check_in', 'hour_date')
    def _compute_room_price(self):
        for rec in self:
            if not rec.room_id:
                rec.room_price = 0.0
                continue
            # Kiểm tra giá mùa nếu có
            target_date = rec.check_in.date() if (rec.rent_type == 'night' and rec.check_in) else (rec.hour_date or fields.Date.today())
            rate = self.env['hotel.room.rate'].search([
                ('room_type_id', '=', rec.room_id.room_type_id.id),
                ('start_date', '<=', target_date),
                ('end_date', '>=', target_date),
                ('active', '=', True)
            ], limit=1)

            if rec.rent_type == 'night':
                rec.room_price = rate.price_night if rate else rec.room_id.price_night
            else:
                rec.room_price = rate.price_hour if rate else rec.room_id.price_hour

    @api.depends('rent_type', 'room_price', 'nights_count', 'hours_duration', 'line_ids.price_subtotal', 'deposit_amount')
    def _compute_totals(self):
        for rec in self:
            if rec.rent_type == 'night':
                rec.amount_room = (rec.room_price or 0.0) * max(1, rec.nights_count)
            else:
                rec.amount_room = (rec.room_price or 0.0) * max(1, rec.hours_duration)
            rec.amount_services = sum(rec.line_ids.mapped('price_subtotal'))
            rec.amount_total = rec.amount_room + rec.amount_services
            rec.amount_residual = max(0.0, rec.amount_total - (rec.deposit_amount or 0.0))

    def _compute_invoice_count(self):
        for rec in self:
            rec.invoice_count = 1 if rec.invoice_id else 0

    # ==========================================
    # CHỐNG TRÙNG LỊCH ĐẶT PHÒNG
    # ==========================================
    @api.constrains('room_id', 'state', 'check_in', 'check_out', 'rent_type', 'hour_date', 'hour_start', 'hour_end')
    def _check_double_booking(self):
        for rec in self:
            if rec.state in ['cancel', 'draft'] or not rec.room_id:
                continue
            
            domain = [
                ('id', '!=', rec.id),
                ('room_id', '=', rec.room_id.id),
                ('state', 'in', ['confirmed', 'check_in', 'check_out', 'invoiced']),
            ]
            conflicts = self.search(domain)
            
            for c in conflicts:
                if rec.rent_type == 'night' and c.rent_type == 'night':
                    if rec.check_in and rec.check_out and c.check_in and c.check_out:
                        # Overlap: max(start1, start2) < min(end1, end2)
                        if rec.check_in < c.check_out and rec.check_out > c.check_in:
                            raise ValidationError(
                                _("Phòng %s đã được đặt hoặc đang có khách lưu trú bởi đơn %s (từ %s đến %s)! Vui lòng chọn phòng khác.") % (
                                    rec.room_id.name, c.name, c.check_in, c.check_out
                                )
                            )
                elif rec.rent_type == 'hour' and c.rent_type == 'hour':
                    if rec.hour_date and c.hour_date and rec.hour_date == c.hour_date:
                        if rec.hour_start < c.hour_end and rec.hour_end > c.hour_start:
                            raise ValidationError(
                                _("Phòng %s bị trùng giờ với đơn %s vào ngày %s (từ %.1fh đến %.1fh)!") % (
                                    rec.room_id.name, c.name, c.hour_date, c.hour_start, c.hour_end
                                )
                            )

    # ==========================================
    # WORKFLOW ACTIONS
    # ==========================================
    def action_confirm(self):
        for rec in self:
            rec.write({'state': 'confirmed'})
            if rec.room_id.status == 'available':
                rec.room_id.write({'status': 'reserved'})

    def action_check_in(self):
        for rec in self:
            if rec.room_id.status == 'occupied' and rec.room_id.current_guest != rec.partner_id.name:
                raise UserError(_("Phòng %s hiện đang có khách khác lưu trú (%s)!") % (rec.room_id.name, rec.room_id.current_guest))
            if rec.room_id.status in ['maintenance', 'out_of_service']:
                raise UserError(_("Phòng %s đang bảo trì hoặc tạm khóa, không thể nhận phòng!") % rec.room_id.name)
            
            rec.write({'state': 'check_in'})
            rec.room_id.write({
                'status': 'occupied',
                'current_guest': rec.partner_id.name,
            })

    def action_check_out(self):
        for rec in self:
            rec.write({'state': 'check_out'})
            # Chuyển phòng sang trạng thái Cần dọn dẹp
            rec.room_id.write({
                'status': 'cleaning',
                'current_guest': False,
            })
            # Tự động thông báo hoặc tạo task buồng phòng (thông qua hook m_hotel_housekeeping)
            if hasattr(self.env['hotel.booking'], '_auto_create_housekeeping_task'):
                rec._auto_create_housekeeping_task()

    def action_cancel(self):
        for rec in self:
            rec.write({'state': 'cancel'})
            if rec.room_id.status in ['reserved', 'occupied']:
                rec.room_id.write({'status': 'available', 'current_guest': False})

    # ==========================================
    # XUẤT HÓA ĐƠN ODOO CHUẨN (ACCOUNT.MOVE)
    # ==========================================
    def action_create_invoice(self):
        self.ensure_one()
        if self.invoice_id:
            return self.action_view_invoice()

        # Tạo journal entry invoice (Customer Invoice: out_invoice)
        invoice_vals = {
            'move_type': 'out_invoice',
            'partner_id': self.partner_id.id,
            'company_id': self.company_id.id,
            'invoice_date': fields.Date.today(),
            'hotel_booking_id': self.id,
            'narration': f"Thanh toán đơn đặt phòng {self.name} - Phòng {self.room_id.name}",
            'invoice_line_ids': []
        }

        # Dòng 1: Tiền phòng
        rent_desc = f"Tiền thuê phòng {self.room_id.name} ({self.nights_count} đêm)" if self.rent_type == 'night' else f"Tiền thuê phòng {self.room_id.name} ({self.hours_duration} giờ)"
        qty = self.nights_count if self.rent_type == 'night' else self.hours_duration
        invoice_vals['invoice_line_ids'].append((0, 0, {
            'name': rent_desc,
            'quantity': max(1, qty),
            'price_unit': self.room_price,
        }))

        # Dòng dịch vụ Folio
        for line in self.line_ids:
            invoice_vals['invoice_line_ids'].append((0, 0, {
                'product_id': line.product_id.id if line.product_id else False,
                'name': line.name or (line.product_id.name if line.product_id else 'Dịch vụ phụ trợ'),
                'quantity': line.quantity,
                'price_unit': line.price_unit,
            }))

        move = self.env['account.move'].create(invoice_vals)
        self.invoice_id = move.id
        self.state = 'invoiced'
        return self.action_view_invoice()

    def action_view_invoice(self):
        self.ensure_one()
        return {
            'name': _('Hóa Đơn Khách Hàng'),
            'type': 'ir.actions.act_window',
            'res_model': 'account.move',
            'view_mode': 'form',
            'res_id': self.invoice_id.id,
            'target': 'current',
        }


class HotelBookingLine(models.Model):
    _name = 'hotel.booking.line'
    _description = 'Chi Tiết Dịch Vụ Folio Đặt Phòng'

    booking_id = fields.Many2one('hotel.booking', string='Đơn đặt phòng', required=True, ondelete='cascade')
    product_id = fields.Many2one('product.product', string='Dịch vụ / Hàng tiêu dùng',
                                 domain="['|', ('is_hotel_service', '=', True), ('is_hotel_minibar', '=', True)]")
    name = fields.Char(string='Diễn giải', required=True)
    quantity = fields.Float(string='Số lượng', default=1.0, required=True)
    price_unit = fields.Float(string='Đơn giá (VNĐ)', required=True)
    price_subtotal = fields.Float(string='Thành tiền', compute='_compute_subtotal', store=True)

    @api.onchange('product_id')
    def _onchange_product_id(self):
        if self.product_id:
            self.name = self.product_id.name
            self.price_unit = self.product_id.lst_price

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for rec in self:
            rec.price_subtotal = (rec.quantity or 0.0) * (rec.price_unit or 0.0)
