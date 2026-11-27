# BẢNG RÀ SOÁT CHI TIẾT CÁC MỤC & ĐIỂM CẦN SỬA ĐỐI VỚI FILE `IS336.R11_ERP-3.pdf`

> **Tài liệu đối chiếu:** [IS336.R11_ERP-3.pdf](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/IS336.R11_ERP-3.pdf) *(244 trang)*  
> **Căn cứ kiểm tra:**
> 1. Góp ý chuyên môn về BPMN & ánh xạ Odoo của giảng viên **ThS. Huỳnh Đức Huy** (`IS336.R11`).
> 2. Mã nguồn thực tế của dự án tại `M-Hotel_Docker/addons/` và dữ liệu nền [demo_data.xml](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/M-Hotel_Docker/addons/m_hotel_base/data/demo_data.xml).
> 3. Tính nhất quán xuyên suốt từ Chương 1 đến Chương 4.

---

## PHẦN 1. TỔNG HỢP 6 LỖI NGHIÊM TRỌNG NHẤT CẦN XỬ LÝ NGAY (ƯU TIÊN SỐ 1)

Trước khi chỉnh câu chữ, nhóm cần xử lý ngay **6 lỗi "chết người"** đang xuất hiện trực tiếp trong file PDF:

1. **Dính bản nháp thừa & ghi chú nội bộ quên xóa trong PDF:**
   - **Trang 13 – 19:** Bị lặp nguyên **một mục `1.1.5. Dữ liệu giao dịch` bản cũ** (chứa toàn ảnh màn hình trống rỗng *"No available dashboard"*, *"0 To Do"*, *"My Company"*) nằm ngay trước mục `1.1.5` bản mới (Trang 20 – 29).
   - **Trang 239 – 242:** Cuối file PDF còn dính 4 trang bảng nháp ghi tiêu đề **`"M hotel ở quê nha"`** và **`"M hotel ở Vũng Tàu"`** với số tầng/số phòng lệch hoàn toàn so với Chương 1.
   - **Trang 92, 133–148, 200–217, 236, 238:** Còn nguyên các dòng nhắc việc nội bộ như `(Chèn ảnh chụp màn hình...)`, `Bảng 3.XX`, `[Hình 3.XX: ... — Đính kèm ảnh...]`, và câu nhắc `→ Người dùng, mở tài khoản của nhân viên lễ tân Dương Đình Thảo... rồi chụp lại màn hình)`.
2. **Dán nhầm sơ đồ BPMN giữa hai quy trình khác nhau:**
   - **Trang 177 (`Hình 3.7.1` – Kiểm kê kho vật tư):** Văn bản mô tả quy trình Kiểm kê kho 2 làn, nhưng **ảnh sơ đồ chèn vào lại là sơ đồ BPMN 4 làn của mục `3.4` (Định mức vật tư buồng phòng)**!
3. **Mất tiêu đề cấp Chương (Heading 1):**
   - **Trang 41:** Mất hoàn toàn tiêu đề **`CHƯƠNG 2...`** và mục **`2.1. Giới thiệu ERP`** (nhảy thẳng vào `2.1.1`).
   - **Trang 62:** Mất hoàn toàn tiêu đề **`CHƯƠNG 3...`** (nhảy thẳng vào `3.1`).
4. **Vi phạm trực tiếp góp ý BPMN của thầy Huỳnh Đức Huy:**
   - Sơ đồ `3.2` (Trang 67 – 41 bước) và `3.3` (Trang 103 – 24 bước) quá khổng lồ, chữ trên trang A4 bị thu nhỏ không thể đọc được.
   - Các mục `3.3`, `3.5`, `3.8` đưa quá nhiều bước làm việc tay chân ngoài đời thực (*thu gom đồ vải, hút bụi, xịt rửa dàn lạnh, đo gas, tìm kiếm NCC*) vào BPMN thay vì tập trung vào thao tác trên Odoo (**System-Oriented**).
5. **Trùng lặp nội dung nặng nề giữa các mục trong Chương 3 & thiếu Báo cáo quản trị:**
   - Mục `3.2`, `3.3`, `3.4`, `3.8` lặp đi lặp lại cùng các bảng dữ liệu (*Nhiệm vụ buồng phòng, Sự cố, Định mức vật tư, Thiết bị, Phiếu bảo trì*).
   - Mục `3.9` và `3.10` lặp lại 100% quy trình thanh toán Hóa đơn nhà cung cấp, trong khi mục `3.10` tên là *"Quy trình kế toán và **báo cáo quản trị**"* nhưng **không có bất kỳ nội dung hay hình ảnh nào về Báo cáo quản trị (`Pivot` / `Graph`)**.
