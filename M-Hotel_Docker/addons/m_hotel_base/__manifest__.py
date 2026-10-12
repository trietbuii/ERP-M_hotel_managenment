# -*- coding: utf-8 -*-
{
    'name': 'M-Hotel Core — Base Models & Room Inventory',
    'version': '19.0.1.0.0',
    'category': 'Services/Hotel',
    'summary': 'Multi-company hotel foundation, room types, room registry, seasonal pricing, guest profiles, and RBAC security',
    'description': """
M-Hotel Core (m_hotel_base):
============================
- 5 RBAC Security Groups: Receptionist, Housekeeping, Technician, Inventory Clerk, Hotel Manager.
- Multi-company: Support for multiple branches (M-Hotel Saigon Central, M-Hotel Vung Tau Resort).
- Room Type Directory (Standard Cozy, Superior City View, Deluxe Ocean, Executive Suite, Family Penthouse).
- Seasonal and weekend rate tables with automated pricing rules.
- Detailed Room Registry (54 rooms, visual Kanban view & floor plan grouping).
- Res.partner inheritance: Citizen ID / Passport, nationality, VIP tier classification.
- Product.template inheritance: Flags for hotel services, housekeeping supplies, and minibar items.
    """,
    'author': 'Group 12 — Enterprise Resource Planning (ERP)',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'contacts', 'product'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hotel_room_type_views.xml',
        'views/hotel_room_rate_views.xml',
        'views/hotel_room_views.xml',
        'views/res_partner_views.xml',
        'views/product_template_views.xml',
        'views/menu_views.xml',
        'data/demo_data.xml',
    ],
    'demo': [
        'data/demo_data.xml',
    ],
    'application': True,
    'installable': True,
    'auto_install': False,
}
