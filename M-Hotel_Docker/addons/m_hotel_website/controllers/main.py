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
        now = datetime.now()
        default_check_in = (now + timedelta(days=1)).strftime('%Y-%m-%dT14:00')
        default_check_out = (now + timedelta(days=3)).strftime('%Y-%m-%dT12:00')
        return request.render('m_hotel_website.hotel_booking_form', {
            'room_types': room_types,
            'companies': companies,
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

        # 2. Room lookup (prioritize available room of selected type and branch)
        Room = request.env['hotel.room'].sudo()
        room = Room.search([
            ('room_type_id', '=', room_type_id),
            ('company_id', '=', company_id),
            ('status', '=', 'available'),
        ], limit=1)
        if not room:
            room = Room.search([
                ('room_type_id', '=', room_type_id),
                ('company_id', '=', company_id),
            ], limit=1)
        if not room:
            room = Room.search([('room_type_id', '=', room_type_id)], limit=1)

        # 3. Datetime parse
        try:
            check_in = datetime.strptime(check_in_str.replace('T', ' ')[:16], '%Y-%m-%d %H:%M')
        except Exception:
            check_in = datetime.now() + timedelta(days=1, hours=14)
        try:
            check_out = datetime.strptime(check_out_str.replace('T', ' ')[:16], '%Y-%m-%d %H:%M')
        except Exception:
            check_out = check_in + timedelta(days=2)

        # 4. Room price calculation
        rt = request.env['hotel.room.type'].sudo().browse(room_type_id)
        room_price = rt.base_price_night if rent_type == 'night' else rt.base_price_hour

        # 5. Create booking in hotel.booking
        Booking = request.env['hotel.booking'].sudo()
        booking = Booking.create({
            'partner_id': partner.id,
            'company_id': company_id,
            'room_id': room.id,
            'room_type_id': room_type_id,
            'rent_type': rent_type,
            'check_in': check_in,
            'check_out': check_out,
            'room_price': room_price,
            'state': 'confirmed',
            'note': f'Đặt trực tuyến từ Website M-Hotel. Yêu cầu của khách: {note}' if note else 'Đặt trực tuyến từ Website M-Hotel',
        })

        return request.redirect(f'/hotel/booking/confirmation?booking_id={booking.id}')

    @http.route('/hotel/booking/confirmation', type='http', auth='public', website=True)
    def hotel_booking_confirmation(self, booking_id=None, **kw):
        if not booking_id:
            return request.redirect('/hotel')
        booking = request.env['hotel.booking'].sudo().browse(int(booking_id))
        if not booking.exists():
            return request.redirect('/hotel')
        return request.render('m_hotel_website.hotel_booking_confirmation', {
            'booking': booking,
        })
