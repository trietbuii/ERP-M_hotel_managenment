# -*- coding: utf-8 -*-
{
    'name': 'M-Hotel Inventory — Housekeeping Supply Consumption & Norms',
    'version': '19.0.1.0.0',
    'category': 'Services/Hotel',
    'summary': 'Define room supply norms per room type and automate stock consumption upon housekeeping completion',
    'description': """
M-Hotel Inventory (m_hotel_inventory):
======================================
- Room Supply Norms (hotel.supply.norm): Set standard quantities for toothbrushes, shampoo, bottled water, and towels per room type.
- Automatic Stock Consumption: Standard Odoo internal stock moves triggered automatically when housekeeping marks a room clean.
- Detailed consumption audit trail tracked per room and per cleaning session.
    """,
    'author': 'Group 12 — Enterprise Resource Planning (ERP)',
    'license': 'LGPL-3',
    'depends': ['m_hotel_base', 'm_hotel_housekeeping', 'stock'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hotel_supply_norm_views.xml',
        'views/hotel_housekeeping_task_inherit_views.xml',
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
