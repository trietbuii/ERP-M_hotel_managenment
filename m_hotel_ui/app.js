/* ==========================================================================
   M-HOTEL PMS — HOTEL MANAGEMENT SYSTEM ENGINE
   Master JavaScript Application Logic & Interactive State
   ========================================================================== */

// --- INITIAL STATE & MASTER DATA ---
const STATE = {
  currentBranch: 'all',
  activeView: 'dashboard',
  searchQuery: '',
  
  // 1. Branches
  branches: [
    { id: 'b1', name: 'M-Hotel Quy Nhơn Beach', address: '01 Xuân Diệu, TP. Quy Nhơn, Bình Định' },
    { id: 'b2', name: 'M-Hotel Nhơn Lý - Eo Gió', address: 'Xã Nhơn Lý, TP. Quy Nhơn, Bình Định' }
  ],

  // 2. Room Types
  roomTypes: [
    { id: 'RT-STD', name: 'Standard Mountain View', priceNight: 650000, priceHour: 150000, capacity: 2, image: 'assets/room_standard.jpg' },
    { id: 'RT-SUP', name: 'Superior Double', priceNight: 1100000, priceHour: 250000, capacity: 2, image: 'assets/room_standard.jpg' },
    { id: 'RT-DLX', name: 'Deluxe Ocean View', priceNight: 1450000, priceHour: 350000, capacity: 2, image: 'assets/room_deluxe.jpg' },
    { id: 'RT-FAM', name: 'Family Suite', priceNight: 1800000, priceHour: 450000, capacity: 4, image: 'assets/room_family.jpg' },
    { id: 'RT-EXE', name: 'Executive Ocean View', priceNight: 2800000, priceHour: 600000, capacity: 4, image: 'assets/room_deluxe.jpg' }
  ],

  // 3. Rooms (20 Phòng chuẩn PMS)
  rooms: [
    // Chi nhánh 1: M-Hotel Quy Nhơn Beach (14 phòng)
    { id: '101', number: 'P.101', floor: 1, typeId: 'RT-STD', branchId: 'b1', status: 'available', guest: null },
    { id: '102', number: 'P.102', floor: 1, typeId: 'RT-STD', branchId: 'b1', status: 'occupied', guest: 'Trần Thị Bình' },
    { id: '103', number: 'P.103', floor: 1, typeId: 'RT-SUP', branchId: 'b1', status: 'available', guest: null },
    { id: '104', number: 'P.104', floor: 1, typeId: 'RT-SUP', branchId: 'b1', status: 'maintenance', guest: null },
    { id: '105', number: 'P.105', floor: 1, typeId: 'RT-DLX', branchId: 'b1', status: 'cleaning', guest: null },
    
    { id: '201', number: 'P.201', floor: 2, typeId: 'RT-DLX', branchId: 'b1', status: 'confirmed', guest: 'Lê Hoàng Long' },
    { id: '202', number: 'P.202', floor: 2, typeId: 'RT-DLX', branchId: 'b1', status: 'occupied', guest: 'Trần Mai Phương' },
    { id: '203', number: 'P.203', floor: 2, typeId: 'RT-FAM', branchId: 'b1', status: 'available', guest: null },
    { id: '204', number: 'P.204', floor: 2, typeId: 'RT-FAM', branchId: 'b1', status: 'cleaning', guest: null },
    { id: '205', number: 'P.205', floor: 2, typeId: 'RT-EXE', branchId: 'b1', status: 'occupied', guest: 'Vũ Đình Trọng' },

    { id: '301', number: 'P.301', floor: 3, typeId: 'RT-DLX', branchId: 'b1', status: 'occupied', guest: 'Nguyễn Thu Thảo' },
    { id: '302', number: 'P.302', floor: 3, typeId: 'RT-FAM', branchId: 'b1', status: 'confirmed', guest: 'Đoàn Ngọc Hải' },
    { id: '303', number: 'P.303', floor: 3, typeId: 'RT-EXE', branchId: 'b1', status: 'available', guest: null },
    { id: '304', number: 'P.304', floor: 3, typeId: 'RT-EXE', branchId: 'b1', status: 'available', guest: null },

    // Chi nhánh 2: M-Hotel Nhơn Lý - Eo Gió (6 phòng)
    { id: '501', number: 'P.501', floor: 1, typeId: 'RT-STD', branchId: 'b2', status: 'available', guest: null },
    { id: '502', number: 'P.502', floor: 1, typeId: 'RT-SUP', branchId: 'b2', status: 'occupied', guest: 'Cty Saigontourist' },
    { id: '503', number: 'P.503', floor: 1, typeId: 'RT-DLX', branchId: 'b2', status: 'confirmed', guest: 'Nguyễn Thùy Trang' },
    { id: '601', number: 'P.601', floor: 2, typeId: 'RT-FAM', branchId: 'b2', status: 'occupied', guest: 'Hoàng Bách' },
    { id: '602', number: 'P.602', floor: 2, typeId: 'RT-EXE', branchId: 'b2', status: 'available', guest: null },
    { id: '603', number: 'P.603', floor: 2, typeId: 'RT-EXE', branchId: 'b2', status: 'available', guest: null }
  ],

  // 4. Bookings (Đơn Đặt Phòng Mẫu Đa Dạng Nghiệp Vụ)
  bookings: [
    {
      id: 'BK-2026-001',
      customer: 'Nguyễn Văn An',
      phone: '0912 345 678',
      email: 'an.nguyen@gmail.com',
      roomId: '101',
      branchId: 'b1',
      checkIn: '2026-10-13',
      checkOut: '2026-10-13',
      hourDate: '2026-10-13',
      hourStart: '08:00',
      hourEnd: '12:00',
      rentType: 'hour',
      hoursDuration: 4,
      nights: 0,
      totalAmount: 600000,
      depositAmount: 200000,
      status: 'confirmed',
      createdDate: '2026-10-12',
      note: 'Khách đến nghỉ sáng chờ họp tại Quy Nhơn, cần phòng yên tĩnh.'
    },
    {
      id: 'BK-2026-001B',
      customer: 'Phạm Quốc Huy',
      phone: '0938 123 789',
      email: 'huy.pham@gmail.com',
      roomId: '101',
      branchId: 'b1',
      checkIn: '2026-10-13',
      checkOut: '2026-10-13',
      hourDate: '2026-10-13',
      hourStart: '14:00',
      hourEnd: '18:00',
      rentType: 'hour',
      hoursDuration: 4,
      nights: 0,
      totalAmount: 600000,
      depositAmount: 300000,
      status: 'confirmed',
      createdDate: '2026-10-13',
      note: 'Khách nối tiếp lượt chiều tại P.101.'
    },
    {
      id: 'BK-2026-002',
      customer: 'Trần Thị Bình',
      phone: '0905 111 222',
      email: 'binh.tran@yahoo.com',
      roomId: '102',
      branchId: 'b1',
      checkIn: '2026-10-13',
      checkOut: '2026-10-15',
      rentType: 'night',
      nights: 2,
      totalAmount: 1300000,
      depositAmount: 500000,
      status: 'occupied',
      createdDate: '2026-10-11',
      note: 'Khách check-in 14:00 ngày 13/10 đến 12:00 ngày 15/10.'
    },
    {
      id: 'BK-2026-003',
      customer: 'Lê Hoàng Long',
      phone: '0908 777 888',
      email: 'long.le@hoanglongcorp.vn',
      roomId: '201',
      branchId: 'b1',
      checkIn: '2026-10-13',
      checkOut: '2026-10-16',
      rentType: 'night',
      nights: 3,
      totalAmount: 4350000,
      depositAmount: 2000000,
      status: 'confirmed',
      createdDate: '2026-10-11',
      note: 'Khách công tác, chuẩn bị hóa đơn đỏ VAT cho công ty.'
    },
    {
      id: 'BK-2026-004',
      customer: 'Trần Mai Phương',
      phone: '0933 222 111',
      email: 'phuong.tran@gmail.com',
      roomId: '202',
      branchId: 'b1',
      checkIn: '2026-10-11',
      checkOut: '2026-10-14',
      rentType: 'night',
      nights: 3,
      totalAmount: 4350000,
      depositAmount: 4350000,
      status: 'occupied',
      createdDate: '2026-10-09',
      note: 'Gia đình có trẻ nhỏ, yêu cầu thêm 1 nôi em bé.'
    },
    {
      id: 'BK-2026-005',
      customer: 'Vũ Đình Trọng',
      phone: '0978 654 321',
      email: 'trong.vu@outlook.com',
      roomId: '205',
      branchId: 'b1',
      checkIn: '2026-10-13',
      checkOut: '2026-10-15',
      rentType: 'night',
      nights: 2,
      totalAmount: 5600000,
      depositAmount: 3000000,
      status: 'occupied',
      createdDate: '2026-10-12',
      note: 'Khách VIP Executive, hoa quả tươi chào mừng phòng.'
    },
    {
      id: 'BK-2026-006',
      customer: 'Đoàn Ngọc Hải',
      phone: '0918 888 999',
      email: 'hai.doan@gmail.com',
      roomId: '302',
      branchId: 'b1',
      checkIn: '2026-10-14',
      checkOut: '2026-10-17',
      rentType: 'night',
      nights: 3,
      totalAmount: 5400000,
      depositAmount: 2000000,
      status: 'confirmed',
      createdDate: '2026-10-12',
      note: 'Đặt phòng Family 4 người lớn.'
    },
    {
      id: 'BK-2026-007',
      customer: 'Cty Saigontourist',
      phone: '028 3829 5925',
      email: 'booking@saigontourist.com.vn',
      roomId: '502',
      branchId: 'b2',
      checkIn: '2026-10-12',
      checkOut: '2026-10-16',
      rentType: 'night',
      nights: 4,
      totalAmount: 4400000,
      depositAmount: 4400000,
      status: 'occupied',
      createdDate: '2026-10-08',
      note: 'Đoàn tour lữ hành Nhơn Lý - Kỳ Co.'
    },
    {
      id: 'BK-2026-008',
      customer: 'Nguyễn Thùy Trang',
      phone: '0989 123 456',
      email: 'trang.nguyen@vnn.vn',
      roomId: '503',
      branchId: 'b2',
      checkIn: '2026-10-13',
      checkOut: '2026-10-13',
      hourDate: '2026-10-13',
      hourStart: '09:00',
      hourEnd: '13:00',
      rentType: 'hour',
      hoursDuration: 4,
      nights: 0,
      totalAmount: 1400000,
      depositAmount: 500000,
      status: 'confirmed',
      createdDate: '2026-10-12',
      note: 'Nghỉ trưa ngắm biển Eo Gió.'
    },
    {
      id: 'BK-2026-009',
      customer: 'Hoàng Bách',
      phone: '0944 555 666',
      email: 'bach.hoang@musician.vn',
      roomId: '601',
      branchId: 'b2',
      checkIn: '2026-10-12',
      checkOut: '2026-10-15',
      rentType: 'night',
      nights: 3,
      totalAmount: 5400000,
      depositAmount: 3000000,
      status: 'occupied',
      createdDate: '2026-10-10',
      note: 'Khách nghỉ dưỡng Family Suite.'
    },
    {
      id: 'BK-2026-010',
      customer: 'Nguyễn Thu Thảo',
      phone: '0938 999 000',
      email: 'thao.nguyen@fpt.com.vn',
      roomId: '301',
      branchId: 'b1',
      checkIn: '2026-10-13',
      checkOut: '2026-10-13',
      hourDate: '2026-10-13',
      hourStart: '10:00',
      hourEnd: '14:00',
      rentType: 'hour',
      hoursDuration: 4,
      nights: 0,
      totalAmount: 1400000,
      depositAmount: 500000,
      status: 'occupied',
      createdDate: '2026-10-13',
      note: 'Khách đang ở phòng Deluxe theo giờ.'
    },
    {
      id: 'BK-2026-011',
      customer: 'Phạm Minh Tuấn',
      phone: '0903 456 789',
      email: 'tuan.pm@gmail.com',
      roomId: '104',
      branchId: 'b1',
      checkIn: '2026-10-10',
      checkOut: '2026-10-13',
      rentType: 'night',
      nights: 3,
      totalAmount: 3300000,
      depositAmount: 3300000,
      status: 'completed',
      createdDate: '2026-10-08',
      note: 'Khách đã trả phòng sáng 13/10.'
    },
    {
      id: 'BK-2026-012',
      customer: 'Đặng Hồng Nhung',
      phone: '0919 777 666',
      email: 'nhung.dang@vietcombank.com.vn',
      roomId: '203',
      branchId: 'b1',
      checkIn: '2026-10-16',
      checkOut: '2026-10-18',
      rentType: 'night',
      nights: 2,
      totalAmount: 3600000,
      depositAmount: 1500000,
      status: 'confirmed',
      createdDate: '2026-10-13',
      note: 'Đặt trước cuối tuần.'
    },
    {
      id: 'BK-2026-CANCEL',
      customer: 'Bùi Quốc Bảo',
      phone: '0966 888 777',
      email: 'bao.bui@viettel.com.vn',
      roomId: '103',
      branchId: 'b1',
      checkIn: '2026-10-13',
      checkOut: '2026-10-14',
      rentType: 'night',
      nights: 1,
      totalAmount: 1100000,
      depositAmount: 0,
      status: 'cancelled',
      createdDate: '2026-10-11',
      note: 'Khách báo hủy chuyến công tác -> Không chặn lịch phòng.'
    }
  ],

  // 5. Housekeeping Tasks
  housekeeping: [
    { id: 'HK-101', roomId: '104', assignedTo: 'Chị Mai (Tổ 1)', status: 'cleaning', priority: 'Cao', note: 'Khách vừa check-out lúc 10h' },
    { id: 'HK-102', roomId: '204', assignedTo: 'Chị Lan (Tổ 2)', status: 'dirty', priority: 'Trung bình', note: 'Dọn phòng định kỳ đón khách tối' }
  ],

  // 6. Maintenance Issues
  maintenance: [
    { id: 'MT-001', roomId: '101', title: 'Điều hòa Panasonic 12000 BTU không mát', technician: 'Anh Tuấn Kỹ Thuật', priority: 'Khẩn cấp', status: 'in_progress', reportedAt: '12/10/2026' },
    { id: 'MT-002', roomId: '201', title: 'Khóa thẻ từ thông minh Adel yếu pin', technician: 'Anh Dũng', priority: 'Trung bình', status: 'new', reportedAt: '13/10/2026' },
    { id: 'MT-003', roomId: '102', title: 'Tủ lạnh minibar phát tiếng ồn', technician: 'Anh Tuấn Kỹ Thuật', priority: 'Thấp', status: 'resolved', reportedAt: '11/10/2026' }
  ],

  // 7. Customers (CRM)
  customers: [
    { id: 'C01', name: 'Nguyễn Văn An', phone: '0912 345 678', email: 'an.nguyen@gmail.com', type: 'VIP Gold', stays: 5, totalSpend: 16500000 },
    { id: 'C02', name: 'Lê Hoàng Long', phone: '0908 777 888', email: 'long.le@hoanglongcorp.vn', type: 'Doanh nghiệp', stays: 8, totalSpend: 38200000 },
    { id: 'C03', name: 'Trần Mai Phương', phone: '0933 222 111', email: 'phuong.tran@gmail.com', type: 'Khách lẻ', stays: 2, totalSpend: 8700000 },
    { id: 'C04', name: 'Vũ Đình Trọng', phone: '0978 654 321', email: 'trong.vu@outlook.com', type: 'VIP Platinum', stays: 6, totalSpend: 24500000 },
    { id: 'C05', name: 'Cty Saigontourist', phone: '028 3829 5925', email: 'contact@saigontourist.net', type: 'Đại lý lữ hành', stays: 15, totalSpend: 112000000 }
  ],

  // 8. Services
  services: [
    { id: 'SRV-01', name: 'Giặt ủi quần áo cao cấp', price: 80000, unit: 'Lượt / Bộ' },
    { id: 'SRV-02', name: 'Buffet sáng hải sản Quy Nhơn', price: 120000, unit: 'Suất' },
    { id: 'SRV-03', name: 'Thuê xe máy tay ga (AirBlade)', price: 150000, unit: 'Ngày' },
    { id: 'SRV-04', name: 'Đưa đón sân bay Phù Cát', price: 350000, unit: 'Chuyến xe 7 chỗ' },
    { id: 'SRV-05', name: 'Bia Quy Nhơn lon (Minibar)', price: 25000, unit: 'Lon' },
    { id: 'SRV-06', name: 'Bánh tráng nước dừa Tam Quan', price: 45000, unit: 'Gói đặc sản' }
  ],

  // 9. Inventory (Vật tư)
  inventory: [
    { id: 'VT-01', name: 'Bia Quy Nhơn lon (Minibar)', onHand: 120, minLevel: 40, unit: 'Lon', status: 'good' },
    { id: 'VT-02', name: 'Bánh tráng nước dừa Tam Quan', onHand: 60, minLevel: 25, unit: 'Gói', status: 'good' },
    { id: 'VT-03', name: 'Bộ bàn chải tre sinh học', onHand: 350, minLevel: 100, unit: 'Bộ', status: 'good' },
    { id: 'VT-04', name: 'Khăn tắm cotton cao cấp 70x140', onHand: 85, minLevel: 50, unit: 'Chiếc', status: 'good' },
    { id: 'VT-05', name: 'Dầu gội & Sữa tắm thảo mộc 50ml', onHand: 24, minLevel: 50, unit: 'Chai', status: 'low' },
    { id: 'VT-06', name: 'Nước khoáng Đảnh Thạnh 500ml', onHand: 180, minLevel: 60, unit: 'Chai', status: 'good' }
  ],

  // 10. Staff Users & RBAC
  users: [
    { id: 'u1', name: 'Trần Minh Đức', username: 'admin', role: 'manager', email: 'duc.tran@m-hotel.vn', phone: '0903 888 999', branchId: 'all', status: 'active' },
    { id: 'u2', name: 'Nguyễn Thị Thu Hà', username: 'ha_reception', role: 'receptionist', email: 'ha.nguyen@m-hotel.vn', phone: '0912 345 678', branchId: 'b1', status: 'active' },
    { id: 'u3', name: 'Trần Thanh Tâm', username: 'tam_reception', role: 'receptionist', email: 'tam.tran@m-hotel.vn', phone: '0938 111 222', branchId: 'b2', status: 'active' },
    { id: 'u4', name: 'Lê Thị Mai', username: 'mai_housekeeping', role: 'housekeeping', email: 'mai.le@m-hotel.vn', phone: '0989 333 444', branchId: 'b1', status: 'active' },
    { id: 'u5', name: 'Nguyễn Văn Tuấn', username: 'tuan_tech', role: 'technician', email: 'tuan.nguyen@m-hotel.vn', phone: '0977 555 666', branchId: 'all', status: 'active' },
    { id: 'u6', name: 'Phạm Hồng Phúc', username: 'phuc_inventory', role: 'inventory', email: 'phuc.pham@m-hotel.vn', phone: '0908 777 999', branchId: 'b1', status: 'active' }
  ],
  activeRole: 'manager',
  rbacTab: 'users',
  permissionMatrix: [
    { id: 'm1', module: '1. Quản lý Đặt phòng (Bookings & Room Rack)', manager: 'full', receptionist: 'full', housekeeping: 'read', technician: 'lock', inventory: 'lock' },
    { id: 'm2', module: '2. Sơ đồ phòng & Giá phòng (Room Rates)', manager: 'full', receptionist: 'read', housekeeping: 'custom', technician: 'custom', inventory: 'read' },
    { id: 'm3', module: '3. Nhận phòng / Trả phòng (Check-in / Check-out)', manager: 'full', receptionist: 'full', housekeeping: 'lock', technician: 'lock', inventory: 'lock' },
    { id: 'm4', module: '4. Buồng phòng & Vệ sinh (Housekeeping)', manager: 'full', receptionist: 'read', housekeeping: 'full', technician: 'lock', inventory: 'read' },
    { id: 'm5', module: '5. Kỹ thuật & Bảo trì sự cố (Maintenance)', manager: 'full', receptionist: 'custom', housekeeping: 'custom', technician: 'full', inventory: 'custom' },
    { id: 'm6', module: '6. Hồ sơ khách hàng (CRM & Đối tác)', manager: 'full', receptionist: 'custom', housekeeping: 'lock', technician: 'lock', inventory: 'lock' },
    { id: 'm7', module: '7. Kho vật tư & Minibar (Inventory)', manager: 'full', receptionist: 'read', housekeeping: 'custom', technician: 'custom', inventory: 'full' },
    { id: 'm8', module: '8. Báo cáo tài chính & Doanh thu (Reports)', manager: 'full', receptionist: 'lock', housekeeping: 'lock', technician: 'lock', inventory: 'custom' },
    { id: 'm9', module: '9. Cấu hình hệ thống & Phân quyền (Settings / RBAC)', manager: 'full', receptionist: 'lock', housekeeping: 'lock', technician: 'lock', inventory: 'lock' }
  ]
};

