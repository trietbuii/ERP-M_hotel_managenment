# HƯỚNG DẪN XÂY DỰNG VÀ TRIỂN KHAI MODULE M-HOTEL TRÊN ODOO 17 COMMUNITY (DOCKER & ANTIGRAVITY)

---

## PHẦN 1. CHỌN ĐÚNG MÔI TRƯỜNG TRƯỚC KHI LẬP TRÌNH

Bạn đã đăng ký Odoo Education trên trình duyệt, nhưng cần phân biệt hai môi trường:
- **Odoo Education trên web:** Dùng để trải nghiệm các ứng dụng Odoo có sẵn, tìm hiểu luồng chuẩn.
- **Odoo Community chạy trên máy tính (Local):** Cho phép bạn tạo và cài module Python tùy chỉnh `m_hotel`, kiểm soát 100% mã nguồn và làm việc hiệu quả với Antigravity.

Vì vậy, ta sẽ **giữ tài khoản Education để tham khảo**, đồng thời xây dựng môi trường phát triển riêng trên Windows. Bạn không cần xóa tài khoản Education.

### Mô hình kiến trúc phát triển:
```
[Antigravity IDE]  --->  Viết code Python, XML views, phân tích lỗi, tạo module m_hotel
       |
       v
[Docker Desktop]   --->  Chạy Odoo 17 Community và cơ sở dữ liệu PostgreSQL 15
       |
       v
[Trình duyệt Web] --->  Truy cập http://localhost:8069 (Cài module, nạp dữ liệu, test UI)
```

> **Mục tiêu cuối cùng:** Bạn sở hữu một module `M-Hotel` độc lập, chạy mượt mà trên máy tính cá nhân, dễ dàng đưa mã nguồn lên GitHub và sẵn sàng triển khai lên máy chủ demo khi bảo vệ đồ án.

---

## PHẦN 2. CÀI ĐẶT MÔI TRƯỜNG TRÊN WINDOWS

Ta sẽ dùng **Odoo 17 Community + PostgreSQL 15 + Docker Desktop + WSL 2** để bắt đầu. Đây là bộ phiên bản cố định, phù hợp với tài liệu Docker của Odoo 17; nếu đề tài hoặc module của bạn yêu cầu phiên bản khác, ta có thể điều chỉnh trước khi tạo code.

---

### Bước 1 — Kiểm tra Windows 11 trước khi cài

#### 1.1. Kiểm tra máy có đáp ứng yêu cầu không
Mở PowerShell bằng cách:
1. Nhấn phím `Windows`.
2. Gõ `PowerShell`.
3. Mở **Windows PowerShell** hoặc **Terminal**.

Chạy từng lệnh dưới đây, mỗi lệnh kiểm tra một thông tin:

* **Lệnh 1 — Xem phiên bản Windows:**
  ```powershell
  winver
  ```
  *Lệnh này mở cửa sổ hiển thị phiên bản Windows. Kiểm tra bạn đang dùng Windows 11.*

* **Lệnh 2 — Kiểm tra kiến trúc CPU:**
  ```powershell
  $env:PROCESSOR_ARCHITECTURE
  ```
  *Lệnh này cho biết kiến trúc hệ thống. Máy Intel thông thường sẽ trả về `AMD64`.*

* **Lệnh 3 — Kiểm tra RAM:**
  ```powershell
  Get-CimInstance Win32_ComputerSystem | Select-Object @{Name="RAM_GB";Expression={[math]::Round($_.TotalPhysicalMemory/1GB,1)}}
  ```
  *Lệnh này hiển thị tổng RAM theo GB. Có 8 GB vẫn có thể thử, nhưng 16 GB trở lên sẽ thoải mái hơn khi chạy Docker, Odoo và Antigravity cùng lúc.*

* **Lệnh 4 — Kiểm tra dung lượng ổ C:**
  ```powershell
  Get-PSDrive C
  ```
  *Lệnh này hiển thị dung lượng còn trống của ổ C. Nên chừa khoảng 20 GB trở lên để tải image, lưu database và phát triển module.*

