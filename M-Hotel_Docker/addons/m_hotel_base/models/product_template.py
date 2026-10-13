# -*- coding: utf-8 -*-
from odoo import models, fields

class ProductTemplate(models.Model):
    _inherit = 'product.template'

    is_hotel_service = fields.Boolean(string='Dịch vụ khách sạn', default=False,
                                      help='Đánh dấu nếu đây là dịch vụ khách sạn như giặt ủi, buffet sáng, đón tiễn sân bay...')
    is_hotel_supply = fields.Boolean(string='Vật tư buồng phòng', default=False,
                                     help='Đánh dấu nếu là đồ tiêu hao buồng phòng (dầu gội, xà phòng, bàn chải...)')
    is_hotel_minibar = fields.Boolean(string='Đồ Minibar', default=False,
                                      help='Đánh dấu nếu là đồ uống, đồ ăn nhẹ trong minibar của phòng')
