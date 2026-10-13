# -*- coding: utf-8 -*-
{
    'name': 'M-Hotel Report — Occupancy & Revenue Analytics',
    'version': '19.0.1.0.0',
    'category': 'Services/Hotel',
    'summary': 'Multi-dimensional Pivot tables and graphical charts analyzing room revenue, service sales, and occupancy rates',
    'description': """
M-Hotel Report (m_hotel_report):
================================
- Dynamic SQL view consolidating metrics from bookings, stays, and check-outs.
- Pivot Tables: Cross-tab analysis by branch, room type, room, and period (monthly/quarterly/yearly).
- Graph Charts: Visualize trends for room revenue, minibar service revenue, and occupied night/hour counts.
    """,
    'author': 'Group 12 — Enterprise Resource Planning (ERP)',
    'license': 'LGPL-3',
    'depends': ['m_hotel_base', 'm_hotel_booking'],
    'data': [
        'security/ir.model.access.csv',
        'views/hotel_occupancy_report_views.xml',
        'views/menu_views.xml',
    ],
    'application': False,
    'installable': True,
    'auto_install': False,
}
