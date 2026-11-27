# -*- coding: utf-8 -*-
from datetime import datetime, timedelta
from odoo.tests.common import TransactionCase, tagged
from odoo.exceptions import ValidationError, UserError

@tagged('post_install', '-at_install')
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

    def test_06_minibar_stock_warning(self):
        """TC06: Cảnh báo khi thêm số lượng minibar vượt quá tồn kho khả dụng"""
        # Tạo sản phẩm minibar mẫu có tồn kho 2 chai
        minibar_product = self.env['product.product'].create({
            'name': 'Coca Cola Test',
            'is_hotel_minibar': True,
            'lst_price': 25000.0,
            'type': 'consu',
        })
        line = self.BookingLine.new({
            'product_id': minibar_product,
            'quantity': 3.0,
        })
        warning_res = line._onchange_product_id()
        self.assertIsNotNone(warning_res)
        self.assertIn('warning', warning_res)
        self.assertIn('Cảnh Báo Tồn Kho Minibar', warning_res['warning']['title'])

    def test_07_receptionist_invoice_and_payment(self):
        """TC07: Tài khoản Lễ tân đủ quyền tạo, vào sổ và thu tiền hóa đơn khách hàng"""
        receptionist_user = self.env['res.users'].create({
            'name': 'Lễ Tân Test RBAC',
            'login': 'test_receptionist_rbac',
            'email': 'test_receptionist_rbac@example.com',
            'group_ids': [(6, 0, [self.env.ref('m_hotel_base.group_hotel_receptionist').id])],
        })
        now = datetime.now()
        BookingAsRecep = self.Booking.with_user(receptionist_user)
        booking = BookingAsRecep.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': now + timedelta(days=1),
            'deposit_amount': 200000.0,
        })
        booking.action_confirm()
        booking.action_check_in()
        booking.action_check_out()
        booking.action_create_invoice()

        invoice = booking.invoice_id.with_user(receptionist_user)
        self.assertTrue(invoice)
        self.assertEqual(invoice.amount_total, 800000.0)
        self.assertEqual(invoice.amount_total, booking.amount_residual)
        invoice.action_post()
        self.assertEqual(invoice.state, 'posted')

        journal = self.env['account.journal'].sudo().search([
            ('type', '=', 'cash'),
            ('company_id', '=', booking.company_id.id),
        ], limit=1) or self.env['account.journal'].sudo().search([
            ('type', '=', 'bank'),
            ('company_id', '=', booking.company_id.id),
        ], limit=1)
        self.assertTrue(journal, "Cần ít nhất 1 sổ Tiền mặt hoặc Ngân hàng để test thanh toán")
        pay_wiz = self.env['account.payment.register'].with_user(receptionist_user).with_context(
            active_model='account.move',
            active_ids=invoice.ids,
        ).create({'journal_id': journal.id})
        pay_wiz.action_create_payments()
        self.assertEqual(invoice.payment_state, 'paid' if journal.type == 'cash' else 'in_payment')
        self.assertEqual(invoice.amount_residual, 0.0)

    def test_08_cross_rent_type_and_wizard_occupied_filter(self):
        """TC08: Chặn trùng chéo thuê đêm-giờ và ẩn phòng Đang có khách khỏi Wizard nhận ngay"""
        now = datetime.now()
        # Đơn thuê đêm hiện đang ở (quá hạn check-out giả lập giống phòng kẹt chưa trả)
        past_in = now - timedelta(days=5)
        past_out = now - timedelta(days=3)
        b_stay = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': past_in,
            'check_out': past_out,
        })
        b_stay.action_confirm()
        b_stay.action_check_in()

        # Wizard tìm phòng nhận ngay hôm nay KHÔNG được hiện phòng đang occupied
        wiz = self.env['hotel.room.search.wizard'].create({
            'company_id': self.room.company_id.id,
            'room_type_id': self.room_type.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': now + timedelta(days=1),
        })
        wiz.action_search_rooms()
        self.assertNotIn(self.room, wiz.available_room_ids)

        # Chặn đặt trùng theo giờ đè lên đơn thuê đêm tương lai
        fut_in = datetime(2026, 12, 20, 7, 0)   # 14:00 GMT+7
        fut_out = datetime(2026, 12, 22, 5, 0)  # 12:00 GMT+7
        b_night = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': fut_in,
            'check_out': fut_out,
        })
        b_night.action_confirm()
        with self.assertRaises(ValidationError):
            b_hour = self.Booking.create({
                'partner_id': self.guest.id,
                'room_id': self.room.id,
                'rent_type': 'hour',
                'hour_date': fut_in.date() + timedelta(days=1),
                'hour_start': 10.0,
                'hours_duration': 2,
            })
            b_hour.action_confirm()

    def test_09_cancel_future_booking_and_block_cleaning_checkin(self):
        """TC09: Hủy đơn tương lai không làm mất trạng thái Đang ở; chặn nhận phòng đang Cần dọn"""
        now = datetime.now()
        b_stay = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': now + timedelta(days=1),
        })
        b_stay.action_confirm()
        b_stay.action_check_in()

        b_future = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now + timedelta(days=10),
            'check_out': now + timedelta(days=12),
        })
        b_future.action_confirm()
        b_future.action_cancel()

        self.assertEqual(self.room.status, 'occupied')
        self.assertEqual(self.room.current_guest, self.guest.name)

        # Trả phòng -> phòng Cần dọn dẹp -> phải chặn nếu cố nhận phòng đơn khác khi chưa dọn xong
        b_stay.action_check_out()
        self.assertEqual(self.room.status, 'cleaning')
        b_next = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now + timedelta(days=2),
            'check_out': now + timedelta(days=3),
        })
        b_next.action_confirm()
        with self.assertRaises(UserError):
            b_next.action_check_in()

    def test_10_checkout_and_invoice_not_blocked_by_checked_out_booking(self):
        """TC10: Đơn đã trả phòng/xuất hóa đơn không chặn tạo hóa đơn hay đặt phòng mới khi khách trả sớm"""
        now = datetime.now()
        b1 = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now,
            'check_out': now + timedelta(days=3),
        })
        b1.action_confirm()
        b1.action_check_in()
        # Khách b1 trả phòng sớm sau 1 ngày
        b1.action_check_out()
        self.room.action_set_available()

        # Đơn b2 đặt vào đúng khoảng ngày còn lại của b1 phải thành công và xuất hóa đơn bình thường
        b2 = self.Booking.create({
            'partner_id': self.guest.id,
            'room_id': self.room.id,
            'rent_type': 'night',
            'check_in': now + timedelta(days=1),
            'check_out': now + timedelta(days=2),
        })
        b2.action_confirm()
        b2.action_check_in()
        b2.action_check_out()
        b2.action_create_invoice()
        self.assertEqual(b2.state, 'invoiced')
        b1.action_create_invoice()
        self.assertEqual(b1.state, 'invoiced')