// --- HELPER FUNCTIONS ---
function formatVND(amount) {
  return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
}

function showToast(msg, type = 'success') {
  const container = document.getElementById('toast-container');
  if (!container) return;
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerHTML = `
    <span>${type === 'success' ? '✅' : type === 'error' ? '❌' : '⚠️'}</span>
    <span>${msg}</span>
  `;
  container.appendChild(toast);
  setTimeout(() => {
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    toast.style.transition = 'all 0.3s ease';
    setTimeout(() => toast.remove(), 300);
  }, 3500);
}

function getRoomById(id) {
  return STATE.rooms.find(r => r.id === id);
}

function getRoomTypeById(typeId) {
  return STATE.roomTypes.find(rt => rt.id === typeId);
}

function getBranchById(branchId) {
  return STATE.branches.find(b => b.id === branchId);
}

// --- RENDER FUNCTIONS ---

// 1. DASHBOARD
function renderDashboard() {
  const filteredRooms = STATE.rooms.filter(r => STATE.currentBranch === 'all' || r.branchId === STATE.currentBranch);
  const totalRooms = filteredRooms.length;
  const availableRooms = filteredRooms.filter(r => r.status === 'available').length;
  const occupiedRooms = filteredRooms.filter(r => r.status === 'occupied').length;
  const confirmedRooms = filteredRooms.filter(r => r.status === 'confirmed').length;
  const cleaningRooms = filteredRooms.filter(r => r.status === 'cleaning').length;
  const maintenanceRooms = filteredRooms.filter(r => r.status === 'maintenance').length;
  
  // Today bookings
  const today = '2026-10-13';
  const checkInToday = STATE.bookings.filter(b => b.checkIn === today && b.status !== 'cancelled').length;
  const checkOutToday = STATE.bookings.filter(b => b.checkOut === today && b.status !== 'cancelled').length;
  const totalRevenue = STATE.bookings.filter(b => b.status !== 'cancelled').reduce((acc, b) => acc + b.totalAmount, 0);

  // Update KPI Cards
  document.getElementById('kpi-total-rooms').innerText = totalRooms;
  document.getElementById('kpi-available-rooms').innerText = availableRooms;
  document.getElementById('kpi-occupied-rooms').innerText = occupiedRooms;
  document.getElementById('kpi-confirmed-rooms').innerText = confirmedRooms;
  document.getElementById('kpi-cleaning-rooms').innerText = cleaningRooms;
  document.getElementById('kpi-maintenance-rooms').innerText = maintenanceRooms;
  document.getElementById('kpi-checkin-today').innerText = checkInToday;
  document.getElementById('kpi-checkout-today').innerText = checkOutToday;
  document.getElementById('kpi-revenue').innerText = formatVND(totalRevenue);

  // Recent Bookings Table
  const tbody = document.getElementById('recent-bookings-tbody');
  tbody.innerHTML = '';
  STATE.bookings.slice(0, 5).forEach(b => {
    const room = getRoomById(b.roomId);
    const roomType = room ? getRoomTypeById(room.typeId) : null;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${b.id}</strong></td>
      <td>
        <div style="font-weight:600;">${b.customer}</div>
        <small style="color:var(--text-muted);">${b.phone}</small>
      </td>
      <td><span style="font-weight:700; color:var(--primary);">${room ? room.number : ''}</span> (${roomType ? roomType.name : ''})</td>
      <td>${b.checkIn} &rarr; ${b.checkOut} (${b.nights} đêm)</td>
      <td><strong style="color:var(--gold);">${formatVND(b.totalAmount)}</strong></td>
      <td>${renderStatusBadge(b.status)}</td>
      <td>
        <button class="btn-action-icon" title="Xem chi tiết" onclick="viewBookingDetails('${b.id}')">👁️</button>
      </td>
    `;
    tbody.appendChild(tr);
  });

  // Today Schedule List
  const todayList = document.getElementById('today-tasks-list');
  todayList.innerHTML = `
    <div style="display:flex; flex-direction:column; gap:10px;">
      <div style="padding:10px; background:var(--primary-subtle); border-radius:var(--radius-sm); border-left:3px solid var(--primary); display:flex; justify-content:space-between; align-items:center;">
        <div>
          <strong style="font-size:0.84rem; color:var(--primary);">🛎️ Check-in hôm nay (13/10):</strong>
          <p style="font-size:0.78rem; color:var(--text-main); margin-top:2px;">Khách Lê Hoàng Long (P.201) & Vũ Đình Trọng (P.205)</p>
        </div>
        <button class="btn-secondary" style="padding:4px 10px; font-size:0.74rem;" onclick="switchView('checkin')">Xử lý</button>
      </div>
      <div style="padding:10px; background:var(--warning-subtle); border-radius:var(--radius-sm); border-left:3px solid var(--warning); display:flex; justify-content:space-between; align-items:center;">
        <div>
          <strong style="font-size:0.84rem; color:var(--warning);">🧹 Buồng phòng cần dọn:</strong>
          <p style="font-size:0.78rem; color:var(--text-main); margin-top:2px;">Phòng 104 (Khách check-out) & Phòng 204</p>
        </div>
        <button class="btn-secondary" style="padding:4px 10px; font-size:0.74rem;" onclick="switchView('housekeeping')">Điều phối</button>
      </div>
      <div style="padding:10px; background:var(--danger-subtle); border-radius:var(--radius-sm); border-left:3px solid var(--danger); display:flex; justify-content:space-between; align-items:center;">
        <div>
          <strong style="font-size:0.84rem; color:var(--danger);">🔧 Sự cố bảo trì khẩn cấp:</strong>
          <p style="font-size:0.78rem; color:var(--text-main); margin-top:2px;">Điều hòa P.101 không mát (Đang xử lý)</p>
        </div>
        <button class="btn-secondary" style="padding:4px 10px; font-size:0.74rem;" onclick="switchView('maintenance')">Xem</button>
      </div>
    </div>
  `;

  // Draw Charts
  drawOccupancyChart();
}

function renderStatusBadge(status) {
  const map = {
    available: { label: 'Trống / Sẵn sàng', cls: 'badge-available' },
    occupied: { label: 'Đang lưu trú', cls: 'badge-occupied' },
    confirmed: { label: 'Đã xác nhận', cls: 'badge-confirmed' },
    cleaning: { label: 'Đang dọn dẹp', cls: 'badge-cleaning' },
    maintenance: { label: 'Đang bảo trì', cls: 'badge-maintenance' },
    completed: { label: 'Đã trả phòng', cls: 'badge-completed' },
    cancelled: { label: 'Đã hủy', cls: 'badge-cancelled' },
    draft: { label: 'Dự thảo', cls: 'badge-draft' }
  };
  const item = map[status] || { label: status, cls: 'badge-draft' };
  return `<span class="status-badge ${item.cls}"><span class="dot"></span>${item.label}</span>`;
}

// 2. BOOKINGS VIEW
function renderBookings() {
  const tbody = document.getElementById('bookings-tbody');
  tbody.innerHTML = '';
  
  const query = STATE.searchQuery.toLowerCase();
  const filtered = STATE.bookings.filter(b => {
    const matchBranch = STATE.currentBranch === 'all' || b.branchId === STATE.currentBranch;
    const matchQuery = !query || b.id.toLowerCase().includes(query) || b.customer.toLowerCase().includes(query) || b.phone.includes(query);
    return matchBranch && matchQuery;
  });

  filtered.forEach(b => {
    const room = getRoomById(b.roomId);
    const roomType = room ? getRoomTypeById(room.typeId) : null;
    const branch = getBranchById(b.branchId);

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${b.id}</strong></td>
      <td>
        <div style="font-weight:700;">${b.customer}</div>
        <small style="color:var(--text-muted);">${b.phone}</small>
      </td>
      <td><span style="font-size:0.78rem; font-weight:600; color:var(--text-muted);">${branch ? branch.name : ''}</span></td>
      <td><strong style="color:var(--primary);">${room ? room.number : ''}</strong></td>
      <td>
        ${b.rentType === 'hour' 
          ? `<div style="font-weight:700; color:#d97706;">📅 ${b.hourDate || b.checkIn}</div><small style="color:var(--text-muted); font-weight:600;">⏰ ${b.hourStart || '10:00'} &rarr; ${b.hourEnd || '12:00'}</small>` 
          : `<div>${b.checkIn} &rarr; ${b.checkOut}</div><small style="color:var(--text-muted);">${b.nights} đêm</small>`
        }
      </td>
      <td>
        ${b.rentType === 'hour'
          ? `<span class="status-badge" style="background:#fef3c7; color:#d97706; font-weight:700;">⏰ Thuê ${b.hoursDuration || 2} giờ</span>`
          : `<span class="status-badge" style="background:#eff6ff; color:#2563eb; font-weight:700;">🌙 Qua đêm (${b.nights}đ)</span>`
        }
      </td>
      <td><strong style="color:var(--gold);">${formatVND(b.totalAmount)}</strong></td>
      <td>${renderStatusBadge(b.status)}</td>
      <td>
        <div style="display:flex; gap:6px;">
          ${b.status === 'confirmed' ? `<button class="btn-action-icon" title="Check-in ngay" onclick="checkInBooking('${b.id}')" style="color:var(--success);">📥</button>` : ''}
          ${b.status === 'occupied' ? `<button class="btn-action-icon" title="Check-out & Tính tiền" onclick="checkOutBooking('${b.id}')" style="color:var(--danger);">📤</button>` : ''}
          <button class="btn-action-icon" title="Xem chi tiết" onclick="viewBookingDetails('${b.id}')">👁️</button>
          ${b.status !== 'cancelled' && b.status !== 'completed' ? `<button class="btn-action-icon" title="Hủy đặt phòng" onclick="cancelBooking('${b.id}')" style="color:var(--danger);">❌</button>` : ''}
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

// 3. ROOM RACK & TIMELINE PMS ENGINE
STATE.rackMode = 'hour'; // 'hour' (00:00 - 24:00), 'day' (7 ngày), 'month' (tháng)
STATE.rackDate = '2026-10-13';

function setRackMode(mode) {
  STATE.rackMode = mode;
  const btnHour = document.getElementById('btn-rack-hour');
  const btnDay = document.getElementById('btn-rack-day');
  const btnMonth = document.getElementById('btn-rack-month');

  if (btnHour) btnHour.classList.toggle('active', mode === 'hour');
  if (btnDay) btnDay.classList.toggle('active', mode === 'day');
  if (btnMonth) btnMonth.classList.toggle('active', mode === 'month');

  const containerTable = document.getElementById('room-rack-container');
  const containerMonth = document.getElementById('room-month-grid');
  if (containerTable) containerTable.style.display = mode === 'month' ? 'none' : 'block';
  if (containerMonth) containerMonth.style.display = mode === 'month' ? 'grid' : 'none';

  const desc = document.getElementById('rack-view-desc');
  if (desc) {
    if (mode === 'hour') {
      desc.innerText = 'Trục thời gian theo giờ trong ngày (00:00 - 24:00). Hiển thị chi tiết khách thuê theo giờ (màu cam), khách ở qua đêm (màu tím), vạch giờ hiện tại và các ô trống để đặt phòng nhanh.';
    } else if (mode === 'day') {
      desc.innerText = 'Lịch theo tuần (7 ngày). Mỗi dòng là một phòng, thanh đặt phòng kéo dài từ ngày nhận đến ngày trả. Bấm vào tiêu đề ngày để xem tổng kết toàn bộ phòng trong ngày đó.';
    } else {
      desc.innerText = 'Lịch tháng tổng quan. Mỗi ô thể hiện số lượng phòng có lịch và tỷ lệ công suất phòng. Bấm vào một ngày bất kỳ để mở danh sách chi tiết đặt phòng.';
    }
  }

  renderRoomRack();
}

function navigateRackDate(delta) {
  const cur = new Date(STATE.rackDate || '2026-10-13');
  if (STATE.rackMode === 'day') {
    cur.setDate(cur.getDate() + delta * 7);
  } else if (STATE.rackMode === 'month') {
    cur.setMonth(cur.getMonth() + delta);
  } else {
    cur.setDate(cur.getDate() + delta);
  }
  const yyyy = cur.getFullYear();
  const mm = String(cur.getMonth() + 1).padStart(2, '0');
  const dd = String(cur.getDate()).padStart(2, '0');
  STATE.rackDate = `${yyyy}-${mm}-${dd}`;

  const dateInput = document.getElementById('rack-selected-date');
  if (dateInput) dateInput.value = STATE.rackDate;

  renderRoomRack();
}

function todayRackDate() {
  STATE.rackDate = '2026-10-13';
  const dateInput = document.getElementById('rack-selected-date');
  if (dateInput) dateInput.value = STATE.rackDate;
  renderRoomRack();
}

function onRackDateChanged() {
  const dateInput = document.getElementById('rack-selected-date');
  if (dateInput && dateInput.value) {
    STATE.rackDate = dateInput.value;
    renderRoomRack();
  }
}

function updateRackKPIs(roomsToDisplay) {
  const curDate = STATE.rackDate || '2026-10-13';
  const total = roomsToDisplay.length;

  let bookedCount = 0;
  let occupiedCount = 0;
  let blockedCount = 0;

  roomsToDisplay.forEach(r => {
    if (r.status === 'maintenance' || r.status === 'cleaning') {
      blockedCount++;
      return;
    }

    const b = STATE.bookings.find(bk => {
      if (bk.roomId !== r.id || bk.status === 'cancelled') return false;
      if (bk.rentType === 'hour') {
        return (bk.hourDate === curDate || bk.checkIn === curDate);
      } else {
        return (curDate >= bk.checkIn && curDate < bk.checkOut);
      }
    });

    if (b) {
      bookedCount++;
      if (b.status === 'occupied') occupiedCount++;
    }
  });

  const availableCount = Math.max(0, total - bookedCount - blockedCount);

  const elTotal = document.getElementById('rack-kpi-total');
  const elBooked = document.getElementById('rack-kpi-booked');
  const elOccupied = document.getElementById('rack-kpi-occupied');
  const elAvailable = document.getElementById('rack-kpi-available');
  const elBlocked = document.getElementById('rack-kpi-blocked');

  if (elTotal) elTotal.innerText = total;
  if (elBooked) elBooked.innerText = bookedCount;
  if (elOccupied) elOccupied.innerText = occupiedCount;
  if (elAvailable) elAvailable.innerText = availableCount;
  if (elBlocked) elBlocked.innerText = blockedCount;
}

function renderRoomRack() {
  const thead = document.getElementById('room-rack-table-head');
  const tbody = document.getElementById('room-rack-table-body');
  if (!thead || !tbody) return;

  const mode = STATE.rackMode || 'hour';
  const selectedDate = STATE.rackDate || '2026-10-13';

  // Read secondary filters
  const filterBranch = document.getElementById('rack-filter-branch') ? document.getElementById('rack-filter-branch').value : 'all';
  const filterType = document.getElementById('rack-filter-type') ? document.getElementById('rack-filter-type').value : 'all';
  const filterFloor = document.getElementById('rack-filter-floor') ? document.getElementById('rack-filter-floor').value : 'all';
  const filterRentType = document.getElementById('rack-filter-rent-type') ? document.getElementById('rack-filter-rent-type').value : 'all';
  const searchQuery = document.getElementById('rack-search-input') ? document.getElementById('rack-search-input').value.trim().toLowerCase() : '';

  // Filter rooms
  const filteredRooms = STATE.rooms.filter(r => {
    if (filterBranch !== 'all' && r.branchId !== filterBranch) return false;
    if (filterType !== 'all' && r.typeId !== filterType) return false;
    if (filterFloor !== 'all' && String(r.floor) !== filterFloor) return false;
    return true;
  });

  // Update KPI cards
  updateRackKPIs(filteredRooms);

  if (mode === 'hour') {
    // ==========================================
    // 1. LỊCH THEO GIỜ (TIMELINE 00:00 - 24:00)
    // ==========================================
    const hours = [];
    for (let h = 0; h < 24; h++) {
      const hStr = String(h).padStart(2, '0') + ':00';
      const nextH = String((h + 1) % 24).padStart(2, '0') + ':00';
      hours.push({ start: hStr, end: nextH, label: hStr, hourNum: h });
    }

    // Now marker: current simulated hour is 11:00
    const nowHour = 11;

    thead.innerHTML = `
      <tr>
        <th class="rack-room-col">Phòng &amp; Hạng</th>
        ${hours.map(h => `
          <th class="${h.hourNum === nowHour ? 'now-column' : ''}" style="min-width:56px; font-size:0.72rem; padding:6px 2px;">
            ${h.label}
            ${h.hourNum === nowHour ? '<div style="font-size:0.58rem; color:#d97706; font-weight:800;">Hiện tại</div>' : ''}
          </th>
        `).join('')}
      </tr>
    `;

    tbody.innerHTML = '';
    filteredRooms.forEach(r => {
      const roomType = getRoomTypeById(r.typeId);

      // Check if matches rentType or search query
      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="rack-room-col">
          <div style="display:flex; align-items:center; justify-content:space-between;">
            <span style="font-weight:800; font-size:0.92rem; color:var(--text-main);">${r.number}</span>
            <span style="font-size:0.68rem; padding:2px 6px; border-radius:3px; background:#f1f5f9; color:var(--text-muted); font-weight:700;">T.${r.floor}</span>
          </div>
          <div style="font-size:0.7rem; color:var(--text-muted); margin-top:1px;">${roomType ? roomType.name.split(' ')[0] + ' ' + (roomType.name.split(' ')[1] || '') : ''}</div>
          <div style="font-size:0.68rem; color:var(--gold); font-weight:700;">${formatVND(roomType ? roomType.priceHour : 0)}/h</div>
        </td>
        ${hours.map(h => {
          // 1. Bảo trì
          if (r.status === 'maintenance') {
            return `<td class="rack-cell" style="background:#fef2f2;"><div class="rack-bar" style="background:#dc2626; font-size:0.65rem;">Bảo trì</div></td>`;
          }

          // 2. Chờ dọn phòng
          if (r.status === 'cleaning' && h.hourNum < 12) {
            return `<td class="rack-cell" style="background:#fefce8;"><div class="rack-bar" style="background:#ca8a04; font-size:0.65rem;">Chờ dọn</div></td>`;
          }

          // 3. Khách thuê qua đêm (bao phủ cả ngày nếu ngày rơi vào [checkIn, checkOut))
          const overnightBooking = STATE.bookings.find(b => {
            if (b.roomId !== r.id || b.status === 'cancelled' || b.rentType === 'hour') return false;
            return (selectedDate >= b.checkIn && selectedDate < b.checkOut);
          });

          if (overnightBooking && (filterRentType === 'all' || filterRentType === 'night')) {
            const isMatchSearch = !searchQuery || overnightBooking.customer.toLowerCase().includes(searchQuery) || overnightBooking.id.toLowerCase().includes(searchQuery);
            if (isMatchSearch) {
              const bg = overnightBooking.status === 'occupied' ? '#8b5cf6' : '#2563eb';
              return `
                <td class="rack-cell ${h.hourNum === nowHour ? 'now-column' : ''}" onclick="viewBookingDetails('${overnightBooking.id}')" title="Khách ở qua đêm: ${overnightBooking.customer} (${overnightBooking.checkIn} - ${overnightBooking.checkOut})">
                  <div class="rack-bar" style="background:${bg}; font-size:0.66rem; opacity:0.92;">
                    ${h.hourNum === 8 ? `🌙 ${overnightBooking.customer.split(' ').slice(-1)[0]} (Đêm)` : ''}
                  </div>
                </td>
              `;
            }
          }

          // 4. Khách thuê theo giờ trong khung giờ này
          const hourlyBooking = STATE.bookings.find(b => {
            if (b.roomId !== r.id || b.status === 'cancelled' || b.rentType !== 'hour') return false;
            const bDate = b.hourDate || b.checkIn;
            if (bDate !== selectedDate) return false;
            return (h.start < b.hourEnd && h.end > b.hourStart);
          });

          if (hourlyBooking && (filterRentType === 'all' || filterRentType === 'hour')) {
            const isMatchSearch = !searchQuery || hourlyBooking.customer.toLowerCase().includes(searchQuery) || hourlyBooking.id.toLowerCase().includes(searchQuery);
            if (isMatchSearch) {
              const [bStartH] = (hourlyBooking.hourStart || '08:00').split(':').map(Number);
              const isStartCol = (h.hourNum === bStartH);
              return `
                <td class="rack-cell ${h.hourNum === nowHour ? 'now-column' : ''}" onclick="viewBookingDetails('${hourlyBooking.id}')" title="Thuê theo giờ: ${hourlyBooking.customer} (${hourlyBooking.hourStart} - ${hourlyBooking.hourEnd})">
                  <div class="rack-bar" style="background:#d97706; font-size:0.67rem; box-shadow:0 2px 4px rgba(217,119,6,0.35);">
                    ${isStartCol ? `⏰ ${hourlyBooking.customer.split(' ').slice(-1)[0]} (${hourlyBooking.hourStart}-${hourlyBooking.hourEnd})` : ''}
                  </div>
                </td>
              `;
            }
          }

          // 5. Ô trống lúc khung giờ này -> Nhấn để tạo booking theo giờ
          return `
            <td class="rack-cell ${h.hourNum === nowHour ? 'now-column' : ''}" onclick="openHourlyBookingModalForSlot('${r.id}', '${selectedDate}', '${h.start}')" title="Phòng trống lúc ${h.start} ngày ${selectedDate} - Nhấn để đặt nhanh">
              <span style="color:#cbd5e1; font-size:0.7rem;">+ Trống</span>
            </td>
          `;
        }).join('')}
      `;
      tbody.appendChild(tr);
    });

  } else if (mode === 'day') {
    // ==========================================
    // 2. LỊCH THEO TUẦN (7 NGÀY LIÊN TIẾP)
    // ==========================================
    const startDate = new Date(selectedDate);
    const dayOfWeek = startDate.getDay(); // 0 is Sunday, 1 is Monday
    // Align to Monday
    const mondayOffset = (dayOfWeek === 0 ? -6 : 1 - dayOfWeek);
    const monday = new Date(startDate);
    monday.setDate(startDate.getDate() + mondayOffset);

    const weekDates = [];
    const weekDaysName = ['T2', 'T3', 'T4', 'T5', 'T6', 'T7', 'CN'];
    for (let i = 0; i < 7; i++) {
      const d = new Date(monday);
      d.setDate(monday.getDate() + i);
      const yyyy = d.getFullYear();
      const mm = String(d.getMonth() + 1).padStart(2, '0');
      const dd = String(d.getDate()).padStart(2, '0');
      const dateStr = `${yyyy}-${mm}-${dd}`;
      weekDates.push({
        date: dateStr,
        label: `${weekDaysName[i]} (${dd}/${mm})`,
        isToday: dateStr === '2026-10-13',
        isSelected: dateStr === selectedDate
      });
    }

    thead.innerHTML = `
      <tr>
        <th class="rack-room-col">Phòng &amp; Hạng</th>
        ${weekDates.map(w => `
          <th style="min-width:130px; cursor:pointer; ${w.isToday ? 'background:#eff6ff; color:var(--primary); font-weight:800;' : ''}" onclick="openDaySummaryModal('${w.date}')" title="Bấm để xem chi tiết lịch phòng ngày ${w.date}">
            <div>${w.label}</div>
            <div style="font-size:0.62rem; color:var(--primary); font-weight:600; text-decoration:underline;">📋 Xem ngày</div>
          </th>
        `).join('')}
      </tr>
    `;

    tbody.innerHTML = '';
    filteredRooms.forEach(r => {
      const roomType = getRoomTypeById(r.typeId);

      const tr = document.createElement('tr');
      tr.innerHTML = `
        <td class="rack-room-col">
          <div style="font-weight:800; font-size:0.92rem; color:var(--text-main);">${r.number}</div>
          <div style="font-size:0.72rem; color:var(--text-muted);">${roomType ? roomType.name : ''}</div>
          <div style="font-size:0.68rem; color:var(--primary); font-weight:700;">${formatVND(roomType ? roomType.priceNight : 0)}/đêm</div>
        </td>
        ${weekDates.map(w => {
          if (r.status === 'maintenance') {
            return `<td class="rack-cell" style="background:#fef2f2;"><div class="rack-bar" style="background:#dc2626;">Bảo trì</div></td>`;
          }

          // Kiểm tra khách thuê theo giờ trong ngày này
          const hourlyBooking = STATE.bookings.find(b => b.roomId === r.id && b.status !== 'cancelled' && b.rentType === 'hour' && (b.hourDate === w.date || b.checkIn === w.date));
          if (hourlyBooking && (filterRentType === 'all' || filterRentType === 'hour')) {
            return `
              <td class="rack-cell" onclick="viewBookingDetails('${hourlyBooking.id}')" title="Thuê theo giờ: ${hourlyBooking.customer} (${hourlyBooking.hourStart} - ${hourlyBooking.hourEnd})">
                <div class="rack-bar" style="background:#d97706; box-shadow:0 2px 4px rgba(217, 119, 6, 0.35);">
                  ⏰ ${hourlyBooking.customer.split(' ').slice(-1)[0]} (${hourlyBooking.hourStart}-${hourlyBooking.hourEnd})
                </div>
              </td>
            `;
          }

          // Kiểm tra khách thuê theo đêm
          const booking = STATE.bookings.find(b => b.roomId === r.id && b.status !== 'cancelled' && b.rentType !== 'hour' && w.date >= b.checkIn && w.date < b.checkOut);
          if (booking && (filterRentType === 'all' || filterRentType === 'night')) {
            const bg = booking.status === 'occupied' ? '#8b5cf6' : '#2563eb';
            return `
              <td class="rack-cell" onclick="viewBookingDetails('${booking.id}')" title="Khách qua đêm: ${booking.customer} (${booking.checkIn} - ${booking.checkOut})">
                <div class="rack-bar" style="background:${bg};">
                  🌙 ${booking.customer}
                </div>
              </td>
            `;
          }

          // Ô trống
          return `
            <td class="rack-cell" onclick="openNewBookingModal('${r.id}', '${w.date}')" title="Trống ngày ${w.date} - Bấm để đặt phòng">
              <span style="color:#94a3b8; font-size:0.75rem;">+ Trống</span>
            </td>
          `;
        }).join('')}
      `;
      tbody.appendChild(tr);
    });

  } else if (mode === 'month') {
    // ==========================================
    // 3. LỊCH THÁNG (MONTH VIEW GRID)
    // ==========================================
    const monthContainer = document.getElementById('room-month-grid');
    if (!monthContainer) return;
    monthContainer.innerHTML = '';

    const cur = new Date(selectedDate);
    const curYear = cur.getFullYear();
    const curMonth = cur.getMonth(); // 0-indexed
    const daysInMonth = new Date(curYear, curMonth + 1, 0).getDate();

    const weekDays = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'Chủ nhật'];
    
    // Header for week days
    weekDays.forEach(wd => {
      const hEl = document.createElement('div');
      hEl.style.fontWeight = '800';
      hEl.style.fontSize = '0.8rem';
      hEl.style.textAlign = 'center';
      hEl.style.color = 'var(--text-muted)';
      hEl.style.padding = '4px';
      hEl.innerText = wd;
      monthContainer.appendChild(hEl);
    });

    const totalRooms = STATE.rooms.length;

    for (let day = 1; day <= daysInMonth; day++) {
      const dStr = `${curYear}-${String(curMonth + 1).padStart(2, '0')}-${String(day).padStart(2, '0')}`;
      
      // Calculate bookings on this date
      let bookedCount = 0;
      STATE.rooms.forEach(r => {
        if (r.status === 'maintenance') return;
        const b = STATE.bookings.find(bk => {
          if (bk.roomId !== r.id || bk.status === 'cancelled') return false;
          if (bk.rentType === 'hour') return (bk.hourDate === dStr || bk.checkIn === dStr);
          return (dStr >= bk.checkIn && dStr < bk.checkOut);
        });
        if (b) bookedCount++;
      });

      const occupancyRate = Math.round((bookedCount / totalRooms) * 100);
      const isToday = (dStr === '2026-10-13');

      const card = document.createElement('div');
      card.className = `month-day-card ${isToday ? 'today' : ''}`;
      card.onclick = () => openDaySummaryModal(dStr);
      card.innerHTML = `
        <div class="month-day-header">
          <span>Ngày ${day}</span>
          ${isToday ? '<span class="status-badge" style="background:#2563eb; color:#fff; font-size:0.65rem; padding:2px 5px;">Hôm nay</span>' : ''}
        </div>
        <div class="month-day-stats">
          <div style="font-weight:700; color:var(--text-main); font-size:0.8rem;">${bookedCount} / ${totalRooms} phòng</div>
          <div style="font-size:0.7rem; color:var(--text-muted);">Công suất: ${occupancyRate}%</div>
          <div class="month-progress-bar">
            <div class="month-progress-fill" style="width:${occupancyRate}%; background:${occupancyRate > 70 ? '#dc2626' : occupancyRate > 40 ? '#2563eb' : '#10b981'};"></div>
          </div>
        </div>
        <div class="month-day-sub" style="font-size:0.7rem; color:var(--primary); font-weight:700;">
          📋 Bấm xem chi tiết &rarr;
        </div>
      `;
      monthContainer.appendChild(card);
    }
  }
}

