# Bộ mã Mermaid cho các sơ đồ Chương 4 (PSE.G102)

Bạn có thể dán trực tiếp các đoạn mã dưới đây vào:
- **Mermaid Live Editor:** https://mermaid.live (chỉnh sửa và tải ảnh PNG/SVG độ phân giải cao)
- **Draw.io (diagrams.net):** Menu *Arrange -> Insert -> Advanced -> Mermaid*
- **Notion / GitHub Markdown / Obsidian**

---

## Hình 4.1: Sơ đồ khối kiến trúc phân tầng logic Clean Layered Architecture

```mermaid
flowchart TD
    subgraph L1["1. PRESENTATION LAYER (Giao diện người dùng đa thiết bị)"]
        direction LR
        UI1["Admin Web Dashboard<br/>(Desktop 1920x1080)"]
        UI2["Mobile Web Kỹ thuật viên<br/>(Mobile 375x812)"]
        UI3["Cổng tra cứu Khách hàng<br/>(Public Portal)"]
    end

    subgraph L2["2. APPLICATION & API ROUTING LAYER (Tiếp nhận & Bảo mật)"]
        direction LR
        API1["Reverse Proxy (Nginx)<br/>& Rate Limiter"]
        API2["Auth & RBAC Middleware<br/>(JWT / Kiểm tra quyền)"]
        API3["DTO Validation (Pydantic v2)<br/>& Audit Logger"]
    end

    subgraph L3["3. CORE DOMAIN SERVICES LAYER (Nghiệp vụ cốt lõi BR01–BR10)"]
        direction LR
        DOM1["TicketService & WarrantyService<br/>(BR01, BR02, BR03)"]
        DOM2["RepairService & InventoryService<br/>(BR04, BR05, BR06, BR07, BR09)"]
        DOM3["SlaService, PortalService & Dash<br/>(BR08, BR10, TB.12)"]
    end

    subgraph L4["4. INFRASTRUCTURE & DATA PERSISTENCE LAYER (Lưu trữ dữ liệu)"]
        direction LR
        INF1[("PostgreSQL Repository<br/>(SQLAlchemy 2.0 Async)")]
        INF2[("Redis Cache<br/>(KPI & Rate Limit)")]
        INF3["Attachment Storage<br/>(Ảnh chữ ký & Biên bản)"]
    end

    subgraph L5["5. EXTERNAL ADAPTERS & TESTABILITY LAYER (Trừu tượng hóa kiểm thử)"]
        direction LR
        EXT1["IClockService<br/>(SystemClock / SimulatedClock - TB.02)"]
        EXT2["IEmailService<br/>(SMTP Adapter / MockEmail - TB.05)"]
    end

    UI1 -->|"HTTPS"| API1
    UI2 -->|"REST JSON"| API2
    UI3 -->|"HTTPS"| API3

    API1 --> DOM1
    API2 -->|"Dependency Injection"| DOM2
    API3 --> DOM3

    DOM1 -->|"Ports"| INF1
    DOM1 -->|"Files"| INF3
    DOM2 -->|"ACID / Cache"| INF2

    DOM3 -.->|"Clock Interface"| EXT1
    DOM3 -.->|"Mail Interface"| EXT2
```

---

## Hình 4.2: Sơ đồ triển khai hạ tầng Container hóa với Docker Compose

