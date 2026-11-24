import os
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import parse_xml, OxmlElement
from docx.oxml.ns import nsdecls, qn

from doc_content_builder import (
    create_document,
    format_row,
    set_cell_border,
    add_title,
    add_heading_1,
    add_heading_2,
    add_heading_3,
    add_body_p,
    add_table_caption,
    add_figure_caption,
    add_diagram_box
)

def build_sad_doc():
    doc = create_document()
    
    # Meta header
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.line_spacing = 1.2
    p_meta.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_meta.paragraph_format.first_line_indent = Inches(0)
    r_meta = p_meta.add_run(
        "MÃ TÀI LIỆU: PSE.G102_SAD_KienTrucHeThong_v1.0\n"
        "BỘ MÔN: CÔNG NGHỆ PHẦN MỀM - DỰ ÁN PSE.G102\n"
        "TÁC GIẢ: NGUYỄN HOÀNG THIỆN ANH (MSV: B23DCKD003) - ROLE D&T\n"
        "TIÊU CHUẨN THIẾT KẾ: IEEE 1471 / ISO/IEC 42010"
    )
    r_meta.font.name = 'Times New Roman'
    r_meta.font.size = Pt(10)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(80, 80, 80)

    add_title(doc, "TÀI LIỆU THIẾT KẾ KIẾN TRÚC PHẦN MỀM (SAD v1.0)\nSOFTWARE ARCHITECTURE DOCUMENT")

    add_heading_1(doc, "1. Giới thiệu tổng quan (Introduction)")
    add_body_p(
        doc,
        "Tài liệu này cung cấp bản thiết kế kiến trúc toàn diện cho Hệ thống Quản lý Hoạt động Bảo hành của Trung tâm Hỗ trợ Kỹ thuật "
        "tại Công ty máy tính Hưng Thiện theo mô hình 4+1 Architectural View Model (Kruchten, 1995) và chuẩn IEEE 1471 / ISO/IEC 42010. "
        "Tài liệu đóng vai trò kim chỉ nam định hướng kỹ thuật cho toàn bộ các phần tăng trưởng INC1, INC2 và INC3 trong suốt 6 tuần thực hiện dự án."
    )

    add_heading_1(doc, "2. Mục tiêu kiến trúc và Ràng buộc kỹ thuật (Architectural Goals & Constraints)")
    add_body_p(
        doc,
        "Kiến trúc hệ thống được thiết kế để thỏa mãn 5 mục tiêu chất lượng cốt lõi theo ISO/IEC 25010:2023:\n"
        "1. Tính kiểm thử được (Testability): Cho phép kiểm thử viên điều khiển môi trường và quan sát kết quả dễ dàng. Hỗ trợ giả lập thời gian "
        "(SimulatedClockService) để kiểm thử batch job 08:00 (TB.02) và dịch vụ email giả lập (TB.05).\n"
        "2. Hiệu năng hệ thống (Performance): Thời gian xử lý các giao dịch tiếp nhận, cập nhật dưới 3 giây (NFR_PERF_01); thời gian tải biểu đồ dưới 2 giây "
        "và xuất báo cáo dưới 3 giây trên tập dữ liệu tối thiểu 5.000 phiếu (NFR_PERF_02).\n"
        "3. Bảo mật kiểm soát truy cập (Security & RBAC): 100% các yêu cầu trái quyền bị chặn ở phía máy chủ (NFR_SEC_01); mật khẩu và mã tra cứu bí mật "
        "được băm an toàn (bcrypt, SHA-256) và không xuất hiện trong nhật ký (NFR_SEC_02).\n"
        "4. Độ tin cậy và tính toàn vẹn (Reliability): Các thao tác tiếp nhận, xuất kho linh kiện, chuyển đổi trạng thái và bàn giao phải tuân thủ "
        "giao dịch nguyên tố ACID, chống cập nhật đồng thời gây mất mát dữ liệu (NFR_REL_01).\n"
        "5. Tương thích đa thiết bị (Compatibility): Giao diện web hiển thị tốt trên máy tính để bàn (1920x1080) lẫn điện thoại di động (375x812) theo NFR_COMP_01."
    )

    add_heading_1(doc, "3. Khung nhìn logic (Logical View)")
    add_body_p(
        doc,
        "Hệ thống áp dụng mô hình Clean Layered Architecture với 5 tầng phân lập:\n"
        "• Presentation Layer: Ứng dụng Next.js/React responsive tương tác qua REST API.\n"
        "• API & Application Layer: FastAPI Router, Pydantic DTO Validation, JWT Authentication Middleware, Exception Handlers.\n"
        "• Domain Services Layer: TicketService (BR01, BR02), WarrantyService (BR03), RepairService (BR04, BR05, BR07, BR09), "
        "InventoryService (BR06), SlaService (BR08), PortalService (BR10), DashboardService (TB.12).\n"
        "• Infrastructure Layer: SQLAlchemy 2.0 Async, PostgreSQL 16 Repository, Redis Cache, File Attachment Storage.\n"
        "• External Adapters: SystemClockAdapter/SimulatedClockAdapter, SmtpEmailAdapter/MockEmailAdapter."
    )

    add_heading_1(doc, "4. Khung nhìn tiến trình (Process View)")
    add_body_p(
        doc,
        "Các tiến trình chạy đồng thời và phi đồng bộ trong hệ thống được quản lý thông qua máy chủ ứng dụng Uvicorn với kiến trúc hướng sự kiện (Event Loop). "
        "Tiến trình nền (Background Scheduler) chạy độc lập để thực thi tác vụ quét hạn SLA lúc 08:00 sáng hàng ngày, gom nhóm phiếu theo BR08 và gửi email thông báo "
        "mà không chặn luồng xử lý chính của người dùng."
    )

    add_heading_1(doc, "5. Khung nhìn triển khai vật lý (Physical / Deployment View)")
    add_body_p(
        doc,
        "Hệ thống được đóng gói thành 5 Docker Containers thông qua Docker Compose:\n"
        "1. `frontend-server`: Nginx 1.25 đóng vai trò Reverse Proxy và phục vụ Static Web UI.\n"
        "2. `api-backend`: Python 3.12 / FastAPI chạy trên cổng 8000.\n"
        "3. `db-postgres`: PostgreSQL 16.2 lưu trữ cơ sở dữ liệu quan hệ với Docker Volume persistent.\n"
        "4. `cache-redis`: Redis 7.2 phục vụ bộ nhớ đệm chỉ số Dashboard và Rate Limiting.\n"
        "5. `mock-mailpit`: Dịch vụ SMTP testing giả lập dùng trong môi trường kiểm thử (TB.05)."
    )

    add_heading_1(doc, "6. Khung nhìn kịch bản (Scenarios / Use Case View)")
    add_body_p(
        doc,
        "Khung nhìn kịch bản kết nối 12 Use Case đã xác định tại Chương 3 (từ UC01 Đăng nhập đến UC12 Xuất báo cáo). Các kịch bản trọng yếu gồm:\n"
        "• UC03: Tiếp nhận và lập phiếu bảo hành với kiểm tra danh mục linh kiện ký đối chiếu khi giữ máy.\n"
        "• UC04: Thẩm định điều kiện bảo hành phân loại Đổi 1-1, Sửa miễn phí, Sửa có phí.\n"
        "• UC06: Bàn giao công việc giữa hai kỹ thuật viên có hỗ trợ KTV cũ vắng mặt.\n"
        "• UC07 & UC08: Cập nhật sửa chữa, chuyển trạng thái và ghi nhận linh kiện sử dụng.\n"
        "• UC10: Cổng tra cứu tiến độ bảo hành cho khách hàng bằng mã phiếu và mã bí mật."
    )

    out_file = r'E:\Warranty Management System\docs\PSE.G102_SAD_KienTrucHeThong.docx'
    doc.save(out_file)
    print(f"SAD doc saved at {out_file}")

