# -*- coding: utf-8 -*-
{
    'name': 'M-Hotel Booking — Reservations & Front Desk Management',
    'version': '19.0.1.0.0',
    'category': 'Services/Hotel',
    'summary': 'Daily and hourly bookings, double-booking prevention, service folio, check-in/out, room search wizard, and standard customer invoicing',
    'description': """
M-Hotel Booking (m_hotel_booking):
==================================
- Flexible Bookings: Overnight stays (Night) and hourly rentals (Hourly booking).
- Automated double-booking prevention algorithm across overlapping time windows.
- Folio Management: Minibar consumption, food & beverage, laundry, and surcharges.
- Check-in & Check-out workflows with real-time room occupancy updates.
- Fast Room Search Wizard for front desk receptionists.
- Accounting Integration: Standard customer invoice generation (account.move) with payment tracking.
    """,
    'author': 'Group 12 — Enterprise Resource Planning (ERP)',
    'license': 'LGPL-3',
    'depends': ['m_hotel_base', 'account'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/hotel_booking_views.xml',
        'wizard/room_search_wizard_views.xml',
        'views/menu_views.xml',
        'data/demo_data.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