// 4. DAY SUMMARY MODAL (CHI TIẾT LỊCH PHÒNG TRONG NGÀY)
function openDaySummaryModal(dateStr) {
  const date = dateStr || STATE.rackDate || '2026-10-13';
  const modal = document.getElementById('day-summary-modal');
  if (!modal) return;

  const d = new Date(date);
  const weekDayNames = ['Chủ nhật', 'Thứ Hai', 'Thứ Ba', 'Thứ Tư', 'Thứ Năm', 'Thứ Sáu', 'Thứ Bảy'];
  const weekDay = weekDayNames[d.getDay()] || 'Thứ';

  const [yyyy, mm, dd] = date.split('-');
  const displayDate = `${dd}/${mm}/${yyyy}`;

  const titleEl = document.getElementById('day-summary-modal-title');
  const subEl = document.getElementById('day-summary-modal-sub');
  if (titleEl) titleEl.innerText = `Lịch phòng — ${displayDate}`;
  if (subEl) subEl.innerText = `${weekDay} · Chi tiết 20 phòng và các đơn lưu trú trong ngày`;

  // Calculate day stats
  const total = STATE.rooms.length;
  let bookedCount = 0;
  let blockedCount = 0;

  STATE.rooms.forEach(r => {
    if (r.status === 'maintenance' || r.status === 'cleaning') {
      blockedCount++;
      return;
    }
    const b = STATE.bookings.find(bk => {
      if (bk.roomId !== r.id || bk.status === 'cancelled') return false;
      if (bk.rentType === 'hour') return (bk.hourDate === date || bk.checkIn === date);
      return (date >= bk.checkIn && date < bk.checkOut);
    });
    if (b) bookedCount++;
  });

  const emptyCount = Math.max(0, total - bookedCount - blockedCount);

  if (document.getElementById('day-stat-total')) document.getElementById('day-stat-total').innerText = total;
  if (document.getElementById('day-stat-booked')) document.getElementById('day-stat-booked').innerText = bookedCount;
  if (document.getElementById('day-stat-empty')) document.getElementById('day-stat-empty').innerText = emptyCount;
  if (document.getElementById('day-stat-blocked')) document.getElementById('day-stat-blocked').innerText = blockedCount;

  // Render rooms list
  const container = document.getElementById('day-room-list-container');
  if (container) {
    container.innerHTML = '';

    STATE.rooms.forEach(r => {
      const roomType = getRoomTypeById(r.typeId);
      const branch = getBranchById(r.branchId);

      // Check bookings for this room on this date
      const roomBookings = STATE.bookings.filter(b => {
        if (b.roomId !== r.id || b.status === 'cancelled') return false;
        if (b.rentType === 'hour') return (b.hourDate === date || b.checkIn === date);
        return (date >= b.checkIn && date < b.checkOut);
      });

      const item = document.createElement('div');
      item.className = 'day-room-item';

      if (r.status === 'maintenance') {
        item.innerHTML = `
          <div class="day-room-left">
            <div class="day-room-num-badge" style="background:#dc2626;">
              ${r.number}
              <small>Bảo trì</small>
            </div>
            <div class="day-room-info">
              <div class="day-room-title">${roomType ? roomType.name : ''} — Tầng ${r.floor}</div>
              <div class="day-room-time-desc" style="color:#dc2626; font-weight:700;">🛠️ Đang sửa chữa kỹ thuật / Không khả dụng</div>
            </div>
          </div>
          <div class="day-room-right">
            <span class="status-badge badge-maintenance">Đang bảo trì</span>
          </div>
        `;
      } else if (roomBookings.length > 0) {
        // Có 1 hoặc nhiều booking trong ngày (ví dụ ca theo giờ)
        item.innerHTML = `
          <div class="day-room-left">
            <div class="day-room-num-badge" style="background:${roomBookings[0].rentType === 'hour' ? '#d97706' : '#2563eb'};">
              ${r.number}
              <small>${roomBookings[0].rentType === 'hour' ? 'Theo giờ' : 'Qua đêm'}</small>
            </div>
            <div class="day-room-info">
              ${roomBookings.map(bk => `
                <div style="margin-bottom:4px;">
                  <span class="day-room-title">${bk.customer}</span>
                  <span style="font-size:0.75rem; color:var(--text-muted); margin-left:6px;">(${bk.phone})</span>
                  <div class="day-room-time-desc">
                    ${bk.rentType === 'hour' 
                      ? `<strong style="color:#d97706;">⏰ ${bk.hourStart} &rarr; ${bk.hourEnd}</strong> · Đặt theo giờ (${bk.hoursDuration || 2}h)` 
                      : `<strong style="color:#2563eb;">🌙 ${bk.checkIn} &rarr; ${bk.checkOut}</strong> · Đặt theo đêm (${bk.nights} đêm)`
                    }
                  </div>
                </div>
              `).join('')}
            </div>
          </div>
          <div class="day-room-right">
            ${renderStatusBadge(roomBookings[0].status)}
            <button class="btn-secondary btn-sm" onclick="closeDaySummaryModal(); viewBookingDetails('${roomBookings[0].id}')" style="padding:6px 10px; font-size:0.78rem;">👁️ Xem đơn</button>
          </div>
        `;
      } else {
        // Phòng trống lịch trong ngày
        item.innerHTML = `
          <div class="day-room-left">
            <div class="day-room-num-badge" style="background:#0f172a;">
              ${r.number}
              <small>Tầng ${r.floor}</small>
            </div>
            <div class="day-room-info">
              <div class="day-room-title">${roomType ? roomType.name : ''}</div>
              <div class="day-room-time-desc" style="color:#10b981; font-weight:700;">🟢 Chưa có lịch đặt trong ngày · Phòng trống sẵn sàng</div>
            </div>
          </div>
          <div class="day-room-right">
            <span class="status-badge badge-available">Trống lịch</span>
            <button class="btn-primary-action btn-sm" onclick="closeDaySummaryModal(); openNewBookingModal('${r.id}', '${date}')" style="padding:6px 12px; font-size:0.78rem;">➕ Đặt phòng</button>
          </div>
        `;
      }

      container.appendChild(item);
    });
  }

  modal.classList.add('active');
}

