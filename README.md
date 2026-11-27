# M-Hotel ERP — Hệ Thống Quản Lý Vận Hành Chuỗi Khách Sạn (Odoo 19)

> **Học phần:** IS336 — Hoạch định nguồn lực doanh nghiệp (*Enterprise Resource Planning*)  
> **Lớp:** IS336.R11.1 | **Nhóm thực hiện:** Nhóm 12  
> **Giảng viên hướng dẫn:** ThS. Huỳnh Đức Huy  
> **Nền tảng triển khai:** Odoo 19 Community Edition + PostgreSQL 15 (Dockerized Multi-Company Architecture)

---

## 📌 Tổng Quan Dự Án (Project Overview)

**M-Hotel ERP** là giải pháp Hoạch định nguồn lực doanh nghiệp toàn diện được thiết kế và tùy biến trực tiếp trên nền tảng **Odoo 19 Community** cho bài toán vận hành chuỗi khách sạn. Hệ thống số hóa và liên thông xuyên suốt các quy trình cốt lõi theo hướng **System-Oriented**: Đặt phòng đa kênh (theo đêm & theo giờ), Nhận/Trả phòng (*Check-in / Check-out*), Quản lý dịch vụ phát sinh & Minibar (*Folio*), Lập hóa đơn & Thu tiền, Điều phối buồng phòng, Tự động xuất kho vật tư tiêu hao theo định mức, Mua hàng tiếp tế (*RFQ → PO*), Nhập kho & Kiểm kê vật tư, Quản lý sự cố & Bảo trì trang thiết bị, và Báo cáo quản trị đa chi nhánh (*Pivot & Graph*).

### 🏨 Kiến Trúc Đa Chi Nhánh (Multi-Company Branch Architecture)
Hệ thống vận hành đồng thời **02 cơ sở lưu trú** độc lập về kho hàng và sổ kế toán nhưng dùng chung danh mục chuẩn hóa trên cùng một cơ sở dữ liệu (`31 phòng` / `6 hạng phòng`):
1. **Khách Sạn M (Cơ sở 1 – Gia Lai)** *(Trụ sở chính: Thôn Dương Liễu Tây, xã Bình Dương, tỉnh Gia Lai)* — **13 phòng** bố trí từ Tầng 1 đến Tầng 3.
2. **M-Hotel Vũng Tàu Resort (Cơ sở 2 – Vũng Tàu)** *(Chi nhánh mở rộng: 125 Thùy Vân, Phường Thắng Tam, TP. Vũng Tàu)* — **18 phòng** bố trí từ Tầng 1 đến Tầng 5 (bao gồm hạng *Phòng gia đình* & *Căn hộ áp mái – Penthouse*).

---

## 🏗️ Kiến Trúc Phân Hệ (Architecture & Modules)

Mã nguồn tại `M-Hotel_Docker/addons/` được tổ chức thành **8 gói module chuyên biệt** kết hợp chặt chẽ với các phân hệ chuẩn của Odoo 19 (*Purchase, Inventory, Invoicing, Maintenance*):

