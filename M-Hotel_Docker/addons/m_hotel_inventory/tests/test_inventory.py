# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestHotelInventory(TransactionCase):

    def setUp(self):
        super().setUp()
        self.room_type = self.env['hotel.room.type'].create({
            'name': 'Inventory Test Room Type',
            'code': 'ITR',
        })
        self.room = self.env['hotel.room'].create({
            'name': 'P.777',
            'floor': 'Tầng 7',
            'room_type_id': self.room_type.id,
            'status': 'available',
        })
        self.supply = self.env['product.product'].create({
            'name': 'Dầu gội mini cao cấp',
            'is_hotel_supply': True,
            'type': 'consu',
        })
        self.norm = self.env['hotel.supply.norm'].create({
            'room_type_id': self.room_type.id,
            'product_id': self.supply.id,
            'quantity': 3.0,
            'task_type': 'all',
        })

    def test_01_auto_supply_consumption(self):
        """TC: Hoàn thành dọn phòng tự động tiêu hao vật tư theo định mức"""
        task = self.env['hotel.housekeeping.task'].create({
            'room_id': self.room.id,
            'task_type': 'checkout_clean',
            'state': 'pending',
        })
        task.action_start()
        task.action_complete()
        self.assertEqual(task.state, 'done')

        consumed = self.env['hotel.task.supply.consumed'].search([('task_id', '=', task.id)])
        self.assertEqual(len(consumed), 1)
        self.assertEqual(consumed.product_id.id, self.supply.id)
        self.assertEqual(consumed.quantity, 3.0)