6. **Râu ông nọ cắm cằm bà kia về Tên chi nhánh, Kho và Tiền tệ:**
   - Chi nhánh ở Chương 1 là **Gia Lai** & **Vũng Tàu**, nhưng Trang 62 (`3.1`) lại ghi **Quy Nhơn Beach & Nhơn Lý - Eo Gió**, còn ảnh kho Trang 127 & 195 lại hiện **Kho Trung Tâm Quy Nhơn Central (`QN/OUT`, `QN/INT`)**.
   - Nhiều ảnh hóa đơn/mua hàng bị hiển thị ký hiệu đô-la **`$`** trước số tiền VNĐ (`$ 3.600.000,00`), giá 1 chai Lavie nhập `500.000 ₫/chai` (Trang 165), hoặc lấy tên khách ở (`Nguyễn Văn An`, `David Miller`) và tên chi nhánh (`M-Hotel Vũng Tàu Resort`) làm Nhà cung cấp bán vật tư!

---

## PHẦN 2. CHI TIẾT CÁC ĐIỂM CẦN SỬA THEO TỪNG CHƯƠNG & TỪNG TRANG PDF

### I. Lỗi trình bày & Bố cục toàn file PDF

| Vị trí trang PDF | Lỗi hiện tại trong `IS336.R11_ERP-3.pdf` | Hướng xử lý / Cách sửa |
| :--- | :--- | :--- |
| **Trang 2, 30, 33, 38–40, 47, 52, 61, 168, 234, 243–244** | Có tới **13 trang trắng hoàn toàn** (hoặc chỉ có 1 dòng chữ trơ trọi như Trang 168) do ngắt trang `Page Break` thừa. | Xóa các dấu `Enter` / `Page Break` thừa, chỉ ngắt trang mới khi sang đầu mỗi Chương lớn. |
| **Toàn bộ file** | Chưa có Trang bìa, Mục lục tự động, Danh mục Bảng và Danh mục Hình vẽ. | Bổ sung Trang bìa chuẩn UIT (`IS336.R11 - Nhóm 12`), Mục lục tự động và Danh mục Bảng/Hình ở đầu báo cáo. |

---

### II. Chương 1 – Giới thiệu đề tài (Trang 1 – 37)

