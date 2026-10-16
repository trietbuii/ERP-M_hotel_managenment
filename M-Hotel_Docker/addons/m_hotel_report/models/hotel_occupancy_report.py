# -*- coding: utf-8 -*-
from odoo import models, fields, tools

class HotelOccupancyReport(models.Model):
    _name = 'hotel.occupancy.report'
    _description = 'Báo Cáo Công Suất & Phân Tích Doanh Thu Buồng Phòng'
    _auto = False
    _order = 'date desc'

    date = fields.Date(string='Ngày hạch toán', readonly=True)
    company_id = fields.Many2one('res.company', string='Cơ sở / Chi nhánh', readonly=True)
    room_id = fields.Many2one('hotel.room', string='Phòng', readonly=True)
    room_type_id = fields.Many2one('hotel.room.type', string='Hạng phòng', readonly=True)
    rent_type = fields.Selection([
        ('night', 'Thuê theo đêm'),
        ('hour', 'Thuê theo giờ'),
    ], string='Hình thức thuê', readonly=True)
    state = fields.Selection([
        ('draft', 'Dự thảo'),
        ('confirmed', 'Đã xác nhận'),
        ('check_in', 'Đang lưu trú'),
        ('check_out', 'Đã trả phòng'),
        ('invoiced', 'Đã xuất hóa đơn'),
        ('cancel', 'Đã hủy'),
    ], string='Trạng thái đơn', readonly=True)
    partner_id = fields.Many2one('res.partner', string='Khách hàng', readonly=True)

    nights_count = fields.Integer(string='Số đêm đã bán', readonly=True)
    hours_duration = fields.Integer(string='Số giờ đã bán', readonly=True)
    booking_count = fields.Integer(string='Lượt đặt phòng', readonly=True)
    
    amount_room = fields.Float(string='Doanh thu phòng (VNĐ)', readonly=True)
    amount_services = fields.Float(string='Doanh thu dịch vụ (VNĐ)', readonly=True)
    amount_total = fields.Float(string='Tổng doanh thu (VNĐ)', readonly=True)

    def init(self):
        tools.drop_view_if_exists(self.env.cr, self._table)
        self.env.cr.execute(f"""
            CREATE OR REPLACE VIEW {self._table} AS (
                SELECT
                    b.id AS id,
                    COALESCE(b.check_in::date, b.hour_date, b.create_date::date) AS date,
                    b.company_id AS company_id,
                    b.room_id AS room_id,
                    b.room_type_id AS room_type_id,
                    b.rent_type AS rent_type,
                    b.state AS state,
                    b.partner_id AS partner_id,
                    b.nights_count AS nights_count,
                    b.hours_duration AS hours_duration,
                    1 AS booking_count,
                    b.amount_room AS amount_room,
                    b.amount_services AS amount_services,
                    b.amount_total AS amount_total
                FROM hotel_booking b
                WHERE b.state NOT IN ('draft', 'cancel')
            )
        """)