```mermaid
flowchart TD
    subgraph CLIENTS["THIẾT BỊ ĐẦU CUỐI (CLIENT DEVICES)"]
        direction LR
        C1["PC Quản trị viên<br/>(Desktop Browser)"]
        C2["Điện thoại KTV<br/>(Mobile Browser)"]
        C3["Trình duyệt Khách hàng<br/>(Public Web)"]
    end

    subgraph DOCKER["DOCKER HOST ENGINE (Docker Compose Network)"]
        direction TB
        N1["Container 1: frontend-server — Nginx 1.25 (Port 80/443)<br/>Phục vụ Next.js UI & Reverse Proxy"]
        N2["Container 2: backend-api-service — Python 3.12 / FastAPI (Port 8000)<br/>Uvicorn Workers, Domain Services, State Machine & Scheduler 08:00"]

        subgraph DATA_TIER["INTERNAL DATA & TESTING SERVICES"]
            direction LR
            D1[("Container 3: db-postgres<br/>PostgreSQL 16.2 (Port 5432)<br/>Persistent Volume (ACID)")]
            D2[("Container 4: cache-redis<br/>Redis 7.2 (Port 6379)<br/>Dashboard Cache & Rate Limit")]
            D3["Container 5: mock-mailpit<br/>SMTP Test Server (1025 / UI 8025)<br/>Giả lập gửi mail SLA (TB.05)"]
        end

        N1 -->|"Internal HTTP (Port 8000)"| N2
        N2 -->|"SQL / Asyncpg (5432)"| D1
        N2 -->|"Cache / Token (6379)"| D2
        N2 -->|"SMTP (1025)"| D3
    end

    C1 -->|"HTTPS"| N1
    C2 -->|"HTTPS / TLS 1.3"| N1
    C3 -->|"HTTPS"| N1
```

---

## Hình 4.3: Sơ đồ luồng dữ liệu ngữ cảnh (Context DFD Cấp 0)

```mermaid
flowchart LR
    ADM["ADMIN<br/>(Tiếp nhận, Điều phối, Kho)"]
    CUS["KHÁCH HÀNG<br/>(Gửi máy, Tra cứu, Ký nhận)"]
    TEC["KỸ THUẬT VIÊN<br/>(Kiểm tra, Sửa chữa, Bàn giao)"]

    SYS(("0.0<br/>HỆ THỐNG QUẢN LÝ<br/>HOẠT ĐỘNG BẢO HÀNH<br/>HƯNG THIỆN"))
    DB[("D0: Kho dữ liệu<br/>tập trung (3NF)")]

    ADM -->|"1. Hồ sơ tiếp nhận, thẩm định,<br/>phân công, nhập/xuất kho"| SYS
    SYS -->|"2. Báo cáo SLA 08:00, Dashboard,<br/>cảnh báo tồn kho, DS bàn giao"| ADM

    CUS -->|"3. Thiết bị, chữ ký linh kiện,<br/>mã phiếu + mã bí mật"| SYS
    SYS -->|"4. Phiếu hẹn, tiến độ công khai,<br/>biên bản giao trả máy"| CUS

    TEC -->|"5. Nhật ký sửa, trạng thái,<br/>LK dùng, duyệt bàn giao"| SYS
    SYS -->|"6. DS phiếu giao, hồ sơ máy,<br/>hạn trả, yêu cầu bàn giao"| TEC

    SYS <-->|"7. Đọc / Ghi dữ liệu 3NF"| DB
```

---

## Hình 4.4: Sơ đồ luồng dữ liệu DFD Cấp 1 phân rã tiến trình hệ thống

```mermaid
flowchart TD
    CUS["KHÁCH HÀNG"]
    ADM["ADMIN"]
    TEC["KỸ THUẬT VIÊN"]
    SCH["BỘ LẬP LỊCH 08:00"]

    P1(["1.0 Tiếp nhận & Thẩm định BH<br/>(BR01–BR03)"])
    P2(["2.0 Điều phối & Bàn giao KTV<br/>(BR04, BR07)"])
    P3(["3.0 Sửa chữa & Kho linh kiện<br/>(BR05, BR06)"])
    P4(["4.0 Nghiệm thu Test & Giao trả<br/>(BR09)"])
    P5(["5.0 Giám sát SLA, Portal & Thống kê<br/>(BR08, BR10)"])

    D1[("D1: Phiếu & Thiết bị")]
    D2[("D2: Phân công & Bàn giao")]
    D3[("D3: Nhật ký & Kho LK")]
    D4[("D4: Lịch sử giao nhận")]
    D5[("D5: SLA Logs & Báo cáo")]

    CUS -->|"Máy, lỗi, chữ ký LK"| P1
    ADM -->|"Lập phiếu, thẩm định"| P1
    P1 -->|"Lưu hồ sơ"| D1

    D1 -->|"Phiếu Chờ phân công"| P2
    ADM -->|"Chỉ định / Bàn giao"| P2
    P2 <-->|"Phiên bàn giao"| D2
    TEC <-->|"Nhận / Từ chối"| P2

    D1 -->|"Hồ sơ phiếu"| P3
    TEC -->|"Chẩn đoán, trạng thái, LK dùng"| P3
    ADM -->|"Nhập / Xuất kho"| P3
    P3 <-->|"Nhật ký & Tồn kho"| D3

    D1 <-->|"Cập nhật Đã trả / Hủy"| P4
    TEC -->|"Báo test đạt"| P4
    ADM -->|"Đối chiếu chữ ký & Đóng"| P4
    CUS -->|"Chạy test & Ký nhận"| P4
    P4 -->|"Biên bản trả"| D4

    SCH -->|"Trigger 08:00"| P5
    D1 -->|"Dữ liệu phiếu"| P5
    D3 -->|"Trạng thái Chờ LK"| P5
    P5 -->|"Log gửi mail"| D5
    P5 -->|"Email SLA & KPI"| ADM
    CUS <-->|"Tra cứu (Mã + Pass)"| P5
```

