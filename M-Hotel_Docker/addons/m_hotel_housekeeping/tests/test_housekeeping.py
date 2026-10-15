# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase

class TestHotelHousekeeping(TransactionCase):

    def setUp(self):
        super().setUp()
        self.room_type = self.env['hotel.room.type'].create({
            'name': 'Housekeeping Test Type',
            'code': 'HKT',
        })
        self.room = self.env['hotel.room'].create({
            'name': 'P.888',
            'floor': 'Tầng 8',
            'room_type_id': self.room_type.id,
            'status': 'available',
        })

    def test_01_housekeeping_task_lifecycle(self):
        """TC: Vòng đời nhiệm vụ buồng phòng: pending -> in_progress -> done"""
        task = self.env['hotel.housekeeping.task'].create({
            'room_id': self.room.id,
            'task_type': 'checkout_clean',
            'state': 'pending',
        })
        task.action_start()
        self.assertEqual(task.state, 'in_progress')
        self.assertEqual(self.room.status, 'cleaning')

        task.action_complete()
        self.assertEqual(task.state, 'done')
        self.assertEqual(self.room.status, 'available')

    def test_02_incident_block_and_resolve(self):
        """TC: Báo sự cố khóa phòng và mở khóa sau khi sửa xong"""
        incident = self.env['hotel.incident'].create({
            'title': 'Hỏng máy nước nóng',
            'room_id': self.room.id,
            'severity': 'critical',
            'block_room': True,
        })
        self.assertEqual(self.room.status, 'maintenance')

        # Khắc phục xong
        incident.action_resolve()
        self.assertEqual(incident.state, 'resolved')
        self.assertEqual(self.room.status, 'cleaning')
