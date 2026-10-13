# KE HOACH CHI TIET - MUC 1.1.4 & 1.1.5
## De tai: ERP Quan ly Van hanh Khach san M-Hotel (Binh Dinh)
## Mon hoc: IS336 - Hoach dinh Nguon luc Doanh nghiep | Nhom 12

---

## NGUYEN TAC LOGIC DAU BAI

| Tieu chi | 1.1.4 Master Data | 1.1.5 Transaction Data |
|---|---|---|
| Ban chat | Du lieu nen tang, chuan bi truoc khi van hanh | Du lieu phat sinh khi he thong chay thuc te |
| Tinh chat | Tinh, on dinh, it thay doi | Dong, lien tuc cap nhat theo nghiep vu |
| Vi du | Danh muc phong, Ho so khach, Thiet bi phong | Don dat phong, Hoa don, Yeu cau bao tri |
| Trinh tu | Phai lam TRUOC -> La nen cho transaction | Lam SAU khi co master data -> Mo phong van hanh |

> Luu y: Giai doan M1 (12-18/10/2026) nhom chuan bi nen tang du lieu tren Odoo built-in.
> Module tuy bien m_hotel se phat trien tu Moc M3 (15/11/2026).

---

## MUC 1.1.4. MASTER DATA

### Cau truc trinh bay:
  a. Co so khach san (Multi-company)      -> 2 co so
  b. Danh muc hang phong & Dich vu        -> 44 ban ghi
     - Phong luu tru (20 phong)
     - Dich vu khach san (8 dich vu)
     - Hang hoa Minibar (10 mat hang)
     - Vat tu Amenities (10 loai)
  c. Ho so khach hang & Doi tac           -> 25 ho so
  d. Ton kho ban dau (Opening Stock)      -> 10+ vat tu co so du
  e. Ho so trang thiet bi phong           -> 25 thiet bi
  f. Phan quyen nguoi dung               -> 5 vai tro

---

### a. Co so khach san (Multi-company) - MUC TIEU: 2 CO SO
- M-Hotel Quy Nhon Beach (Duong Xuan Dieu, TP. Quy Nhon, Binh Dinh)
- M-Hotel Nhon Ly - Eo Gio (Xa Nhon Ly, TP. Quy Nhon, Binh Dinh)

MAN HINH MINH CHUNG:
- Odoo: Settings -> Companies -> Danh sach 2 cong ty

---

### b1. Danh muc san pham (Product Categories) - 4 nhom

| Ma nhom | Ten nhom | Mo ta |
|---|---|---|
| PHONG | Phong luu tru | Tat ca cac hang phong nghi |
| DV | Dich vu khach san | Giat ui, an sang, thue xe... |
| MINI | Hang hoa Minibar | Do uong, snack trong phong |
| AMN | Vat tu tieu hao Amenities | Khan, do ve sinh ca nhan |

MAN HINH: Odoo: Inventory -> Configuration -> Product Categories

---

### b2. Phong luu tru - TOI THIEU 20 PHONG

| Ma | Ten phong | Gia/dem | Chi nhanh |
|---|---|---|---|
| ROOM-101 | Phong Standard 101 (Don) | 650.000 d | Quy Nhon Beach |
| ROOM-102 | Phong Standard 102 (Doi) | 750.000 d | Quy Nhon Beach |
| ROOM-103 | Phong Standard 103 (Don) | 650.000 d | Quy Nhon Beach |
| ROOM-104 | Phong Standard 104 (Doi) | 750.000 d | Quy Nhon Beach |
| ROOM-201 | Phong Superior 201 (Sea View) | 1.100.000 d | Quy Nhon Beach |
| ROOM-202 | Phong Superior 202 (Sea View) | 1.100.000 d | Quy Nhon Beach |
| ROOM-203 | Phong Superior 203 (City View) | 950.000 d | Quy Nhon Beach |
| ROOM-204 | Phong Superior 204 (City View) | 950.000 d | Quy Nhon Beach |
| ROOM-301 | Phong Deluxe 301 (Balcony Ocean) | 1.500.000 d | Quy Nhon Beach |
| ROOM-302 | Phong Deluxe 302 (Balcony Ocean) | 1.500.000 d | Quy Nhon Beach |
| ROOM-303 | Phong Deluxe 303 (Balcony Ocean) | 1.500.000 d | Quy Nhon Beach |
| ROOM-304 | Phong Deluxe 304 (Family Ocean) | 1.700.000 d | Quy Nhon Beach |
| ROOM-401 | Phong Suite 401 (President Ocean) | 2.500.000 d | Quy Nhon Beach |
| ROOM-402 | Phong Suite 402 (President Ocean) | 2.500.000 d | Quy Nhon Beach |
| ROOM-501 | Phong Family 501 (Connecting) | 1.900.000 d | Quy Nhon Beach |
| ROOM-502 | Phong Family 502 (Connecting) | 1.900.000 d | Quy Nhon Beach |
| ROOM-NL101 | Phong Huong Bien NL101 | 1.200.000 d | Nhon Ly |
| ROOM-NL102 | Phong Huong Bien NL102 | 1.200.000 d | Nhon Ly |
| ROOM-NL201 | Phong Bungalow NL201 | 1.800.000 d | Nhon Ly |
| ROOM-NL202 | Phong Bungalow NL202 | 1.800.000 d | Nhon Ly |

