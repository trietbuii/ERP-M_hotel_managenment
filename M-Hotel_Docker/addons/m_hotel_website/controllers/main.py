from odoo import http
from odoo.http import request
from datetime import datetime, timedelta

class MHotelWebsite(http.Controller):

    @http.route(['/', '/hotel'], type='http', auth='public', website=True, sitemap=True)
    def hotel_home(self, **kw):
        room_types = request.env['hotel.room.type'].sudo().search([('active', '=', True)])
        companies = request.env['res.company'].sudo().search([('id', 'in', [1, 2])])
        return request.render('m_hotel_website.hotel_home', {
            'room_types': room_types,
            'companies': companies,
        })

    @http.route('/hotel/rooms', type='http', auth='public', website=True, sitemap=True)
    def hotel_rooms(self, company_id=None, **kw):
        domain = [('active', '=', True)]
        room_types = request.env['hotel.room.type'].sudo().search(domain)
        companies = request.env['res.company'].sudo().search([('id', 'in', [1, 2])])
        return request.render('m_hotel_website.hotel_rooms', {
            'room_types': room_types,
            'companies': companies,
            'selected_company': int(company_id) if company_id else None,
        })

    @http.route('/hotel/booking', type='http', auth='public', website=True, sitemap=True)
    def hotel_booking(self, type_id=None, company_id=None, **kw):
        room_types = request.env['hotel.room.type'].sudo().search([('active', '=', True)])
        companies = request.env['res.company'].sudo().search([('id', 'in', [1, 2])])
        rooms = request.env['hotel.room'].sudo().search([
            ('active', '=', True),
            ('status', 'not in', ['maintenance', 'out_of_service'])
        ], order='company_id asc, floor asc, name asc')
        now = datetime.now()
        default_check_in = (now + timedelta(days=1)).strftime('%Y-%m-%dT14:00')
        default_check_out = (now + timedelta(days=3)).strftime('%Y-%m-%dT12:00')
        return request.render('m_hotel_website.hotel_booking_form', {
            'room_types': room_types,
            'companies': companies,
            'rooms': rooms,
            'selected_type_id': int(type_id) if type_id else (room_types[0].id if room_types else None),
            'selected_company_id': int(company_id) if company_id else 1,
            'default_check_in': default_check_in,
            'default_check_out': default_check_out,
        })

    @http.route('/hotel/booking/submit', type='http', auth='public', methods=['POST'], website=True, csrf=False)
    def hotel_booking_submit(self, **post):
        customer_name = post.get('customer_name', '').strip()
        phone = post.get('phone', '').strip()
        email = post.get('email', '').strip()
        id_number = post.get('id_number', '').strip()
        company_id = int(post.get('company_id', 1))
        room_type_id = int(post.get('room_type_id', 1))
        room_id_str = post.get('room_id', '').strip()
        rent_type = post.get('rent_type', 'night')
        check_in_str = post.get('check_in')
        check_out_str = post.get('check_out')
        note = post.get('note', '').strip()

        # 1. Partner lookup or creation
        Partner = request.env['res.partner'].sudo()
        partner = False
        if phone:
            partner = Partner.search([('phone', '=', phone)], limit=1)
        if not partner and email:
            partner = Partner.search([('email', '=', email)], limit=1)
        if not partner:
            partner = Partner.create({
                'name': customer_name or 'Khách đặt trực tuyến Website',
                'phone': phone or False,
                'email': email or False,
                'comment': f'CCCD/Passport: {id_number}' if id_number else False,
            })
        elif customer_name and partner.name != customer_name:
            partner.write({'name': customer_name})

        # Helper parse datetime
        def _parse_datetime(dt_str, fallback):
            if not dt_str:
                return fallback
            clean = dt_str.replace('T', ' ').replace(',', ' ').strip()
            for fmt in ['%Y-%m-%d %H:%M', '%Y-%m-%d %H:%M:%S', '%m/%d/%Y %H:%M', '%d/%m/%Y %H:%M', '%Y/%m/%d %H:%M']:
                try:
                    return datetime.strptime(clean[:16], fmt)
                except Exception:
                    pass
            return fallback

        now = datetime.now()
        check_in = _parse_datetime(check_in_str, now + timedelta(days=1, hours=14))
        check_out = _parse_datetime(check_out_str, check_in + (timedelta(hours=4) if rent_type == 'hour' else timedelta(days=2)))

        # 2. Xử lý thời gian thuê theo giờ
        hour_date = check_in.date()
        hour_start = check_in.hour + (check_in.minute / 60.0)
        if check_out and check_out.date() == hour_date and check_out > check_in:
            hour_end = check_out.hour + (check_out.minute / 60.0)
            hours_duration = max(1, int(round(hour_end - hour_start)))
        else:
            hours_duration = 2
            hour_end = hour_start + hours_duration

        # 3. Thuật toán tìm phòng trống thông minh (Quét tất cả phòng của hạng phòng và cơ sở)
        Room = request.env['hotel.room'].sudo()
        Booking = request.env['hotel.booking'].sudo()

        candidate_rooms = Room.search([
            ('room_type_id', '=', room_type_id),
            ('company_id', '=', company_id),
            ('status', 'not in', ['maintenance', 'out_of_service']),
        ], order='status asc, id asc')

        selected_room = False
        for r in candidate_rooms:
            conflict_domain = [
                ('room_id', '=', r.id),
                ('state', 'in', ['confirmed', 'check_in', 'check_out', 'invoiced']),
            ]
            existing_bookings = Booking.search(conflict_domain)
            is_busy = False

            if rent_type == 'night':
                for eb in existing_bookings:
                    if eb.rent_type == 'night' and eb.check_in and eb.check_out:
                        if check_in < eb.check_out and check_out > eb.check_in:
                            is_busy = True
                            break
            else:
                for eb in existing_bookings:
                    if eb.rent_type == 'hour' and eb.hour_date == hour_date:
                        eb_hour_end = (eb.hour_start or 0.0) + (eb.hours_duration or 0)
                        if hour_start < eb_hour_end and hour_end > eb.hour_start:
                            is_busy = True
                            break

            if not is_busy:
                selected_room = r
                break

        if not selected_room:
            selected_room = candidate_rooms[0] if candidate_rooms else Room.search([('room_type_id', '=', room_type_id)], limit=1)

        # Nếu khách chọn phòng cụ thể trên giao diện
        if room_id_str:
            try:
                explicit_room = Room.browse(int(room_id_str))
                if explicit_room.exists():
                    selected_room = explicit_room
            except Exception:
                pass

        # 4. Tính toán giá phòng
        rt = request.env['hotel.room.type'].sudo().browse(room_type_id)
        room_price = rt.base_price_night if rent_type == 'night' else rt.base_price_hour

        # 5. Khởi tạo đơn đặt phòng
        booking_vals = {
            'partner_id': partner.id,
            'company_id': company_id,
            'room_id': selected_room.id,
            'room_type_id': room_type_id,
            'rent_type': rent_type,
            'check_in': check_in,
            'check_out': check_out,
            'room_price': room_price,
            'state': 'confirmed',
            'note': f'Đặt trực tuyến từ Website M-Hotel. Yêu cầu của khách: {note}' if note else 'Đặt trực tuyến từ Website M-Hotel',
        }
        if rent_type == 'hour':
            booking_vals.update({
                'hour_date': hour_date,
                'hour_start': hour_start,
                'hours_duration': hours_duration,
            })

        booking = False
        try:
            booking = Booking.create(booking_vals)
        except Exception:
            # Nếu phòng được chọn bị lỗi ràng buộc, tự động thử các phòng còn lại
            for alt_room in candidate_rooms:
                if alt_room.id != selected_room.id:
                    try:
                        booking_vals['room_id'] = alt_room.id
                        booking = Booking.create(booking_vals)
                        break
                    except Exception:
                        continue

        if not booking:
            # Fallback nếu tất cả đều quá tải
            booking = Booking.create(booking_vals)

        return request.redirect(f'/hotel/booking/confirmation?booking_id={booking.id}')

    @http.route('/hotel/booking/confirmation', type='http', auth='public', website=True)
    def hotel_booking_confirmation(self, booking_id=None, **kw):
        if not booking_id:
            return request.redirect('/hotel')
        booking = request.env['hotel.booking'].sudo().browse(int(booking_id))
        if not booking.exists():
            return request.redirect('/hotel')

        # Cấu hình thanh toán VietQR - Ngân hàng Techcombank (TCB)
        bank_id = 'TCB'
        account_no = '2101200646'
        account_name = 'BUI MINH TRIET'
        amount = int(booking.amount_total or booking.room_price or 0)
        memo = f"MHOTEL {booking.name.replace('/', '').replace(' ', '')}"
        vietqr_url = f"https://img.vietqr.io/image/{bank_id}-{account_no}-compact2.png?amount={amount}&addInfo={memo}&accountName={account_name}"

        return request.render('m_hotel_website.hotel_booking_confirmation', {
            'booking': booking,
            'vietqr_url': vietqr_url,
            'bank_account_no': account_no,
            'bank_account_name': account_name,
            'bank_name': 'Techcombank (Ngân hàng Kỹ thương Việt Nam)',
            'transfer_amount': amount,
            'transfer_memo': memo,
        })
