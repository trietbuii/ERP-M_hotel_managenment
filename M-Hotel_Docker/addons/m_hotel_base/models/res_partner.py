# -*- coding: utf-8 -*-
from odoo import models, fields

class ResPartner(models.Model):
    _inherit = 'res.partner'

    id_card_number = fields.Char(string='CCCD / Hộ chiếu', index=True)
    nationality_id = fields.Many2one('res.country', string='Quốc tịch')
    gender = fields.Selection([
        ('male', 'Nam'),
        ('female', 'Nữ'),
        ('other', 'Khác')
    ], string='Giới tính')
    birthdate = fields.Date(string='Ngày sinh')
    
    hotel_guest_type = fields.Selection([
        ('standard', 'Khách tiêu chuẩn'),
        ('vip', 'Khách VIP'),
        ('blacklisted', 'Cảnh báo / Hạn chế'),
    ], string='Phân loại khách', default='standard')
    
    hotel_notes = fields.Text(string='Ghi chú lưu trú & Sở thích')