| Mục | Trang PDF | Điểm chưa hợp lý / Lỗi sai | Cách sửa cụ thể |
| :--- | :---: | :--- | :--- |
| **1.1.1** | Trang 3 | Dòng `- Người đại diện pháp luật:` đang bỏ trống thông tin. | Điền tên Giám đốc: **`Bùi Minh Triết`** (đồng bộ với Bảng 1.2 ở Trang 35). |
| **1.1.3** | Trang 5 | Dòng cuối của *Bộ phận Tài chính – Kế toán* bị dư dấu ngoặc vuông: `...toàn bộ hệ thống].` | Xóa dấu `]`, sửa thành `...toàn bộ hệ thống.` |
| **1.1.4.b** | Trang 8 | Ghi *"Mỗi phòng được quản lý chặt chẽ theo **5** trạng thái vòng đời"*, thiếu trạng thái thứ 6 có trong code `hotel_room.py`. | Sửa thành **6 trạng thái** (bổ sung `Khóa tạm thời - Out of Service` để khớp với Bảng trạng thái phòng ở Chương 3). |
| **1.1.4.d** | Trang 11 | `Hình 1.5` ghi chú thích là *"Danh mục vật tư tiêu hao Amenities và dịch vụ Minibar"*, nhưng ảnh chèn vào lại là **Định mức vật tư buồng phòng** (trùng với `Hình 1.15` trang 26). | Thay `Hình 1.5` bằng ảnh chụp màn hình danh sách **Sản phẩm (`product.template`)** có lọc các mặt hàng Vật tư, Minibar và Dịch vụ khách sạn. |
| **1.1.4.f** | Trang 12 | Trong bảng ảnh `Hình 1.7`, Cơ sở Gia Lai xuất hiện phòng `P.108`, `P.501` và Vũng Tàu xuất hiện `KC.301`, `KC.Villa-1` (không khớp danh sách 31 phòng ở Trang 8). | Chỉnh lại tên phòng gắn thiết bị trên Odoo về đúng dải phòng `P.101 – P.303` (Gia Lai) và `P.101 – P.502` (Vũng Tàu) rồi chụp lại, hoặc lọc ẩn các dòng demo cũ. |
| **1.1.5 (Bản cũ bị thừa)** | **Trang 13 – 19** | **Bị lặp nguyên 1 mục `1.1.5. Dữ liệu giao dịch` cũ** gồm `a` đến `i` (`Hình 1.8` $\rightarrow$ `Hình 1.17`) chứa giao diện trống rỗng (*No available dashboard*, *Create a customer invoice*, *My Company*, 5 hạng phòng tiếng Anh cũ). | **XÓA BỎ HOÀN TOÀN từ Trang 13 đến hết Trang 19.** Chỉ giữ lại mục `1.1.5` hoàn chỉnh ở Trang 20 – 29. |
| **1.1.5 (Bản chuẩn)** | Trang 20 – 29 | - Trang 27–28 (`Hình 1.17, 1.18, 1.19`): Đơn vị tiền tệ hiển thị dấu `$` trước số tiền VNĐ.<br>- Trang 28: Từ `Hình 1.19` nhảy cóc thẳng lên `Hình 1.22` và `Hình 1.23` (mất `1.20`, `1.21`). | - Đánh lại số hình liên tục: `Hình 1.8a, 1.8b, 1.9 ... 1.19, 1.20, 1.21`.<br>- Cấu hình ký hiệu tiền tệ `₫` (VND) thay cho `$` nếu chụp lại ảnh. |
| **1.3** | Trang 35 – 37 | **Bảng 1.2:**<br>1. `Trần Hoàng Phúc` (Nhân viên Lễ tân) và `Mai Anh Tuấn` (Trưởng bộ phận Lễ tân) bị copy-paste **trùng y hệt 100%** mô tả trách nhiệm.<br>2. Bị lệch vai trò so với Trang 238 (ghi Dương Đình Thảo là Lễ tân) và `THONG_TIN_TAI_KHOAN_PHAN_QUYEN.md` (Trần Hoàng Phúc là Buồng phòng, Mai Anh Tuấn là Kỹ thuật). | Tách rõ trách nhiệm của Trưởng lễ tân (phê duyệt đổi giá/hủy cọc, giám sát ca) với Nhân viên lễ tân; đồng thời thống nhất đúng 1 danh sách phân vai nhân sự giữa Chương 1, ảnh chụp Chương 3 và Chương 4. |

---

### III. Chương 2 – Cơ sở lý thuyết & Bài toán ứng dụng (Trang 41 – 60)

| Mục | Trang PDF | Điểm chưa hợp lý / Lỗi sai | Cách sửa cụ thể |
| :--- | :---: | :--- | :--- |
| **Đầu Chương 2** | Trang 41 | **Mất tiêu đề `CHƯƠNG 2`** và **mất tiêu đề mục `2.1. Giới thiệu ERP`**, vào trang 41 là hiện ngay `2.1.1. Khái niệm về ERP`. | Chèn thêm tiêu đề cấp 1 **`CHƯƠNG 2. TỔNG QUAN VỀ ERP VÀ BÀI TOÁN ỨNG DỤNG TẠI M-HOTEL`**, đoạn dẫn nhập chương và tiêu đề **`2.1. Giới thiệu ERP`**. |
| **2.1.4** | Trang 45 | Đoạn *"Tối ưu công suất phòng và chống trùng lặp:..."* bị thiếu dấu gạch đầu dòng `-` và không in đậm đầu mục như các ý khác. | Thêm dấu `-` đầu dòng và định dạng đồng bộ các ý lợi ích. |
| **2.3** | Trang 53 | Tiêu đề `2.3. Mô tả bài toán ứng dụng ERP vào đề tài hay Casestudy` còn giữ nguyên chữ trong template đề cương môn học (*"vào đề tài hay Casestudy"*). | Sửa lại trang trọng thành: **`2.3. Mô tả bài toán ứng dụng ERP tại chuỗi Khách Sạn M (M-Hotel)`**. |
| **2.3.3** | Trang 58 | Lỗi chính tả ở ý thứ 3: *"nước khoảng, minibar"*. | Sửa thành *"nước khoáng, minibar"*. |

---

### IV. Chương 3 – Phân tích, thiết kế và triển khai quy trình nghiệp vụ (Trang 62 – 234)