function closeDaySummaryModal() {
  const modal = document.getElementById('day-summary-modal');
  if (modal) modal.classList.remove('active');
}

function openNewBookingForDate(date) {
  closeDaySummaryModal();
  openNewBookingModal(null, date);
}

// 5. BOOKING DETAIL MODAL (CHI TIẾT ĐƠN ĐẶT PHÒNG)
function viewBookingDetails(bookingId) {
  const booking = STATE.bookings.find(b => b.id === bookingId);
  if (!booking) {
    showToast('Không tìm thấy thông tin đơn đặt phòng!', 'error');
    return;
  }

  const room = getRoomById(booking.roomId);
  const roomType = room ? getRoomTypeById(room.typeId) : null;
  const branch = getBranchById(booking.branchId);

  const modal = document.getElementById('booking-detail-modal');
  const codeEl = document.getElementById('booking-detail-code');
  const bodyEl = document.getElementById('booking-detail-body');
  const footerEl = document.getElementById('booking-detail-footer');

  if (codeEl) codeEl.innerText = `${booking.id} — ${booking.rentType === 'hour' ? '⏰ Thuê theo Giờ' : '🌙 Thuê theo Đêm'}`;

  if (bodyEl) {
    bodyEl.innerHTML = `
      <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:14px; background:#f8fafc; padding:10px 14px; border-radius:var(--radius-sm); border:1px solid var(--border-color);">
        <div>
          <span style="font-size:0.75rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Trạng thái đơn:</span>
          <div style="margin-top:2px;">${renderStatusBadge(booking.status)}</div>
        </div>
        <div style="text-align:right;">
          <span style="font-size:0.75rem; color:var(--text-muted); font-weight:700; text-transform:uppercase;">Ngày tạo:</span>
          <div style="font-weight:700; color:var(--text-main); font-size:0.85rem;">${booking.createdDate || '12/10/2026'}</div>
        </div>
      </div>

      <div class="booking-detail-grid">
        <div class="booking-detail-card">
          <h4>👤 Thông tin Khách hàng</h4>
          <div class="detail-row"><span>Họ và tên:</span><span>${booking.customer}</span></div>
          <div class="detail-row"><span>Số điện thoại:</span><span>${booking.phone}</span></div>
          <div class="detail-row"><span>Email liên hệ:</span><span>${booking.email || 'khachhang@m-hotel.vn'}</span></div>
          <div class="detail-row"><span>Hạng thành viên:</span><span style="color:var(--gold);">VIP Khách sạn</span></div>
        </div>

        <div class="booking-detail-card">
          <h4>🏨 Thông tin Phòng lưu trú</h4>
          <div class="detail-row"><span>Số phòng:</span><strong style="color:var(--primary); font-size:0.95rem;">${room ? room.number : ''}</strong></div>
          <div class="detail-row"><span>Hạng phòng:</span><span>${roomType ? roomType.name : ''}</span></div>
          <div class="detail-row"><span>Chi nhánh:</span><span>${branch ? branch.name : ''}</span></div>
          <div class="detail-row"><span>Vị trí:</span><span>Tầng ${room ? room.floor : 1}</span></div>
        </div>
      </div>

      <div class="booking-detail-grid">
        <div class="booking-detail-card">
          <h4>⏱️ Thời gian lưu trú</h4>
          <div class="detail-row"><span>Hình thức thuê:</span><span>${booking.rentType === 'hour' ? '⏰ Thuê theo giờ' : '🌙 Thuê qua đêm'}</span></div>
          ${booking.rentType === 'hour' ? `
            <div class="detail-row"><span>Ngày thuê:</span><span>${booking.hourDate || booking.checkIn}</span></div>
            <div class="detail-row"><span>Giờ nhận phòng:</span><strong style="color:#d97706;">${booking.hourStart || '10:00'}</strong></div>
            <div class="detail-row"><span>Giờ trả phòng:</span><strong style="color:#d97706;">${booking.hourEnd || '12:00'}</strong></div>
            <div class="detail-row"><span>Số giờ thuê:</span><span>${booking.hoursDuration || 2} giờ</span></div>
          ` : `
            <div class="detail-row"><span>Ngày nhận (Check-in):</span><strong>${booking.checkIn} (14:00)</strong></div>
            <div class="detail-row"><span>Ngày trả (Check-out):</span><strong>${booking.checkOut} (12:00)</strong></div>
            <div class="detail-row"><span>Tổng số đêm:</span><span>${booking.nights} đêm</span></div>
          `}
        </div>

        <div class="booking-detail-card">
          <h4>💳 Chi phí &amp; Thanh toán</h4>
          <div class="detail-row"><span>Đơn giá niêm yết:</span><span>${formatVND(booking.rentType === 'hour' ? (roomType ? roomType.priceHour : 0) : (roomType ? roomType.priceNight : 0))}</span></div>
          <div class="detail-row"><span>Tiền cọc đã nhận:</span><span style="color:#10b981;">${formatVND(booking.depositAmount || 0)}</span></div>
          <div class="detail-row"><span>Còn phải thu:</span><span style="color:#ef4444; font-weight:800;">${formatVND(Math.max(0, booking.totalAmount - (booking.depositAmount || 0)))}</span></div>
          <div class="detail-row" style="border-top:1px dashed #cbd5e1; padding-top:6px; margin-top:6px;">
            <span>TỔNG THANH TOÁN:</span>
            <strong style="color:var(--primary); font-size:1.05rem;">${formatVND(booking.totalAmount)}</strong>
          </div>
        </div>
      </div>

      <div style="background:#f8fafc; border:1px solid var(--border-color); border-radius:var(--radius-sm); padding:10px 14px;">
        <span style="font-size:0.75rem; font-weight:700; color:var(--text-muted); text-transform:uppercase;">📝 Ghi chú yêu cầu của khách:</span>
        <p style="font-size:0.82rem; color:var(--text-main); margin-top:3px;">${booking.note || 'Không có yêu cầu đặc biệt.'}</p>
      </div>
    `;
  }

  if (footerEl) {
    footerEl.innerHTML = `
      <div style="display:flex; justify-content:space-between; width:100%; align-items:center;">
        <div>
          ${booking.status !== 'cancelled' && booking.status !== 'completed' ? `
            <button class="btn-secondary" onclick="cancelBooking('${booking.id}')" style="color:var(--danger); border-color:#fca5a5;">❌ Hủy đơn này</button>
          ` : ''}
        </div>
        <div style="display:flex; gap:8px;">
          <button class="btn-secondary" onclick="printBooking('${booking.id}')">🖨️ In hóa đơn</button>
          ${booking.status === 'confirmed' ? `
            <button class="btn-primary-action" onclick="checkInBooking('${booking.id}')" style="background:var(--success);">📥 Check-in Nhận phòng</button>
          ` : ''}
          ${booking.status === 'occupied' ? `
            <button class="btn-primary-action" onclick="checkOutBooking('${booking.id}')" style="background:var(--danger);">📤 Check-out Trả phòng</button>
          ` : ''}
          <button class="btn-secondary" onclick="closeBookingDetailModal()">Đóng</button>
        </div>
      </div>
    `;
  }

  if (modal) modal.classList.add('active');
}

