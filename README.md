# PSE.G102 - Warranty Management System
## Phần mềm Quản lý Hoạt động Bảo hành của Trung tâm Hỗ trợ Kỹ thuật tại Công ty Máy tính Hưng Thiện

Dự án môn học: **Công nghệ phần mềm (PSE)**  
Khoa Viễn thông 1 - Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
Nhóm thực hiện: **PSE.G102**

---

## 1. Cấu trúc thư mục dự án

```text
E:\Warranty Management System\
├── .github/workflows/ci.yml               # Tự động chạy pytest kiểm thử khi push / PR
├── docs/                                  # Thư mục lưu trữ tài liệu Word theo chuẩn Thông tư 30
│   ├── images/                            # 8 hình ảnh sơ đồ kiến trúc, DFD, Sequence độ phân giải cao
│   ├── diagrams_mermaid.md                # Mã nguồn Mermaid của các sơ đồ Chương 4
│   ├── PSE.G102_Chuong4_KienTrucPhanMem.docx
│   ├── PSE.G102_SAD_KienTrucHeThong.docx
│   ├── PSE.G102_QuyTacDatTen_NamingStandard.docx
│   └── PSE.G102_ThietKeLuongDuLieu_DataFlowSpec.docx
├── src/                                   # Mã nguồn kiến trúc khung (Clean Layered Architecture)
│   ├── warranty_app/                       # FastAPI: tiếp nhận phiếu và API cổng tra cứu
│   └── warranty_core/
│       ├── domain_models.py               # Thực thể nghiệp vụ (Domain Entities)
│       ├── enums.py                       # Các bộ giá trị hằng số (Status, Roles, Policies)
│       ├── repository.py                  # Tầng truy xuất dữ liệu trừu tượng
│       └── services/                      # Tầng xử lý quy tắc nghiệp vụ (Business Rules BR01-BR10)
│           ├── clock_service.py           # Dịch vụ đồng hồ (hỗ trợ giả lập giờ TB.02)
│           ├── email_service.py           # Dịch vụ gửi email (hỗ trợ mock email TB.05)
│           ├── ticket_service.py          # Nghiệp vụ tiếp nhận và thẩm tra phiếu (BR01, BR02)
│           ├── warranty_service.py        # Nghiệp vụ thẩm định chính sách bảo hành (BR03)
│           ├── repair_service.py          # Nghiệp vụ FSM, điều phối & bàn giao (BR04, BR05, BR07, BR09)
│           ├── inventory_service.py       # Quản lý xuất/nhập/dùng linh kiện kho (BR06)
│           ├── sla_service.py             # Quét hạn và gom nhóm email điểm tin 08:00 (BR08)
│           └── portal_service.py          # Tra cứu tiến độ công khai bảo mật SHA-256 (BR10)
├── tests/                                 # Bộ kiểm thử tự động (Unit & Integration Tests)
│   ├── conftest.py
│   ├── test_inventory_and_usage.py
│   ├── test_portal_security.py
│   ├── test_repair_and_handover.py
│   ├── test_sla_and_clock.py
│   ├── test_ticket_lifecycle.py
│   └── test_warranty_policy.py
├── frontend/                              # Cổng tra cứu React/Next.js, có kiểm thử giao diện
├── .gitignore                             # Loại trừ file rác, virtualenv, file nhạy cảm
├── pytest.ini                             # Cấu hình pythonpath cho pytest
├── requirements.txt                       # Thư viện phụ thuộc
└── README.md                              # Hướng dẫn dự án và quy chế Git
```

---

## 2. Hướng dẫn Clone dự án, Cài đặt và Chạy kiểm thử

### Bước 0: Clone repository về máy (chỉ làm 1 lần đầu)
```bash
git clone -b develop https://github.com/Thien-anh-De/PSE.G102-Warranty-Management-System.git
cd PSE.G102-Warranty-Management-System
```

### Cài đặt môi trường
Yêu cầu: Python >= 3.10 (khuyến nghị Python 3.12).
```bash
python -m venv .venv
# Trên Windows:
.venv\Scripts\activate
# Cài đặt thư viện:
pip install -r requirements.txt
```

### Chạy kiểm thử tự động
```bash
pytest -v
```

---

## 3. Quy chuẩn và Quy trình Git cho nhóm (Git Workflow)

### 3.1. Mô hình phân nhánh (Branching Strategy)
- **`main`**: Nhánh chính thức, lưu phiên bản ổn định để nộp bài. **Không push trực tiếp vào `main`**.
- **`develop`**: Nhánh tích hợp chung của nhóm. Tất cả các tính năng hoàn thiện sẽ được gộp vào đây.
- **`feat/<module>-<tên_task>`**: Nhánh tính năng cá nhân (ví dụ: `feat/tkt-create`, `feat/dash-chart`, `feat/portal-search`). Mỗi thành viên tạo nhánh mới từ `develop`.
- **`fix/<mã_lỗi>`**: Nhánh sửa lỗi phát sinh trong quá trình kiểm thử.

