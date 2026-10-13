{
    'name': 'M-Hotel Website & Online Booking',
    'version': '19.0.1.0.0',
    'category': 'Website/Hotel',
    'summary': 'Public hotel portal and online booking engine for guests',
    'description': """
M-Hotel Website & Online Booking (m_hotel_website):
===================================================
- Public hotel portal presenting both branches (Saigon Central & Vung Tau Resort).
- Explore room categories (Standard Cozy, Superior City View, Deluxe Ocean, Executive Suite, Family Penthouse).
- Online reservation form synchronized with backend Odoo booking records (hotel.booking).
- Confirmation page and pro-forma invoice breakdown for guests.
    """,
    'author': 'Group 12 — Enterprise Resource Planning (ERP)',
    'depends': ['website', 'm_hotel_base', 'm_hotel_booking'],
    'data': [
        'views/website_templates.xml',
        'views/website_menu.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