---

### b3. Dich vu gia tang - TOI THIEU 8 DICH VU

| Ma | Ten dich vu | Gia |
|---|---|---|
| SRV-BF | Suat an sang Buffet thuong hang | 120.000 d |
| SRV-LND-01 | Giat ui ao so mi / quan tay | 35.000 d |
| SRV-LND-02 | Giat hap ao vest / dam da hoi | 90.000 d |
| SRV-MTO-AB | Thue xe may tay ga AirBlade | 150.000 d |
| SRV-MTO-WV | Thue xe may so Wave Alpha | 100.000 d |
| SRV-CLN-EX | Don phong tang cuong | 100.000 d |
| SRV-SPA-01 | Massage thu gian Foot Spa | 250.000 d |
| SRV-LND | Giat ui cao cap (combo) | 80.000 d |

---

### b4. Hang hoa Minibar - TOI THIEU 10 MAT HANG (50+ don vi/loai trong kho)

| Ma | Ten hang | Gia ban | Gia von | Ton kho |
|---|---|---|---|---|
| MINI-HEI-01 | Bia Heineken lon 330ml | 35.000 | 20.000 | 100 lon |
| MINI-TIG-01 | Bia Tiger Crystal lon 330ml | 30.000 | 18.000 | 80 lon |
| MINI-QN-01 | Bia Quy Nhon Special lon | 25.000 | 14.000 | 120 lon |
| MINI-LAV-01 | Nuoc khoang Lavie 500ml | 15.000 | 6.000 | 150 chai |
| MINI-DAN-01 | Nuoc khoang Danh Thanh co ga 450ml | 20.000 | 8.000 | 100 chai |
| MINI-COC-01 | Nuoc ngot Coca Cola lon 320ml | 20.000 | 10.000 | 80 lon |
| MINI-RED-01 | Nuoc tang luc Redbull lon 250ml | 25.000 | 12.000 | 60 lon |
| MINI-BANH-01 | Banh trang nuoc dua Tam Quan | 25.000 | 12.000 | 60 goi |
| MINI-DIEU-01 | Hat dieu rang muoi Binh Dinh hu 150g | 65.000 | 35.000 | 50 hu |
| MINI-MUC-01 | Muc rim ngao Quy Nhon hop 200g | 85.000 | 45.000 | 40 hop |

---

### b5. Vat tu tieu hao Amenities - TOI THIEU 10 LOAI

| Ma | Ten vat tu | Gia von | Ton kho ban dau |
|---|---|---|---|
| AMN-TB-ECO | Bo ban chai & kem danh rang than tre | 6.000 | 300 bo |
| AMN-COMB-01 | Luoc go tu nhien cao cap | 4.000 | 200 cai |
| AMN-SHAV-01 | Dao cao rau kem kem cao Eco | 8.000 | 150 cai |
| AMN-SHAMP-01 | Dau goi dau thao moc chai 40ml | 9.000 | 400 chai |
| AMN-BODY-01 | Sua tam duong the thao moc chai 40ml | 9.000 | 400 chai |
| AMN-CAP-01 | Chup toc tam sinh hoc Eco | 2.000 | 300 cai |
| AMN-TOW-L | Khan tam cotton 70x140cm khach san | 55.000 | 100 cai |
| AMN-TOW-M | Khan mat cotton 34x70cm khach san | 20.000 | 150 cai |
| AMN-SLIP-01 | Dep di trong phong vai cotton det to ong | 12.000 | 200 doi |
| AMN-BAG-01 | Tui giat ui vai khong det logo M-Hotel | 5.000 | 200 tui |

