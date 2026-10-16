# -*- coding: utf-8 -*-
from odoo import models, fields

class HotelSupplyNorm(models.Model):
    _name = 'hotel.supply.norm'
    _description = 'Định Mức Vật Tư Tiêu Hao Buồng Phòng'
    _order = 'room_type_id asc, product_id asc'

    name = fields.Char(string='Tên định mức', compute='_compute_name', store=True)
    room_type_id = fields.Many2one('hotel.room.type', string='Hạng phòng áp dụng', required=True, ondelete='cascade')
    company_id = fields.Many2one('res.company', string='Cơ sở', default=lambda self: self.env.company)
    
    product_id = fields.Many2one('product.product', string='Vật tư tiêu hao', required=True,
                                 domain="['|', ('is_hotel_supply', '=', True), ('is_hotel_minibar', '=', True)]")
    uom_id = fields.Many2one('uom.uom', string='Đơn vị tính', related='product_id.uom_id', readonly=True)
    quantity = fields.Float(string='Định mức 1 lượt dọn', default=1.0, required=True)
    
    task_type = fields.Selection([
        ('all', 'Mọi loại dọn dẹp'),
        ('checkout_clean', 'Chỉ dọn sau khi trả phòng (Check-out)'),
        ('stayover_clean', 'Dọn phòng khách đang ở'),
        ('deep_clean', 'Tổng vệ sinh định kỳ'),
    ], string='Áp dụng cho lượt', default='all', required=True)

    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.room_type_id.name} - {rec.product_id.name} ({rec.quantity})"


class HotelTaskSupplyConsumed(models.Model):
    _name = 'hotel.task.supply.consumed'
    _description = 'Chi Tiết Vật Tư Đã Tiêu Hao Cho Lượt Dọn'
    _order = 'date desc'

    task_id = fields.Many2one('hotel.housekeeping.task', string='Nhiệm vụ dọn buồng', required=True, ondelete='cascade')
    room_id = fields.Many2one('hotel.room', string='Phòng', related='task_id.room_id', store=True)
    product_id = fields.Many2one('product.product', string='Vật tư', required=True)
    quantity = fields.Float(string='Số lượng xuất', required=True)
    uom_id = fields.Many2one('uom.uom', string='ĐVT', related='product_id.uom_id')
    date = fields.Datetime(string='Thời điểm xuất dùng', default=fields.Datetime.now)