*(Đây là trọng tâm chấm điểm của môn học và là phần thầy Huỳnh Đức Huy trực tiếp góp ý. Bạn có thể thay thế toàn bộ khung nội dung bằng file [CHUONG_3_MOI_CHUAN_SYSTEM_ORIENTED.md](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/CHUONG_3_MOI_CHUAN_SYSTEM_ORIENTED.md) tôi vừa tạo).*

| Mục hiện tại trong PDF | Trang PDF | Các lỗi cụ thể trong `IS336.R11_ERP-3.pdf` | Cách sửa theo chuẩn System-Oriented của thầy Huy |
| :--- | :---: | :--- | :--- |
| **Đầu Chương 3 & Mục 3.1** | Trang 62 – 66 | 1. **Thiếu tiêu đề `CHƯƠNG 3...`** ở đầu trang 62.<br>2. Dòng cuối đoạn 1 (Trang 62) ghi sai tên chi nhánh thành: ***"(Cơ sở Quy Nhơn Beach và Cơ sở Nhơn Lý - Eo Gió)"***.<br>3. Trang 65 (`3.1.2.c`) gọi tên hạng phòng là *"Phòng tiêu chuẩn, Phòng cao cấp"* không khớp với 6 hạng phòng ở Chương 1. | 1. Bổ sung tiêu đề Chương 3.<br>2. Sửa thành: **Khách Sạn M (Cơ sở 1 - Gia Lai)** và **M-Hotel Vũng Tàu Resort (Cơ sở 2 - Vũng Tàu)**.<br>3. Đổi tên hạng phòng về đúng `Phòng đơn, Phòng đôi, Phòng ba giường, Phòng tập thể, Phòng gia đình, Căn hộ áp mái`. |
| **3.2. Quy trình bán hàng** | Trang 67 – 102 | 1. **BPMN `Hình 3.1` (Trang 67) & `Bảng 3.2` (Trang 67–78):** Gộp tới **41 bước** (cả Lễ tân, Kế toán, Buồng phòng dọn dẹp, Sự cố kỹ thuật, Xuất kho vật tư) vào 1 hình duy nhất $\rightarrow$ **Chữ trên A4 mờ tịt không đọc được**, vi phạm nghiêm trọng nguyên tắc *Clean & Clear* và *Không ôm đồm*.<br>2. **Nhảy số & Trùng bảng (Trang 83–86):** Mất `Bảng 3.6`, mất `Hình 3.5`; đưa nhầm `Bảng 3.7 (Nhiệm vụ buồng phòng)` và `Bảng 3.8 (Biên bản sự cố)` vào mục Bán hàng.<br>3. **Sót ghi chú nháp (Trang 92):** Dòng cuối trang 92 còn chữ `(Chèn ảnh chụp màn hình tab Dịch Vụ & Minibar)`.<br>4. **Sai mã chứng từ:** Bảng 3.4 ghi `BK/2026/001`, trong khi code & ảnh là `HB/2026/...`.<br>5. **Lấn sân mục khác:** Bước 9–10 (Trang 96–97) và Ngoại lệ `b` (Trang 99–101, mất `Hình 3.23`) lại đi minh họa Dọn phòng và Sự cố kỹ thuật! | **Tách mục `3.2` quá tải thành 2 quy trình gọn (mỗi BPMN chỉ 8 bước trên Odoo):**<br>- **`3.2.` Quy trình Đặt phòng đa kênh và Nhận phòng (`Booking & Check-in`)**: Chỉ giữ `res.partner`, `hotel.room.rate`, `hotel.booking`; ngoại lệ Overbooking & Hủy đơn.<br>- **`3.3.` Quy trình Phục vụ lưu trú, Trả phòng và Quyết toán (`Check-out & Billing`)**: Giữ `hotel.booking.line` (Folio) và `account.move` (Hóa đơn khách hàng); xóa toàn bộ bước dọn phòng/sự cố bị lẫn vào đây. |
| **3.3. Vận hành buồng phòng & xử lý sự cố** | Trang 103 – 127 | 1. **Nhảy vọt số hiệu:** Từ `Hình 3.26` nhảy vọt lên `Hình 3.42`; từ `Bảng 3.9` nhảy lên `Bảng 3.14`.<br>2. **Vi phạm System-Oriented (Trang 104–106):** Đưa hàng loạt việc tay chân ngoài phần mềm vào BPMN (*Thu gom đồ vải bẩn, phân loại giặt là, hút bụi sàn, lau toilet, nạp gas điều hòa, thay vòi sen*).<br>3. **Trùng lặp 4 bảng dữ liệu (Trang 110–116):** Bảng `3.17, 3.18` trùng với mục `3.4`; Bảng `3.19, 3.20` trùng với mục `3.8`.<br>4. **Lộ dữ liệu chi nhánh Quy Nhơn cũ (Trang 127):** `Hình 3.68` và `3.69` hiện kho **`Kho Trung Tâm Quy Nhơn Central (QN/OUT/00002)`** và phòng `P.305, P.501` tại Gia Lai! | 1. **Tách phần Sự cố sang đi chung với Bảo trì kỹ thuật (Mục `3.5` mới)**; còn phần Dọn phòng ghép với Định mức tiêu hao thành **Mục `3.4` mới**.<br>2. Xóa bỏ toàn bộ các bước vệ sinh vật lý khỏi BPMN, chỉ giữ thao tác bấm `Bắt Đầu Dọn Dẹp` $\rightarrow$ `Hoàn Thành (Phòng Sạch)` và xử lý tự động của Odoo.<br>3. Chụp lại 2 ảnh phiếu kho `Hình 3.68, 3.69` trên kho **Khách Sạn M (Cơ sở 1 - Gia Lai)** thay vì kho Quy Nhơn. |
| **3.4. Định mức vật tư tiêu hao buồng phòng** | Trang 128 – 148 | 1. **Đánh lùi số Hình & trùng số Bảng:** Đang từ `Hình 3.69` lùi ngược về `Hình 3.37 – 3.55`; trùng toàn bộ số `Bảng 3.14 – 3.19` với mục `3.3`!<br>2. **Dính chữ placeholder nháp ở TẤT CẢ 18 hình (Trang 133–148):** Mọi hình đều bị lặp dòng `[Hình 3.xx: ... — Đính kèm ảnh giao diện thực tế hệ thống Odoo 19]` (Trang 133 còn thiếu dấu `]`).<br>3. Trang 134 (Bảng 3.16, STT 5): Lỗi gõ phím `"Đơn vị mđo lường"`. | 1. Xóa toàn bộ 18 dòng chữ nháp trong ngoặc vuông `[...]`, chỉ giữ lại 1 dòng chú thích chuẩn dưới mỗi ảnh.<br>2. Sửa lỗi chính tả `"đo lường"` và gộp gọn với phần Nhiệm vụ buồng phòng thành quy trình **Điều phối buồng phòng & Tự động trừ định mức** (7 bước). |
| **3.5. Mua hàng tiếp tế vật tư** | Trang 149 – 168 | 1. **Đúng lỗi thầy Huy nêu ví dụ trong email:** BPMN `Hình 3.5.1` (Trang 149) và bảng `3.5.2.1` viết chung chung ngoài hệ thống (*Kiểm tra nguồn cung, Tìm kiếm NCC, Đánh giá chọn NCC*), cột *Đối tượng thực hiện* từ STT 2–7 để trống.<br>2. **Thừa bảng lý thuyết E-commerce (Trang 156–164):** `Bảng 3.23 (Biến thể sản phẩm)` và mục `f (Thuộc tính sản phẩm - thiếu tên bảng)` bàn về bộ lọc Website E-commerce, Ribbon màu sắc... không dùng trong mua vật tư khách sạn.<br>3. **Ảnh chụp form rỗng / dữ liệu vô lý:** Trang 155, 161 chụp mẫu `VD: Burger phô mai`, `Lumber Inc`; Trang 164 cắt ảnh tiếng Anh; Trang 165 (`Hình 3.87`) nhập `Nước khoáng Lavie 500ml` đơn giá **`500.000 ₫/chai`**; Trang 167 (`Hình 3.93`) hóa đơn `0 ₫`!<br>4. **Lỗi biên tập:** Trang 164 lặp 2 lần câu *"Bước 1: Trong phần mua hàng..."*; mất `Hình 3.90–3.92, 3.94`; Trang 168 trắng tinh chỉ có 1 dòng caption; **thiếu mục `3.5.3.2. Ngoại lệ`**. | 1. Vẽ lại BPMN Mua hàng chỉ gồm **6 bước trên Odoo**: `Tạo RFQ` $\rightarrow$ `Gửi RFQ qua Email` $\rightarrow$ `Cập nhật giá báo giá` $\rightarrow$ `Xác nhận đơn hàng (PO)` $\rightarrow$ `Odoo tự sinh Phiếu nhận kho WH/IN`.<br>2. Xóa bảng Biến thể & Thuộc tính E-commerce; thay các ảnh `Burger phô mai / Lumber Inc / Lavie 500k` bằng dữ liệu thật của M-Hotel.<br>3. Xóa Bước 5 (Thanh toán Bill) ở cuối mục này vì đã có quy trình Nhập kho và Công nợ riêng; bổ sung ngoại lệ *Hủy RFQ*. |
| **3.6. Nhập kho vật tư** | Trang 169 – 176 | 1. Tiêu đề `3.6. QUY TRÌNH NHẬP KHO VẬT TƯ` viết IN HOA lệch chuẩn.<br>2. Trang 169 ghi *"3 làn tác nghiệp"*, nhưng trong hình `Hình 3.6.1` lại vẽ **4 làn** (thêm làn Nhà cung cấp ở đáy).<br>3. **Tất cả 7 ảnh chụp Odoo từ Trang 172 đến 176 đều KHÔNG CÓ dòng chú thích `Hình 3.xx`**. | 1. Đổi tiêu đề về chữ thường; bỏ làn Nhà cung cấp hoặc bỏ bước Lập hóa đơn của Kế toán ra khỏi BPMN Nhập kho để gọn đúng 2 làn (`Bộ phận Kho` & `Hệ thống Odoo`).<br>2. Bổ sung đầy đủ chú thích `Hình 3.xx` dưới tất cả các ảnh. |
| **3.7. Kiểm kê kho vật tư** | Trang 177 – 182 | 1. **LỖI NẶNG NHẤT (Trang 177):** `Hình 3.7.1` **dán nhầm ảnh sơ đồ BPMN của mục `3.4` (Định mức vật tư)**!<br>2. Tiêu đề `3.7` viết IN HOA.<br>3. Tất cả 6 ảnh chụp từ Trang 180 đến 182 đều **thiếu chú thích `Hình 3.xx`**. | 1. **Thay ngay `Hình 3.7.1`** bằng sơ đồ BPMN Kiểm kê kho 2 làn (`Bộ phận Kho` & `Hệ thống Odoo` – 6 bước).<br>2. Đổi tiêu đề về chữ thường và đánh số chú thích cho toàn bộ 6 ảnh chụp màn hình. |
| **3.8. Quản trị tài sản & bảo trì thiết bị** | Trang 183 – 199 | 1. **Trong bản PDF đang bị trùng lặp nặng với nửa sau mục `3.3`** (cùng mô tả lập biên bản sự cố `INC/...` $\rightarrow$ khóa phòng $\rightarrow$ tạo phiếu bảo trì `Khắc phục`), trong khi thực tế code `maintenance.request` có tách 2 kiểu: **`Khắc phục` (`corrective` - từ sự cố)** và **`Phòng ngừa` (`preventive` - bảo dưỡng định kỳ)**.<br>2. **Vi phạm System-Oriented (Trang 185):** Các bước 10, 12, 14, 15 mô tả chi tiết thao tác thợ điện lạnh (*xịt rửa dàn tản nhiệt, nạp gas, siết đấu nối điện, chạy thử tải 15–30 phút*).<br>3. **Lỗi đánh số & dữ liệu ảnh:** Đánh trùng lại `Bảng 3.22 – 3.26`; mất `Hình 3.75 – 3.77`; Trang 195 (`Hình 3.85`) lại lộ chữ **`Kho Trung Tâm Quy Nhơn Central`**; cuối Trang 199 gõ thiếu số thành `(Hình 3.9: ...)` và trên viết `P.203`, dưới ghi `P.104`. | 1. **Tách rạch ròi thành 2 quy trình riêng biệt theo đúng code:**<br>- **Mục `3.5` mới: Quy trình Xử lý sự cố buồng phòng (`Corrective` – 7 hộp):** Lập `hotel.incident` $\rightarrow$ khóa phòng $\rightarrow$ sinh phiếu sửa chữa `Khắc phục` $\rightarrow$ mở khóa phòng.<br>- **Mục `3.6` mới: Quy trình Bảo dưỡng định kỳ thiết bị (`Preventive` – 6 hộp):** Quản lý `maintenance.equipment` gắn `room_id` $\rightarrow$ tạo phiếu kiểu `Phòng ngừa` theo lịch hẹn (`schedule_date`) $\rightarrow$ cộng dồn Smart Button `Bảo trì` trên phòng.<br>2. Xóa các bước tháo lắp cơ khí ngoài đời khỏi BPMN; sửa ảnh phiếu kho Quy Nhơn Trang 195 và lỗi chú thích Trang 199. |
| **3.9. Quản lý công nợ nhà cung cấp** | Trang 200 – 217 | 1. **Chưa đánh số bất kỳ Bảng và Hình nào** trong suốt 18 trang: Toàn bộ đang để `Bảng 3.XX` và `[Hình 3.XX: ... — Đính kèm ảnh...]`.<br>2. **Trang 207:** Ảnh hóa đơn `BILL/2026/11/0001` đang ở trạng thái **Nháp trống trơn** (không có sản phẩm), lại ghi chú thích là *"Hóa đơn đã vào sổ"*, và chọn Nhà cung cấp là **`M-Hotel Vũng Tàu Resort`** (chi nhánh của chính mình!).<br>3. Số tiền mua 100 bàn chải hiển thị `$ 1.200,00` (đơn giá `12,00` và dính ký hiệu `$`). | 1. Gộp với phần không trùng của `3.10` thành mục **`3.9` mới**, điền đầy đủ số thứ tự Bảng và Hình, xóa chữ `[Đính kèm ảnh...]`.<br>2. Xóa/thay ảnh Trang 207 bằng hóa đơn mua từ Nhà cung cấp thực tế (VD: *Công ty TNHH Cung Cấp Đồ Dùng Khách Sạn Á Châu*) với mệnh giá VNĐ chuẩn (`12.000 ₫` thay vì `12,00`). |
| **3.10. Kế toán và báo cáo quản trị** | Trang 218 – 234 | 1. **Lệch cấu trúc mục:** Chia thành `3.10.1` $\rightarrow$ `3.10.5` (khác hoàn toàn cấu trúc `3.x.1 – 3.x.2 – 3.x.3` của cả chương) và thiếu mục **Ngoại lệ**.<br>2. **Thiếu 100% Báo cáo quản trị:** Tên mục có *"và báo cáo quản trị"* nhưng hoàn toàn không đề cập đến module `m_hotel_report` (bảng `Pivot` và biểu đồ `Graph` công suất/doanh thu).<br>3. **Trùng lặp 100%:** Toàn bộ nhánh thanh toán tiền hàng tiếp tế vật tư lặp lại y nguyên mục `3.9`; nhánh thu tiền khách lưu trú lặp lại cuối mục `3.2`.<br>4. **Sai tên tiêu đề & STT:** Trang 219 tiêu đề `3.10.2.1` ghi *"đơn hoàn tiền và công nợ nhà cung cấp"* nhưng hình BPMN bên dưới lại là *Thu tiền phòng khách hàng*! Trang 221 có **2 dòng cùng STT `5`**; Trang 223 & 224 có **2 mục cùng đánh số `3.10.4.1`**.<br>5. **Sai đối tượng trên ảnh Odoo:** Trang 219, 231, 232 chọn Nhà cung cấp bán mền gối là **`Nguyễn Văn An`** và **`David Miller`** (tên khách thuê phòng!) trên công ty `My Company`; toàn bộ ảnh thiếu chú thích `Hình 3.xx`. | 1. Cắt bỏ phần thu tiền khách hàng (đã đưa về `3.3` mới) và cắt bỏ phần lặp lại thanh toán NCC.<br>2. Chuyển trọng tâm mục cuối Chương 3 sang **Kế toán công nợ nhà cung cấp & Báo cáo quản trị đa chi nhánh (`hotel.occupancy.report`)**, bổ sung đặc tả SQL View và hình minh họa bảng xoay **Pivot + Biểu đồ Graph** so sánh doanh thu/công suất giữa **Cơ sở 1 (Gia Lai)** và **Cơ sở 2 (Vũng Tàu)**. |

