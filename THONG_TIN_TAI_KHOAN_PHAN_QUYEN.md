# THÔNG TIN TÀI KHOẢN & PHÂN QUYỀN HỆ THỐNG ERP M-HOTEL

> **Dự án:** ERP Quản lý Vận hành Khách sạn M-Hotel  
> **Học phần:** IS336 — Hoạch định nguồn lực doanh nghiệp | **Nhóm:** Nhóm 12  
> **Nền tảng:** Odoo 19 Community Edition + Docker  
> **Cơ sở dữ liệu (Database Name):** `mhotel_dev`  
> **Địa chỉ truy cập (URL):** [http://localhost:8069](http://localhost:8069)  
> **Mật khẩu dùng chung cho tất cả tài khoản:** `admin`

---

## 1. Sơ Đồ Cơ Cấu Tổ Chức & Ánh Xạ Phân Quyền (RBAC)

Hệ thống được thiết kế và ánh xạ chính xác 100% theo sơ đồ cơ cấu tổ chức của khách sạn:

```
                      ┌──────────────────────┐
                      │    Ban Giám Đốc      │
                      └──────────┬───────────┘
                                 │
     ┌─────────────────┬─────────┼─────────┬─────────────────┐
     │                 │         │         │                 │
┌────┴──────────┐ ┌────┴─────┐ ┌─┴───────┐ ┌────┴────┐ ┌─────┴──────────────┐
│Bộ phận lễ tân │ │ Bộ phận  │ │ Bộ phận │ │ Bộ phận │ │Bộ phận tài chính - │
│               │ │buồngphòng│ │Kỹ thuật │ │   kho   │ │       kế toán      │
│               │ │          │ │& Bảo trì│ │         │ │                    │
└───────────────┘ └──────────┘ └─────────┘ └─────────┘ └────────────────────┘
```

---

## 2. Danh Sách Tài Khoản Theo Đúng Tên Bộ Phận

Hệ thống hỗ trợ 2 kiểu đăng nhập: **Tên đầy đủ theo bộ phận** (khuyên dùng khi demo/chấm bài) hoặc **Tên viết tắt**:

| STT | Tên hiển thị (Góc phải màn hình) | Tên đăng nhập chuẩn (Login) | Tên đăng nhập viết tắt | Mật khẩu | Các Menu & Phân hệ được phép truy cập (Đã cô lập 100%) |
| :---: | :--- | :---: | :---: | :---: | :--- |
| **1** | **Ban Giám Đốc** | `bangiamdoc` | `admin` | `admin` | **Toàn quyền:** Thấy tất cả 8 menu (Sơ đồ, Lễ tân, Buồng phòng, Khách hàng, Kho, Kỹ thuật, Báo cáo, Cấu hình). |
| **2** | **Bộ phận lễ tân** | `bophanletan` | `letan` | `admin` | **Chỉ thấy:** `Sơ Đồ & Phòng`, `Lễ Tân & Đặt Phòng`, `Khách Hàng`, `Báo Cáo Sự Cố Phòng`, và phân hệ **Hóa đơn** (`Invoicing` để xuất hóa đơn & thu tiền tại quầy). *(Ẩn: Bảng dọn phòng, Kỹ thuật, Kho, Báo cáo quản trị, Cấu hình)*. |
| **3** | **Bộ phận buồng phòng** | `bophanbuongphong` | `buongphong` | `admin` | **Chỉ thấy:** `Sơ Đồ Phòng Trực Quan` và `Buồng Phòng & Sự Cố` (Nhiệm vụ dọn dẹp + Báo sự cố). *(Ẩn toàn bộ: Đặt phòng, Khách hàng, Kỹ thuật, Kho, Báo cáo, Cấu hình)*. |
| **4** | **Bộ phận Kỹ thuật & Bảo trì** | `bophankythuat` | `kythuat` | `admin` | **Chỉ thấy:** `Kỹ Thuật & Thiết Bị` (Thiết bị phòng, Phiếu sửa chữa) và `Báo Cáo Sự Cố Phòng`. *(Ẩn toàn bộ: Đặt phòng, Buồng phòng, Khách hàng, Kho, Báo cáo, Cấu hình)*. |
| **5** | **Bộ phận kho** | `bophankho` | `kho` | `admin` | **Thấy:** `Kho & Vật Tư` (Định mức vật tư tiêu hao buồng phòng) cùng phân hệ **Mua hàng** (`Purchase`) & **Tồn kho** (`Inventory`: Nhập kho `WH/IN`, Kiểm kê). *(Ẩn các menu Lễ tân, Buồng phòng, Kỹ thuật, Báo cáo, Cấu hình)*. |
| **6** | **Bộ phận tài chính - kế toán** | `bophantaichinhketoan` | `ketoan` | `admin` | **Chỉ thấy:** `Báo Cáo & Phân Tích` (Doanh thu & Công suất) và phân hệ **Hóa đơn** (`Invoicing`). *(Ẩn toàn bộ: Lễ tân, Buồng phòng, Kỹ thuật, Kho, Cấu hình)*. |

---

## 3. Danh Sách Tài Khoản Cá Nhân Thành Viên Nhóm 12

Các thành viên nhóm đã được gắn quyền chuẩn xác theo phân công công việc và vai trò trong hệ thống:

| STT | Thành viên nhóm | Vai trò phụ trách | Tên đăng nhập (Login) | Mật khẩu | Quyền truy cập & Menu |
| :---: | :--- | :--- | :---: | :---: | :--- |
| 1 | **Bùi Minh Triết** | Project Manager / Ban Giám Đốc | `triet.bm` | `admin` | **Toàn quyền:** Thấy đầy đủ 8 menu quản trị hệ thống. |
| 2 | **Dương Đình Thảo** | Bộ phận Lễ tân (Booking, Check-in/out, Thu tiền) | `thao.dd` | `admin` | **Lễ tân:** Sơ đồ phòng, Đặt phòng, Khách hàng, Báo sự cố, Hóa đơn khách hàng. |
| 3 | **Trần Hoàng Phúc** | Bộ phận Buồng phòng (Trưởng nhóm Buồng phòng) | `phuc.th` | `admin` | **Buồng phòng:** Sơ đồ phòng, Nhiệm vụ dọn phòng, Báo sự cố. |
| 4 | **Lê Minh Khoa** | Bộ phận Buồng phòng (Nhân viên buồng phòng) | `khoa.lm` | `admin` | **Buồng phòng:** Sơ đồ phòng, Nhiệm vụ dọn phòng, Báo sự cố. |
| 5 | **Nguyễn Hoàng Nam** | Bộ phận Buồng phòng (Nhân viên buồng phòng) | `nam.nh` | `admin` | **Buồng phòng:** Sơ đồ phòng, Nhiệm vụ dọn phòng, Báo sự cố. |
| 6 | **Mai Anh Tuấn** | Bộ phận Kỹ thuật & Bảo trì (Thiết bị) | `tuan.ma` | `admin` | **Kỹ thuật:** Thiết bị phòng, Phiếu sửa chữa, Báo sự cố. |
| 7 | **Nguyễn Quốc Triệu** | Bộ phận Kho (Định mức vật tư, DevOps) | `trieu.nq` | `admin` | **Kho vật tư:** Kho hàng, Định mức vật tư tiêu hao. |
| 8 | **Đặng Thị Mai Hương** | Bộ phận Tài chính - Kế toán (Hóa đơn & Doanh thu) | `huong.dtm` | `admin` | **Kế toán:** Báo cáo doanh thu & công suất, Phân hệ Hóa đơn. |

---

## 4. Kịch Bản Demo Luồng Nghiệp Vụ Liên Phòng Ban (Cross-Department Flow)

Để minh họa tính đồng bộ dữ liệu giữa 5 bộ phận và Ban Giám Đốc:

1. **Khách đặt phòng & Nhận phòng (Bộ phận Lễ tân - `bophanletan`):**
   - Vào menu `Lễ Tân & Đặt Phòng` ➔ `Tìm Phòng Trống Nhanh` ➔ Chọn ngày và tạo đơn đặt phòng.
   - Bấm **"Xác Nhận Giữ Phòng"** ➔ Khách đến bấm **"Nhận Phòng (Check-in)"** (Phòng chuyển sang `Đang ở`).
   - Thêm dịch vụ tiêu dùng minibar / giặt ủi vào tab Folio.

2. **Trả phòng (`Check-out` - Lễ tân `bophanletan`):**
   - Lễ tân kiểm tra, bổ sung dịch vụ minibar / giặt ủi vào tab Folio và bấm **"Trả Phòng"**:
     * Phòng tự động đổi trạng thái sang `Cần dọn dẹp` (Cleaning).
     * Hệ thống tự động tạo 1 nhiệm vụ dọn phòng cho Buồng phòng.

3. **Lập hóa đơn & Thu tiền tại quầy (Lễ tân `bophanletan`) ➔ Đối soát Kế toán (`bophantaichinhketoan`):**
   - Trên đơn đặt phòng, Lễ tân bấm **"Tạo Hóa Đơn Khách Hàng"**: Hóa đơn `account.move` (`Nháp`) được sinh ra với đầy đủ tiền phòng + tiền minibar/dịch vụ.
   - Lễ tân kiểm tra chi tiết, bấm **Xác nhận** cấp số `INV/...` và bấm **Thanh toán** để thu tiền mặt/ngân hàng ngay tại quầy.
   - Bộ phận Tài chính - Kế toán (`bophantaichinhketoan`) quản lý công nợ nhà cung cấp (`BILL/...`), đối soát phiếu thu trên phân hệ **Hóa đơn (`Invoicing`)** và xem `Báo Cáo & Phân Tích` doanh thu & công suất theo chi nhánh.

4. **Dọn phòng & Trừ kho tự động (Buồng phòng ➔ Kho vật tư):**
   - Đăng nhập bằng `bophanbuongphong`.
   - Mở nhiệm vụ dọn phòng vừa sinh ra ➔ Bấm **"Bắt đầu dọn"** ➔ Sau khi dọn xong bấm **"Hoàn tất"**.
   - Phòng tự động chuyển về trạng thái `Trống` (Available) sẵn sàng đón khách mới.
   - Module Kho (`bophankho`) tự động kích hoạt phiếu xuất kho vật tư tiêu hao (bàn chải, xà phòng, nước suối) theo đúng định mức.

5. **Xử lý sự cố kỹ thuật (Buồng phòng ➔ Kỹ thuật & Bảo trì):**
   - Nếu phát hiện hư hỏng (ví dụ: hỏng điều hòa P.201), Buồng phòng bấm **"Báo Cáo Sự Cố Phòng"** (Mức khẩn cấp ➔ Phòng tự động khóa, chuyển sang `Bảo trì`).
   - Đăng nhập `bophankythuat` ➔ Mở menu `Kỹ Thuật & Thiết Bị` ➔ Tiếp nhận phiếu sửa chữa ➔ Sửa xong chuyển trạng thái hoàn tất ➔ Phòng tự mở khóa sử dụng.

6. **Giám sát toàn diện (Ban Giám Đốc - `bangiamdoc`):**
   - Đăng nhập bằng `bangiamdoc`.
   - Xem toàn bộ sơ đồ phòng trực quan của cả 2 chi nhánh (Quy Nhơn & Nhơn Lý).
   - Xem báo cáo phân tích công suất phòng (Occupancy Rate) và biểu đồ doanh thu tổng.

---

## 5. Lệnh Quản Trị Hệ Thống Nhanh (Cheat Sheet)

```bash
# Di chuyển vào thư mục Docker
cd ERP-M_hotel_managenment/M-Hotel_Docker

# Khởi động cụm dịch vụ Odoo 19 & PostgreSQL
docker compose up -d

# Nâng cấp phân quyền và các module M-Hotel
docker exec -i m-hotel-web odoo -c /etc/odoo/odoo.conf -d mhotel_dev -u m_hotel_base,m_hotel_booking,m_hotel_report --stop-after-init

# Chạy bộ Unit Tests kiểm thử tự động
docker exec -i m-hotel-web odoo -c /etc/odoo/odoo.conf -d mhotel_dev --http-port=8070 --test-tags /m_hotel_booking,/m_hotel_housekeeping,/m_hotel_inventory --stop-after-init

# Khởi động lại Web container
docker compose restart web
```