def build_naming_standard_doc():
    doc = create_document()
    
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.line_spacing = 1.2
    p_meta.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_meta.paragraph_format.first_line_indent = Inches(0)
    r_meta = p_meta.add_run(
        "MÃ TÀI LIỆU: PSE.G102_STD_QuyTacDatTen_v1.0\n"
        "PHỤ LỤC A: BỘ QUY TẮC ĐẶT TÊN DỰ ÁN PHẦN MỀM PSE.G102\n"
        "TÁC GIẢ: NGUYỄN HOÀNG THIỆN ANH (MSV: B23DCKD003) - ROLE D&T"
    )
    r_meta.font.name = 'Times New Roman'
    r_meta.font.size = Pt(10)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(80, 80, 80)

    add_title(doc, "BỘ QUY TẮC ĐẶT TÊN CHUẨN KỸ THUẬT (NAMING STANDARDS)\nPHỤ LỤC A - DỰ ÁN PSE.G102")

    add_heading_1(doc, "1. Mục đích và Phạm vi áp dụng")
    add_body_p(
        doc,
        "Bộ quy tắc đặt tên kỹ thuật này được ban hành nhằm chuẩn hóa toàn bộ các đối tượng phát sinh trong vòng đời phát triển dự án "
        "Quản lý Bảo hành Hưng Thiện, bao gồm tài liệu kỹ thuật, mã nghiệp vụ, mã nguồn, cơ sở dữ liệu, giao diện lập trình REST API "
        "và hệ thống quản lý phiên bản Git. Toàn bộ 9 thành viên nhóm bắt buộc tuân thủ 100% quy chuẩn này."
    )

    add_heading_1(doc, "2. Quy chuẩn đặt tên tài liệu kỹ thuật và sản phẩm chuyển giao")
    add_body_p(
        doc,
        "Cấu trúc định danh: PSE.G102_[Increment]_[DocumentType]_[Description]_[Version].[ext]\n"
        "• PSE.G102: Mã định danh dự án thống nhất.\n"
        "• Increment: Mã phần tăng trưởng (INC1, INC2, INC3; tài liệu chung toàn dự án thì để trống).\n"
        "• DocumentType: Loại tài liệu (SAD: Thiết kế kiến trúc; SRS: Đặc tả yêu cầu; PMP: Kế hoạch dự án; TEST: Báo cáo kiểm thử; STD: Tiêu chuẩn).\n"
        "• Description: Nội dung ngắn gọn bằng tiếng Việt không dấu hoặc tiếng Anh.\n"
        "• Version: Phiên bản tài liệu (v1.0: phát hành chính thức; v1.1: cập nhật nhỏ; v2.0: cập nhật lớn)."
    )

    add_heading_1(doc, "3. Quy chuẩn đặt tên mã nghiệp vụ hệ thống")
    add_body_p(
        doc,
        "Mọi thực thể nghiệp vụ cốt lõi đều được cấp mã định danh có cấu trúc rõ ràng:\n"
        "• Mã phiếu tiếp nhận: TKT_YYYYMMDD_x (x là số thứ tự tăng dần tự động cấp trong ngày, ví dụ: TKT_20261124_1).\n"
        "• Mã thẩm định bảo hành: WAR_XXXXXXXX (ví dụ: WAR_A1B2C3D4).\n"
        "• Mã linh kiện trong kho: PRT_XXXXXX (ví dụ: PRT_RAM16G, PRT_PINXPS).\n"
        "• Mã cấp phát linh kiện: ALC_XXXXXXXX (ví dụ: ALC_12345678).\n"
        "• Mã phiên bàn giao KTV: HO_XXXXXXXX (ví dụ: HO_87654321).\n"
        "• Mã tài khoản nhân sự: USR_VAI_TRÒ_xx (ví dụ: USR_ADMIN_01, USR_TECH_01)."
    )

    add_heading_1(doc, "4. Quy chuẩn đặt tên mã nguồn (Clean Code Naming Conventions)")
    add_body_p(
        doc,
        "• Tên Class / Interface / Model: PascalCase (ví dụ: WarrantyTicket, TicketService, InMemoryRepository).\n"
        "• Tên Hàm / Phương thức: snake_case trong Python (ví dụ: create_ticket, finalize_return); camelCase trong JavaScript/TypeScript.\n"
        "• Tên Biến / Thuộc tính: snake_case (ví dụ: promised_return_date, current_technician_id).\n"
        "• Tên Hằng số / Enum items: UPPER_SNAKE_CASE (ví dụ: TICKET_STATUS, WAITING_FOR_PARTS, RED_ALERT).\n"
        "• Tên Tệp tin và Thư mục gói: Toàn bộ chữ thường snake_case (ví dụ: ticket_service.py, domain_models.py)."
    )

    add_heading_1(doc, "5. Quy chuẩn đặt tên cơ sở dữ liệu (PostgreSQL)")
    add_body_p(
        doc,
        "• Tên bảng: Danh từ số nhiều, chữ thường snake_case (ví dụ: users, customers, devices, warranty_tickets, spare_parts).\n"
        "• Tên khóa chính: <tên_bảng_số_ít>_id (ví dụ: ticket_id, customer_id, part_id).\n"
        "• Tên khóa ngoại: Trùng tên với khóa chính của bảng tham chiếu.\n"
        "• Tên chỉ mục: idx_<table>_<column> (ví dụ: idx_tickets_status, idx_devices_serial).\n"
        "• Tên ràng buộc: uq_<table>_<column> cho unique; chk_<table>_<rule> cho check constraint."
    )

    add_heading_1(doc, "6. Quy chuẩn đặt tên RESTful API và Git Commits")
    add_body_p(
        doc,
        "• REST API: Sử dụng danh từ số nhiều ở dạng chữ thường (/api/v1/tickets, /api/v1/spare-parts, /api/v1/tickets/{id}/work-logs).\n"
        "• Conventional Commits: <type>(<scope>): <subject> (ví dụ: feat(tkt): add signed parts validation per BR02; fix(sla): correct 08:00 digest grouping).\n"
        "• Release Tags trên Git: INC1-v1.0, INC2-v1.0, INC3-v1.0."
    )

    out_file = r'E:\Warranty Management System\docs\PSE.G102_QuyTacDatTen_NamingStandard.docx'
    doc.save(out_file)
    print(f"Naming Standard doc saved at {out_file}")

