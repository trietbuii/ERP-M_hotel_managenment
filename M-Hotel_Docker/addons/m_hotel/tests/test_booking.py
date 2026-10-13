# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError
from datetime import datetime, date

class TestMHotelBooking(TransactionCase):

    def setUp(self):
        super(TestMHotelBooking, self).setUp()
        self.partner = self.env['res.partner'].create({'name': 'Khách Hàng Test'})
        self.hotel = self.env['m.hotel'].create({
            'name': 'M-Hotel Test',
            'code': 'TEST-HOTEL'
        })
        self.room_type = self.env['m.hotel.room.type'].create({
            'name': 'Hạng Deluxe Test',
            'code': 'TEST-DLX',
            'price_night': 1000000.0,
            'price_hour': 200000.0
        })
        self.room = self.env['m.hotel.room'].create({
            'name': 'P.999',
            'hotel_id': self.hotel.id,
            'room_type_id': self.room_type.id,
            'status': 'available'
        })

    def test_tc01_valid_booking(self):
        """TC01: Đặt phòng hợp lệ từ 15/11 đến 18/11 (3 đêm), tổng tiền 3.000.000 VNĐ"""
        now = datetime(2026, 11, 15, 14, 0, 0)
        checkout = datetime(2026, 11, 18, 12, 0, 0)
        booking = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': checkout
        })
        self.assertEqual(booking.nights_count, 3)
        self.assertEqual(booking.total_amount, 3000000.0)

    def test_tc02_invalid_checkout_date(self):
        """TC02: Ngày trả phòng trước ngày nhận phòng -> Phải raise ValidationError"""
        now = datetime(2026, 11, 18, 14, 0, 0)
        checkout = datetime(2026, 11, 15, 12, 0, 0)
        with self.assertRaises(ValidationError):
            self.env['m.hotel.booking'].create({
                'partner_id': self.partner.id,
                'hotel_id': self.hotel.id,
                'room_id': self.room.id,
                'rent_type': 'night',
                'check_in': now,
                'check_out': checkout
            })

    def test_tc03_double_booking_conflict(self):
        """TC03: Hai booking trùng ngày trên cùng phòng -> Chặn booking thứ hai"""
        self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': datetime(2026, 11, 15, 14, 0, 0),
            'check_out': datetime(2026, 11, 18, 12, 0, 0),
            'status': 'confirmed'
        })
        # Thử đặt đè khoảng ngày
        with self.assertRaises(ValidationError):
            self.env['m.hotel.booking'].create({
                'partner_id': self.partner.id,
                'hotel_id': self.hotel.id,
                'room_id': self.room.id,
                'rent_type': 'night',
                'check_in': datetime(2026, 11, 16, 14, 0, 0),
                'check_out': datetime(2026, 11, 19, 12, 0, 0),
                'status': 'confirmed'
            })

    def test_tc04_hourly_booking(self):
        """TC04: Đặt phòng theo giờ (3 giờ x 200.000đ = 600.000 VNĐ)"""
        booking = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'hour',
            'hours_duration': 3,
            'hour_date': date(2026, 11, 15),
            'hour_start': 10.0,
            'check_in': datetime(2026, 11, 15, 10, 0, 0),
            'check_out': datetime(2026, 11, 15, 13, 0, 0)
        })
        self.assertEqual(booking.total_amount, 600000.0)
        self.assertEqual(booking.hour_end, 13.0)

    def test_tc05_hourly_booking_conflict(self):
        """TC05: Trùng khung giờ giữa 2 đơn đặt theo giờ trên cùng một phòng"""
        self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'hour',
            'hours_duration': 3,
            'hour_date': date(2026, 11, 15),
            'hour_start': 9.0,
            'check_in': datetime(2026, 11, 15, 9, 0, 0),
            'check_out': datetime(2026, 11, 15, 12, 0, 0),
            'status': 'confirmed'
        })
        # Thử đặt từ 10.0 đến 13.0 (giao với 9.0 - 12.0)
        with self.assertRaises(ValidationError):
            self.env['m.hotel.booking'].create({
                'partner_id': self.partner.id,
                'hotel_id': self.hotel.id,
                'room_id': self.room.id,
                'rent_type': 'hour',
                'hours_duration': 3,
                'hour_date': date(2026, 11, 15),
                'hour_start': 10.0,
                'check_in': datetime(2026, 11, 15, 10, 0, 0),
                'check_out': datetime(2026, 11, 15, 13, 0, 0),
                'status': 'confirmed'
            })

    def test_tc06_maintenance_room_refusal(self):
        """TC06: Phòng đang bảo trì -> Không cho phép tạo booking"""
        self.room.status = 'maintenance'
        with self.assertRaises(ValidationError):
            self.env['m.hotel.booking'].create({
                'partner_id': self.partner.id,
                'hotel_id': self.hotel.id,
                'room_id': self.room.id,
                'rent_type': 'night',
                'check_in': datetime(2026, 11, 15, 14, 0, 0),
                'check_out': datetime(2026, 11, 16, 12, 0, 0)
            })

    def test_tc07_cancelled_booking_does_not_block(self):
        """TC07: Đơn đặt phòng đã hủy không chặn các booking mới"""
        b_cancelled = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': datetime(2026, 11, 20, 14, 0, 0),
            'check_out': datetime(2026, 11, 22, 12, 0, 0),
            'status': 'cancelled'
        })
        # Tạo đơn mới cùng thời gian -> Phải thành công
        b_new = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': datetime(2026, 11, 20, 14, 0, 0),
            'check_out': datetime(2026, 11, 22, 12, 0, 0),
            'status': 'confirmed'
        })
        self.assertTrue(b_new.id)

    def test_tc08_checkout_and_housekeeping(self):
        """TC08: Check-out tự động chuyển phòng sang 'cleaning' và tạo phiếu buồng phòng"""
        booking = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': datetime(2026, 11, 20, 14, 0, 0),
            'check_out': datetime(2026, 11, 22, 12, 0, 0),
            'status': 'occupied'
        })
        self.room.status = 'occupied'
        booking.action_check_out()

        self.assertEqual(booking.status, 'completed')
        self.assertEqual(self.room.status, 'cleaning')
        sr = self.env['m.hotel.service.request'].search([('room_id', '=', self.room.id)], limit=1)
        self.assertTrue(sr)
        self.assertEqual(sr.request_type, 'housekeeping')

    def test_tc09_checkin_cancelled_booking_refusal(self):
        """TC09: Chặn check-in đối với đơn đặt phòng đã bị Hủy"""
        booking = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': datetime(2026, 11, 20, 14, 0, 0),
            'check_out': datetime(2026, 11, 22, 12, 0, 0),
            'status': 'cancelled'
        })
        with self.assertRaises(ValidationError):
            booking.action_check_in()

    def test_tc10_checkout_unconfirmed_booking_refusal(self):
        """TC10: Chặn check-out đối với đơn đặt phòng chưa check-in/chưa occupied"""
        booking = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': datetime(2026, 11, 20, 14, 0, 0),
            'check_out': datetime(2026, 11, 22, 12, 0, 0),
            'status': 'confirmed'
        })
        with self.assertRaises(ValidationError):
            booking.action_check_out()

    def test_tc11_consecutive_bookings_allowed(self):
        """TC11: Hai booking nối tiếp nhau (Khách A trả 18/11, Khách B nhận 18/11) được phép"""
        b1 = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': datetime(2026, 11, 15, 14, 0, 0),
            'check_out': datetime(2026, 11, 18, 12, 0, 0),
            'status': 'confirmed'
        })
        b2 = self.env['m.hotel.booking'].create({
            'partner_id': self.partner.id,
            'hotel_id': self.hotel.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': datetime(2026, 11, 18, 14, 0, 0),
            'check_out': datetime(2026, 11, 20, 12, 0, 0),
            'status': 'confirmed'
        })
        self.assertTrue(b1.id)
        self.assertTrue(b2.id)

    def test_tc12_demo_data_integrity(self):
        """TC12: Kiểm tra số lượng và tính nhất quán dữ liệu mẫu (Demo Data Integrity)"""
        rooms = self.env['m.hotel.room'].search([])
        self.assertGreaterEqual(len(rooms), 40, "Phải có ít nhất 40 phòng nghỉ mẫu")

        bookings = self.env['m.hotel.booking'].search([])
        self.assertGreaterEqual(len(bookings), 50, "Phải có ít nhất 50 đơn đặt phòng mẫu")

        service_reqs = self.env['m.hotel.service.request'].search([])
        self.assertGreaterEqual(len(service_reqs), 20, "Phải có ít nhất 20 sự vụ buồng phòng / bảo trì mẫu")

        # Kiểm tra tính cách ly đa chi nhánh giữa cơ sở và phòng
        for b in bookings:
            self.assertEqual(
                b.hotel_id.id,
                b.room_id.hotel_id.id,
                f"Booking {b.name} bị lệch chi nhánh giữa cơ sở và phòng!"
            )