### 3.2. Quy trình làm việc hằng ngày (Pull -> Code -> Test -> Push)
1. **Lấy mã nguồn mới nhất trước khi làm:**
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. **Tạo nhánh tính năng mới cho task của mình:**
   ```bash
   git checkout -b feat/tkt-create-ticket
   ```
3. **Thực hiện viết code và kiểm thử cục bộ:**
   - Code gọn gàng, sạch sẽ, không đưa icon hay comment thừa thãi.
   - Chạy kiểm thử trước khi commit:
     ```bash
     pytest -v
     ```
4. **Commit theo chuẩn gọn rõ:**
   - Cú pháp gợi ý: `<loại>(<phân_hệ>): <mô tả ngắn gọn>`
   - Ví dụ:
     - `feat(tkt): implement hold for repair signed parts check per BR02`
     - `fix(sla): resolve 08:00 email grouping condition`
     - `test(portal): add unit test for secret code hashing verification`
     - `docs(sad): update database schema diagram`
5. **Đẩy nhánh lên GitHub:**
   ```bash
   git push -u origin feat/tkt-create-ticket
   ```
6. **Tạo Pull Request (PR) vào `develop`:**
   - Vào GitHub bấm **Compare & pull request** để gộp từ `feat/...` vào `develop`.
   - Sau khi test tự động (CI) báo xanh và xem nhanh không xung đột file thì bấm **Merge pull request** (nếu lỡ lỗi có thể bấm **Revert** ngay trên PR).

### 3.3. Lưu ý an toàn bắt buộc
- **Không commit file nhạy cảm:** Mật khẩu, API key, token bí mật, file `.env`.
- **Không commit file rác / cache:** `__pycache__/`, `.pytest_cache/`, `.venv/`, file tạm của Word (`~$...`) — đã được chặn sẵn trong `.gitignore`.
- **Hạn chế sửa chung 1 file Word cùng lúc:** Khi ghép hoặc sửa `.docx`, nên báo nhau trước để tránh conflict file nhị phân.

---

## 4. Cổng tra cứu tiến độ bảo hành cho khách hàng (PORTAL / INC3)

Phạm vi: FR_PORTAL_01–02, NFR_SEC_02 và phần khách hàng của UC10.
Giao diện React/Next.js gọi FastAPI, dùng `PortalService` và **cùng repository với
module tiếp nhận**. Cổng không tạo kho phiếu riêng trong trình duyệt.

### 4.1. Chạy bản minh họa trên máy cá nhân

Yêu cầu: môi trường Python ở Mục 2 đã được cài đặt và kích hoạt; Node.js từ
22.12 trở lên (khuyến nghị Node.js 24).

Từ thư mục gốc repository, chạy:

```bash
cd frontend
npm ci
npm run build
cd ..
python -m src.warranty_app.demo --port 3000
```

Mở **http://127.0.0.1:3000**. FastAPI phục vụ cả giao diện đã build và API trên
cùng địa chỉ. Dữ liệu minh họa chỉ được nạp khi chạy lệnh `demo` trên; quy trình
khởi động API thông thường không tự tạo các phiếu này.
Nếu bộ ZIP đã có `frontend/out`, có thể bỏ qua các lệnh npm và chạy ngay lệnh
Python. Lệnh `demo` luôn chọn RAM; chế độ PostgreSQL được hướng dẫn ở Mục 4.6.

| Mã phiếu mẫu | Mã tra cứu mẫu | Trạng thái |
|---|---|---|
| `TKT_20261126_1` | `HT-DEMO-001` | Đang sửa chữa |
| `TKT_20261126_2` | `HT-DEMO-002` | Chờ linh kiện |
| `TKT_20261126_3` | `HT-DEMO-003` | Chờ trả |
| `TKT_20261126_4` | `HT-DEMO-004` | Đã hủy |

Các mã trên là dữ liệu giả công khai, không dùng cho hồ sơ thật. Ngày của bộ
minh họa được cố định để mã phiếu và kết quả có thể tái hiện. Phiếu được tạo và
chuyển trạng thái qua các service nghiệp vụ hiện có; khi dừng tiến trình, toàn
bộ dữ liệu trong RAM mất đi.

### 4.2. Phát triển giao diện và API song song

Terminal 1, tại thư mục gốc và trong môi trường Python đã kích hoạt:

```bash
python -m uvicorn src.warranty_app.main:app --host 127.0.0.1 --port 8008
```