MAN HINH: Odoo: Inventory -> Products -> On Hand (ton kho thuc te)

---

### c. Ho so Khach hang - TOI THIEU 25 HO SO

| Phan khuc | So luong | Vi du |
|---|---|---|
| Khach le dia phuong | 8 | Nguyen Van An (Quy Nhon), Phan Thanh Hai (Pleiku)... |
| Khach du lich ca nhan | 8 | Tran Mai Phuong (Da Nang), Pham Thu Huong (Ha Noi)... |
| Khach VIP / Cong tac | 5 | Le Hoang Long, Vu Dinh Trong, Mai Van Chien... |
| Cong ty Lu hanh / Dai ly | 4 | Saigontourist, Quy Nhon Tourist, Cty Du lich & Su kien Viet... |

MAN HINH: Odoo: Contacts -> List view (loc Customer = True)

---

### e. Ho so Trang thiet bi phong - TOI THIEU 25 THIET BI

| Phong | Thiet bi |
|---|---|
| Phong 101 (Quy Nhon Beach) | Dieu hoa Panasonic, Tivi Sony, Khoa the tu Adel, Tu lanh Minibar, May say toc Philips |
| Phong 102 (Quy Nhon Beach) | Dieu hoa Panasonic, Tivi Sony, Khoa the tu Adel, Tu lanh Minibar |
| Phong 201 (Quy Nhon Beach) | Dieu hoa Daikin, Tivi LG, Khoa the tu Adel, Tu lanh Minibar |
| Phong 301 (Quy Nhon Beach) | Dieu hoa Daikin 18000BTU, Tivi Samsung QLED 65in, Khoa the tu, Minibar |
| Phong Suite 401 | Dieu hoa Daikin VRV, Tivi Sony OLED 75in, Khoa van tay Hafele, Tu ruou |
| Phong NL101 (Nhon Ly) | Dieu hoa Panasonic, Tivi TCL, Khoa the tu Adel |

MAN HINH: Odoo: Maintenance -> Equipment -> List view

---

### f. Phan quyen nguoi dung - 5 VAI TRO

| Vai tro | Phan he duoc truy cap | Han che |
|---|---|---|
| Chu / Quan ly khach san | Tat ca phan he + Bao cao Dashboard | Khong gioi han |
| Le tan | Sales (Booking), Contacts, Invoicing | Chi xem Inventory |
| Buong phong | Maintenance (Requests) | Chi xem trang thai phong |
| Ky thuat / Bao tri | Maintenance (Equipment + Requests) | Khong truy cap ke toan |
| Kho / Mua hang | Inventory, Purchase | Khong truy cap ke toan |

---

## MUC 1.1.5. TRANSACTION DATA

### Cau truc trinh bay:
  a. Phan he Dat phong & Lich phong    -> 20+ don dat phong + Calendar View
  b. Phan he Bao tri & Su vu hu hong   -> 10 yeu cau bao tri
  c. Phan he Xuat-Nhap kho vat tu      -> 15 phieu xuat/nhap kho
  d. Phan he Hoa don & Thanh toan      -> 15+ hoa don (Posted)
  e. Bao cao & Dashboard               -> 4 loai bieu do

---

### a. Phan he Dat phong - TOI THIEU 20 DON