| Module | Tên kỹ thuật | Chức năng & Nghiệp vụ cốt lõi |
| :--- | :--- | :--- |
| **Core Base** | `m_hotel_base` | Nền tảng Đa chi nhánh (`Multi-Company`), **6 hạng phòng**, danh mục **31 phòng** (vòng đời 6 trạng thái trực quan), bảng giá mùa vụ/dịp lễ, hồ sơ khách lưu trú mở rộng CCCD/Hộ chiếu (`69 đối tác`) và cấu hình phân quyền **6 vai trò RBAC**. |
| **Booking & Frontdesk** | `m_hotel_booking` | Đặt phòng theo đêm & theo giờ (`HB/2026/...`), thuật toán chặn trùng lịch (*Overbooking Constraint*), tìm phòng trống nhanh, *Check-in / Check-out*, quản lý *Folio* dịch vụ/Minibar và tự động sinh hóa đơn khách hàng (`account.move`). |
| **Housekeeping & Incident** | `m_hotel_housekeeping` | Tự động sinh nhiệm vụ dọn phòng sau *Check-out*, bảng điều phối Kanban trực quan, ghi nhận biên bản sự cố (`hotel.incident`) và tự động khóa phòng khẩn cấp sang trạng thái *Bảo trì*. |
| **Inventory & Supply** | `m_hotel_inventory` | Thiết lập định mức vật tư tiêu hao (*Amenities & Minibar*) theo từng hạng phòng (`39 mặt hàng`), tự động sinh phiếu xuất kho nội bộ (`stock.picking`) ngay khi hoàn tất dọn phòng; liên thông Nhập kho (`WH/IN`) & Kiểm kê kho. |
| **Asset & Maintenance** | `m_hotel_asset` | Quản lý danh mục **21 trang thiết bị** gắn mã tài sản & số Serial theo từng phòng, liên kết trực tiếp với phân hệ Bảo trì (`maintenance.request`) cho cả sửa chữa sự cố (*Corrective*) và bảo dưỡng định kỳ (*Preventive*). |
| **Management Reports** | `m_hotel_report` | Khung nhìn phân tích SQL View (`hotel.occupancy.report`) tổng hợp công suất buồng phòng và cơ cấu doanh thu theo chi nhánh, hạng phòng, thời gian trên bảng xoay **Pivot** và biểu đồ **Graph**. |
| **Website Booking** | `m_hotel_website` | Cổng thông tin trực tuyến giới thiệu hệ thống chi nhánh, tra cứu hạng phòng và gửi yêu cầu đặt phòng đồng bộ trực tiếp về phân hệ Lễ tân. |
| **Umbrella Package** | `m_hotel` | Gói tích hợp tổng (*Meta-package*) hỗ trợ cài đặt trọn bộ giải pháp M-Hotel ERP chỉ với một thao tác. |

---

## 🔐 Phân Quyền Truy Cập Theo Phòng Ban (RBAC Security)

Hệ thống cô lập quyền truy cập và giao diện Menu theo đúng **6 nhóm vai trò trong sơ đồ tổ chức**:
- `bangiamdoc` (**Ban Giám Đốc**) — Toàn quyền giám sát vận hành & báo cáo quản trị cả 2 chi nhánh.
- `bophanletan` (**Bộ phận Lễ tân**) — Sơ đồ phòng, Đặt phòng, *Check-in/out*, Khách hàng, Báo sự cố, Xuất hóa đơn & Thu tiền.
- `bophanbuongphong` (**Bộ phận Buồng phòng**) — Sơ đồ phòng trực quan, Nhiệm vụ dọn phòng, Báo cáo sự cố phòng.
- `bophankythuat` (**Bộ phận Kỹ thuật & Bảo trì**) — Hồ sơ thiết bị phòng, Phiếu sửa chữa & Bảo dưỡng định kỳ, Sự cố phòng.
- `bophankho` (**Bộ phận Kho & Mua hàng**) — Định mức vật tư, Mua hàng tiếp tế (*RFQ/PO*), Nhập kho (`WH/IN`), Kiểm kê & Xuất hủy.
- `bophantaichinhketoan` (**Bộ phận Tài chính – Kế toán**) — Quản lý hóa đơn khách hàng (`INV`), Công nợ nhà cung cấp (`BILL`) & Báo cáo doanh thu/công suất.

👉 **Chi tiết danh sách tài khoản đăng nhập & kịch bản Demo liên phòng ban:** Xem tại [THONG_TIN_TAI_KHOAN_PHAN_QUYEN.md](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/THONG_TIN_TAI_KHOAN_PHAN_QUYEN.md).

---

## 🚀 Hướng Dẫn Khởi Chạy Nhanh (Docker Environment)

### Yêu cầu môi trường
- Docker Engine & Docker Compose v2+
- Cổng khả dụng: `8069` (Odoo Web) và `5432` (PostgreSQL)