Terminal 2:

```bash
cd frontend
npm ci
npm run dev
```

Mở **http://127.0.0.1:3001**. Next.js chuyển tiếp `/api/` tới backend ở cổng
8008 khi phát triển. Có thể cấu hình `PORTAL_API_ORIGIN` nếu dùng địa chỉ API
khác. Khi build static và phục vụ bằng FastAPI, trình duyệt dùng API cùng origin.

### 4.3. Hợp đồng API và bảo vệ thông tin tra cứu

`POST /api/v1/portal/lookups` nhận JSON:

```json
{
  "ticket_id": "TKT_20261126_1",
  "plain_secret_code": "HT-DEMO-001"
}
```

Kết quả `200` chỉ gồm năm trường:

```json
{
  "ticket_id": "TKT_20261126_1",
  "device_model": "Dell XPS 15 9520",
  "device_serial_masked": "SN****00",
  "status": "UNDER_REPAIR",
  "promised_return_date": "2026-11-28"
}
```

- Mã bí mật được gửi trong thân POST, không nằm trên URL. `PortalService`
  đối chiếu mã với giá trị SHA-256 đã lưu khi tiếp nhận.
- Sai mã bí mật và không tồn tại phiếu đều trả `404` với cùng thông báo.
- Lỗi dữ liệu trả `422` đã lược bỏ đầu vào, không phản hồi lại mã bí mật.
- Kết quả và lỗi của endpoint đều có `Cache-Control: no-store`. Giao diện không
  ghi mã vào localStorage, sessionStorage hoặc URL.
- Tối đa mặc định **5 lượt/60 giây cho mỗi địa chỉ client**; lượt hợp lệ và sai
  mã đều được tính. Vượt ngưỡng trả `429` và `Retry-After`; giao diện hiển thị
  thời gian chờ. Các ngưỡng là cấu hình đề xuất cần nhóm chốt theo OPEN05.
- Mã phiếu được bỏ khoảng trắng hai đầu. Mã bí mật phân biệt hoa/thường,
  được giữ nguyên khi xác minh; đầu vào tối đa 64 ký tự cho mã phiếu và 256
  ký tự cho mã bí mật.

| Biến môi trường | Mặc định | Ý nghĩa |
|---|---|---|
| `PORTAL_LOOKUP_MAX_ATTEMPTS` | `5` | Số lượt được phép trong một cửa sổ thời gian |
| `PORTAL_LOOKUP_WINDOW_SECONDS` | `60` | Độ dài cửa sổ tính bằng giây |

Thiết lập biến trước khi khởi động backend. Bộ giới hạn dùng đồng hồ có thể
giả lập và khóa để xử lý yêu cầu đồng thời. Nó chỉ lưu địa chỉ client và thời
điểm yêu cầu, không lưu mã tra cứu; số client được giữ trong bộ nhớ có giới hạn.

### 4.4. Kiểm thử và bàn giao

Tại thư mục gốc, chạy kiểm thử backend theo quy định của nhóm:

```bash
python -m pytest -v
```

Kiểm thử bao gồm tạo phiếu qua API tiếp nhận rồi tra cứu cùng phiếu, đọc trạng
thái mới nhất, lọc thông tin nội bộ, phản hồi sai mã/không tồn tại giống nhau,
lỗi đầu vào không lộ mã, giới hạn thử sai và hết thời gian chờ giả lập.

Kiểm thử frontend và build:

```bash
cd frontend
npm test
npm run build
```

Kiểm thử tương tác dùng React Testing Library/Vitest với DOM giả lập: nhập
thiếu, tra cứu thành công, nhập sai, không giữ kết quả cũ, lỗi mạng, chờ do vượt
giới hạn, thử lại, ẩn/hiện mã và hiển thị dữ liệu an toàn. Các kiểm thử này không
thay thế việc kiểm tra trực tiếp bố cục trên trình duyệt và các kích thước màn hình.
GitHub Actions chạy cả pytest, kiểm thử frontend và build trên PR vào `develop`.

### 4.5. Giới hạn tích hợp hiện tại

- Tiếp nhận phiếu và portal dùng cùng lựa chọn `WARRANTY_STORAGE`: `memory`
  hoặc `postgresql`. Bản PostgreSQL tái sử dụng SQL và repository từ nhánh
  `feat/database-tung` (commit `a97ca44`), kết nối qua psycopg. Hợp đồng API
  portal giữ nguyên. Các dịch vụ sửa chữa, kho và Dashboard vẫn cần nhóm
  tích hợp riêng với tầng lưu trữ PostgreSQL; bộ kiểm thử portal đọc các trạng
  thái đã lưu, không thay thế kiểm thử nghiệp vụ cập nhật sửa chữa trên CSDL.