def build_data_flow_spec_doc():
    doc = create_document()
    
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.line_spacing = 1.2
    p_meta.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_meta.paragraph_format.first_line_indent = Inches(0)
    r_meta = p_meta.add_run(
        "MÃ TÀI LIỆU: PSE.G102_SPEC_ThietKeLuongDuLieu_v1.0\n"
        "ĐẶC TẢ KỸ THUẬT: THIẾT KẾ CHI TIẾT LUỒNG DỮ LIỆU BẢO HÀNH & CSDL VẬT LÝ\n"
        "TÁC GIẢ: NGUYỄN HOÀNG THIỆN ANH (MSV: B23DCKD003) - ROLE D&T"
    )
    r_meta.font.name = 'Times New Roman'
    r_meta.font.size = Pt(10)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(80, 80, 80)

    add_title(doc, "ĐẶC TẢ CHI TIẾT LUỒNG DỮ LIỆU BẢO HÀNH\nVÀ THIẾT KẾ CƠ SỞ DỮ LIỆU MỨC VẬT LÝ")

    add_heading_1(doc, "1. Tổng quan luồng dữ liệu bảo hành (Warranty Data Flow Overview)")
    add_body_p(
        doc,
        "Luồng dữ liệu bảo hành mô tả toàn bộ sự luân chuyển, biến đổi và lưu trữ thông tin của thiết bị qua từng giai đoạn tiếp nhận, "
        "thẩm định, phân công, điều chuyển, sửa chữa, thay thế linh kiện và bàn giao trả máy tại Công ty máy tính Hưng Thiện. "
        "Hệ thống luồng dữ liệu được thiết kế bám sát 10 quy tắc nghiệp vụ BR01-BR10 nhằm giải quyết triệt để 3 bất cập lớn: "
        "thiếu dữ liệu tập trung, chậm trễ cập nhật tiến độ và mất mát thông tin khi chuyển giao ca trực giữa các kỹ thuật viên."
    )

    add_heading_1(doc, "2. Sơ đồ luồng dữ liệu phân rã (DFD Level 0, Level 1, Level 2)")
    add_body_p(
        doc,
        "Tài liệu phân rã toàn diện 6 luồng dữ liệu nghiệp vụ chính:\n"
        "• Luồng DFD 1.1: Tiếp nhận và Lập hồ sơ phiếu bảo hành với chữ ký đối chiếu linh kiện (BR01, BR02).\n"
        "• Luồng DFD 1.2: Thẩm định chính sách và Phân loại 3 phương án bảo hành (BR03).\n"
        "• Luồng DFD 2.0: Phân công kỹ thuật viên và Quy trình bàn giao điều chuyển công việc có hỗ trợ KTV cũ vắng mặt (BR04, BR07).\n"
        "• Luồng DFD 3.0: Cập nhật sửa chữa, chuyển đổi cỗ máy trạng thái FSM và Quản lý linh kiện kho không trừ trùng lặp (BR05, BR06).\n"
        "• Luồng DFD 4.0: Nghiệm thu chạy thử, đối chiếu chữ ký tem mác và Bàn giao trả thiết bị (BR09).\n"
        "• Luồng DFD 5.0: Bộ máy tự động quét hạn SLA và Gửi email điểm tin 08:00 sáng chia 2 nhóm không giao nhau (BR08)."
    )

    add_heading_1(doc, "3. Cỗ máy trạng thái và Bảng ma trận chuyển trạng thái hợp lệ")
    add_body_p(
        doc,
        "Vòng đời phiếu bảo hành được quản lý bởi cỗ máy trạng thái hữu hạn gồm 9 trạng thái: RECEIVED (Đã tiếp nhận), "
        "PENDING_ASSIGNMENT (Chờ phân công), UNDER_INSPECTION (Đang kiểm tra), UNDER_REPAIR (Đang sửa chữa), "
        "WAITING_FOR_PARTS (Chờ linh kiện), WAITING_FOR_RESULT_CHECK (Chờ kiểm tra kết quả), WAITING_FOR_RETURN (Chờ trả), "
        "RETURNED (Đã trả) và CANCELLED (Đã hủy). Các quy tắc chuyển đổi trạng thái được bảo vệ nghiêm ngặt ở tầng xử lý server, "
        "chặn đứng 100% các chuyển dịch sai quy trình (ví dụ: từ Đang kiểm tra nhảy thẳng sang Đã trả)."
    )

    add_heading_1(doc, "4. Thiết kế Cơ sở dữ liệu vật lý và Chiến lược lập chỉ mục (Indexing Strategy)")
    add_body_p(
        doc,
        "Lược đồ cơ sở dữ liệu quan hệ gồm 10 bảng đạt chuẩn 3NF: users, customers, devices, warranty_tickets, "
        "warranty_assessments, ticket_status_history, repair_work_logs, handover_sessions, spare_parts, part_allocations.\n"
        "Để đáp ứng NFR_PERF_02 (thời gian tải biểu đồ dưới 2 giây và xuất báo cáo dưới 3 giây trên 5.000 phiếu bảo hành), "
        "hệ thống thiết lập chiến lược lập chỉ mục tối ưu:\n"
        "• B-Tree Index trên `status` và `promised_return_date`: Tối ưu hóa bộ lọc Dashboard và batch job quét hạn SLA 08:00.\n"
        "• B-Tree Index trên `serial_number`: Tối ưu tra cứu hồ sơ thiết bị lịch sử.\n"
        "• B-Tree Index trên `current_technician_id`: Tối ưu danh sách công việc giao cho từng kỹ thuật viên.\n"
        "• GIN Index trên `signed_parts_json`: Cho phép truy vấn nhanh linh kiện có chữ ký trong tài liệu JSONB."
    )

    out_file = r'E:\Warranty Management System\docs\PSE.G102_ThietKeLuongDuLieu_DataFlowSpec.docx'
    doc.save(out_file)
    print(f"Data Flow Spec doc saved at {out_file}")

if __name__ == '__main__':
    build_sad_doc()
    build_naming_standard_doc()
    build_data_flow_spec_doc()