### Khởi động hệ thống
```bash
# Di chuyển vào thư mục cấu hình Docker
cd M-Hotel_Docker

# Khởi chạy cụm container ở chế độ nền
docker compose up -d

# Kiểm tra trạng thái container
docker compose ps
```

### Thông tin truy cập mặc định
- **Ứng dụng Web ERP:** [http://localhost:8069](http://localhost:8069)
- **Quản lý Database:** [http://localhost:8069/web/database/manager](http://localhost:8069/web/database/manager)
- **Tên cơ sở dữ liệu (Database):** `mhotel_dev`
- **Tài khoản Quản trị / Ban Giám Đốc:** `admin` / `admin` *(hoặc `bangiamdoc` / `admin`)*

---

## 🧪 Kiểm Thử Tự Động (Automated Unit Tests)

Các quy trình nghiệp vụ và ràng buộc cốt lõi (*chống trùng lịch phòng, vòng đời trạng thái buồng phòng, tự động trừ kho định mức*) được kiểm chứng bằng bộ Unit Tests tự động:
```bash
docker exec -i m-hotel-web odoo -c /etc/odoo/odoo.conf -d mhotel_dev --http-port=8070 \
  --test-tags /m_hotel_booking,/m_hotel_housekeeping,/m_hotel_inventory --stop-after-init
```
**Kết quả kiểm thử:** `14 tests, 0 failures, 0 errors (100% Pass Rate)`.

---

## 📄 Tài Liệu Báo Cáo & Slide Tiến Độ

- **Báo cáo đồ án mới nhất (PDF):** [IS336.R11_ERP-5.pdf](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/IS336.R11_ERP-5.pdf)
- **Project Charter:** [Project_Charter_M-Hotel.docx](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/Project_Charter_M-Hotel.docx)
- **Bộ Slide báo cáo tiến độ (11 trang):** [BAO_CAO_TIEN_DO_NHOM_12_M_HOTEL.pptx](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/BAO_CAO_TIEN_DO_NHOM_12_M_HOTEL.pptx) | [BAO_CAO_TIEN_DO_NHOM_12_M_HOTEL.pdf](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/BAO_CAO_TIEN_DO_NHOM_12_M_HOTEL.pdf)
- **Kịch bản thuyết trình 5 phút:** [NOI_DUNG_BAO_CAO_TIEN_DO_28_11_NHOM_12.md](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/NOI_DUNG_BAO_CAO_TIEN_DO_28_11_NHOM_12.md)

---

## 👥 Thành Viên Nhóm Thực Hiện (Group 12)

| STT | Họ và Tên | MSSV | Vai trò & Phân công phụ trách chính |
| :---: | :--- | :---: | :--- |
| 1 | **Bùi Minh Triết** | **24521845** | **Project Manager & BA** — Kiến trúc tổng thể, mô hình dữ liệu nền (`m_hotel_base`), Project Charter & điều phối báo cáo. |
| 2 | **Dương Đình Thảo** | **24521645** | **Developer** — Phân hệ Đặt phòng & Lễ tân (`m_hotel_booking`), cổng đặt phòng trực tuyến (`m_hotel_website`), xuất hóa đơn & thanh toán. |
| 3 | **Trần Hoàng Phúc** | **24521398** | **Developer** — Phân hệ Buồng phòng & Sự cố (`m_hotel_housekeeping`), vòng đời 6 trạng thái phòng và cơ chế khóa phòng bảo trì. |
| 4 | **Mai Anh Tuấn** | **24521929** | **Developer** — Định mức & xuất kho vật tư (`m_hotel_inventory`), quản lý thiết bị bảo trì (`m_hotel_asset`) và báo cáo `Pivot/Graph` (`m_hotel_report`). |
| 5 | **Nguyễn Quốc Triệu** | **24521855** | **DevOps & QA** — Đóng gói hạ tầng Docker, cấu hình Đa chi nhánh, phân quyền bảo mật 6 vai trò RBAC, bộ kiểm thử tự động & sao lưu CSDL. |