function closeBookingDetailModal() {
  const modal = document.getElementById('booking-detail-modal');
  if (modal) modal.classList.remove('active');
}

function checkInBooking(bookingId) {
  const b = STATE.bookings.find(bk => bk.id === bookingId);
  if (!b) return;
  b.status = 'occupied';
  const r = getRoomById(b.roomId);
  if (r) {
    r.status = 'occupied';
    r.guest = b.customer;
  }
  showToast(`Check-in thành công cho khách [${b.customer}] vào phòng ${r ? r.number : ''}!`, 'success');
  closeBookingDetailModal();
  refreshActiveView();
}

function checkOutBooking(bookingId) {
  const b = STATE.bookings.find(bk => bk.id === bookingId);
  if (!b) return;
  b.status = 'completed';
  const r = getRoomById(b.roomId);
  if (r) {
    r.status = 'cleaning';
    r.guest = null;
  }
  // Thêm sự vụ buồng phòng tự động
  STATE.housekeeping.push({
    id: `HK-${Date.now()}`,
    roomId: b.roomId,
    assignedTo: 'Đội buồng phòng trực',
    status: 'dirty',
    priority: 'Cao',
    note: `Dọn dẹp phòng sau khi khách ${b.customer} check-out đơn ${b.id}`
  });
  showToast(`Check-out thành công đơn [${b.id}]. Phòng ${r ? r.number : ''} đã chuyển sang trạng thái CHỜ DỌN DẸP!`, 'success');
  closeBookingDetailModal();
  refreshActiveView();
}

function cancelBooking(bookingId) {
  const b = STATE.bookings.find(bk => bk.id === bookingId);
  if (!b) return;
  if (!confirm(`Bạn có chắc chắn muốn hủy đơn đặt phòng [${b.id}] của khách ${b.customer}?`)) return;

  b.status = 'cancelled';
  const r = getRoomById(b.roomId);
  if (r && r.status === 'confirmed') {
    r.status = 'available';
  }
  showToast(`Đã hủy đơn [${b.id}]. Phòng ${r ? r.number : ''} đã được giải phóng trên lịch!`, 'info');
  closeBookingDetailModal();
  refreshActiveView();
}

function printBooking(bookingId) {
  const b = STATE.bookings.find(bk => bk.id === bookingId);
  if (!b) return;
  showToast(`Đang gửi lệnh in phiếu xác nhận đơn [${b.id}] tới máy in nhiệt lễ tân...`, 'info');
}

function openHourlyBookingModalForSlot(roomId, date, startTime) {
  openNewBookingModal(roomId, date);
  const rentTypeSelect = document.getElementById('modal-rent-type');
  if (rentTypeSelect) {
    rentTypeSelect.value = 'hour';
    toggleRentTypeFields();
  }
  const dateInput = document.getElementById('modal-hour-date');
  if (dateInput) dateInput.value = date;
  const timeInput = document.getElementById('modal-hour-time');
  if (timeInput) timeInput.value = startTime;
  calculateModalPrice();
}

// 4. ROOMS (KANBAN & LIST)
function renderRooms() {
  const kanbanGrid = document.getElementById('rooms-kanban-grid');
  kanbanGrid.innerHTML = '';

  const filtered = STATE.rooms.filter(r => STATE.currentBranch === 'all' || r.branchId === STATE.currentBranch);

  filtered.forEach(r => {
    const roomType = getRoomTypeById(r.typeId);
    const branch = getBranchById(r.branchId);
    const card = document.createElement('div');
    card.className = 'room-card';
    card.innerHTML = `
      <div class="room-card-img-wrap">
        <img class="room-card-img" src="${roomType ? roomType.image : 'assets/room_standard.jpg'}" alt="${r.number}" />
        <div class="room-card-status-tag">${renderStatusBadge(r.status)}</div>
      </div>
      <div class="room-card-body">
        <div class="room-card-header">
          <div class="room-number">${r.number}</div>
          <div class="room-price">${formatVND(roomType ? roomType.priceNight : 0)}<small style="font-size:0.7rem; color:var(--text-muted);">/đêm</small></div>
        </div>
        <div class="room-type-label">${roomType ? roomType.name : ''} &bull; Tầng ${r.floor}</div>
        <div style="margin-top:10px; font-size:0.8rem; color:var(--text-muted);">
          ${r.guest ? `👤 Khách đang ở: <strong>${r.guest}</strong>` : '✨ Phòng sẵn sàng phục vụ'}
        </div>
      </div>
      <div class="room-card-footer">
        <span>📍 ${branch ? branch.name : ''}</span>
        <button class="btn-secondary" style="padding:4px 10px; font-size:0.74rem;" onclick="openNewBookingModal('${r.id}')">Đặt phòng</button>
      </div>
    `;
    kanbanGrid.appendChild(card);
  });
}

