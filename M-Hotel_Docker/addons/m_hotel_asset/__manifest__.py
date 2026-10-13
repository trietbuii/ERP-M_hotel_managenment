# -*- coding: utf-8 -*-
{
    'name': 'M-Hotel Asset & Maintenance — Room Equipment & Repairs',
    'version': '19.0.1.0.0',
    'category': 'Services/Hotel',
    'summary': 'Manage room equipment assets and link incident tickets directly with Maintenance work orders',
    'description': """
M-Hotel Asset & Maintenance (m_hotel_asset):
============================================
- Odoo Maintenance Inheritance: Assign equipment (Air Conditioners, Smart TVs, Minibars, Water Heaters) to specific rooms.
- Incident Integration: Seamlessly escalate room incidents (hotel.incident) to Odoo Maintenance Requests (maintenance.request).
- Room Smart Buttons: Instantly inspect room equipment inventory and breakdown maintenance history.
    """,
    'author': 'Group 12 — Enterprise Resource Planning (ERP)',
    'license': 'LGPL-3',
    'depends': ['m_hotel_base', 'm_hotel_housekeeping', 'maintenance'],
    'data': [
        'security/ir.model.access.csv',
        'views/maintenance_equipment_views.xml',
        'views/maintenance_request_views.xml',
        'views/hotel_room_inherit_views.xml',
        'views/hotel_incident_inherit_views.xml',
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