---

### Hình 4.5: Biểu đồ tuần tự luồng tiếp nhận thiết bị giữ máy và ký linh kiện (UC03 – BR02)

```mermaid
%%{init: {'sequence': {'actorMargin': 28, 'width': 145, 'actorFontSize': 15, 'messageFontSize': 14}}}%%
sequenceDiagram
    autonumber
    participant Admin as Admin
    participant Ctrl as TicketController
    participant Svc as TicketService
    participant Repo as Repository

    Admin->>Ctrl: Gửi hồ sơ tiếp nhận<br/>(HOLD_FOR_REPAIR, DS LK ký)
    Ctrl->>Svc: create_ticket(admin_id,<br/>customer, device, signed_parts)
    Svc->>Svc: Kiểm tra quy tắc BR02<br/>(có LK ký & chữ ký khách)
    alt Thiếu danh sách LK ký hoặc chữ ký
        Svc-->>Ctrl: TicketServiceError (400)
        Ctrl-->>Admin: Từ chối & chỉ rõ mục thiếu
    else Hợp lệ theo BR02
        Svc->>Repo: get_next_daily_ticket_number()
        Repo-->>Svc: Số thứ tự trong ngày (x)
        Svc->>Svc: Sinh mã TKT_YYYYMMDD_x<br/>& băm SHA-256 mã bí mật
        Svc->>Repo: Lưu WarrantyTicket (RECEIVED)<br/>& StatusChangeLog
        Repo-->>Svc: Xác nhận lưu thành công (ACID)
        Svc-->>Ctrl: Trả về WarrantyTicket
        Ctrl-->>Admin: In phiếu + mã tra cứu bí mật
    end
```

---

## Hình 4.6: Biểu đồ tuần tự quy trình bàn giao điều chuyển KTV khi KTV cũ vắng mặt (UC06 – BR07)

```mermaid
%%{init: {'sequence': {'actorMargin': 28, 'width': 145, 'actorFontSize': 15, 'messageFontSize': 14}}}%%
sequenceDiagram
    autonumber
    participant Admin as Admin
    participant Svc as RepairService
    participant Repo as Repository
    participant TechNew as KTV mới (Target)

    Admin->>Svc: initiate_handover(ticket_id,<br/>target_tech, is_absent=True)
    Svc->>Repo: get_pending_handover(ticket_id)
    Repo-->>Svc: Chưa có phiên PENDING (BR07)
    Svc->>Repo: Lưu HandoverSession (PENDING,<br/>ghi nhận KTV cũ vắng mặt)
    Repo-->>Svc: session_id (HO_xxxxxxxx)
    Svc-->>Admin: Khởi tạo xong (giữ KTV cũ)

    TechNew->>Svc: Đọc hồ sơ & nhật ký cũ
    alt Từ chối tiếp nhận
        TechNew->>Svc: respond_handover(False, reason)
        Svc->>Repo: Session = REJECTED + lý do
        Repo-->>Svc: Xác nhận (giữ nguyên KTV cũ)
        Svc-->>TechNew: Hoàn tất từ chối
    else Chấp nhận tiếp nhận
        TechNew->>Svc: respond_handover(accept=True)
        Svc->>Repo: Đổi current_technician = TechNew<br/>& giữ nguyên trạng thái máy
        Svc->>Repo: Session = ACCEPTED & Audit Log
        Repo-->>Svc: Xác nhận giao dịch nhất quán
        Svc-->>TechNew: Chuyển quyền sửa cho KTV mới
        Svc-->>Admin: Thông báo bàn giao hoàn tất
    end
```

