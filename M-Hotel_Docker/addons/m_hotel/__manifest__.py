# -*- coding: utf-8 -*-
{
    'name': 'M-Hotel — Quản Lý Vận Hành Khách Sạn & Đặt Phòng',
    'version': '17.0.1.0.0',
    'category': 'Services/Hotel',
    'summary': 'Quản lý Đặt phòng (theo ngày & theo giờ), Lịch phòng, Sơ đồ phòng, Buồng phòng và Sự cố',
    'description': """
M-Hotel Hotel Management System (Odoo 17 Community):
- Quản lý cơ sở khách sạn đa chi nhánh (Multi-company).
- Quản lý hạng phòng và danh mục phòng.
- Đặt phòng linh hoạt: Thuê theo đêm (Night) và Thuê theo giờ (Hourly booking).
- Chống trùng lịch (Double-booking prevention).
- Luồng Check-in / Check-out tự động cập nhật trạng thái phòng.
- Phân hệ Buồng phòng (Housekeeping) và Bảo trì sự cố (Maintenance).
    """,
    'author': 'Nhóm 12 — IS336 Hoạch Định Nguồn Lực Doanh Nghiệp',
    'website': 'https://m-hotel.vn',
    'license': 'LGPL-3',
    'depends': ['base', 'mail'],
    'data': [
        'security/security.xml',
        'security/ir.model.access.csv',
        'views/hotel_views.xml',
        'views/room_views.xml',
        'views/booking_views.xml',
        'views/service_request_views.xml',
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