* **Lệnh 5 — Kiểm tra Docker đã cài chưa:**
  ```powershell
  docker --version
  ```
  *Lệnh này hiển thị phiên bản Docker CLI nếu đã cài. Nếu báo không nhận diện lệnh, có thể Docker Desktop chưa được cài hoặc chưa nằm trong PATH.*

* **Lệnh 6 — Kiểm tra WSL 2:**
  ```powershell
  wsl --status
  ```
  *Lệnh này kiểm tra Windows Subsystem for Linux. Nếu chưa có WSL hoặc chưa cấu hình đúng, ta sẽ xử lý trước khi chạy Docker.*

---

### Bước 2 — Đánh giá kết quả kiểm tra máy & Cài Docker Desktop

Sau khi chạy các lệnh trên, kiểm tra 5 thông tin sau:
- **Phiên bản Windows** từ `winver` (Windows 11)
- **Kiến trúc CPU** (`AMD64`)
- **RAM** (Khuyến nghị ≥ 8GB – 16GB)
- **Dung lượng trống ổ C** (Đảm bảo trống ≥ 20GB)
- **Kết quả của** `docker --version` và `wsl --status`

> **Lưu ý:** Chưa cần cài PostgreSQL riêng, Python hay Odoo lúc này. PostgreSQL sẽ chạy trong container riêng, còn Odoo chạy trong container khác; Docker Compose sẽ quản lý hai dịch vụ này.

