# PSE.G102 - Warranty Management System
## Phần mềm Quản lý Hoạt động Bảo hành của Trung tâm Hỗ trợ Kỹ thuật tại Công ty Máy tính Hưng Thiện

Dự án môn học: **Công nghệ phần mềm (PSE)**  
Khoa Viễn thông 1 - Học viện Công nghệ Bưu chính Viễn thông (PTIT)  
Nhóm thực hiện: **PSE.G102**

---

## 1. Cấu trúc thư mục dự án

```text
E:\Warranty Management System\
├── docs/                                  # Thư mục lưu trữ tài liệu Word theo chuẩn Thông tư 30
│   ├── PSE.G102_Chuong4_KienTrucPhanMem.docx
│   ├── PSE.G102_SAD_KienTrucHeThong.docx
│   ├── PSE.G102_QuyTacDatTen_NamingStandard.docx
│   └── PSE.G102_ThietKeLuongDuLieu_DataFlowSpec.docx
├── src/                                   # Mã nguồn kiến trúc khung (Clean Layered Architecture)
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
├── .gitignore                             # Loại trừ file rác, virtualenv, file nhạy cảm
├── requirements.txt                       # Thư viện phụ thuộc
└── README.md                              # Hướng dẫn dự án và quy chế Git
```

---

## 2. Hướng dẫn cài đặt và chạy kiểm thử

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

## 3. Quy chuẩn và Quy trình Git an toàn cho nhóm (Git Workflow & Safety Rules)

### 3.1. Mô hình phân nhánh (Branching Strategy)
- **`main`**: Nhánh chính thức, chứa mã nguồn ổn định nhất. **Nghiêm cấm push trực tiếp vào `main`**.
- **`develop`**: Nhánh tích hợp chung của nhóm. Tất cả các tính năng hoàn thiện sẽ được merge vào đây trước.
- **`feat/<module>-<tên_task>`**: Nhánh tính năng cá nhân (ví dụ: `feat/tkt-create`, `feat/dash-chart`, `feat/portal-search`). Mỗi thành viên khi làm task mới bắt buộc phải tạo nhánh từ `develop`.
- **`fix/<mã_lỗi>`**: Nhánh sửa lỗi phát sinh trong quá trình kiểm thử.

### 3.2. Quy trình làm việc 6 bước của từng thành viên
1. **Lấy mã nguồn mới nhất:**
   ```bash
   git checkout develop
   git pull origin develop
   ```
2. **Tạo nhánh tính năng mới:**
   ```bash
   git checkout -b feat/tkt-create-ticket
   ```
3. **Thực hiện viết code và kiểm thử cục bộ:**
   - Code tuân thủ Clean Code, không đưa icon, không để comment thừa thãi.
   - Luôn chạy lệnh kiểm thử trước khi commit:
     ```bash
     pytest
     ```
   - Chỉ khi 100% test pass mới được commit.
4. **Commit theo chuẩn Conventional Commits:**
   - Cú pháp: `<loại>(<phân_hệ>): <mô tả ngắn gọn bằng tiếng Anh/Việt không dấu>`
   - Ví dụ:
     - `feat(tkt): implement hold for repair signed parts check per BR02`
     - `fix(sla): resolve 08:00 email grouping condition`
     - `test(portal): add unit test for secret code hashing verification`
     - `docs(sad): update database schema diagram`
5. **Đẩy nhánh lên Remote:**
   ```bash
   git push -u origin feat/tkt-create-ticket
   ```
6. **Tạo Pull Request (PR) và Rà soát chéo (Peer Review):**
   - Vào GitHub/GitLab tạo Pull Request từ `feat/...` vào `develop`.
   - Gắn ít nhất 1 thành viên khác (hoặc vai trò D&T) vào review.
   - Chỉ được Merge khi reviewer phê duyệt và các bài test tự động đều Đạt (Pass).

### 3.3. Các nguyên tắc an toàn bắt buộc (Safety Checklist)
- **Không bao giờ commit file nhạy cảm:** Mật khẩu, API key, token bí mật, file `.env`. Sử dụng file `.env.example` để chia sẻ cấu hình mẫu.
- **Không commit file rác / build cache:** `__pycache__`, `.pytest_cache`, `.venv`, file tạm của Word (`~$...`).
- **Luôn pull code mới nhất trước khi push:** Giúp giải quyết xung đột (conflict) ngay trên máy cá nhân thay vì gây lỗi trên repo chung.