| Don | Khach hang | Phong | Ngay o | Tong tien |
|---|---|---|---|---|
| S00001 | Nguyen Van An | Phong Deluxe 301 | 12/10-14/10 (2 dem) | 3.080.000 d |
| S00002 | Le Hoang Long (VIP) | Phong Suite 401 | 12/10-15/10 (3 dem) | 7.500.000 d |
| S00003 | Tran Mai Phuong | Phong Family 501 | 13/10-16/10 (3 dem) | 4.880.000 d |
| S00004 | Pham Thu Huong | Phong Superior 201 | 14/10-16/10 (2 dem) | 2.440.000 d |
| S00005 | Vu Dinh Trong | Phong Executive 402 | 15/10-18/10 (3 dem) | 7.500.000 d |
| S00006-S00011 | Saigontourist (doan 6 phong) | Phong Standard 101-104 | 17/10-20/10 (3 dem) | 13.500.000 d |
| S00012 | Hoang Minh Tuan | Phong Superior 203 | 18/10-20/10 (2 dem) | 2.000.000 d |
| S00013 | Do Bich Ngoc | Phong Deluxe 302 | 19/10-21/10 (2 dem) | 3.080.000 d |
| S00014 | Truong Quoc Bao | Phong Standard 103 | 20/10-22/10 (2 dem) | 1.400.000 d |
| S00015 | Phan Thanh Hai | Phong Superior 204 | 21/10-24/10 (3 dem) | 2.850.000 d |
| S00016 | Vo Thi Hong Nhung | Phong Suite 402 | 22/10-25/10 (3 dem) | 7.500.000 d |
| S00017 | Bui Duc Tri | Phong Family 502 | 23/10-26/10 (3 dem) | 5.700.000 d |
| S00018 | Duong Thuy Kieu | Phong Deluxe 303 | 24/10-27/10 (3 dem) | 4.620.000 d |
| S00019 | Lam Quang Khai | Phong Standard 102 | 25/10-27/10 (2 dem) | 1.500.000 d |
| S00020 | Quy Nhon Tourist (doan) | Phong NL101, NL102 | 25/10-28/10 (3 dem) | 7.200.000 d |

MAN HINH: Odoo: Sales -> Orders -> List view (20+ don) + CALENDAR VIEW

---

### b. Phan he Bao tri - TOI THIEU 10 YEU CAU

| # | Ten su vu | Thiet bi | Phong | Muc uu tien | Trang thai |
|---|---|---|---|---|---|
| 1 | Dieu hoa khong mat | Dieu hoa Panasonic | 101 | Cao | Dang xu ly |
| 2 | Tu lanh khong dong lanh | Tu lanh Minibar | 101 | Trung binh | Dang xu ly |
| 3 | Remote tivi bi mat pin | Tivi Sony | 102 | Thap | Hoan thanh |
| 4 | Khoa the tu khong nhan the | Khoa the tu Adel | 201 | Cao | Dang xu ly |
| 5 | Bong den phong tam chay | He thong dien | 301 | Trung binh | Hoan thanh |
| 6 | May say toc bi ngan nguon | May say toc Philips | 101 | Thap | Tiep nhan |
| 7 | Voi sen nuoc nong yeu | He thong nuoc | 202 | Trung binh | Dang xu ly |
| 8 | Tivi mat ket noi internet | Smart Tivi LG | 201 | Thap | Hoan thanh |
| 9 | Hong o cam dien trong phong | He thong dien | 304 | Cao | Dang xu ly |
| 10 | Dieu hoa Daikin phat tieng on | Dieu hoa Daikin | 301 | Trung binh | Tiep nhan |

MAN HINH: Maintenance -> Requests -> Kanban view + Graph/Pivot view

---

### c. Phan he Kho - TOI THIEU 15 PHIEU XUAT/NHAP

| Loai | Mo ta | So luong phieu |
|---|---|---|
| Nhap kho (IN) | Nhap Amenities dau ky, bo sung Minibar | 5 phieu |
| Xuat kho (OUT) | Cap phat vat tu cho tung phong check-in | 10 phieu |

MAN HINH: Inventory -> Operations -> Transfers + Reporting -> Inventory Moves

---

### d. Hoa don - TOI THIEU 15 HOA DON POSTED

| Hoa don | Khach | Tong tien | Trang thai |
|---|---|---|---|
| INV/2026/00001 | Nguyen Van An | 3.080.000 d | Posted |
| INV/2026/00002 | Le Hoang Long | 7.500.000 d | Posted |
| INV/2026/00003 | Tran Mai Phuong | 4.880.000 d | Posted |
| INV/2026/00004 | Pham Thu Huong | 2.440.000 d | Posted |
| INV/2026/00005 | Vu Dinh Trong | 7.500.000 d | Posted |
| INV/2026/00006-00011 | Saigontourist (doan) | 13.500.000 d | Posted |
| ... (tiep tuc den) | ... | ... | Posted |
| INV/2026/00015 | Quy Nhon Tourist | 7.200.000 d | Posted |

MAN HINH: Invoicing -> Customer Invoices -> List view (15+ hoa don Posted)