---

## Hình 4.7: Biểu đồ tuần tự cập nhật tiến độ sửa chữa và ghi nhận sử dụng linh kiện kho (UC07, UC08 – BR05, BR06)

```mermaid
%%{init: {'sequence': {'actorMargin': 28, 'width': 145, 'actorFontSize': 15, 'messageFontSize': 14}}}%%
sequenceDiagram
    autonumber
    participant Tech as KTV phụ trách
    participant RepSvc as RepairService
    participant InvSvc as InventoryService
    participant Repo as Repository

    Tech->>RepSvc: update_repair_status(ticket_id,<br/>new_status, reason, work_log)
    RepSvc->>Repo: find_ticket_by_id(ticket_id)
    Repo-->>RepSvc: WarrantyTicket
    RepSvc->>RepSvc: Kiểm tra quyền (BR04)<br/>& FSM Guard (BR09)
    RepSvc->>Repo: Lưu StatusChangeLog<br/>& RepairWorkLog (BR05)
    Repo-->>RepSvc: Xác nhận lưu nhật ký
    RepSvc-->>Tech: Cập nhật trạng thái thành công

    opt Có sử dụng linh kiện (UC08 extend UC07)
        Tech->>InvSvc: record_part_usage(ticket_id,<br/>part_id, used_quantity)
        InvSvc->>Repo: Lấy PartAllocation hiện có
        Repo-->>InvSvc: allocated_qty, used_qty
        InvSvc->>InvSvc: Kiểm tra used <= remaining<br/>(Quy tắc BR06)
        InvSvc->>Repo: Cộng dồn used_qty<br/>(KHÔNG giảm tồn kho lần 2)
        Repo-->>InvSvc: Xác nhận cập nhật
        InvSvc-->>Tech: Ghi nhận dùng LK thành công
    end
```

---

## Hình 4.8: Biểu đồ tuần tự bộ máy tự động gửi điểm tin SLA lúc 08:00 (SLA – BR08)

```mermaid
%%{init: {'sequence': {'actorMargin': 28, 'width': 145, 'actorFontSize': 15, 'messageFontSize': 14}}}%%
sequenceDiagram
    autonumber
    participant Cron as Scheduler (08:00)
    participant SlaSvc as SlaService
    participant Clock as IClockService
    participant Repo as Repository
    participant Mail as IEmailService

    Cron->>SlaSvc: dispatch_daily_0800_email()
    SlaSvc->>Clock: today() (Thật hoặc<br/>SimulatedClock - TB.02)
    Clock-->>SlaSvc: Ngày hiện hành
    SlaSvc->>Repo: Lấy DS phiếu chưa hoàn tất<br/>(trước trạng thái Chờ trả)
    Repo-->>SlaSvc: Danh sách WarrantyTickets
    SlaSvc->>SlaSvc: Phân nhóm theo BR08
    Note right of SlaSvc: Nhóm 1 (Báo động đỏ):<br/>Hẹn hôm nay / Quá hạn / Chờ LK<br/>Nhóm 2 (Cần lưu ý): Hẹn ngày mai<br/>(Không trùng lặp, giữ nguyên status)
    SlaSvc->>Mail: send_email(admin, subject, body)
    Mail-->>SlaSvc: Kết quả (SMTP / Mock - TB.05)
    SlaSvc-->>Cron: Hoàn tất điểm tin 08:00
```