#### Hướng dẫn cài đặt Docker Desktop:
1. Tải từ trang chính thức: [Docker Desktop for Windows](https://docs.docker.com/desktop/setup/install/windows-install/) (chọn bản Windows x86-64).
2. Chạy file cài đặt, chọn backend **WSL 2** nếu được hỏi.
3. Hoàn tất cài đặt và khởi động lại máy nếu trình cài đặt yêu cầu.
4. Mở Docker Desktop, đợi trạng thái **Docker Engine** sẵn sàng (Running).

*Nếu WSL chưa được cài hoặc chưa đáp ứng, mở PowerShell bằng quyền Administrator rồi chạy:*
```powershell
# Cài WSL và bản phân phối Linux mặc định
wsl --install

# Cập nhật WSL
wsl --update

# Kiểm tra các bản phân phối và phiên bản WSL
wsl --list --verbose
```

---

### Bước 3 — Tạo cấu trúc thư mục dự án

Ta sẽ đặt toàn bộ dự án tại `C:\Projects\M-Hotel`. Chạy lệnh trong PowerShell:

```powershell
# Tạo thư mục gốc dự án
New-Item -ItemType Directory -Force C:\Projects\M-Hotel

# Chuyển vào thư mục dự án
Set-Location C:\Projects\M-Hotel

# Tạo các thư mục con: addons (chứa code) và config (chứa cấu hình Odoo)
New-Item -ItemType Directory -Force addons, config
```

- `addons/`: Chứa module Odoo tùy chỉnh (`m_hotel`).
- `config/`: Chứa file cấu hình máy chủ Odoo (`odoo.conf`).
- Thư mục gốc: Chứa `compose.yaml` và quản lý Git.

---

### Bước 4 — Tạo cấu hình Docker Compose

Tại thư mục gốc `C:\Projects\M-Hotel`, tạo file `compose.yaml`:

```yaml
services:
  db:
    image: postgres:15
    environment:
      POSTGRES_DB: postgres
      POSTGRES_USER: odoo
      POSTGRES_PASSWORD: dev_only_change_me
    volumes:
      - db-data:/var/lib/postgresql/data
    restart: unless-stopped

  web:
    image: odoo:17.0
    depends_on:
      - db
    ports:
      - "127.0.0.1:8069:8069"
    environment:
      HOST: db
      USER: odoo
      PASSWORD: dev_only_change_me
    volumes:
      - odoo-data:/var/lib/odoo
      - ./addons:/mnt/extra-addons
      - ./config:/etc/odoo
    command: ["odoo", "--config=/etc/odoo/odoo.conf", "--dev=xml"]
    restart: unless-stopped

volumes:
  db-data:
  odoo-data:
```

Tiếp theo, tạo file `config/odoo.conf`:

```ini
[options]
admin_passwd = mhotel_dev_master_change_me
addons_path = /usr/lib/python3/dist-packages/odoo/addons,/mnt/extra-addons
list_db = True
```

> **Lưu ý bảo mật:**
> - `admin_passwd`: Mật khẩu master quản trị cơ sở dữ liệu của Odoo.
> - Cổng Odoo được giới hạn bind vào `127.0.0.1` để an toàn nội bộ máy local.

---

### Bước 5 — Khởi động Odoo lần đầu

Mở PowerShell tại `C:\Projects\M-Hotel` và chạy:

```powershell
# 1. Tải image Odoo 17 và PostgreSQL 15
docker compose pull

# 2. Khởi động các container ở chế độ chạy nền
docker compose up -d

# 3. Kiểm tra trạng thái container
docker compose ps

# 4. Xem log khởi động để kiểm tra lỗi
docker compose logs --tail 100 web
```

Mở trình duyệt truy cập: **[http://localhost:8069](http://localhost:8069)**
- Điền Database Name: `mhotel_dev`
- Điền Email / Password quản trị, chọn Quốc gia Việt Nam, tích chọn Demo data nếu muốn.
- Nhấn **Create database**.

---

## PHẦN 3. DÙNG ANTIGRAVITY TẠO MODULE M_HOTEL

### Bước 6 — Cấu trúc chuẩn của module `m_hotel`

Tạo cây thư mục chuẩn trong `C:\Projects\M-Hotel\addons\m_hotel\`:

```
C:\Projects\M-Hotel\
├── compose.yaml
├── config/
│   └── odoo.conf
└── addons/
    └── m_hotel/
        ├── __init__.py
        ├── __manifest__.py
        ├── models/
        │   ├── __init__.py
        │   ├── hotel.py
        │   ├── room.py
        │   ├── booking.py
        │   └── service_request.py
        ├── security/
        │   ├── security.xml
        │   └── ir.model.access.csv
        ├── views/
        │   ├── hotel_views.xml
        │   ├── room_views.xml
        │   ├── booking_views.xml
        │   ├── service_request_views.xml
        │   └── menu_views.xml
        ├── data/
        │   └── demo_data.xml
        └── tests/
            ├── __init__.py
            └── test_booking.py
```

---

### Bước 7 — Prompt giao việc cho Antigravity (Nhiệm vụ 1)

Sao chép toàn bộ prompt dưới đây và dán vào Antigravity IDE:

```text
NHIỆM VỤ 1 — XÂY DỰNG NỀN TẢNG MODULE M-HOTEL

Bạn là lập trình viên Odoo 17 Community có kinh nghiệm với Python ORM, XML Views, PostgreSQL và kiểm thử.

1. Bối cảnh dự án
Xây dựng module Odoo tùy chỉnh tên kỹ thuật m_hotel cho hệ thống ERP quản lý vận hành khách sạn M-Hotel.
Định hướng đã được giảng viên duyệt:
- Trọng tâm: booking, lịch phòng, trạng thái phòng và sự vụ liên quan đến phòng.
- Mở rộng: vật tư, thiết bị, bảo trì và quản lý nhiều cơ sở khách sạn.
- Mục tiêu: có sản phẩm chạy được, dữ liệu demo và bộ kiểm thử để trình bày trong học phần.

2. Môi trường
- Windows.
- Docker Desktop.
- Odoo 17 Community.
- PostgreSQL 15.
- Mã nguồn addon nằm trong C:\Projects\M-Hotel\addons\m_hotel.
- Addon được mount vào /mnt/extra-addons.
- Không thay đổi phiên bản Odoo, cấu hình Docker hoặc mật khẩu nếu chưa được yêu cầu.

3. Giai đoạn hiện tại
Chỉ xây dựng nền tảng module và các mô hình dữ liệu cốt lõi.
Tạo:
- __manifest__.py
- __init__.py
- Models và các file __init__.py tương ứng.
- Security ACL và record rules cơ bản.
- XML views, actions và menus.
- Demo data.
- Bộ kiểm thử tự động cho nghiệp vụ booking.

Các mô hình ban đầu:
- m.hotel: cơ sở khách sạn.
- m.hotel.room.type: loại phòng.
- m.hotel.room: phòng.
- m.hotel.booking: đặt phòng.
- m.hotel.service.request: yêu cầu dịch vụ/sự vụ gắn với phòng.

4. Quy tắc lập trình
- Dùng ORM của Odoo; không tự tạo bảng PostgreSQL thủ công.
- Có name, active hoặc trường phù hợp cho từng mô hình.
- Có quan hệ Many2one, One2many và các ràng buộc dữ liệu phù hợp.
- Booking có khách hàng, phòng, ngày nhận phòng, ngày trả phòng, trạng thái, số đêm và tổng tiền.
- Khoảng lưu trú dùng quy ước ngày nhận phòng có tính, ngày trả phòng không tính.
- Từ chối booking nếu ngày trả phòng không sau ngày nhận phòng.
- Booking đang hoạt động không được trùng khoảng lưu trú trên cùng phòng.
- Booking đã hủy hoặc không đến không được giữ chỗ.
- Phòng đang bảo trì/ngưng sử dụng không được đặt.
- Phải xử lý xung đột khi hai giao dịch tạo booking đồng thời; không chỉ kiểm tra ở giao diện.
- Chỉ cho phép chuyển trạng thái booking theo luồng nghiệp vụ hợp lệ.
- Không cho check-in booking đã hủy.
- Không cho check-out booking chưa check-in.
- Tránh dùng các API hoặc cú pháp không tương thích Odoo 17.

5. Giao diện
Tạo menu M-Hotel với các mục:
- Tổng quan.
- Cơ sở khách sạn.
- Loại phòng.
- Phòng.
- Booking.
- Sự vụ.
Mỗi mục cần có List và Form view. Booking cần có Calendar view tương thích với Odoo 17.

6. Yêu cầu đầu ra
- Viết code trực tiếp vào đúng thư mục module.
- Không chỉ đưa ví dụ hoặc pseudocode.
- Liệt kê các file đã tạo và giải thích vai trò từng file.
- Chỉ rõ cách cập nhật module và cách xem log khi có lỗi.
- Viết test cho ngày không hợp lệ, booking trùng, booking hủy và chuyển trạng thái.
- Không tuyên bố hoàn thành nếu chưa chạy được kiểm thử.
- Nếu môi trường chưa sẵn sàng để chạy test, phải ghi rõ test nào chưa chạy.

Bắt đầu bằng việc kiểm tra cấu trúc thư mục hiện tại, sau đó thực hiện theo từng bước nhỏ. Không xóa hay ghi đè các file hiện có nếu chưa giải thích và xin xác nhận.
```

---

### Bước 8 — Kiểm tra file module sau khi sinh

Trong PowerShell, kiểm tra các file đã được tạo:

```powershell
# Liệt kê tất cả file trong module
Get-ChildItem .\addons\m_hotel -Recurse -File

# Xem nội dung file manifest
Get-Content .\addons\m_hotel\__manifest__.py
```

File `__manifest__.py` chuẩn có dạng:
```python
{
    "name": "M-Hotel",
    "version": "17.0.1.0.0",
    "category": "Services/Hotel",
    "summary": "Quản lý Vận hành Khách sạn M-Hotel",
    "depends": ["base"],
    "data": [
        "security/security.xml",
        "security/ir.model.access.csv",
        "views/hotel_views.xml",
        "views/room_views.xml",
        "views/booking_views.xml",
        "views/service_request_views.xml",
        "views/menu_views.xml",
    ],
    "demo": [
        "data/demo_data.xml",
    ],
    "application": True,
    "installable": True,
    "license": "LGPL-3",
}
```

---

### Bước 9 — Cài đặt module vào Odoo

1. Khởi động lại container (nếu cần):
   ```powershell
   docker compose up -d
   ```
2. Đăng nhập Odoo tại `http://localhost:8069`.
3. Bật **Developer Mode** (Settings -> Scroll xuống cuối -> *Activate the developer mode*, hoặc thêm `?debug=1` vào thanh địa chỉ).
4. Vào menu **Apps** -> Chọn **Update Apps List** -> Bấm **Update**.
5. Gõ tìm kiếm `M-Hotel` -> Bấm nút **Install**.
6. Sau khi cài đặt xong, ứng dụng **M-Hotel** sẽ xuất hiện trên thanh menu chính.

---

## PHẦN 4. KIỂM THỬ NGHIỆP VỤ TRƯỚC KHI LÀM GIAO DIỆN ĐẸP

### Bước 10 — Ma trận 10 Test Cases kiểm thử Booking

| Mã TC | Tình huống kiểm thử | Kết quả mong đợi |
| :---: | :--- | :--- |
| **TC01** | Đặt phòng từ 15/11 đến 18/11 | Booking hợp lệ, tự động tính số đêm = 3 |
| **TC02** | Ngày trả phòng trước hoặc bằng ngày nhận phòng | Hệ thống báo lỗi ValidationError |
| **TC03** | Hai booking trùng ngày trên cùng một phòng | Từ chối booking thứ hai ngay lập tức |
| **TC04** | Hai booking nối tiếp nhau (Khách A trả ngày 18/11, Khách B nhận ngày 18/11) | Cho phép hợp lệ (Check-out buổi sáng, Check-in buổi chiều) |
| **TC05** | Hủy một booking đã đặt | Phòng lập tức được giải phóng, cho phép khách khác đặt khoảng ngày đó |
| **TC06** | Đặt phòng đang trong trạng thái Bảo trì / Sửa chữa | Hệ thống từ chối cho đặt phòng |
| **TC07** | Thực hiện Check-in cho một booking đã bị Hủy | Hệ thống chặn và báo lỗi nghiệp vụ |
| **TC08** | Thực hiện Check-out cho một booking chưa Check-in | Hệ thống chặn và báo lỗi nghiệp vụ |
| **TC09** | Khách Check-out thành công | Trạng thái phòng tự động chuyển sang "Chờ dọn dẹp" (Dirty/Housekeeping) |
| **TC10** | Hai lễ tân bấm đặt cùng 1 phòng, cùng ngày tại cùng 1 tích tắc | PostgreSQL Constraint / Transaction chặn, chỉ 1 booking thành công |

---

### Bước 11 — Prompt nạp Dữ liệu Demo thực tế (Nhiệm vụ 2)

Sau khi logic cốt lõi chạy ổn định, gửi prompt này cho Antigravity:

```text
NHIỆM VỤ 2 — DỮ LIỆU DEMO VÀ NGHIỆP VỤ M-HOTEL

Tiếp tục module m_hotel hiện có, không viết lại module từ đầu.
- Tạo dữ liệu demo cho hai cơ sở khách sạn:
  + Cơ sở 1: M-Hotel Quy Nhơn Beach (Xuân Diệu, Quy Nhơn)
  + Cơ sở 2: M-Hotel Nhơn Lý - Eo Gió (Nhơn Lý, Quy Nhơn)
- Tạo khoảng 30–50 phòng, nhiều hạng phòng (Standard, Superior, Deluxe, Family, Suite) kèm đơn giá theo ngày và theo giờ.
- Tạo 20–50 booking có trạng thái đa dạng: Nháp, Đã xác nhận, Đang lưu trú, Đã trả phòng, Đã hủy.
- Tạo dữ liệu sự vụ gồm: Dọn phòng (Housekeeping), Yêu cầu dịch vụ, Hư hỏng và Bảo trì kỹ thuật.
- Bổ sung dữ liệu vật tư và thiết bị nếu mô hình tương ứng đã sẵn sàng.
- Tuyệt đối không tạo booking chồng lấn trái phép trên cùng một phòng.
- Không gán booking, phòng hoặc sự vụ nhầm lẫn giữa hai cơ sở.
- Dùng XML demo data chuẩn Odoo 17; tránh việc nạp trùng lặp dữ liệu mỗi lần update module.
- Viết hoặc cập nhật test tự động để xác minh số lượng bản ghi và quan hệ dữ liệu.

Trước khi sửa, kiểm tra các model hiện có và báo cáo phần đã hoàn thành. Sau khi sửa, liệt kê file thay đổi và hướng dẫn cập nhật module.
```

---

## PHẦN 5. XÂY DỰNG GIAO DIỆN & DASHBOARD

### Bước 12 — Hoàn thiện các giao diện có sẵn của Odoo

Trước khi viết OWL/JS phức tạp, hãy cấu hình hoàn hảo các view gốc của Odoo:
- **List view:** Danh sách phòng hiển thị số phòng, loại phòng, cơ sở, đơn giá, trạng thái màu sắc (badge).
- **Form view:** Thông tin chi tiết phòng, lịch sử lưu trú, danh sách thiết bị.
- **Calendar view:** Lịch booking trực quan theo phòng, theo tuần/tháng.
- **Kanban view:** Trạng thái phòng trực quan (Trống - Xanh lá, Đang có khách - Đỏ, Chờ dọn - Vàng, Bảo trì - Xám).

---

### Bước 13 — Prompt tạo Dashboard điều hành (Nhiệm vụ 3)

Gửi prompt này cho Antigravity để xây dựng bảng tổng quan quản trị:

```text
NHIỆM VỤ 3 — DASHBOARD M-HOTEL CHO ODOO 17

Hãy nâng cấp giao diện module m_hotel hiện có. Không tạo dashboard chỉ chứa dữ liệu giả.

1. Phong cách
- Giao diện quản trị khách sạn hiện đại, chuyên nghiệp, sang trọng.
- Tương thích tốt cả màn hình máy tính và điện thoại.
- Thống nhất màu sắc, typography và trạng thái trực quan.
- Giữ vững giao diện chuẩn của Odoo.

2. Chỉ số Dashboard (KPI Cards & Charts)
Hiển thị:
- Tổng số phòng theo từng cơ sở.
- Số phòng trống sẵn sàng nhận khách.
- Số phòng đã được đặt trước.
- Số phòng đang có khách lưu trú.
- Số phòng đang chờ dọn vệ sinh.
- Số phòng đang bảo trì/hỏng hóc.
- Danh sách khách check-in và check-out hôm nay.
- Tỷ lệ công suất phòng (Occupancy Rate) trong kỳ.
- Tổng doanh thu phòng thực tế.
- Số sự vụ buồng phòng / kỹ thuật đang chờ xử lý.
- Cảnh báo tồn kho vật tư Minibar / Amenities dưới mức an toàn.

3. Yêu cầu kỹ thuật
- Các KPI được tính toán thời gian thực từ dữ liệu backend Odoo.
- Bộ lọc linh hoạt theo cơ sở (Chi nhánh) và theo khoảng thời gian.
- Kiểm tra quyền truy cập trước khi hiển thị dữ liệu.
- Ưu tiên XML views/Action cards; kết hợp OWL component nếu cần tương tác biểu đồ động.
- Không chứa dữ liệu nhạy cảm hay mật khẩu cứng trong mã nguồn.
```

---

### Bước 14 — Hoàn thiện các phân hệ mở rộng

Triển khai lần lượt theo thứ tự nghiệp vụ:
1. **Buồng phòng (Housekeeping):** Bảng phân công nhân viên dọn phòng, nút bấm chuyển trạng thái phòng từ *"Chờ dọn"* sang *"Sẵn sàng đón khách"*.
2. **Sự cố & Bảo trì (Maintenance):** Ghi nhận thiết bị hỏng, phân công thợ kỹ thuật, theo dõi tiến độ Kanban.
3. **Quản lý Minibar & Amenities:** Kết nối tồn kho vật tư, xuất kho khi khách sử dụng.
4. **Phân quyền người dùng (RBAC):**
   - Quản trị viên / Giám đốc (Toàn quyền)
   - Lễ tân (Tạo booking, check-in, check-out, lập hóa đơn)
   - Nhân viên buồng phòng (Xem và cập nhật trạng thái dọn phòng)
   - Nhân viên kỹ thuật (Tiếp nhận sự cố bảo trì)

---

## PHẦN 6. KIỂM THỬ CUỐI CÙNG & CHUẨN BỊ DEMO BÁO CÁO

### Bước 15 — Lệnh cập nhật module và kiểm tra Log

Mỗi lần chỉnh sửa code Python hoặc XML, hãy chạy lệnh sau trong PowerShell để nâng cấp module mà không cần bấm thủ công trên web:

```powershell
# Cập nhật module m_hotel trực tiếp từ dòng lệnh
docker compose exec web odoo -d mhotel_dev -u m_hotel --stop-after-init --db_host=db --db_user=odoo --db_password=dev_only_change_me

# Xem 200 dòng log gần nhất để kiểm tra lỗi cú pháp/logic
docker compose logs --tail 200 web
```

---

### Bước 16 — Checklist 12 tiêu chí nghiệm thu đồ án

- [ ] **1.** Module `m_hotel` cài đặt và cập nhật mượt mà, không sinh lỗi hệ thống.
- [ ] **2.** Tạo, sửa, hủy đơn đặt phòng (Booking) hoạt động chuẩn xác.
- [ ] **3.** Chống trùng phòng 100%, từ chối cả trường hợp 2 giao dịch gửi đồng thời.
- [ ] **4.** Quy trình Check-in / Check-out tính đúng số đêm và tổng tiền phòng (VNĐ).
- [ ] **5.** Trạng thái phòng chuyển đổi mượt mà (Trống -> Có khách -> Chờ dọn -> Sẵn sàng).
- [ ] **6.** Phân hệ Sự vụ & Bảo trì phân công đúng người, có lịch sử theo dõi rõ ràng.
- [ ] **7.** Dữ liệu demo đầy đủ 2 cơ sở khách sạn tại Bình Định, 30+ phòng và 30+ booking.
- [ ] **8.** Phân quyền bảo mật đã kiểm thử qua các tài khoản (Quản lý, Lễ tân, Buồng phòng).
- [ ] **9.** Dashboard điều hành tổng hợp chỉ số thực tế từ cơ sở dữ liệu.
- [ ] **10.** Bộ kiểm thử tự động (Unit Tests) chạy pass 100%.
- [ ] **11.** Mã nguồn được đưa lên repository GitHub cá nhân/nhóm chỉn chu.
- [ ] **12.** Chuẩn bị sẵn kịch bản demo trực quan và slide/báo cáo DOCX phục vụ vấn đáp.

---

### Bước 17 — Đưa dự án lên GitHub

```powershell
# Khởi tạo Git repository
git init

# Tạo file .gitignore để không đẩy file rác/mật khẩu
@"
*.pyc
__pycache__/
.env
db-data/
odoo-data/
"@ | Out-File -Encoding utf8 .gitignore

# Commit và push mã nguồn
git add .
git commit -m "feat: hoàn thiện nền tảng module m_hotel cho Odoo 17"
git branch -M main
git remote add origin https://github.com/<tai-khoan-cua-ban>/m-hotel-odoo.git
git push -u origin main
```

---

## 📌 LỘ TRÌNH THỰC HIỆN NGAY HÔM NAY:
1. ✅ **Bước 1-2:** Cài đặt Docker Desktop và kiểm tra `wsl --version`, `docker --version`.
2. ✅ **Bước 3-4:** Tạo thư mục `C:\Projects\M-Hotel`, viết file `compose.yaml` và `config\odoo.conf`.
3. ✅ **Bước 5:** Chạy `docker compose up -d` và mở thành công trang Odoo tại `http://localhost:8069`.
4. ✅ **Bước 6-7:** Mở Antigravity, gửi **Nhiệm vụ 1** để tự động sinh module `m_hotel`.
5. ✅ **Bước 8-9:** Update App List trên Odoo và cài đặt module `M-Hotel`.