---

### V. Chương 4 & Phần cuối tài liệu (Trang 235 – 244)

| Mục / Vị trí | Trang PDF | Điểm chưa hợp lý / Lỗi sai | Cách sửa cụ thể |
| :--- | :---: | :--- | :--- |
| **Mở đầu Chương 4 & Thiếu mục 4.4** | Trang 235 | Mở đầu Chương 4 khẳng định hệ thống bảo mật dựa trên **3 trụ cột**: *"Phân quyền truy cập, An toàn dữ liệu và **Cơ chế dự phòng**"*, nhưng nội dung bên dưới chỉ có `4.1`, `4.2`, `4.3` — **thiếu hẳn mục `4.4. Cơ chế sao lưu và dự phòng phục hồi dữ liệu (Backup & Recovery)`**. | Viết thêm mục **`4.4. Cơ chế sao lưu và dự phòng dữ liệu`** (trình bày cơ chế xuất/khôi phục PostgreSQL `pg_dump` / `backup_mhotel_dev.sql` và Docker Volume trong dự án thực tế của nhóm). |
| **4.1** | Trang 236 | Dưới `Bảng 4.1` có dòng chữ xám `(Hình 4.1: Minh họa các quyền được truy cập của một nhân viên lễ tân trên hệ thống M-Hotel)` nhưng **chưa có ảnh chụp màn hình**. Ngoài ra tên cột Bảng 4.1 chưa khớp hoàn toàn với 6 tài khoản phòng ban trong `THONG_TIN_TAI_KHOAN_PHAN_QUYEN.md`. | Chụp màn hình giao diện khi đăng nhập bằng tài khoản `bophanletan` (chỉ hiện đúng menu Lễ tân, ẩn Kho/Kỹ thuật/Kế toán/Cấu hình) và chèn vào `Hình 4.1`. |
| **4.3** | Trang 238 | Cuối trang 238 còn sót nguyên câu nhắc việc nội bộ:<br>`→ Người dùng, mở tài khoản của nhân viên lễ tân Dương Đình Thảo hoặc Mai Anh Tuấn trên giao diện tiếng Việt của Odoo rồi chụp lại màn hình).` | **Xóa ngay dòng nhắc việc này**, chèn ảnh chụp phần **Chatter (Nhật ký thay đổi trạng thái & tiền cọc)** trên một Phiếu đặt phòng thực tế để minh họa cho mục Vết kiểm toán (`4.3`). |
| **Bảng nháp cuối file** | **Trang 239 – 242** | Còn dính 4 trang bảng nháp ghi tiêu đề **`"M hotel ở quê nha"`** (Tầng 2–4, `P.201–P.403`) và **`"M hotel ở Vũng Tàu"`** (11 phòng) — vừa thiếu tính học thuật vừa mâu thuẫn trực tiếp với số liệu 13 phòng + 18 phòng ở Chương 1 (`Trang 8`). | **XÓA SẠCH 4 trang nháp (Trang 239 – 242).** |
| **Thiếu Chương Kết luận** | Cuối báo cáo | Báo cáo dừng đột ngột sau Chương 4, chưa có phần Tổng kết / Kết luận đồ án. | Bổ sung **`CHƯƠNG 5. KẾT LUẬN VÀ HƯỚNG PHÁT TRIỂN`** (Đánh giá kết quả đạt được so với mục tiêu ở mục `1.2`, hạn chế hiện tại và hướng phát triển tiếp theo như tích hợp khóa từ IoT, kênh OTA Booking/Agoda, khai báo lưu trú trực tuyến ASM). |

