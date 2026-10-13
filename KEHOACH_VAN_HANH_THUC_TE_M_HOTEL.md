# KẾ HOẠCH TRIỂN KHAI VẬN HÀNH THỰC TẾ ODOO CHO M-HOTEL
## Dự án: ERP Quản lý Vận hành Khách sạn Chuỗi M-Hotel (Bình Định)
## Môn học: IS336 - Hoạch định Nguồn lực Doanh nghiệp | Nhóm 12

---

## I. ĐÁNH GIÁ TÌNH TRẠNG HIỆN TẠI (ĐỒ ÁN VS VẬN HÀNH THỰC TẾ)

| Hạng mục | Hiện trạng đồ án (Đã hoàn thành 100%) | Khi áp dụng thực tế cho khách sạn (Go-Live) |
|---|---|---|
| **Cơ sở hạ tầng** | Odoo SaaS Cloud (`edu-m-hotel.odoo.com`) | Cần gắn tên miền riêng (`mhotel.vn`, `booking.mhotel.vn`) và thiết lập sao lưu dữ liệu định kỳ. |
| **Dữ liệu phòng & Giá** | 16 hạng phòng & dịch vụ mẫu (VND) | Cập nhật số phòng thực tế (Room 101 - 505) và bảng giá mùa cao điểm / thấp điểm. |
| **Tồn kho Minibar/Kho** | Số dư mẫu (Bia Quy Nhơn, Bánh dừa, Amenities) | Kiểm kê thực tế tại các kho buồng phòng và thiết lập điểm đặt hàng lại (Reordering Rules). |
| **Thanh toán Online** | Mô phỏng đặt phòng qua website | Tích hợp cổng thanh toán thực tế (VNPAY, MoMo, VietQR, OnePay). |
| **Nhân sự & Phân quyền** | 5 vai trò mẫu trên Odoo | Tạo tài khoản thực tế cho từng nhân viên Lễ tân, Buồng phòng, Kế toán, Kỹ thuật. |

---

## II. KẾ HOẠCH TRIỂN KHAI 5 BƯỚC ĐỂ ĐƯA VÀO VẬN HÀNH THỰC TẾ (ROADMAP GO-LIVE)

### BƯỚC 1: BÀN GIAO & CẤU HÌNH HẠ TẦNG SỐ (DIGITAL INFRASTRUCTURE)
1. **Thiết lập Tên miền & Thương hiệu**:
   - Trỏ domain chính thức: `booking.mhotel.vn` về Odoo.
   - Cập nhật Logo chính thức, Favicon, Banner bãi biển Quy Nhơn, số Hotline và Zalo OA.
2. **Bảo mật & Phân quyền nhân viên**:
   - Khởi tạo tài khoản thực tế theo email/sđt của nhân viên khách sạn.
   - Khóa quyền truy cập cấu hình hệ thống, chỉ cấp quyền nghiệp vụ tương ứng cho từng bộ phận (Lễ tân chỉ thấy Bán hàng/Lịch phòng, Buồng phòng chỉ thấy Vật tư/Minibar, Kỹ thuật chỉ thấy Kanban bảo dưỡng).

---

### BƯỚC 2: CHUẨN HÓA MASTER DATA THỰC TẾ CỦA KHÁCH SẠN
1. **Sơ đồ phòng thực tế**:
   - Gán mã định danh cho từng phòng cụ thể: `QN-101`, `QN-102`, `NL-201`,... theo 2 cơ sở (Quy Nhơn Beach và Nhơn Lý Eo Gió).
2. **Định mức Minibar & Vật tư tiêu hao (Amenities)**:
   - Cài đặt số lượng tiêu chuẩn trong từng phòng (VD: mỗi phòng gồm 2 lon Bia Quy Nhơn, 2 chai nước Đảnh Thạnh, 2 bàn chải tre).
   - Thiết lập quy trình: Khách check-out -> Buồng phòng kiểm tra -> Lễ tân ghi nhận tiêu thụ -> Tự động trừ kho.

---

### BƯỚC 3: TÍCH HỢP THANH TOÁN & KÊNH ĐẶT PHÒNG
1. **Cổng thanh toán tự động (VietQR / MoMo / VNPAY)**:
   - Cấu hình phương thức thanh toán chuyển khoản hiển thị mã QR động có sẵn nội dung chuyển khoản và số tiền theo từng đơn đặt phòng.
2. **Kênh tiếp nhận đa luồng**:
   - **Kênh Web**: Khách tự book qua `https://edu-m-hotel.odoo.com/shop`.
   - **Kênh Lễ tân / Hotline / Walk-in**: Nhân viên lễ tân tạo đơn trực tiếp trên màn hình Sales Calendar (`/odoo/sales`).

---

### BƯỚC 4: ĐÀO TẠO NHÂN SỰ VẬN HÀNH (SOP - STANDARD OPERATING PROCEDURES)
1. **Quy trình Lễ tân (Front Desk SOP)**:
   - Mở giao diện Lịch (`Sales Calendar`) mỗi ca trực.
   - Nhận khách -> Check-in -> Ghi nhận minibar/dịch vụ phát sinh -> Xuất hóa đơn -> Thu tiền.
2. **Quy trình Buồng phòng & Bảo trì (Housekeeping & Maintenance SOP)**:
   - Khi phát hiện hư hỏng (máy lạnh không mát, tivi chập chờn) -> Lễ tân/buồng phòng tạo yêu cầu bảo trì trên app Odoo.
   - Đội kỹ thuật nhận việc trên bảng Kanban -> Chuyển sang "Đang thực hiện" -> Sửa xong chuyển sang "Đã giải quyết".

---

### BƯỚC 5: CHÍNH THỨC VẬN HÀNH (GO-LIVE) & GIÁM SÁT
1. **Kiểm tra luồng xuyên suốt**:
   - Thực hiện 1 đơn thử nghiệm từ Web đặt phòng -> Kiểm tra hóa đơn -> Xuất kho minibar -> Ghi nhận doanh thu.
2. **Quản trị Dashboard**:
   - Giám đốc khách sạn theo dõi doanh thu hàng ngày qua biểu đồ phân tích trên Odoo Reporting.