---

### e. Bao cao & Dashboard - 4 LOAI BIEU DO

| # | Man hinh bao cao | Vi tri tren Odoo | Y nghia |
|---|---|---|---|
| 1 | Dashboard Ban hang | Sales -> Dashboard | Tong doanh thu theo phan hang phong |
| 2 | Bao cao doanh thu theo thang | Sales -> Reporting -> Analysis | Bieu do doanh thu theo thoi gian |
| 3 | Ton kho vat tu thuc te | Inventory -> Reporting -> Inventory | Danh sach ton kho Minibar & Amenities |
| 4 | Bao cao su vu bao tri | Maintenance -> Reporting | So su vu mo/dong theo thiet bi/phong |

---

## CHECKLIST THUC HIEN TREN ODOO

### PHASE 1 - MASTER DATA
- [x] [A] Settings -> Companies: 2 chi nhanh da co
- [ ] [B] Import import_products.csv -> 44 san pham (can upload tren Odoo)
- [ ] [C] Import import_contacts.csv -> 25 khach hang (can upload tren Odoo)
- [ ] [D] Inventory -> Dieu chinh ton kho cho Minibar & Amenities (10+ loai)
- [ ] [E] Import import_equipments.csv -> 25 thiet bi phong (can upload tren Odoo)
- [x] [F] Settings -> Users: 5 vai tro phan quyen

### PHASE 2 - TRANSACTION DATA
- [x] [G1-G3] Da co S00001, S00002, S00003
- [ ] [G4-G20] Tao them 17 don ban hang nua (S00004 - S00020)
- [x] [H1-H3] Da co INV/2026/00001, 00002, 00003
- [ ] [H4-H15] Tao them va Post 12 hoa don nua
- [x] [I1] Da co yeu cau bao tri su vu 1
- [ ] [I2-I10] Tao them 9 yeu cau bao tri nua
- [ ] [J] Tao 15 phieu xuat/nhap kho Minibar & Amenities

### PHASE 3 - BAO CAO
- [ ] [K] Chup Sales Dashboard + Sales Analysis (bieu do doanh thu)
- [ ] [L] Chup Inventory On Hand Report (ton kho vat tu)
- [ ] [M] Chup Maintenance Requests Kanban + Graph view
- [ ] [N] Chup Invoices List voi 15+ hoa don Posted

---

## DANH SACH 15 ANH CAN CHUP

| # | Muc | Man hinh Odoo | Ten file anh |
|---|---|---|---|
| 1 | 1.1.4a | Settings -> Companies | H1_Co_so_khach_san.png |
| 2 | 1.1.4b | Inventory -> Product Categories | H2_Danh_muc_san_pham.png |
| 3 | 1.1.4b | Products -> List (20+ phong) | H3_Danh_sach_phong_dich_vu.png |
| 4 | 1.1.4c | Contacts -> List (25+ khach) | H4_Danh_sach_khach_hang.png |
| 5 | 1.1.4d | Inventory -> On Hand (vat tu) | H5_Ton_kho_vat_tu.png |
| 6 | 1.1.4e | Maintenance -> Equipment List | H6_Thiet_bi_phong.png |
| 7 | 1.1.4f | Settings -> Users | H7_Phan_quyen_nguoi_dung.png |
| 8 | 1.1.5a | Sales -> Orders -> List (20+ don) | H8_Danh_sach_dat_phong.png |
| 9 | 1.1.5a | Sales -> Orders -> Calendar View | H9_Lich_dat_phong.png |
| 10 | 1.1.5b | Maintenance -> Requests Kanban | H10_Su_vu_bao_tri_kanban.png |
| 11 | 1.1.5b | Maintenance -> Graph/Pivot | H11_Bao_cao_bao_tri.png |
| 12 | 1.1.5c | Inventory -> Transfers list | H12_Phieu_xuat_nhap_kho.png |
| 13 | 1.1.5d | Invoicing -> Invoices list (15+) | H13_Danh_sach_hoa_don.png |
| 14 | 1.1.5e | Sales -> Dashboard | H14_Dashboard_doanh_thu.png |
| 15 | 1.1.5e | Sales -> Reporting -> Analysis | H15_Bao_cao_doanh_thu.png |

> Tat ca anh luu vao: D:\HK5\Hoach_Dinh\Do_An\