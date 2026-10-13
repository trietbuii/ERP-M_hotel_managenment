# -*- coding: utf-8 -*-
{
    'name': 'M-Hotel Housekeeping — Room Cleaning & Incident Management',
    'version': '19.0.1.0.0',
    'category': 'Services/Hotel',
    'summary': 'Housekeeping task workflows, automated trigger on check-out, room incident reporting, and maintenance room locking',
    'description': """
M-Hotel Housekeeping (m_hotel_housekeeping):
============================================
- Housekeeping Task Management (hotel.housekeeping.task): Check-out cleaning, stay-over cleaning, deep cleaning.
- Visual Drag-and-Drop Kanban Board: Pending -> In Progress -> Clean (automatically returns room to Available status).
- Automatic housekeeping task creation upon receptionist check-out.
- Room Incident Management (hotel.incident): Equipment breakdown logging and severity categorization.
- Automated Room Blocking: Sets room state to out_of_service / maintenance when critical incidents occur.
    """,
    'author': 'Group 12 — Enterprise Resource Planning (ERP)',
    'license': 'LGPL-3',
    'depends': ['m_hotel_base', 'm_hotel_booking'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'data/ir_sequence_data.xml',
        'views/hotel_housekeeping_task_views.xml',
        'views/hotel_incident_views.xml',
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
