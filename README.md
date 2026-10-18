# M-Hotel ERP — Hotel Operations Management System

> **Course:** IS336 — Enterprise Resource Planning (Hoạch định nguồn lực doanh nghiệp)  
> **Class:** IS336.R11.1 | **Group:** Group 12  
> **Instructor / Sponsor:** M.Sc. Huynh Duc Huy  
> **Platform:** Odoo 19 Community Edition + PostgreSQL 15 (Dockerized Architecture)

---

## 📌 Project Overview

**M-Hotel** is an end-to-end Enterprise Resource Planning (ERP) hotel management solution built natively on Odoo 19 Community. The system is designed to streamline front-desk operations, room status lifecycles, housekeeping assignments, minibar/amenities stock deduction, guest online reservations, room asset maintenance, and multi-branch performance analytics.

### 🏨 Multi-Company Branch Architecture
The system operates across two distinct resort branches:
1. **M-Hotel Quy Nhon Beach** (01 Xuan Dieu, Quy Nhon City) — 24 rooms across 4 floors.
2. **M-Hotel Nhon Ly - Eo Gio** (Ly Luong Village, Nhon Ly, Quy Nhon) — 20 rooms including Cliffside Villas & Seaview Bungalows.

---

## 🏗️ Architecture & Modules

The repository is modularized into 7 specialized business packages:

| Module | Technical Name | Responsibility |
| :--- | :--- | :--- |
| **Core Base** | `m_hotel_base` | Multi-company hotel foundation, 5 room types, room registry (44 rooms), seasonal rate tables, guest profiles (CCCD/Passport), and 5 RBAC security groups. |
| **Booking & Frontdesk** | `m_hotel_booking` | Nightly & hourly reservations, overbooking prevention constraint, check-in, check-out, folio billing & automated invoicing (`account.move`). |
| **Housekeeping & Incident** | `m_hotel_housekeeping` | Room cleaning tasks lifecycle, automated check-out task generation, incident logging, and emergency maintenance room locks. |
| **Inventory & Supply** | `m_hotel_inventory` | Room supply consumption norms (Amenities & Minibar), automated stock deduction via Odoo `stock.picking`. |
| **Asset & Maintenance** | `m_hotel_asset` | In-room equipment tracking (AC, Smart TV, Adel smart locks) linked to Odoo `maintenance` requests. |
| **Management Reports** | `m_hotel_report` | SQL analysis view for Occupancy Rate (buồng phòng), revenue breakdown, Pivot and Graph dashboards. |
| **Guest Website** | `m_hotel_website` | Public responsive booking engine and room catalog for prospective guests. |
| **Umbrella Package** | `m_hotel` | Meta-package for one-click installation of all suite components. |

---

## 🚀 Quick Start (Docker Environment)

### Prerequisites
- Docker Engine & Docker Compose v2+
- Ports `8069` (Web) and `5432` (PostgreSQL) available

### Running the System
```bash
# Navigate to Docker configuration directory
cd M-Hotel_Docker

# Start the cluster in detached mode
docker compose up -d

# Check running containers
docker compose ps
```

### Access URLs & Credentials
- **Web ERP Application:** [http://localhost:8069](http://localhost:8069)
- **Database Manager:** [http://localhost:8069/web/database/manager](http://localhost:8069/web/database/manager)
- **Database Name:** `mhotel_dev`
- **Default Admin Account:** `admin` / `admin`

---

## 🧪 Automated Unit Tests

All business logic workflows have been verified with automated unit tests:
```bash
docker exec -i m-hotel-web odoo -c /etc/odoo/odoo.conf -d mhotel_dev --http-port=8070 \
  --test-tags /m_hotel_booking,/m_hotel_housekeeping,/m_hotel_inventory --stop-after-init
```
**Test Results:** 14 tests, 0 failures, 0 errors (100% Pass Rate).

---

## 👥 Development Team (Group 12)

| STT | Full Name | Student ID | Role & Core Responsibilities |
| :---: | :--- | :---: | :--- |
| 1 | **Bui Minh Triet** | **24521845** | **Project Manager & BA** — System architecture, core base models, Project Charter, and report coordination. |
| 2 | **Duong Dinh Thao** | **24521645** | **Developer** — Booking engine, hourly/nightly workflows, check-in/out, and website booking portal. |
| 3 | **Tran Hoang Phuc** | **24521398** | **Developer** — Housekeeping management, room lifecycle status transitions, and incident logging. |
| 4 | **Mai Anh Tuan** | **24521929** | **Developer** — Inventory supply norms, equipment maintenance integration, and occupancy report views. |
| 5 | **Nguyen Quoc Trieu** | **24521855** | **DevOps & QA** — Docker orchestration, RBAC security profiles, unit test suite, and database backups. |
