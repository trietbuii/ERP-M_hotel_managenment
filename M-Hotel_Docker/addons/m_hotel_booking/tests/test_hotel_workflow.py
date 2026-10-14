# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError, UserError

class TestHotelWorkflow(TransactionCase):

    def setUp(self):
        super().setUp()
        self.Partner = self.env['res.partner']
        self.RoomType = self.env['hotel.room.type']
        self.Room = self.env['hotel.room']
        self.Booking = self.env['hotel.booking']
        self.BookingLine = self.env['hotel.booking.line']

        # Setup Partner
        self.guest = self.Partner.create({
            'name': 'Nguyễn Văn Test',
            'phone': '0987111222',
            'id_card_number': '079123456789',
        })

        # Setup Room Type & Room
        self.room_type = self.RoomType.create({
            'name': 'Test Suite',
            'code': 'TSU',
            'capacity': 2,
            'base_price_night': 1000000.0,
            'base_price_hour': 250000.0,
        })

        self.room = self.Room.create({
            'name': 'P.999',
            'floor': 'Tầng 9',
            'room_type_id': self.room_type.id,
            'status': 'available',
        })

    def test_01_booking_creation_and_totals(self):
        """TC01: Tạo đơn đặt phòng theo đêm và tính toán tiền phòng"""
        now = datetime.now()
        booking = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': now + timedelta(days=2),
            'deposit_amount': 500000.0,
        })
        self.assertEqual(booking.nights_count, 2)
        self.assertEqual(booking.amount_room, 2000000.0)
        self.assertEqual(booking.amount_total, 2000000.0)
        self.assertEqual(booking.amount_residual, 1500000.0)

    def test_02_folio_services(self):
        """TC02: Thêm dịch vụ Folio vào đơn đặt phòng"""
        now = datetime.now()
        booking = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': now + timedelta(days=1),
        })
        self.BookingLine.create({
            'booking_id': booking.id,
            'name': 'Nước ngọt giải khát',
            'quantity': 3,
            'price_unit': 30000.0,
        })
        self.assertEqual(booking.amount_services, 90000.0)
        self.assertEqual(booking.amount_total, 1090000.0)

    def test_03_double_booking_prevention(self):
        """TC03: Kiểm tra chống trùng phòng"""
        now = datetime.now()
        b1 = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now + timedelta(days=5),
            'check_out': now + timedelta(days=8),
        })
        b1.action_confirm()

        # Tạo đơn thứ 2 bị đè khoảng ngày
        with self.assertRaises(ValidationError):
            b2 = self.Booking.create({
                'partner_id': self.guest.id,
                'room_id': self.room.id,
                'rent_type': 'night',
                'check_in': now + timedelta(days=6),
                'check_out': now + timedelta(days=9),
            })
            b2.action_confirm()

    def test_04_checkin_checkout_workflow(self):
        """TC04: Luồng Check-in và Check-out cập nhật trạng thái phòng"""
        now = datetime.now()
        booking = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': now + timedelta(days=1),
        })
        booking.action_confirm()
        self.assertEqual(self.room.status, 'reserved')

        booking.action_check_in()
        self.assertEqual(self.room.status, 'occupied')
        self.assertEqual(self.room.current_guest, self.guest.name)

        booking.action_check_out()
        self.assertEqual(self.room.status, 'cleaning')
        self.assertFalse(self.room.current_guest)

    def test_05_create_invoice(self):
        """TC05: Tạo hóa đơn Odoo account.move từ booking"""
        now = datetime.now()
        booking = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': now + timedelta(days=1),
        })
        booking.action_confirm()
        booking.action_check_in()
        booking.action_check_out()

        booking.action_create_invoice()
        self.assertTrue(booking.invoice_id)
        self.assertEqual(booking.invoice_id.move_type, 'out_invoice')
        self.assertEqual(booking.state, 'invoiced')
