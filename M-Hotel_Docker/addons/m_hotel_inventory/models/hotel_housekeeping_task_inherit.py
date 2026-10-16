# -*- coding: utf-8 -*-
from odoo import models, fields

class HotelHousekeepingTask(models.Model):
    _inherit = 'hotel.housekeeping.task'

    consumed_supply_ids = fields.One2many('hotel.task.supply.consumed', 'task_id', string='Vật Tư Tiêu Hao Cho Lượt Dọn')

    def _consume_room_supplies(self):
        """Tự động trừ vật tư theo định mức khi hoàn tất dọn buồng"""
        for task in self:
            if not task.room_type_id:
                continue
            
            # Tra cứu định mức tương ứng với hạng phòng
            domain = [
                ('room_type_id', '=', task.room_type_id.id),
                ('task_type', 'in', ['all', task.task_type]),
            ]
            norms = self.env['hotel.supply.norm'].search(domain)
            
            consumed_vals = []
            for norm in norms:
                consumed_vals.append({
                    'task_id': task.id,
                    'product_id': norm.product_id.id,
                    'quantity': norm.quantity,
                    'date': fields.Datetime.now(),
                })
            
            if consumed_vals:
                self.env['hotel.task.supply.consumed'].create(consumed_vals)
                supply_summary = ", ".join([f"{n.product_id.name}: {n.quantity}" for n in norms])
                task.message_post(body=f"Đã tự động xuất tiêu hao vật tư buồng phòng theo định mức: {supply_summary}")