// 5. HOUSEKEEPING (BUỒNG PHÒNG)
function renderHousekeeping() {
  const tbody = document.getElementById('housekeeping-tbody');
  tbody.innerHTML = '';

  STATE.housekeeping.forEach(h => {
    const room = getRoomById(h.roomId);
    const roomType = room ? getRoomTypeById(room.typeId) : null;
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${h.id}</strong></td>
      <td><strong style="color:var(--primary); font-size:1.05rem;">${room ? room.number : ''}</strong> (${roomType ? roomType.name : ''})</td>
      <td>${h.assignedTo}</td>
      <td><span style="color:${h.priority === 'Cao' ? 'var(--danger)' : 'var(--text-muted)'}; font-weight:700;">${h.priority}</span></td>
      <td>${h.note}</td>
      <td>${h.status === 'cleaning' ? '<span class="status-badge badge-cleaning"><span class="dot"></span>Đang dọn dẹp</span>' : '<span class="status-badge badge-draft"><span class="dot"></span>Chờ dọn dẹp</span>'}</td>
      <td>
        ${h.status === 'cleaning'
          ? `<button class="btn-primary-action" style="padding:6px 12px; font-size:0.76rem;" onclick="finishCleaning('${h.id}', '${h.roomId}')">✅ Hoàn thành</button>`
          : `<button class="btn-secondary" style="padding:6px 12px; font-size:0.76rem;" onclick="startCleaning('${h.id}')">🧹 Bắt đầu dọn</button>`
        }
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function startCleaning(hkId) {
  const task = STATE.housekeeping.find(t => t.id === hkId);
  if (task) {
    task.status = 'cleaning';
    showToast(`Nhân viên đã bắt đầu dọn phòng ${task.roomId}!`, 'info');
    renderHousekeeping();
  }
}

function finishCleaning(hkId, roomId) {
  STATE.housekeeping = STATE.housekeeping.filter(t => t.id !== hkId);
  const room = getRoomById(roomId);
  if (room) {
    room.status = 'available';
    room.guest = null;
  }
  showToast(`Phòng ${room ? room.number : ''} đã dọn sạch và chuyển sang trạng thái SẴN SÀNG!`, 'success');
  renderHousekeeping();
  renderDashboard();
  renderRooms();
}

// 6. MAINTENANCE (BẢO TRÌ)
function renderMaintenance() {
  const tbody = document.getElementById('maintenance-tbody');
  tbody.innerHTML = '';

  STATE.maintenance.forEach(m => {
    const room = getRoomById(m.roomId);
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${m.id}</strong></td>
      <td><strong style="color:var(--danger);">${room ? room.number : ''}</strong></td>
      <td><strong>${m.title}</strong></td>
      <td>${m.technician}</td>
      <td><span style="font-weight:700; color:${m.priority === 'Khẩn cấp' ? 'var(--danger)' : 'var(--warning)'};">${m.priority}</span></td>
      <td>${m.reportedAt}</td>
      <td>${m.status === 'in_progress' ? '<span class="status-badge badge-maintenance"><span class="dot"></span>Đang sửa chữa</span>' : m.status === 'new' ? '<span class="status-badge badge-warning"><span class="dot"></span>Mới tiếp nhận</span>' : '<span class="status-badge badge-available"><span class="dot"></span>Đã hoàn thành</span>'}</td>
      <td>
        ${m.status !== 'resolved' ? `<button class="btn-primary-action" style="padding:4px 10px; font-size:0.74rem;" onclick="resolveMaintenance('${m.id}')">Đã sửa xong</button>` : '<span style="color:var(--success);">Đã đóng</span>'}
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function resolveMaintenance(mtId) {
  const item = STATE.maintenance.find(m => m.id === mtId);
  if (item) {
    item.status = 'resolved';
    const room = getRoomById(item.roomId);
    if (room) room.status = 'available';
    showToast(`Đã hoàn tất xử lý sự cố tại phòng ${room ? room.number : ''}!`, 'success');
    renderMaintenance();
    renderDashboard();
    renderRooms();
  }
}

// 7. INVENTORY (KHO VẬT TƯ)
function renderInventory() {
  const tbody = document.getElementById('inventory-tbody');
  tbody.innerHTML = '';

  STATE.inventory.forEach(inv => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${inv.id}</strong></td>
      <td><strong>${inv.name}</strong></td>
      <td>${inv.unit}</td>
      <td><strong style="font-size:1rem; color:${inv.onHand <= inv.minLevel ? 'var(--danger)' : 'var(--text-main)'};">${inv.onHand}</strong></td>
      <td>${inv.minLevel}</td>
      <td>${inv.onHand <= inv.minLevel ? '<span class="status-badge badge-maintenance"><span class="dot"></span>Cảnh báo tồn thấp</span>' : '<span class="status-badge badge-available"><span class="dot"></span>Đủ định mức</span>'}</td>
      <td>
        <button class="btn-secondary" style="padding:4px 10px; font-size:0.75rem;" onclick="restockItem('${inv.id}')">+ Nhập kho thêm</button>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function restockItem(id) {
  const item = STATE.inventory.find(i => i.id === id);
  if (item) {
    item.onHand += 50;
    showToast(`Đã nhập thêm 50 ${item.unit} cho mặt hàng: ${item.name}!`, 'success');
    renderInventory();
  }
}

// 8. CUSTOMERS (CRM)
function renderCustomers() {
  const tbody = document.getElementById('customers-tbody');
  tbody.innerHTML = '';

  STATE.customers.forEach(c => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${c.id}</strong></td>
      <td><strong>${c.name}</strong></td>
      <td>${c.phone}</td>
      <td>${c.email}</td>
      <td><span class="status-badge badge-confirmed">${c.type}</span></td>
      <td>${c.stays} lượt</td>
      <td><strong style="color:var(--gold);">${formatVND(c.totalSpend)}</strong></td>
      <td><button class="btn-action-icon" title="Xem lịch sử">📋</button></td>
    `;
    tbody.appendChild(tr);
  });
}

// 9. CHECK-IN / CHECK-OUT FRONT DESK
function renderFrontDesk() {
  const checkinTbody = document.getElementById('frontdesk-checkin-tbody');
  const checkoutTbody = document.getElementById('frontdesk-checkout-tbody');
  checkinTbody.innerHTML = '';
  checkoutTbody.innerHTML = '';

  // Expected check-in
  STATE.bookings.filter(b => b.status === 'confirmed').forEach(b => {
    const room = getRoomById(b.roomId);
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${b.id}</strong></td>
      <td><strong>${b.customer}</strong> (${b.phone})</td>
      <td><strong style="color:var(--primary); font-size:1.05rem;">${room ? room.number : ''}</strong></td>
      <td>${b.checkIn} &rarr; ${b.checkOut} (${b.nights} đêm)</td>
      <td><button class="btn-primary-action" style="padding:6px 14px; font-size:0.78rem;" onclick="checkInBooking('${b.id}')">📥 Nhận phòng (Check-in)</button></td>
    `;
    checkinTbody.appendChild(tr);
  });

  // Expected check-out
  STATE.bookings.filter(b => b.status === 'occupied').forEach(b => {
    const room = getRoomById(b.roomId);
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${b.id}</strong></td>
      <td><strong>${b.customer}</strong> (${b.phone})</td>
      <td><strong style="color:var(--danger); font-size:1.05rem;">${room ? room.number : ''}</strong></td>
      <td>Tổng tiền: <strong style="color:var(--gold);">${formatVND(b.totalAmount)}</strong></td>
      <td><button class="btn-primary-action" style="background:var(--danger); padding:6px 14px; font-size:0.78rem;" onclick="checkOutBooking('${b.id}')">📤 Trả phòng (Check-out)</button></td>
    `;
    checkoutTbody.appendChild(tr);
  });
}

// --- ACTIONS: CHECK-IN, CHECK-OUT, CANCEL ---
function checkInBooking(bId) {
  const b = STATE.bookings.find(x => x.id === bId);
  if (!b) return;
  const room = getRoomById(b.roomId);
  
  if (room && room.status === 'maintenance') {
    showToast(`Không thể Check-in! Phòng ${room.number} đang có sự cố bảo trì.`, 'error');
    return;
  }

  b.status = 'occupied';
  if (room) {
    room.status = 'occupied';
    room.guest = b.customer;
  }
  showToast(`Check-in thành công cho khách ${b.customer} tại phòng ${room ? room.number : ''}!`, 'success');
  refreshActiveView();
}

function checkOutBooking(bId) {
  const b = STATE.bookings.find(x => x.id === bId);
  if (!b) return;
  const room = getRoomById(b.roomId);

  b.status = 'completed';
  if (room) {
    room.status = 'cleaning';
    room.guest = null;
    // Auto-create Housekeeping task
    STATE.housekeeping.push({
      id: `HK-${Date.now().toString().slice(-4)}`,
      roomId: room.id,
      assignedTo: 'Đội buồng phòng',
      status: 'dirty',
      priority: 'Cao',
      note: `Khách ${b.customer} vừa trả phòng lúc ${new Date().toLocaleTimeString('vi-VN')}`
    });
  }
  showToast(`Check-out thành công! Phòng ${room ? room.number : ''} đã chuyển sang chờ dọn dẹp.`, 'success');
  refreshActiveView();
}

function cancelBooking(bId) {
  if (!confirm(`Bạn có chắc chắn muốn hủy đơn đặt phòng ${bId}?`)) return;
  const b = STATE.bookings.find(x => x.id === bId);
  if (b) {
    b.status = 'cancelled';
    const room = getRoomById(b.roomId);
    if (room && room.status === 'confirmed') {
      room.status = 'available';
    }
    showToast(`Đã hủy đặt phòng ${bId}! Phòng đã được giải phóng.`, 'info');
    refreshActiveView();
  }
}

// --- NEW BOOKING MODAL LOGIC & CONFLICT CHECK ---
function openNewBookingModal(preSelectedRoomId = null, preCheckIn = null) {
  const modal = document.getElementById('booking-modal');
  modal.classList.add('active');

  const roomSelect = document.getElementById('modal-room-select');
  roomSelect.innerHTML = '<option value="">-- Chọn phòng trống --</option>';

  STATE.rooms.forEach(r => {
    if (r.status === 'maintenance') return;
    const rt = getRoomTypeById(r.typeId);
    const opt = document.createElement('option');
    opt.value = r.id;
    opt.textContent = `${r.number} - ${rt ? rt.name : ''} (${formatVND(rt ? rt.priceNight : 0)}/đêm)`;
    if (preSelectedRoomId === r.id) opt.selected = true;
    roomSelect.appendChild(opt);
  });

  if (preCheckIn) {
    document.getElementById('modal-checkin').value = preCheckIn;
    // Set next day
    const nextDate = new Date(preCheckIn);
    nextDate.setDate(nextDate.getDate() + 2);
    document.getElementById('modal-checkout').value = nextDate.toISOString().split('T')[0];
  } else {
    document.getElementById('modal-checkin').value = '2026-10-15';
    document.getElementById('modal-checkout').value = '2026-10-18';
  }

  calculateModalPrice();
}

function closeBookingModal() {
  document.getElementById('booking-modal').classList.remove('active');
}

function toggleRentTypeFields() {
  const rentType = document.getElementById('modal-rent-type').value;
  const nightContainer = document.getElementById('container-night-booking');
  const hourContainer = document.getElementById('container-hour-booking');

  if (rentType === 'hour') {
    if (nightContainer) nightContainer.style.display = 'none';
    if (hourContainer) hourContainer.style.display = 'block';
  } else {
    if (nightContainer) nightContainer.style.display = 'grid';
    if (hourContainer) hourContainer.style.display = 'none';
  }
  calculateModalPrice();
}

function calculateModalPrice() {
  const roomId = document.getElementById('modal-room-select').value;
  const rentType = document.getElementById('modal-rent-type').value;

  if (!roomId) {
    document.getElementById('modal-summary-nights').innerText = 'Chưa chọn phòng';
    document.getElementById('modal-summary-total').innerText = '0 ₫';
    return;
  }

  const room = getRoomById(roomId);
  const roomType = room ? getRoomTypeById(room.typeId) : null;
  if (!roomType) return;

  if (rentType === 'hour') {
    const duration = parseInt(document.getElementById('modal-hour-duration').value || '2', 10);
    const startTimeStr = document.getElementById('modal-hour-time').value || '10:00';
    
    // Calculate preview end time
    const [startH, startM] = startTimeStr.split(':').map(Number);
    const endH = (startH + duration) % 24;
    const endTimeStr = `${String(endH).padStart(2, '0')}:${String(startM).padStart(2, '0')}`;
    
    const previewEl = document.getElementById('modal-hour-end-preview');
    if (previewEl) previewEl.value = `${endTimeStr} (Cùng ngày)`;

    const total = duration * roomType.priceHour;
    document.getElementById('modal-summary-nights').innerHTML = `<span style="color:#d97706; font-weight:700;">⏰ ${duration} Giờ</span> (Đơn giá: ${formatVND(roomType.priceHour)}/giờ)`;
    document.getElementById('modal-summary-total').innerText = formatVND(total);
  } else {
    const checkIn = document.getElementById('modal-checkin').value;
    const checkOut = document.getElementById('modal-checkout').value;

    if (!checkIn || !checkOut) {
      document.getElementById('modal-summary-nights').innerText = '0 đêm';
      document.getElementById('modal-summary-total').innerText = '0 ₫';
      return;
    }

    const d1 = new Date(checkIn);
    const d2 = new Date(checkOut);
    const diffTime = d2 - d1;
    const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));

    if (diffDays <= 0) {
      document.getElementById('modal-summary-nights').innerText = 'Lỗi: Ngày trả phòng phải sau ngày nhận!';
      document.getElementById('modal-summary-total').innerText = '0 ₫';
      return;
    }

    const total = diffDays * roomType.priceNight;
    document.getElementById('modal-summary-nights').innerHTML = `<span style="color:#2563eb; font-weight:700;">🌙 ${diffDays} Đêm</span> (Đơn giá: ${formatVND(roomType.priceNight)}/đêm)`;
    document.getElementById('modal-summary-total').innerText = formatVND(total);
  }
}

function handleSaveBooking(e) {
  e.preventDefault();
  const customerName = document.getElementById('modal-customer-name').value.trim();
  const phone = document.getElementById('modal-customer-phone').value.trim();
  const roomId = document.getElementById('modal-room-select').value;
  const rentType = document.getElementById('modal-rent-type').value;

  if (!customerName || !phone || !roomId) {
    showToast('Vui lòng điền đầy đủ họ tên, SĐT và chọn phòng!', 'error');
    return;
  }

  const room = getRoomById(roomId);
  const roomType = room ? getRoomTypeById(room.typeId) : null;
  if (!roomType) return;

  let checkIn, checkOut, total, nights = 0, hourDate = null, hourStart = null, hourEnd = null, hoursDuration = 0;

  if (rentType === 'hour') {
    hourDate = document.getElementById('modal-hour-date').value;
    hourStart = document.getElementById('modal-hour-time').value;
    hoursDuration = parseInt(document.getElementById('modal-hour-duration').value, 10);

    if (!hourDate || !hourStart) {
      showToast('Vui lòng chọn ngày và giờ thuê!', 'error');
      return;
    }

    const [startH, startM] = hourStart.split(':').map(Number);
    const endH = (startH + hoursDuration) % 24;
    hourEnd = `${String(endH).padStart(2, '0')}:${String(startM).padStart(2, '0')}`;

    checkIn = hourDate;
    checkOut = hourDate;
    total = hoursDuration * roomType.priceHour;

    // Check conflict with existing bookings on the same date
    const conflict = STATE.bookings.find(b => {
      if (b.roomId !== roomId || b.status === 'cancelled') return false;
      if (b.rentType === 'hour') {
        if (b.hourDate === hourDate) {
          return (hourStart < b.hourEnd && hourEnd > b.hourStart);
        }
      } else {
        return (hourDate >= b.checkIn && hourDate < b.checkOut);
      }
      return false;
    });

    if (conflict) {
      showToast(`Phòng đã có khách [${conflict.customer}] đặt trong khoảng thời gian này!`, 'error');
      return;
    }
  } else {
    checkIn = document.getElementById('modal-checkin').value;
    checkOut = document.getElementById('modal-checkout').value;

    if (!checkIn || !checkOut) {
      showToast('Vui lòng chọn ngày nhận và trả phòng!', 'error');
      return;
    }

    if (checkOut <= checkIn) {
      showToast('Ngày trả phòng phải sau ngày nhận phòng!', 'error');
      return;
    }

    const d1 = new Date(checkIn);
    const d2 = new Date(checkOut);
    nights = Math.ceil((d2 - d1) / (1000 * 60 * 60 * 24));
    total = nights * roomType.priceNight;

    // Double-booking conflict check
    const conflict = STATE.bookings.find(b => {
      if (b.roomId !== roomId || b.status === 'cancelled') return false;
      return (checkIn < b.checkOut && checkOut > b.checkIn);
    });

    if (conflict) {
      showToast(`Phòng này đã bị trùng lịch với khách [${conflict.customer}] (${conflict.checkIn} - ${conflict.checkOut})!`, 'error');
      return;
    }
  }

  const newBooking = {
    id: `BK-2026-0${STATE.bookings.length + 1}`,
    customer: customerName,
    phone: phone,
    roomId: roomId,
    branchId: room ? room.branchId : 'b1',
    checkIn: checkIn,
    checkOut: checkOut,
    hourDate: hourDate,
    hourStart: hourStart,
    hourEnd: hourEnd,
    hoursDuration: hoursDuration,
    rentType: rentType,
    nights: nights,
    totalAmount: total,
    status: 'confirmed',
    createdDate: new Date().toISOString().split('T')[0]
  };

  STATE.bookings.unshift(newBooking);
  if (room && room.status === 'available') {
    room.status = 'confirmed';
  }

  const rentDesc = rentType === 'hour' ? `Thuê ${hoursDuration} giờ` : `Thuê ${nights} đêm`;
  showToast(`Đặt phòng thành công! Mã đơn: ${newBooking.id} (${rentDesc} - ${formatVND(total)})`, 'success');
  closeBookingModal();
  refreshActiveView();
}

// --- CANVAS CHART LOGIC ---
function drawOccupancyChart() {
  const canvas = document.getElementById('occupancyChart');
  if (!canvas) return;
  const ctx = canvas.getContext('2d');
  const w = canvas.width = canvas.parentElement.clientWidth;
  const h = canvas.height = canvas.parentElement.clientHeight;

  ctx.clearRect(0, 0, w, h);

  const days = ['Thứ 2', 'Thứ 3', 'Thứ 4', 'Thứ 5', 'Thứ 6', 'Thứ 7', 'CN'];
  const rates = [65, 78, 85, 92, 100, 95, 80]; // Occupancy percentage

  const padding = 40;
  const chartW = w - padding * 2;
  const chartH = h - padding * 2;

  // Draw Grid Lines
  ctx.strokeStyle = '#e2e8f0';
  ctx.lineWidth = 1;
  for (let i = 0; i <= 4; i++) {
    const y = padding + (chartH / 4) * i;
    ctx.beginPath();
    ctx.moveTo(padding, y);
    ctx.lineTo(w - padding, y);
    ctx.stroke();

    ctx.fillStyle = '#94a3b8';
    ctx.font = '11px Plus Jakarta Sans';
    ctx.fillText(`${100 - i * 25}%`, 8, y + 4);
  }

  // Draw Area Gradient & Line
  const stepX = chartW / (days.length - 1);
  const points = rates.map((r, idx) => ({
    x: padding + idx * stepX,
    y: padding + chartH - (r / 100) * chartH
  }));

  // Gradient fill
  const grad = ctx.createLinearGradient(0, padding, 0, h - padding);
  grad.addColorStop(0, 'rgba(37, 99, 235, 0.35)');
  grad.addColorStop(1, 'rgba(37, 99, 235, 0.0)');

  ctx.beginPath();
  ctx.moveTo(points[0].x, points[0].y);
  points.forEach(p => ctx.lineTo(p.x, p.y));
  ctx.lineTo(points[points.length - 1].x, h - padding);
  ctx.lineTo(points[0].x, h - padding);
  ctx.closePath();
  ctx.fillStyle = grad;
  ctx.fill();

  // Line stroke
  ctx.beginPath();
  ctx.moveTo(points[0].x, points[0].y);
  points.forEach(p => ctx.lineTo(p.x, p.y));
  ctx.strokeStyle = '#2563eb';
  ctx.lineWidth = 3;
  ctx.stroke();

  // Points & Labels
  points.forEach((p, idx) => {
    ctx.beginPath();
    ctx.arc(p.x, p.y, 5, 0, Math.PI * 2);
    ctx.fillStyle = '#ffffff';
    ctx.fill();
    ctx.strokeStyle = '#2563eb';
    ctx.lineWidth = 2.5;
    ctx.stroke();

    ctx.fillStyle = '#1e293b';
    ctx.font = 'bold 11px Plus Jakarta Sans';
    ctx.textAlign = 'center';
    ctx.fillText(`${rates[idx]}%`, p.x, p.y - 10);

    ctx.fillStyle = '#64748b';
    ctx.font = '11px Plus Jakarta Sans';
    ctx.fillText(days[idx], p.x, h - 14);
  });
}

// --- SWITCHING VIEWS ---
function switchView(viewName) {
  const role = STATE.activeRole;
  const lockedViewsForRole = {
    manager: [],
    receptionist: ['reports', 'settings'],
    housekeeping: ['bookings', 'rack', 'customers', 'reports', 'settings'],
    technician: ['bookings', 'rack', 'customers', 'reports', 'settings'],
    inventory: ['bookings', 'rack', 'customers', 'reports', 'settings']
  };

  const locked = lockedViewsForRole[role] || [];
  if (locked.includes(viewName)) {
    const roleTitles = {
      receptionist: 'Lễ tân (Front Desk)',
      housekeeping: 'Buồng phòng (Housekeeping)',
      technician: 'Kỹ thuật viên (Technician)',
      inventory: 'Thủ kho & Minibar (Inventory)'
    };
    const viewTitles = {
      bookings: 'Quản lý đặt phòng',
      rack: 'Lịch phòng (PMS Rack)',
      customers: 'Hồ sơ khách hàng (CRM)',
      reports: 'Báo cáo doanh thu & Tài chính',
      settings: 'Cấu hình & Phân quyền bảo mật'
    };
    showToast(`⛔ Truy cập bị từ chối! Vai trò [${roleTitles[role] || role}] không có thẩm quyền truy cập phân hệ [${viewTitles[viewName] || viewName}]. Vui lòng chuyển sang vai trò Giám đốc (Admin) để kiểm tra.`, 'error');
    return;
  }

  STATE.activeView = viewName;
  document.querySelectorAll('.view-section').forEach(sec => sec.classList.remove('active'));
  
  const targetSec = document.getElementById(`view-${viewName}`);
  if (targetSec) targetSec.classList.add('active');

  // Update Sidebar active state
  document.querySelectorAll('.nav-item').forEach(item => {
    item.classList.toggle('active', item.getAttribute('data-view') === viewName);
  });

  // Update Breadcrumb
  const breadcrumb = document.getElementById('breadcrumb-current');
  const labels = {
    dashboard: 'Tổng quan hệ thống',
    bookings: 'Quản lý đặt phòng',
    rack: 'Lịch phòng (Room Rack)',
    rooms: 'Sơ đồ & Danh sách phòng',
    frontdesk: 'Nhận phòng & Trả phòng',
    housekeeping: 'Buồng phòng & Vệ sinh',
    maintenance: 'Bảo trì & Sự cố',
    customers: 'Hồ sơ khách hàng (CRM)',
    services: 'Dịch vụ & Minibar',
    inventory: 'Kho vật tư & Amenities',
    reports: 'Báo cáo & Thống kê',
    settings: 'Cấu hình & Phân quyền'
  };
  if (breadcrumb) breadcrumb.innerText = labels[viewName] || viewName;

  refreshActiveView();
}

function refreshActiveView() {
  switch (STATE.activeView) {
    case 'dashboard': renderDashboard(); break;
    case 'bookings': renderBookings(); break;
    case 'rack': renderRoomRack(); break;
    case 'rooms': renderRooms(); break;
    case 'frontdesk': renderFrontDesk(); break;
    case 'housekeeping': renderHousekeeping(); break;
    case 'maintenance': renderMaintenance(); break;
    case 'customers': renderCustomers(); break;
    case 'inventory': renderInventory(); break;
    case 'settings': renderSettings(); break;
  }
}

// ==========================================================================
// 8. RBAC PERMISSIONS & USER ACCESS CONTROL ENGINE
// ==========================================================================

function switchActiveRole(newRole) {
  STATE.activeRole = newRole;

  const roleMeta = {
    manager: { name: 'Trần Minh Đức', title: 'Quản lý / Giám đốc điều hành', avatar: 'AD', bg: '#7e22ce' },
    receptionist: { name: 'Nguyễn Thị Thu Hà', title: 'Trưởng ca Lễ tân (Front Desk)', avatar: 'HA', bg: '#2563eb' },
    housekeeping: { name: 'Lê Thị Mai', title: 'Tổ trưởng Buồng phòng', avatar: 'LM', bg: '#ca8a04' },
    technician: { name: 'Nguyễn Văn Tuấn', title: 'Kỹ thuật viên trưởng', avatar: 'VT', bg: '#dc2626' },
    inventory: { name: 'Phạm Hồng Phúc', title: 'Thủ kho & Quản lý Minibar', avatar: 'PP', bg: '#16a34a' }
  };

  const meta = roleMeta[newRole] || roleMeta.manager;

  // Update Topbar select
  const select = document.getElementById('current-user-role-select');
  if (select) select.value = newRole;

  // Update Sidebar user footer
  const userMetaEl = document.querySelector('.sidebar-footer .user-meta');
  const userAvatarEl = document.querySelector('.sidebar-footer .user-avatar');
  if (userMetaEl) {
    userMetaEl.innerHTML = `<h4>${meta.name}</h4><p>${meta.title}</p>`;
  }
  if (userAvatarEl) {
    userAvatarEl.innerText = meta.avatar;
    userAvatarEl.style.background = meta.bg;
  }

  showToast(`Đã chuyển vai trò sang: [${meta.title}]. Hệ thống kích hoạt quyền truy cập tương ứng!`, 'info');
  applyRolePermissions();

  const lockedViewsForRole = {
    manager: [],
    receptionist: ['reports', 'settings'],
    housekeeping: ['bookings', 'rack', 'customers', 'reports', 'settings'],
    technician: ['bookings', 'rack', 'customers', 'reports', 'settings'],
    inventory: ['bookings', 'rack', 'customers', 'reports', 'settings']
  };

  const locked = lockedViewsForRole[newRole] || [];
  if (locked.includes(STATE.activeView)) {
    const fallback = (newRole === 'housekeeping') ? 'housekeeping' 
      : (newRole === 'technician') ? 'maintenance' 
      : (newRole === 'inventory') ? 'inventory' 
      : 'dashboard';
    showToast(`⚠️ Vai trò [${meta.title}] không được phép xem phân hệ trước đó. Tự động chuyển về giao diện nghiệp vụ cho phép!`, 'warning');
    switchView(fallback);
  } else {
    if (STATE.activeView === 'settings') renderSettings();
  }
}

function applyRolePermissions() {
  const role = STATE.activeRole;
  // Visual lock badge indicators for non-permitted views
  const lockedViewsForRole = {
    manager: [],
    receptionist: ['reports', 'settings'],
    housekeeping: ['bookings', 'rack', 'customers', 'reports', 'settings'],
    technician: ['bookings', 'rack', 'customers', 'reports', 'settings'],
    inventory: ['bookings', 'rack', 'customers', 'reports', 'settings']
  };

  const locked = lockedViewsForRole[role] || [];
  document.querySelectorAll('.nav-item').forEach(item => {
    const v = item.getAttribute('data-view');
    const isLocked = locked.includes(v);
    item.style.opacity = isLocked ? '0.45' : '1';
    item.title = isLocked ? `🔒 Vai trò [${role}] bị khóa truy cập phân hệ này theo chính sách bảo mật RBAC` : '';
  });
}

function switchRbacTab(tabName) {
  STATE.rbacTab = tabName;
  document.querySelectorAll('.rbac-tab-item').forEach(tab => {
    tab.classList.toggle('active', tab.getAttribute('onclick').includes(tabName));
  });

  const tabContents = {
    users: document.getElementById('rbac-content-users'),
    matrix: document.getElementById('rbac-content-matrix'),
    roles: document.getElementById('rbac-content-roles'),
    branches: document.getElementById('rbac-content-branches')
  };

  Object.keys(tabContents).forEach(k => {
    if (tabContents[k]) tabContents[k].style.display = (k === tabName ? 'block' : 'none');
  });

  if (tabName === 'users') renderRbacUsers();
  if (tabName === 'matrix') renderRbacMatrix();
}

function renderSettings() {
  const userCountEl = document.getElementById('rbac-kpi-user-count');
  if (userCountEl) userCountEl.innerText = `${STATE.users.length} Tài khoản`;

  renderRbacUsers();
  renderRbacMatrix();
}

function renderRbacUsers() {
  const tbody = document.getElementById('rbac-users-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  const roleStyles = {
    manager: { label: '👑 Giám đốc / Admin', color: '#7e22ce', bg: '#f3e8ff' },
    receptionist: { label: '🛎️ Lễ tân', color: '#1d4ed8', bg: '#eff6ff' },
    housekeeping: { label: '🧹 Buồng phòng', color: '#b45309', bg: '#fefce8' },
    technician: { label: '🔧 Kỹ thuật viên', color: '#b91c1c', bg: '#fee2e2' },
    inventory: { label: '📦 Thủ kho / Minibar', color: '#15803d', bg: '#dcfce7' }
  };

  STATE.users.forEach(u => {
    const roleInfo = roleStyles[u.role] || { label: u.role, color: '#334155', bg: '#f1f5f9' };
    const branchName = u.branchId === 'all' 
      ? 'Toàn bộ 2 Cơ sở' 
      : (u.branchId === 'b1' ? 'M-Hotel Quy Nhơn Beach' : 'M-Hotel Nhơn Lý - Eo Gió');

    const initials = u.name.split(' ').slice(-2).map(w => w[0]).join('').toUpperCase();

    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td>
        <div style="display:flex; align-items:center; gap:10px;">
          <div class="user-avatar-circle" style="background:${roleInfo.color};">${initials}</div>
          <div>
            <div style="font-weight:700; color:var(--text-main); font-size:0.9rem;">${u.name}</div>
            <small style="color:var(--text-muted); font-size:0.75rem;">Mã NV: #${u.id.toUpperCase()}</small>
          </div>
        </div>
      </td>
      <td><code style="background:#f1f5f9; padding:2px 6px; border-radius:4px; font-weight:700; color:var(--text-main);">${u.username}</code></td>
      <td>
        <div style="font-size:0.8rem;">${u.email}</div>
        <small style="color:var(--text-muted); font-size:0.75rem;">${u.phone}</small>
      </td>
      <td>
        <span class="status-badge" style="background:${roleInfo.bg}; color:${roleInfo.color}; font-weight:700; cursor:pointer;" title="Nhấn để đổi nhanh vai trò nhân viên" onclick="promptChangeRole('${u.id}')">
          ${roleInfo.label} ⟳
        </span>
      </td>
      <td>
        <span style="font-size:0.78rem; font-weight:600; color:var(--text-muted);">${branchName}</span>
      </td>
      <td>
        <span class="status-badge ${u.status === 'active' ? 'badge-available' : 'badge-maintenance'}">
          <span class="dot"></span>
          ${u.status === 'active' ? 'Đang hoạt động' : 'Tạm khóa'}
        </span>
      </td>
      <td>
        <div style="display:flex; gap:6px;">
          <button class="btn-action-icon" title="Đổi vai trò" onclick="promptChangeRole('${u.id}')">🔄</button>
          <button class="btn-action-icon" title="${u.status === 'active' ? 'Khóa tài khoản' : 'Mở khóa'}" onclick="toggleUserStatus('${u.id}')" style="color:${u.status === 'active' ? 'var(--warning)' : 'var(--success)'};">
            ${u.status === 'active' ? '🔒' : '🔓'}
          </button>
          ${u.username !== 'admin' ? `
            <button class="btn-action-icon" title="Xóa tài khoản" onclick="deleteUser('${u.id}')" style="color:var(--danger);">🗑️</button>
          ` : ''}
        </div>
      </td>
    `;
    tbody.appendChild(tr);
  });
}

function renderRbacMatrix() {
  const tbody = document.getElementById('rbac-matrix-tbody');
  if (!tbody) return;
  tbody.innerHTML = '';

  const badgeMap = {
    full: '<span class="perm-badge-full" title="Nhấn để xoay vòng quyền: Full ➔ Limit ➔ Read ➔ Lock">✅ Toàn quyền (CRUD)</span>',
    custom: '<span class="perm-badge-custom" title="Nhấn để xoay vòng quyền: Full ➔ Limit ➔ Read ➔ Lock">⚙️ Giới hạn</span>',
    read: '<span class="perm-badge-read" title="Nhấn để xoay vòng quyền: Full ➔ Limit ➔ Read ➔ Lock">👁️ Chỉ xem</span>',
    lock: '<span class="perm-badge-lock" title="Nhấn để xoay vòng quyền: Full ➔ Limit ➔ Read ➔ Lock">❌ Khóa</span>'
  };

  STATE.permissionMatrix.forEach(row => {
    const tr = document.createElement('tr');
    tr.innerHTML = `
      <td><strong>${row.module}</strong></td>
      <td onclick="cyclePermission('${row.id}', 'manager')">${badgeMap[row.manager] || row.manager}</td>
      <td onclick="cyclePermission('${row.id}', 'receptionist')">${badgeMap[row.receptionist] || row.receptionist}</td>
      <td onclick="cyclePermission('${row.id}', 'housekeeping')">${badgeMap[row.housekeeping] || row.housekeeping}</td>
      <td onclick="cyclePermission('${row.id}', 'technician')">${badgeMap[row.technician] || row.technician}</td>
      <td onclick="cyclePermission('${row.id}', 'inventory')">${badgeMap[row.inventory] || row.inventory}</td>
    `;
    tbody.appendChild(tr);
  });
}

function cyclePermission(rowId, role) {
  const row = STATE.permissionMatrix.find(r => r.id === rowId);
  if (!row) return;
  if (role === 'manager') {
    showToast('👑 Vai trò Giám đốc luôn giữ Toàn quyền (Super Admin) để đảm bảo toàn vẹn dữ liệu hệ thống!', 'warning');
    return;
  }
  const cycle = ['full', 'custom', 'read', 'lock'];
  const curIdx = cycle.indexOf(row[role]);
  const nextPerm = cycle[(curIdx + 1) % cycle.length];
  row[role] = nextPerm;
  renderRbacMatrix();

  const roleNames = {
    receptionist: 'Lễ tân (Front Desk)',
    housekeeping: 'Buồng phòng (Housekeeping)',
    technician: 'Kỹ thuật viên (Technician)',
    inventory: 'Thủ kho / Minibar (Inventory)'
  };
  const permLabels = {
    full: '✅ Toàn quyền (CRUD)',
    custom: '⚙️ Giới hạn nghiệp vụ',
    read: '👁️ Chỉ xem',
    lock: '❌ Khóa truy cập'
  };
  const moduleShort = row.module.split('.')[1]?.trim() || row.module;
  showToast(`Đã đổi quyền [${moduleShort}] của [${roleNames[role]}]: ${permLabels[nextPerm]}! Nhấn "Lưu cấu hình ma trận" để ghi nhận.`, 'info');
}

function openNewUserModal() {
  const modal = document.getElementById('user-modal');
  if (modal) modal.classList.add('active');
}

function closeUserModal() {
  const modal = document.getElementById('user-modal');
  if (modal) modal.classList.remove('active');
}

function handleSaveUser(e) {
  e.preventDefault();
  const fullname = document.getElementById('user-fullname').value.trim();
  const username = document.getElementById('user-username').value.trim().toLowerCase();
  const phone = document.getElementById('user-phone').value.trim();
  const email = document.getElementById('user-email').value.trim() || `${username}@m-hotel.vn`;
  const role = document.getElementById('user-role').value;
  const branchId = document.getElementById('user-branch').value;

  if (!fullname || !username || !phone) {
    showToast('Vui lòng điền đủ thông tin bắt buộc!', 'error');
    return;
  }

  // Check duplicate username
  if (STATE.users.some(u => u.username === username)) {
    showToast(`Tên đăng nhập [${username}] đã tồn tại trong hệ thống!`, 'error');
    return;
  }

  const newUser = {
    id: `u${STATE.users.length + 1}`,
    name: fullname,
    username: username,
    phone: phone,
    email: email,
    role: role,
    branchId: branchId,
    status: 'active'
  };

  const roleLabels = {
    manager: '👑 Giám đốc / Admin',
    receptionist: '🛎️ Lễ tân',
    housekeeping: '🧹 Buồng phòng',
    technician: '🔧 Kỹ thuật viên',
    inventory: '📦 Thủ kho / Minibar'
  };

  STATE.users.push(newUser);
  showToast(`Đã thêm thành công nhân viên [${fullname}] với vai trò [${roleLabels[role] || role}]!`, 'success');
  closeUserModal();
  renderSettings();
  document.getElementById('new-user-form').reset();
}

function toggleUserStatus(userId) {
  const u = STATE.users.find(x => x.id === userId);
  if (!u) return;
  if (u.username === 'admin') {
    showToast('Không thể khóa tài khoản Quản trị viên tối cao (Super Admin)!', 'error');
    return;
  }
  u.status = (u.status === 'active' ? 'locked' : 'active');
  showToast(`Đã ${u.status === 'active' ? 'kích hoạt lại' : 'tạm khóa'} tài khoản [${u.username}]!`, 'info');
  renderRbacUsers();
}

function deleteUser(userId) {
  const u = STATE.users.find(x => x.id === userId);
  if (!u) return;
  if (u.username === 'admin') {
    showToast('Không thể xóa tài khoản Quản trị viên tối cao!', 'error');
    return;
  }
  if (!confirm(`Bạn có chắc chắn muốn xóa nhân viên [${u.name}] khỏi hệ thống?`)) return;
  STATE.users = STATE.users.filter(x => x.id !== userId);
  showToast(`Đã xóa tài khoản [${u.username}]!`, 'info');
  renderSettings();
}

function promptChangeRole(userId) {
  const u = STATE.users.find(x => x.id === userId);
  if (!u) return;
  const roles = ['manager', 'receptionist', 'housekeeping', 'technician', 'inventory'];
  const roleNames = {
    manager: '👑 Giám đốc / Admin',
    receptionist: '🛎️ Lễ tân (Front Desk)',
    housekeeping: '🧹 Buồng phòng (Housekeeping)',
    technician: '🔧 Kỹ thuật viên (Technician)',
    inventory: '📦 Thủ kho / Minibar (Inventory)'
  };
  const curIdx = roles.indexOf(u.role);
  const nextRole = roles[(curIdx + 1) % roles.length];
  u.role = nextRole;
  showToast(`Đã cập nhật vai trò của [${u.name}] sang: [${roleNames[nextRole]}]!`, 'success');
  renderRbacUsers();
}

function savePermissionMatrix() {
  showToast('Đã lưu thành công Ma trận Phân quyền 5 vai trò vào hệ thống M-Hotel!', 'success');
}

// --- INIT EVENT LISTENERS ---
window.addEventListener('DOMContentLoaded', () => {
  // Live Clock
  setInterval(() => {
    const clock = document.getElementById('live-clock');
    if (clock) clock.innerText = new Date().toLocaleTimeString('vi-VN');
  }, 1000);

  // Branch selector change
  const branchSelect = document.getElementById('branch-select');
  if (branchSelect) {
    branchSelect.addEventListener('change', (e) => {
      STATE.currentBranch = e.target.value;
      showToast(`Đã chuyển sang: ${e.target.options[e.target.selectedIndex].text}`, 'info');
      refreshActiveView();
    });
  }

  // Global Search input
  const searchInput = document.getElementById('global-search');
  if (searchInput) {
    searchInput.addEventListener('input', (e) => {
      STATE.searchQuery = e.target.value;
      if (STATE.activeView === 'bookings') renderBookings();
    });
  }

  // Nav clicks
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => {
      const v = item.getAttribute('data-view');
      if (v) switchView(v);
    });
  });

  // Form modal triggers
  const form = document.getElementById('new-booking-form');
  if (form) form.addEventListener('submit', handleSaveBooking);

  ['modal-room-select', 'modal-checkin', 'modal-checkout', 'modal-rent-type', 'modal-hour-duration', 'modal-hour-time', 'modal-hour-date'].forEach(id => {
    const el = document.getElementById(id);
    if (el) {
      el.addEventListener('change', calculateModalPrice);
      el.addEventListener('input', calculateModalPrice);
    }
  });

  window.addEventListener('resize', () => {
    if (STATE.activeView === 'dashboard') drawOccupancyChart();
  });

  // First render
  switchView('dashboard');
});
