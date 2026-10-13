# -*- coding: utf-8 -*-
{
    'name': 'M-Hotel — Hotel Operations Management (ERP Suite)',
    'version': '19.0.1.0.0',
    'category': 'Services/Hotel',
    'summary': 'M-Hotel ERP Management Suite for Odoo 19 Community with native standard views',
    'description': """
M-Hotel ERP Management Suite (Odoo 19 Community):
=================================================
A comprehensive hotel operations management system built entirely on standard Odoo native views:
1. m_hotel_base: Multi-branch hotel foundation, 5 room types, 54 rooms, seasonal rate tables, guest identification (Citizen ID / Passport / VIP tiers).
2. m_hotel_booking: Daily & hourly room reservations, double-booking prevention, service folio, check-in/out workflows, room availability wizard, and standard customer invoicing.
3. m_hotel_housekeeping: Drag-and-drop housekeeping Kanban board, auto-generated tasks upon check-out, incident tracking, and automatic room blocking.
4. m_hotel_inventory: Room supply norms (linens, amenities), automatic stock consumption upon task completion.
5. m_hotel_asset: Room equipment registry and maintenance request integration.
6. m_hotel_report: Dynamic Pivot & Graph analytics for room occupancy and multi-dimensional revenue.
7. m_hotel_website: Public hotel portal and online booking engine.
    """,
    'author': 'Group 12 — Enterprise Resource Planning (ERP)',
    'license': 'LGPL-3',
    'depends': [
        'm_hotel_base',
        'm_hotel_booking',
        'm_hotel_housekeeping',
        'm_hotel_inventory',
        'm_hotel_asset',
        'm_hotel_report',
        'm_hotel_website',
    ],
    'data': [],
    'application': True,
    'installable': True,
    'auto_install': False,
}