---

## PHẦN 3. CHECKLIST KIỂM TRA LẦN CUỐI TRƯỚC KHI XUẤT LẠI FILE PDF NỘP BÀI

- [ ] Đã xóa trang 13–19 (mục `1.1.5` nháp cũ) và trang 239–242 (`"M hotel ở quê nha"`).
- [ ] Đã thêm tiêu đề lớn `CHƯƠNG 2`, `CHƯƠNG 3` và bổ sung `CHƯƠNG 5 (Kết luận)`.
- [ ] Đã thay sơ đồ BPMN bị dán nhầm ở mục Kiểm kê kho (Trang 177) và vẽ lại các BPMN quá dài (`3.2`, `3.3`, `3.5`, `3.8`) theo đúng 6–8 bước **System-Oriented** trong file [CHUONG_3_MOI_CHUAN_SYSTEM_ORIENTED.md](file:///home/trietbui/Documents/HK5/Hoach_Dinh/ERP-M_hotel_managenment/CHUONG_3_MOI_CHUAN_SYSTEM_ORIENTED.md).
- [ ] Đã tìm kiếm (`Ctrl + F`) trong Word các cụm từ sau để đảm bảo **bằng 0 kết quả**:
  - `Quy Nhơn` / `Nhơn Lý` / `Eo Gió`
  - `3.XX` / `Đính kèm ảnh` / `Chèn ảnh` / `Người dùng, mở tài khoản`
  - `M hotel ở quê nha` / `Burger phô mai` / `Lumber Inc` / `My Company`
- [ ] Đã cập nhật lại số thứ tự `Bảng` và `Hình` tăng dần liên tục trong từng chương và cập nhật lại Mục lục tự động trước khi xuất PDF.