- Bộ giới hạn thử sai hiện dùng RAM của **một tiến trình**. Triển khai nhiều
  worker hoặc nhiều máy cần bộ đếm dùng chung, ví dụ Redis theo SAD. Khởi động
  lại ứng dụng sẽ xóa cả dữ liệu demo và bộ đếm.
- Các API nội bộ `/api/v1/tickets` của module tiếp nhận hiện chưa có lớp xác
  thực tài khoản/phân quyền ở router. Phần này cần nhóm hoàn thiện trước khi
  dùng dữ liệu thật hoặc đưa hệ thống ra Internet; không dùng API nội bộ này
  thay endpoint công khai của portal.
- Cơ chế cấp/cấp lại mã bí mật, ngưỡng chống thử sai và điều kiện đo hiệu năng
  vẫn cần nhóm xác nhận ở OPEN05–OPEN06. Việc đạt kiểm thử chức năng không
  tự chứng minh đã đạt mục tiêu phản hồi dưới 3 giây ở tải thực tế.
- Khi đưa nội dung/mã nguồn có AI hỗ trợ vào báo cáo, ghi nhận trung thực tại
  Phụ lục Z và dẫn chiếu theo AUR.99 trong mẫu báo cáo của nhóm.

### 4.6. Chạy portal với PostgreSQL trên Windows

Cài và khởi động PostgreSQL 16, tạo database `warranty_db` và tài khoản
`warranty_user` có quyền tạo bảng trong database đó theo cấu hình nhóm.
Tại thư mục gốc dự án, dùng CMD:

```bat
py -m venv .venv
.venv\Scripts\python.exe -m pip install -r requirements.txt
copy .env.example .env
notepad .env
```

Trong `.env`, điền đúng host, port, database, user và mật khẩu của PostgreSQL
đang chạy; giữ `WARRANTY_STORAGE=postgresql`. Port mặc định trong file mẫu là
5433, cần sửa thành cổng thực tế của máy bạn (PostgreSQL thường dùng 5432).
`.env` được bỏ qua bởi Git; không đưa file chứa mật khẩu lên repository.

Kiểm tra kết nối, rồi khởi tạo 21 bảng trên **database trống**:

```bat
.venv\Scripts\python.exe -m src.warranty_core.database
.venv\Scripts\python.exe -m database.init_db
```

Nếu database đã có cấu trúc từ phần của Tùng thì bỏ qua lệnh khởi tạo. Công cụ
khởi tạo không xóa hoặc ghi đè các bảng sẵn có. Có thể thêm một phiếu minh họa
được lưu qua `PostgreSQLTicketService` bằng lệnh sau; chạy lại sẽ dùng phiếu cũ:

```bat
.venv\Scripts\python.exe -m database.seed_portal_demo
```

Lưu **mã phiếu thực tế được in ra**, mã tra cứu mẫu là `HT-SQL-DEMO-001`.
Mã phiếu phụ thuộc ngày tạo và bộ đếm trong CSDL, có thể khác mã ở Mục 4.1.
Các phiếu khác được tiếp nhận qua `POST /api/v1/tickets` cũng dùng chung CSDL.

Nếu chưa có `frontend/out`, build giao diện theo Mục 4.1. Khởi động API bình
thường, phục vụ cả giao diện và dữ liệu PostgreSQL:

```bat
.venv\Scripts\python.exe -m uvicorn src.warranty_app.main:app --host 127.0.0.1 --port 3000
```

Mở http://127.0.0.1:3000 và nhập cặp mã từ lệnh tạo dữ liệu mẫu. Dừng rồi chạy
lại lệnh uvicorn sẽ giữ nguyên dữ liệu đã lưu. Mỗi lần tra cứu mở một kết nối
CSDL riêng và đóng sau khi xử lý; lỗi CSDL trả thông báo 503 chung, không lộ
chi tiết kết nối. Lệnh `python -m src.warranty_app.demo` ở Mục 4.1 dành cho
minh họa bằng RAM, kể cả khi `.env` đang cấu hình PostgreSQL.

Chạy toàn bộ kiểm thử với PostgreSQL đã khởi tạo:

```bat
.venv\Scripts\python.exe -m pytest -v
```

Nếu chỉ kiểm tra chế độ RAM và chưa chạy PostgreSQL:

```bat
.venv\Scripts\python.exe -m pytest -v -m "not integration"
```

CI backend tạo PostgreSQL 16, chạy công cụ khởi tạo schema và toàn bộ kiểm
thử, đồng thời vẫn giữ job kiểm thử/build frontend. Kiểm thử SQL dùng các bản
ghi có ID riêng, dọn đúng dữ liệu của ca kiểm thử và không truncate bảng.
