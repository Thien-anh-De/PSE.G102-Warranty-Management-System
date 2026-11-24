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

def build_chuong4_document():
    doc = create_document()
    
    # Header Information
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.line_spacing = 1.2
    p_meta.paragraph_format.space_before = Pt(0)
    p_meta.paragraph_format.space_after = Pt(12)
    p_meta.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    p_meta.paragraph_format.first_line_indent = Inches(0)
    r_meta = p_meta.add_run(
        "DỰ ÁN: PHÁT TRIỂN PHẦN MỀM QUẢN LÝ BẢO HÀNH - PSE.G102\n"
        "BỘ MÔN: CÔNG NGHỆ PHẦN MỀM - HỌC VIỆN CÔNG NGHỆ BƯU CHÍNH VIỄN THÔNG\n"
        "THÀNH VIÊN THỰC HIỆN: NGUYỄN HOÀNG THIỆN ANH (MSV: B23DCKD003) - ROLE D&T\n"
        "NHIỆM VỤ: THIẾT KẾ KIẾN TRÚC TỔNG THỂ, QUY TẮC ĐẶT TÊN, THIẾT KẾ LUỒNG DỮ LIỆU"
    )
    r_meta.font.name = 'Times New Roman'
    r_meta.font.size = Pt(10)
    r_meta.font.italic = True
    r_meta.font.color.rgb = RGBColor(80, 80, 80)

    # Title
    add_title(doc, "CHƯƠNG 4. KIẾN TRÚC PHẦN MỀM")

    # Introduction block
    add_body_p(
        doc,
        "Chương này trình bày toàn bộ kết quả phân tích, thiết kế kiến trúc hệ thống phần mềm quản lý hoạt động "
        "bảo hành tại Công ty máy tính Hưng Thiện, do thành viên Nguyễn Hoàng Thiện Anh (Mã SV: B23DCKD003, thuộc nhóm Thiết kế "
        "và Kiểm thử - Role D&T) chịu trách nhiệm thực hiện chính. Căn cứ trên danh sách 30 yêu cầu chức năng (FR_AUTH_01 đến "
        "FR_DASH_03), 10 yêu cầu phi chức năng (NFR_PERF_01 đến NFR_TEST_02), hệ thống 10 quy tắc nghiệp vụ dùng chung "
        "(BR01 đến BR10) và danh sách 12 Use Case đã được đặc tả, rà soát đồng nghiệp (Peer Review) nghiêm ngặt tại Chương 3, "
        "Chương 4 đóng vai trò chuyển giao các yêu cầu phân tích thành giải pháp công nghệ và mô hình kiến trúc có tính khả thi cao, "
        "đảm bảo tính kiểm thử được (Testability) và đáp ứng mô hình phát triển Tăng dần (Incremental Model) xuyên suốt dự án."
    )

    # 4.1. Vai trò của kiến trúc phần mềm
    add_heading_1(doc, "4.1. Vai trò của kiến trúc phần mềm với quá trình phát triển dự án phần mềm")
    
    add_body_p(
        doc,
        "Theo chuẩn quốc tế IEEE 1471 và ISO/IEC 42010 về đặc tả kiến trúc các hệ thống phần mềm chuyên sâu, kiến trúc phần mềm "
        "(Software Architecture) được định nghĩa là cơ cấu tổ chức nền tảng của một hệ thống phần mềm, bao gồm các thành phần cốt lõi, "
        "mối quan hệ tương tác hữu cơ giữa các thành phần đó với môi trường xung quanh, cùng các nguyên tắc định hướng chỉ đạo xuyên suốt "
        "quá trình thiết kế, phát triển và tiến hóa của hệ thống. Trong công nghệ phần mềm hiện đại, kiến trúc không đơn thuần là sơ đồ khối "
        "tĩnh mà là khung xương sống định hình khả năng chịu tải, tính ổn định và tuổi thọ vận hành của toàn bộ sản phẩm."
    )
    
    add_body_p(
        doc,
        "Đối với đề tài 'Phát triển phần mềm quản lý hoạt động bảo hành của trung tâm hỗ trợ kỹ thuật tại Công ty máy tính Hưng Thiện', "
        "thiết kế kiến trúc phần mềm nắm giữ vai trò quyết định trên bốn phương diện then chốt sau:",
        bold_prefix="1. Vai trò định hướng và cầu nối kỹ thuật: "
    )
    
    add_body_p(
        doc,
        "Kiến trúc phần mềm đóng vai trò chuyển hóa những mong muốn nghiệp vụ và các mô hình ca sử dụng (Use Case) từ Chương 3 thành "
        "những thành phần phần mềm có cấu trúc, các hợp đồng giao diện lập trình (API Contracts) và lược đồ cơ sở dữ liệu vật lý có tính khả thi. "
        "Nếu thiếu một bản thiết kế kiến trúc chuẩn mực, các lập trình viên sẽ triển khai mã nguồn một cách tự phát, dẫn đến hiện tượng mã nguồn "
        "rác (spaghetti code), phân mảnh dữ liệu và không thể tích hợp các phân hệ giữa các phần tăng trưởng INC1, INC2 và INC3."
    )

    add_body_p(
        doc,
        "Theo mô hình chất lượng phần mềm ISO/IEC 25010:2023 đã xác định ở Chương 2, hệ thống phải thỏa mãn hàng loạt các thuộc tính chất lượng "
        "khắt khe: thời gian phản hồi giao dịch dưới 3 giây (T05, NFR_PERF_01), thời gian tải biểu đồ dưới 2 giây và xuất báo cáo dưới 3 giây "
        "với quy mô dữ liệu tối thiểu 5.000 phiếu (T12, NFR_PERF_02), kiểm soát truy cập từ chối 100% yêu cầu trái quyền ở phía server (T06, NFR_SEC_01), "
        "tính nhất quán giao dịch tạo phiếu, xuất kho, đổi trạng thái và bàn giao không để dữ liệu cập nhật một phần (T03, T07, T10, NFR_REL_01), "
        "và tỷ lệ chuyển giao email cảnh báo 08:00 đạt trên 95% (T09, NFR_REL_02). Các thuộc tính phi chức năng này không thể tự sinh ra trong "
        "quá trình viết mã chi tiết mà phải được kiến trúc sư hoạch định ngay từ cấu trúc phân tầng, phân vùng bộ nhớ đệm (Cache) và chiến lược lập chỉ mục dữ liệu.",
        bold_prefix="2. Đảm bảo các thuộc tính chất lượng phi chức năng: "
    )

    add_body_p(
        doc,
        "Theo Mục 2.4 và Mục 3.3.7, đặc tính Kiểm thử được (Testability) được nhóm xác định là điều kiện đầu vào bắt buộc (Entry Criteria) "
        "đối với nhóm Lập trình trước khi bàn giao sang kiểm thử. Kiến trúc phần mềm phải bảo đảm tính điều khiển được (Controllability) và tính "
        "quan sát được (Observability) thông qua việc tách biệt triệt để giao diện, nghiệp vụ và truy xuất dữ liệu. Đặc biệt, việc kiến trúc trừu tượng hóa "
        "đồng hồ hệ thống (ClockService) và dịch vụ gửi thư (EmailService) cho phép kiểm thử viên giả lập mốc thời gian chạy batch job 08:00 mà không cần "
        "chờ đợi thời gian thực của hệ điều hành, thỏa mãn trực tiếp tiêu chuẩn TB.02 và TB.05.",
        bold_prefix="3. Hiện thực hóa tiêu chuẩn Kiểm thử được (Testability): "
    )

    add_body_p(
        doc,
        "Dự án áp dụng mô hình phát triển Tăng dần gồm 3 phần tăng trưởng (INC1: Tiếp nhận và kho linh kiện; INC2: Sửa chữa và kiểm soát tiến độ; "
        "INC3: Tra cứu và thống kê). Kiến trúc module hóa cao giúp các lập trình viên có thể phát triển độc lập từng phân hệ mà không làm phá vỡ "
        "tính toàn vẹn của hệ thống hiện hữu. Nghiên cứu của Barry Boehm về kinh tế phần mềm đã chứng minh rằng chi phí sửa chữa một lỗi kiến trúc "
        "nếu phát hiện ở giai đoạn nghiệm thu hoặc vận hành sẽ gấp từ 50 đến 100 lần so với giai đoạn thiết kế. Do đó, việc xây dựng kiến trúc tổng thể "
        "ngay từ giai đoạn P3 là điều kiện tiên quyết giúp tối ưu hóa chi phí và đảm bảo tiến độ bàn giao trong 6 tuần.",
        bold_prefix="4. Giảm thiểu rủi ro kỹ thuật và tối ưu chi phí dự án: "
    )

    # 4.2. Một số kiến trúc phần mềm phổ biến
    add_heading_1(doc, "4.2. Một số kiến trúc phần mềm phổ biến")
    
    add_body_p(
        doc,
        "Trong kỹ nghệ phần mềm hiện đại, có nhiều mẫu kiến trúc được ứng dụng rộng rãi. Để có cơ sở khoa học lựa chọn giải pháp phù hợp nhất "
        "với đặc thù bài toán quản lý bảo hành tại Công ty máy tính Hưng Thiện, nhóm nghiên cứu đã tiến hành khảo sát và đánh giá 5 mô hình kiến trúc tiêu biểu:"
    )

    add_body_p(
        doc,
        "Toàn bộ chức năng giao diện, xử lý nghiệp vụ và truy cập cơ sở dữ liệu được đóng gói thành một đơn vị triển khai duy nhất (single deployable unit). "
        "Ưu điểm lớn nhất là quá trình phát triển ban đầu đơn giản, chi phí hạ tầng thấp và dễ dàng gọi hàm nội bộ mà không cần phụ thuộc mạng. Tuy nhiên, "
        "nhược điểm cốt tử là tính ghép nối rất cao (tight coupling), khó mở rộng theo chiều ngang, và khi một lỗi nhỏ xảy ra có thể làm sụp đổ toàn bộ ứng dụng.",
        bold_prefix="1. Kiến trúc nguyên khối truyền thống (Monolithic Architecture): "
    )

    add_body_p(
        doc,
        "Hệ thống được chia thành 3 tầng vật lý/logic độc lập: Tầng biểu diễn (Presentation Tier), Tầng nghiệp vụ (Application / Business Tier) và "
        "Tầng dữ liệu (Data Tier). Kiến trúc này tách bạch trách nhiệm rõ ràng, dễ bảo trì, dễ kiểm thử giao diện và xử lý nghiệp vụ độc lập. Đây là mô hình "
        "chuẩn mực cho các ứng dụng quản lý doanh nghiệp vừa và nhỏ, rất phù hợp với luồng dữ liệu nghiệp vụ bảo hành tuần tự.",
        bold_prefix="2. Kiến trúc phân tầng (Layered 3-Tier Architecture): "
    )

    add_body_p(
        doc,
        "Hệ thống được chia nhỏ thành tập hợp các dịch vụ độc lập, mỗi dịch vụ sở hữu cơ sở dữ liệu riêng biệt và giao tiếp thông qua mạng (HTTP/REST hoặc gRPC). "
        "Mô hình này mang lại khả năng mở rộng tuyệt vời và tính linh hoạt công nghệ giữa các nhóm phát triển. Đổi lại, kiến trúc này đòi hỏi chi phí hạ tầng máy chủ "
        "rất lớn, độ trễ mạng cao, sự phức tạp trong quản lý giao dịch phân tán (Distributed Transactions - 2PC/Saga) và rủi ro bất đồng bộ dữ liệu, vượt quá nhu cầu "
        "và nguồn lực của một trung tâm bảo hành tầm trung.",
        bold_prefix="3. Kiến trúc vi dịch vụ (Microservices Architecture): "
    )

    add_body_p(
        doc,
        "Các thành phần trong hệ thống giao tiếp phi đồng bộ thông qua các sự kiện (Events) phát ra qua hàng đợi thông điệp (Message Broker như RabbitMQ, Kafka). "
        "Kiến trúc này tối ưu cho các hệ thống có tính phản ứng nhanh, lưu lượng ghi đột biến cao. Tuy nhiên, việc gỡ lỗi (debugging), truy vết luồng thực thi "
        "và đảm bảo tính nhất quán dữ liệu tức thời đòi hỏi các giải pháp phức tạp.",
        bold_prefix="4. Kiến trúc hướng sự kiện (Event-Driven Architecture): "
    )

    add_body_p(
        doc,
        "Do Robert C. Martin và Alistair Cockburn khởi xướng, kiến trúc này đặt logic nghiệp vụ (Domain Entities & Business Rules) vào trung tâm tuyệt đối, "
        "hoàn toàn độc lập với khung phát triển (framework), cơ sở dữ liệu hay giao diện người dùng. Mọi phụ thuộc đều hướng vào trong thông qua các cổng giao tiếp "
        "(Ports) và bộ điều hợp (Adapters). Mô hình này mang lại tính kiểm thử độc lập (Isolateability) hoàn hảo, cho phép thay thế cơ sở dữ liệu thật hoặc dịch vụ "
        "gửi email bằng các đối tượng giả lập (Mock/Stub) một cách dễ dàng.",
        bold_prefix="5. Kiến trúc linh hoạt Clean Architecture / Ports & Adapters: "
    )

    add_table_caption(doc, "Bảng 4.1: Ma trận đánh giá và so sánh các kiến trúc phần mềm")
    
    table_arch = doc.add_table(rows=6, cols=6)
    table_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    headers = ["Tiêu chí đánh giá", "Monolith", "Layered 3-Tier", "Microservices", "Event-Driven", "Clean Layered"]
    for i, h in enumerate(headers):
        cell = table_arch.cell(0, i)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(11)
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_row(table_arch.rows[0], is_header=True)

    arch_data = [
        ["Độ phức tạp triển khai", "Rất thấp", "Thấp", "Rất cao", "Cao", "Trung bình"],
        ["Chi phí hạ tầng máy chủ", "Tối thiểu", "Thấp", "Rất tốn kém", "Tương đối cao", "Tiết kiệm"],
        ["Tính kiểm thử được (Testability)", "Thấp", "Khá", "Phức tạp", "Khá", "Tuyệt đối (Rất cao)"],
        ["Mức độ ghép nối (Coupling)", "Cao", "Vừa phải", "Rất thấp", "Rất thấp", "Rất lỏng (Loose)"],
        ["Phù hợp Incremental (6 tuần)", "Trung bình", "Tốt", "Không phù hợp", "Kém", "Tối ưu nhất"]
    ]
    for row_idx, r in enumerate(arch_data, start=1):
        for col_idx, val in enumerate(r):
            cell = table_arch.cell(row_idx, col_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx > 0 else WD_ALIGN_PARAGRAPH.LEFT
        format_row(table_arch.rows[row_idx], is_header=False)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_body_p(
        doc,
        "Kết luận lựa chọn kiến trúc: Căn cứ bảng phân tích định lượng trên và yêu cầu nghiệp vụ của Công ty máy tính Hưng Thiện, nhóm phát triển "
        "quyết định lựa chọn mô hình Kiến trúc phân tầng dạng Clean Layered Architecture kết hợp cơ chế Tiêm phụ thuộc (Dependency Injection). "
        "Mô hình này dung hòa trọn vẹn ưu điểm triển khai gọn nhẹ của kiến trúc phân tầng với tính tách biệt kiểm thử (Isolateability) mạnh mẽ của Clean Architecture. "
        "Toàn bộ logic nghiệp vụ tiếp nhận, thẩm định bảo hành, phân công kỹ thuật, điều phối linh kiện và cảnh báo SLA được đóng gói nguyên vẹn trong tầng Domain Service, "
        "hoàn toàn miễn nhiễm trước sự thay đổi của công nghệ lưu trữ hay giao diện người dùng."
    )

    # 4.3. Kiến trúc tổng thể của hệ thống
    add_heading_1(doc, "4.3. Kiến trúc tổng thể của hệ thống")
    
    add_body_p(
        doc,
        "Hệ thống quản lý bảo hành Hưng Thiện được thiết kế theo mô hình tổng thể gồm ba góc nhìn: Mô hình phân tầng logic (Logical Tiered View), "
        "Mô hình triển khai hạ tầng vật lý (Physical Deployment View) và Ranh giới bảo mật phân quyền (RBAC Security Boundary)."
    )

    add_heading_2(doc, "4.3.1. Mô hình phân tầng logic của hệ thống")
    add_body_p(
        doc,
        "Về mặt logic, hệ thống được cấu trúc thành 5 tầng rõ ràng, đảm bảo nguyên tắc phân tách trách nhiệm (Separation of Concerns - SoC):"
    )

    add_diagram_box(doc, [
        "+-----------------------------------------------------------------------------------+",
        "|                             1. PRESENTATION LAYER (UI)                            |",
        "|  - Admin Dashboard (Desktop)       - Technician Mobile Web    - Customer Tracking |",
        "+-----------------------------------------+-----------------------------------------+",
        "                                          | HTTPS / REST API / JSON",
        "+-----------------------------------------v-----------------------------------------+",
        "|                         2. APPLICATION & API ROUTING LAYER                         |",
        "|  - Reverse Proxy (Nginx)           - Auth Middleware (JWT)    - Rate Limiter       |",
        "|  - Input Validation (Pydantic v2)  - Exception Handlers       - Audit Logging      |",
        "+-----------------------------------------+-----------------------------------------+",
        "                                          | Inversion of Control / DI",
        "+-----------------------------------------v-----------------------------------------+",
        "|                        3. CORE DOMAIN SERVICES LAYER (BUS)                         |",
        "|  - TicketService (BR01, BR02)      - WarrantyService (BR03)   - RepairService     |",
        "|  - InventoryService (BR06)         - SlaEngineService (BR08)  - PortalService     |",
        "+-----------------------------------------+-----------------------------------------+",
        "                                          | Domain Contracts / Ports",
        "+-----------------------------------------v-----------------------------------------+",
        "|                     4. INFRASTRUCTURE & DATA PERSISTENCE LAYER                    |",
        "|  - Relational Repositories (PostgreSQL 16)      - Redis Cache (Dashboard Metrics) |",
        "|  - File Attachment Storage (Customer Signature) - Transaction Manager (ACID)      |",
        "+-----------------------------------------+-----------------------------------------+",
        "                                          | Interfaces",
        "+-----------------------------------------v-----------------------------------------+",
        "|                      5. EXTERNAL ADAPTERS & TESTABILITY LAYER                     |",
        "|  - SystemClockAdapter (Real)  <-->  SimulatedClockAdapter (TB.02 Mock Clock)       |",
        "|  - SmtpEmailAdapter (Real)    <-->  MockEmailAdapter (TB.05 Buffer Inspector)     |",
        "+-----------------------------------------------------------------------------------+"
    ])
    add_figure_caption(doc, "Hình 4.1: Sơ đồ khối kiến trúc phân tầng logic Clean Layered Architecture")

    add_body_p(
        doc,
        "Đặc điểm nổi bật của mô hình này nằm ở tầng External Adapters & Testability Layer. Khi chạy trên môi trường thực tế, hệ thống kết nối với "
        "đồng hồ thời gian thực và máy chủ SMTP. Nhưng khi chạy trong môi trường kiểm thử tự động (Pytest), kiến trúc cho phép tiêm (inject) đối tượng "
        "SimulatedClockService để tự do dịch chuyển ngày giờ hệ thống kiểm thử cảnh báo 08:00 (FR_SLA_03) và MockEmailService để kiểm chứng nội dung "
        "thư gửi đi mà không cần phát tán email thật ra internet, đáp ứng trọn vẹn yêu cầu TB.02 và TB.05."
    )

    add_heading_2(doc, "4.3.2. Mô hình triển khai hạ tầng vật lý (Physical Deployment View)")
    add_body_p(
        doc,
        "Toàn bộ giải pháp được đóng gói theo kiến trúc Container hóa với Docker Compose, bảo đảm tính độc lập môi trường, khả năng tái hiện lỗi 100% "
        "và dễ dàng thiết lập môi trường kiểm thử sạch chỉ bằng một câu lệnh duy nhất (thỏa mãn NFR_TEST_01 và tiêu chí kiểm tra TB.08)."
    )

    add_diagram_box(doc, [
        "+-----------------------------------------------------------------------------------+",
        "|                             CLIENT DEVICES / BROWSERS                             |",
        "|      [Admin Desktop PC]          [Technician Smartphone]      [Customer Browser]  |",
        "+-----------------------------------------+-----------------------------------------+",
        "                                          | Port 80/443 (HTTPS / TLS 1.3)",
        "+-----------------------------------------v-----------------------------------------+",
        "|                                DOCKER HOST ENGINE                                 |",
        "|  +-----------------------------------------------------------------------------+  |",
        "|  | Container 1: frontend-server (Nginx 1.25)                                   |  |",
        "|  |   - Serves React/Next.js Client Application                                 |  |",
        "|  |   - SSL Termination, Reverse Proxy to Backend API                           |  |",
        "|  +--------------------------------------+--------------------------------------+  |",
        "|                                         | Internal Network (Port 8000)            |",
        "|  +--------------------------------------v--------------------------------------+  |",
        "|  | Container 2: backend-api-service (Python 3.12 / FastAPI Async)              |  |",
        "|  |   - Uvicorn Workers with High Concurrency Async Event Loop                  |  |",
        "|  |   - Business Services, State Machine Engine, Clean Architecture Core        |  |",
        "|  +-------------------+------------------+-------------------+------------------+  |",
        "|                      |                  |                   |                     |",
        "|  +-------------------v---+  +-----------v--------+  +-------v------------------+  |",
        "|  | Container 3:          |  | Container 4:       |  | Container 5:             |  |",
        "|  | db-postgres (16.2)    |  | cache-redis (7.2)  |  | mock-mailpit (SMTP test) |  |",
        "|  | Port 5432 (Internal)  |  | Port 6379 Internal |  | Web UI Port 8025         |  |",
        "|  | Data Volume Persistent|  | Fast Dashboard KPI |  | Mock SMTP Port 1025      |  |",
        "|  +-----------------------+  +--------------------+  +--------------------------+  |",
        "+-----------------------------------------------------------------------------------+"
    ])
    add_figure_caption(doc, "Hình 4.2: Sơ đồ triển khai hạ tầng Container hóa với Docker Compose")

    add_heading_2(doc, "4.3.3. Ranh giới bảo mật và ma trận kiểm soát truy cập (RBAC Matrix)")
    add_body_p(
        doc,
        "Để đáp ứng NFR_SEC_01 (100% yêu cầu trái quyền bị từ chối ở tầng xử lý server) và bảo đảm tính toàn vẹn dữ liệu giữa các phân hệ, "
        "hệ thống thiết lập cơ chế kiểm soát truy cập dựa trên vai trò (Role-Based Access Control - RBAC). Bảng 4.2 mô tả ma trận phân quyền "
        "giữa 3 tác nhân chính (Admin, Kỹ thuật viên, Khách hàng) trên 8 phân hệ cốt lõi:"
    )

    add_table_caption(doc, "Bảng 4.2: Ma trận phân quyền kiểm soát truy cập hệ thống (RBAC)")
    table_rbac = doc.add_table(rows=9, cols=5)
    table_rbac.alignment = WD_TABLE_ALIGNMENT.CENTER
    rbac_headers = ["Mã phân hệ", "Tên chức năng nghiệp vụ", "Admin", "Kỹ thuật viên", "Khách hàng"]
    for i, h in enumerate(rbac_headers):
        cell = table_rbac.cell(0, i)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(11)
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_row(table_rbac.rows[0], is_header=True)

    rbac_data = [
        ["AUTH", "Quản lý tài khoản, phân quyền, đăng nhập", "Toàn quyền (CRUD)", "Đăng nhập cá nhân", "Không truy cập"],
        ["TKT", "Lập phiếu, xác nhận chữ ký, đóng/trả phiếu", "Toàn quyền thực thi", "Chỉ xem phiếu phụ trách", "Không truy cập"],
        ["WAR", "Thẩm định điều kiện bảo hành, duyệt đổi máy", "Toàn quyền thực thi", "Chỉ đọc kết quả", "Không truy cập"],
        ["REP", "Phân công, điều chuyển, ghi nhật ký sửa chữa", "Phân công / Bàn giao", "Cập nhật phiếu mình phụ trách", "Không truy cập"],
        ["INV", "Quản lý kho linh kiện, nhập/xuất kho", "Toàn quyền quản lý", "Ghi linh kiện thực tế dùng", "Không truy cập"],
        ["SLA", "Giám sát hạn trả, cấu hình điểm tin 08:00", "Xem cảnh báo, nhận mail", "Xem hạn trả phiếu mình", "Không truy cập"],
        ["PORTAL", "Tra cứu công khai tiến độ và lịch hẹn", "Không cần dùng cổng này", "Không cần dùng cổng này", "Xác thực (Mã + Bí mật)"],
        ["DASH", "Thống kê chỉ số, bộ lọc, xuất Excel/PDF", "Toàn quyền thống kê", "Không có quyền truy cập", "Không truy cập"]
    ]
    for row_idx, r in enumerate(rbac_data, start=1):
        for col_idx, val in enumerate(r):
            cell = table_rbac.cell(row_idx, col_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 2, 3, 4] else WD_ALIGN_PARAGRAPH.LEFT
        format_row(table_rbac.rows[row_idx], is_header=False)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 4.4. Lựa chọn công nghệ phát triển
    add_heading_1(doc, "4.4. Lựa chọn công nghệ phát triển cho hệ thống")
    add_body_p(
        doc,
        "Việc lựa chọn Tech Stack phát triển được cân nhắc dựa trên các tiêu chí: Hiệu năng xử lý bất đồng bộ, tính an toàn kiểu dữ liệu, "
        "hỗ trợ mạnh mẽ cho đặc tính Kiểm thử được (Testability), khả năng mở rộng và sự phổ biến trong ngành công nghiệp phần mềm hiện đại:"
    )

    add_body_p(
        doc,
        "Python 3.12 kết hợp với framework hiện đại FastAPI được chọn làm công nghệ chủ đạo cho tầng backend. Khác với Django truyền thống cồng kềnh, "
        "FastAPI hoạt động trên chuẩn ASGI (Asynchronous Server Gateway Interface) với bộ máy uvloop, mang lại tốc độ xử lý I/O tương đương Node.js và Go. "
        "FastAPI tích hợp sẵn cơ chế kiểm thực dữ liệu nghiêm ngặt qua thư viện Pydantic v2, tự động phát hiện sai lệch tham số trước khi đi vào tầng logic nghiệp vụ. "
        "Đặc biệt, hệ thống Tiêm phụ thuộc (Dependency Injection) của FastAPI là công cụ đắc lực nhất để hiện thực hóa việc tráo đổi các Adapter phục vụ kiểm thử (TB.02, TB.05).",
        bold_prefix="1. Tầng dịch vụ nghiệp vụ Backend (Python 3.12 + FastAPI + Pydantic v2): "
    )

    add_body_p(
        doc,
        "SQLAlchemy 2.0 theo phong cách ánh xạ khai báo hiện đại (Declarative 2.0 Style) kết hợp với công cụ quản lý di chuyển lược đồ Alembic. "
        "Mô hình này giúp nhóm duy trì tính độc lập hoàn toàn giữa mã nguồn Python và hệ quản trị cơ sở dữ liệu, hỗ trợ giao dịch ACID chặt chẽ "
        "và ngăn ngừa triệt để lỗi SQL Injection.",
        bold_prefix="2. Tầng truy xuất dữ liệu ORM (SQLAlchemy 2.0 Async + Alembic): "
    )

    add_body_p(
        doc,
        "Hệ quản trị CSDL quan hệ mã nguồn mở mạnh mẽ nhất thế giới PostgreSQL phiên bản 16.2 được chọn làm kho lưu trữ chính. PostgreSQL vượt trội ở khả năng "
        "bảo đảm toàn vẹn khóa ngoại (Foreign Keys), hỗ trợ các kiểu dữ liệu nâng cao như JSONB (lưu trữ danh sách linh kiện đã ký của khách hàng một cách linh hoạt), "
        "và các thuật toán lập chỉ mục (B-Tree, Hash, GiST) giúp câu lệnh tổng hợp Dashboard trên 5.000 phiếu phản hồi dưới 0.1 giây (đáp ứng xuất sắc NFR_PERF_02).",
        bold_prefix="3. Hệ quản trị cơ sở dữ liệu quan hệ (PostgreSQL 16.2): "
    )

    add_body_p(
        doc,
        "React kết hợp kiến trúc Next.js và thư viện giao diện Tailwind CSS cùng Ant Design. Kiến trúc này mang lại trải nghiệm ứng dụng trang đơn (SPA) mượt mà, "
        "tối ưu hóa giao diện co giãn linh hoạt (Responsive Layout) trên màn hình máy tính để bàn (1920x1080) lẫn điện thoại kỹ thuật viên (375x812) theo NFR_COMP_01.",
        bold_prefix="4. Giao diện người dùng Web Frontend (Next.js / React + Tailwind CSS): "
    )

    add_body_p(
        doc,
        "Bộ công cụ kiểm thử Pytest 9.2 được sử dụng làm nền tảng kiểm thử tự động. Nhóm xây dựng kịch bản kiểm thử bao phủ toàn bộ 10 quy tắc nghiệp vụ BR01-BR10 "
        "với thời gian thực thi cực nhanh (dưới 0.1 giây cho toàn bộ test suite), kết hợp Docker Compose để kiểm thử môi trường cô lập.",
        bold_prefix="5. Công cụ kiểm thử tự động (Pytest + Pytest-Asyncio + Docker): "
    )

    # 4.5. Kiến trúc phần mềm của hệ thống
    add_heading_1(doc, "4.5. Kiến trúc phần mềm của hệ thống")
    add_body_p(
        doc,
        "Kiến trúc phần mềm bên trong được phân rã thành 8 phân hệ nghiệp vụ độc lập, tương ứng với cấu trúc phân rã yêu cầu tại Chương 2 và Chương 3:"
    )

    modules_desc = [
        ("Phân hệ Quản lý truy cập và người dùng (AUTH): ", "Chịu trách nhiệm xác thực tài khoản, cấp phát mã phiên JWT an toàn, quản lý vòng đời tài khoản Admin và Kỹ thuật viên (FR_AUTH_01, FR_AUTH_02) và bảo đảm kiểm tra quyền hạn chặt chẽ trên từng API endpoint (FR_AUTH_03)."),
        ("Phân hệ Tiếp nhận phiếu bảo hành (TKT): ", "Thực thi quy trình lập phiếu theo cấu trúc mã TKT_YYYYMMDD_x (BR01, FR_TKT_02), phân loại hình thức lấy ngay hoặc giữ máy 3-7 ngày, thẩm tra bắt buộc danh mục linh kiện có chữ ký (BR02, FR_TKT_01), lưu vết lịch sử trạng thái (FR_TKT_04), nghiệm thu linh kiện chữ ký và test máy trước khi đóng phiếu sang Đã trả (BR09, FR_TKT_05)."),
        ("Phân hệ Thẩm định chính sách bảo hành (WAR): ", "Đối chiếu căn cứ ngày mua, thời điểm phát sinh lỗi, xác định nguyên nhân lỗi do nhà sản xuất hay người dùng. Phân loại chuẩn xác 3 phương án: Đổi 1-1 trong 2-3 ngày, Sửa chữa miễn phí hoặc Sửa chữa có phí có xác nhận của khách hàng (BR03, FR_WAR_01, FR_WAR_02)."),
        ("Phân hệ Điều phối và sửa chữa (REP): ", "Phân công kỹ thuật viên phụ trách duy nhất (BR04, FR_REP_01), kiểm soát cỗ máy trạng thái sửa chữa kỹ thuật theo Hình 3.7 (BR09, FR_REP_03), ghi nhận nhật ký chẩn đoán và thao tác kỹ thuật (BR05, FR_REP_04), và hiện thực hóa quy trình bàn giao điều chuyển công việc hỗ trợ trường hợp KTV cũ vắng mặt (BR07, FR_REP_05, FR_REP_06)."),
        ("Phân hệ Quản lý kho linh kiện (INV): ", "Quản lý mã, tên, tồn kho và ngưỡng an toàn (FR_INV_01, FR_INV_05), ghi nhận nhập kho tăng tồn (FR_INV_02), xuất cấp phát linh kiện cho phiếu chưa kết thúc (BR06, FR_INV_03), ghi nhận số lượng thực tế sử dụng gắn với nhật ký mà không giảm tồn lần hai (BR06, FR_REP_07)."),
        ("Phân hệ Kiểm soát hạn trả và cảnh báo SLA (SLA): ", "Theo dõi hạn hẹn trả cụ thể của từng phiếu (FR_SLA_01), thuật toán tự động phân nhóm tại thời điểm 08:00 sáng chia thành Nhóm 1 (Báo động đỏ: hẹn hôm nay, quá hạn, chờ linh kiện) và Nhóm 2 (Cần lưu ý: hẹn ngày mai) theo BR08 (FR_SLA_02), và gửi email điểm tin tổng hợp tự động cho ban quản lý (FR_SLA_03)."),
        ("Phân hệ Cổng tra cứu trực tuyến (PORTAL): ", "Cung cấp giao diện tra cứu dành riêng cho khách hàng với cơ chế xác minh kép gồm Mã phiếu và Mã tra cứu bí mật được băm mật mã SHA-256 (BR10, FR_PORTAL_01), chỉ trả về thông tin tiến độ rút gọn và ẩn hoàn toàn nhật ký nội bộ và thông tin nhạy cảm (FR_PORTAL_02)."),
        ("Phân hệ Dashboard thống kê và báo cáo (DASH): ", "Tổng hợp trực quan các chỉ số KPI hoạt động theo thời gian thực (FR_DASH_01), cung cấp bộ lọc đa tiêu chí đồng thời (FR_DASH_02) và xuất tệp báo cáo Excel/PDF đối chiếu khớp 100% với số liệu gốc (FR_DASH_03), tách biệt hoàn toàn logic tính toán khỏi giao diện biểu đồ (TB.12).")
    ]
    for m_title, m_desc in modules_desc:
        add_body_p(doc, m_desc, bold_prefix=m_title)

    # 4.6. Thiết kế luồng dữ liệu bảo hành & CSDL mức vật lý
    add_heading_1(doc, "4.6. Thiết kế chi tiết luồng dữ liệu bảo hành và cơ sở dữ liệu mức vật lý")
    
    add_heading_2(doc, "4.6.1. Thiết kế luồng dữ liệu bảo hành (Warranty Data Flow Design)")
    add_body_p(
        doc,
        "Luồng dữ liệu bảo hành là trục xương sống kết nối toàn bộ hoạt động của trung tâm kỹ thuật từ khi khách hàng mang thiết bị đến, "
        "qua các khâu thẩm định, điều phối sửa chữa, xuất linh kiện kho cho đến khi kiểm tra kết quả và giao trả thiết bị. "
        "Dưới đây là các mô hình luồng dữ liệu (Data Flow Diagrams - DFD) từ cấp tổng quát đến cấp chi tiết:"
    )

    add_heading_3(doc, "a) Sơ đồ luồng dữ liệu ngữ cảnh (Context DFD - Cấp 0)")
    add_diagram_box(doc, [
        "                 +-------------------------------------------------------+",
        "                 |                     ADMINISTRATOR                     |",
        "                 +-----------------------+-------^-----------------------+",
        "             1. Thông tin tiếp nhận, ký LK|       | 6. Báo cáo SLA 08:00, Dashboard",
        "             2. Thẩm định BH, phân công  |       | 7. Cảnh báo tồn kho, DS bàn giao",
        "             3. Xác nhận nhập/xuất kho   |       |",
        "                                         v       |",
        "                               +-----------------+---------------+",
        "                               |                                 |",
        "   +-----------------------+   |              ( 0 )              |   +-----------------------+",
        "   |                       |   |                                 |   |                       |",
        "   |                       |-->|        HỆ THỐNG PHẦN MỀM        |-->|                       |",
        "   |      KHÁCH HÀNG       |   |        QUẢN LÝ BẢO HÀNH         |   |     KỸ THUẬT VIÊN     |",
        "   |                       |<--|        CÔNG TY HƯNG THIỆN       |<--|                       |",
        "   |                       |   |                                 |   |                       |",
        "   +-----------------------+   |                                 |   +-----------------------+",
        "    4. Tra cứu tiến độ (Mã+Pass)|                                 | 8. Xem DS phiếu được giao",
        "    5. Nhận kết quả tra cứu    +-----------------+---------------+ 9. Ghi nhật ký, đổi status",
        "       Biên bản giao trả máy                     ^                 10. Xác nhận bàn giao",
        "                                                 |                 11. Ghi linh kiện dùng",
        "                                                 v",
        "                                       [ KHO DỮ LIỆU TẬP TRUNG ]"
    ])
    add_figure_caption(doc, "Hình 4.3: Sơ đồ luồng dữ liệu ngữ cảnh (Context DFD Cấp 0)")

    add_heading_3(doc, "b) Sơ đồ luồng dữ liệu mức 1 (DFD Cấp 1)")
    add_body_p(
        doc,
        "Sơ đồ DFD cấp 1 phân rã toàn bộ hệ thống bảo hành thành 5 tiến trình nghiệp vụ cốt lõi, tương ứng với vòng đời di chuyển của dữ liệu:"
    )

    add_diagram_box(doc, [
        "  [Khách hàng] ---> ( 1.0 Tiếp nhận & Thẩm định BH ) ---> [ D1: Phiếu & Thiết bị ]",
        "                           | (BR01, BR02, BR03)                 |",
        "                           v                                    v",
        "  [Admin] --------> ( 2.0 Điều chuyển & Bàn giao KTV) <------- [ D2: Phân công & Bàn giao ]",
        "                           | (BR04, BR07)                       |",
        "                           v                                    v",
        "  [Kỹ thuật viên]-> ( 3.0 Cập nhật Sửa chữa & Kho LK) <------> [ D3: Nhật ký & Kho LK ]",
        "                           | (BR05, BR06)                       |",
        "                           v                                    v",
        "  [Admin / KTV] --> ( 4.0 Nghiệm thu Test & Trả máy ) -------> [ D4: Lịch sử Giao nhận ]",
        "                           | (BR09)                             |",
        "                           v                                    v",
        "  [Admin / Batch]-> ( 5.0 Giám sát Hạn & Thống kê SLA) ------> [ D5: SlaLogs & Dashboard ]",
        "                           (BR08, BR10)"
    ])
    add_figure_caption(doc, "Hình 4.4: Sơ đồ luồng dữ liệu DFD Cấp 1 phân rã tiến trình hệ thống")

    add_heading_3(doc, "c) Đặc tả chi tiết các luồng dữ liệu DFD Cấp 2")
    
    add_body_p(
        doc,
        "Dữ liệu đầu vào gồm: Khách hàng (Họ tên, SĐT), Thiết bị (Loại máy, Serial, Hiện trạng, Phụ kiện), "
        "Hình thức nhận (Lấy ngay hoặc Giữ máy 3-7 ngày), Ngày hẹn trả cụ thể và Danh sách linh kiện khách đã ký đối chiếu. "
        "Hệ thống tự động sinh mã phiếu định dạng TKT_YYYYMMDD_x theo BR01 và sinh mã tra cứu bí mật cho khách. Sau đó, tiến trình thẩm định "
        "chính sách bảo hành kiểm tra ngày mua và nguyên nhân lỗi để đưa ra 1 trong 3 phương án (Đổi 1-1, Sửa miễn phí, Sửa có phí có khách đồng ý). "
        "Dữ liệu được ghi đồng thời vào kho dữ liệu D1 (Tickets) và phát sinh bản ghi lịch sử đầu tiên trạng thái Đã tiếp nhận.",
        bold_prefix="Luồng 1 - Tiếp nhận và Thẩm định bảo hành (TKT & WAR): "
    )

    add_body_p(
        doc,
        "Admin khởi tạo phân công KTV cho phiếu Chờ phân công. Khi phát sinh nhu cầu chuyển giao giữa hai kỹ thuật viên, Admin khởi tạo phiên bàn giao (BR07). "
        "Dữ liệu phiên bàn giao bao gồm: Mã phiên (HO_xxx), KTV cũ, KTV mới, Lý do điều chuyển, cờ KTV cũ vắng mặt và ghi chú tài liệu còn thiếu. "
        "KTV mới đăng nhập kiểm tra hồ sơ và quyết định Chấp thuận (hệ thống cập nhật KTV phụ trách mới nhất) hoặc Từ chối (bắt buộc nhập lý do từ chối). "
        "Toàn bộ tiến trình không làm gián đoạn trạng thái kỹ thuật của phiếu.",
        bold_prefix="Luồng 2 - Điều phối và Bàn giao công việc (REP): "
    )

    add_body_p(
        doc,
        "Chỉ có kỹ thuật viên phụ trách hiện hành mới được quyền gửi dữ liệu cập nhật sửa chữa (BR04). Mỗi lần chuyển trạng thái kỹ thuật phải kèm dữ liệu "
        "Nhật ký công việc gồm: Kết quả chẩn đoán, Thao tác đã làm, Công việc còn tồn (BR05). Khi cần linh kiện, Admin xuất linh kiện từ kho (trừ tồn kho ngay lúc xuất theo BR06); "
        "Kỹ thuật viên sau đó ghi nhận lượng thực tế dùng gắn với nhật ký (chỉ kiểm tra không vượt lượng đã cấp, tuyệt đối không giảm tồn lần hai).",
        bold_prefix="Luồng 3 - Sửa chữa kỹ thuật và Cấp phát linh kiện kho (REP & INV): "
    )

    add_body_p(
        doc,
        "Khi máy sửa xong chuyển sang Chờ kiểm tra kết quả, KTV chạy kiểm thử kỹ thuật. Nếu đạt chuyển Chờ trả; nếu chưa đạt quay về Đang sửa chữa kèm lỗi còn tồn. "
        "Tại quầy bàn giao (Chờ trả), khách hàng trực tiếp đối chiếu chữ ký trên các linh kiện đã ký ban đầu, kiểm tra tem mác và chạy thử chức năng. "
        "Chỉ khi khách hàng ký xác nhận hài lòng và linh kiện khớp 100%, Admin mới xác nhận đóng phiếu sang Đã trả (BR09). Nếu phát hiện sai lệch hoặc test lỗi, "
        "hệ thống chuyển ngược phiếu về Chờ kiểm tra kết quả và ghi rõ sai lệch.",
        bold_prefix="Luồng 4 - Kiểm tra kết quả, Đối chiếu chữ ký và Giao trả máy (REP & TKT): "
    )

    add_body_p(
        doc,
        "Bộ lập lịch kích hoạt lúc 08:00 sáng hàng ngày quét toàn bộ các phiếu chưa hoàn tất. Dữ liệu được phân thành hai tập hợp không giao nhau (BR08): "
        "Nhóm 1 (Báo động đỏ): Gồm các phiếu hẹn trả hôm nay, các phiếu đã quá hạn, và các phiếu đang ở trạng thái Chờ linh kiện. "
        "Nhóm 2 (Cần lưu ý): Gồm các phiếu hẹn trả ngày mai (loại trừ các phiếu đã rơi vào Nhóm 1). "
        "Dữ liệu tổng hợp được định dạng thành báo cáo điểm tin gửi qua email quản trị mà không làm thay đổi trạng thái của phiếu.",
        bold_prefix="Luồng 5 - Cảnh báo hạn trả và Điểm tin SLA 08:00 (SLA): "
    )

    add_body_p(
        doc,
        "Khách hàng nhập Mã phiếu và Mã tra cứu bí mật qua cổng Web Portal. Hệ thống băm mã bí mật bằng SHA-256 đối chiếu với cơ sở dữ liệu (BR10, NFR_SEC_02). "
        "Nếu khớp, hệ thống lọc và chỉ trả về các trường dữ liệu an toàn: Mã phiếu, Tên dòng máy, Serial đã ẩn ký tự (ví dụ: SN****00), Tiến độ xử lý và Ngày hẹn trả. "
        "Các trường nhạy cảm như nhật ký nội bộ của KTV, giá tiền linh kiện hay số điện thoại liên lạc đều được lược bỏ hoàn toàn ở tầng backend.",
        bold_prefix="Luồng 6 - Tra cứu tiến độ công khai cho khách hàng (PORTAL): "
    )

    add_heading_3(doc, "d) Biểu đồ máy trạng thái (State Machine Diagram) và Quy tắc chuyển trạng thái")
    add_body_p(
        doc,
        "Căn cứ trên Hình 3.7 và Bảng 3.16 của Chương 3, vòng đời dữ liệu của phiếu bảo hành tuân thủ nghiêm ngặt cỗ máy trạng thái hữu hạn (Finite State Machine). "
        "Bảng 4.3 đối chiếu chi tiết ma trận chuyển trạng thái hợp lệ và các điều kiện ràng buộc bảo vệ (Guards) đã được lập trình và kiểm thử trong module RepairService:"
    )

    add_table_caption(doc, "Bảng 4.3: Ma trận chuyển trạng thái hợp lệ của phiếu bảo hành (State Transitions)")
    table_fsm = doc.add_table(rows=11, cols=4)
    table_fsm.alignment = WD_TABLE_ALIGNMENT.CENTER
    fsm_headers = ["Trạng thái hiện tại", "Trạng thái tiếp theo", "Tác nhân", "Điều kiện ràng buộc bảo vệ (Guard Condition)"]
    for i, h in enumerate(fsm_headers):
        cell = table_fsm.cell(0, i)
        cell.paragraphs[0].text = h
        cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
        cell.paragraphs[0].runs[0].font.size = Pt(11)
        cell.paragraphs[0].runs[0].font.bold = True
        cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
    format_row(table_fsm.rows[0], is_header=True)

    fsm_data = [
        ["Đã tiếp nhận (RECEIVED)", "Chờ phân công (PENDING_ASSIGNMENT)", "Admin", "Đã đánh giá chính sách BH; nếu sửa có phí phải có khách đồng ý (BR03)"],
        ["Đã tiếp nhận / Chờ phân công", "Đã hủy (CANCELLED)", "Admin", "Chỉ hủy trước khi bắt đầu sửa; phải ghi lý do và biên bản trả lại thiết bị (BR09)"],
        ["Chờ phân công (PENDING_ASSIGNMENT)", "Đang kiểm tra (UNDER_INSPECTION)", "Admin", "Phân công thành công một KTV có tài khoản đang hoạt động (FR_REP_01)"],
        ["Đang kiểm tra (UNDER_INSPECTION)", "Đang sửa chữa (UNDER_REPAIR)", "KTV phụ trách", "Ghi kết quả chẩn đoán ban đầu và phương án xử lý kèm nhật ký (BR05)"],
        ["Đang kiểm tra (UNDER_INSPECTION)", "Chờ kiểm tra kết quả (WAITING_FOR_RESULT_CHECK)", "Admin / KTV", "Dành cho trường hợp đổi 1-1 đã duyệt: ghi serial máy mới và kiểm tra máy đổi"],
        ["Đang sửa chữa (UNDER_REPAIR)", "Chờ linh kiện (WAITING_FOR_PARTS)", "KTV phụ trách", "Bắt buộc ghi lý do thiếu linh kiện và danh mục linh kiện cần cấp"],
        ["Chờ linh kiện (WAITING_FOR_PARTS)", "Đang sửa chữa (UNDER_REPAIR)", "KTV phụ trách", "Admin đã xuất cấp đủ linh kiện hoặc duyệt phương án thay thế"],
        ["Đang sửa chữa (UNDER_REPAIR)", "Chờ kiểm tra kết quả (WAITING_FOR_RESULT_CHECK)", "KTV phụ trách", "Ghi nhận toàn bộ thao tác đã hoàn tất, đề nghị nghiệm thu kỹ thuật"],
        ["Chờ kiểm tra kết quả (WAITING_FOR_RESULT_CHECK)", "Chờ trả (WAITING_FOR_RETURN)", "Admin / KTV", "Kiểm tra kỹ thuật đạt 100% các bài test chạy thử chức năng"],
        ["Chờ trả (WAITING_FOR_RETURN)", "Đã trả (RETURNED)", "Admin", "Khách hàng kiểm tra chữ ký linh kiện, tem mác, test máy đạt và ký nhận (BR09)"]
    ]
    for row_idx, r in enumerate(fsm_data, start=1):
        for col_idx, val in enumerate(r):
            cell = table_fsm.cell(row_idx, col_idx)
            cell.paragraphs[0].text = val
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER if col_idx in [0, 1, 2] else WD_ALIGN_PARAGRAPH.LEFT
        format_row(table_fsm.rows[row_idx], is_header=False)

    doc.add_paragraph().paragraph_format.space_after = Pt(4)

    add_heading_2(doc, "4.6.2. Thiết kế Cơ sở dữ liệu mức vật lý (Physical Database Schema)")
    add_body_p(
        doc,
        "Cơ sở dữ liệu vật lý được thiết kế đạt chuẩn chuẩn hóa 3NF (Third Normal Form) nhằm loại bỏ hoàn toàn các dị thường thêm, xóa, sửa, "
        "đồng thời thiết lập các ràng buộc toàn vẹn khóa ngoại (Foreign Key Constraints) và chỉ mục chuyên dụng (B-Tree Indexes). "
        "Lược đồ cơ sở dữ liệu gồm 10 bảng thực thể chính:"
    )

    db_tables_spec = [
        ("1. Bảng users (Tài khoản người dùng nội bộ)", [
            ("user_id", "VARCHAR(36)", "PRIMARY KEY", "Định danh duy nhất UUID của tài khoản"),
            ("username", "VARCHAR(50)", "NOT NULL, UNIQUE", "Tên đăng nhập hệ thống nội bộ"),
            ("password_hash", "VARCHAR(255)", "NOT NULL", "Mật khẩu băm an toàn theo bcrypt/Argon2"),
            ("full_name", "VARCHAR(100)", "NOT NULL", "Họ và tên đầy đủ của nhân sự"),
            ("role", "VARCHAR(20)", "NOT NULL", "Vai trò RBAC: 'ADMIN' hoặc 'TECHNICIAN'"),
            ("is_active", "BOOLEAN", "NOT NULL DEFAULT TRUE", "Trạng thái hoạt động tài khoản (cho phép khóa)"),
            ("created_at", "TIMESTAMP WITH TIME ZONE", "NOT NULL", "Thời điểm tạo tài khoản")
        ]),
        ("2. Bảng customers (Hồ sơ khách hàng)", [
            ("customer_id", "VARCHAR(36)", "PRIMARY KEY", "Định danh khách hàng UUID"),
            ("full_name", "VARCHAR(100)", "NOT NULL", "Họ tên khách hàng mang máy đến bảo hành"),
            ("phone_number", "VARCHAR(20)", "NOT NULL, INDEX", "Số điện thoại liên hệ (có lập chỉ mục tìm kiếm)"),
            ("email", "VARCHAR(100)", "NULL", "Địa chỉ email khách hàng nếu có"),
            ("address", "VARCHAR(255)", "NULL", "Địa chỉ liên hệ nhận trả thiết bị")
        ]),
        ("3. Bảng devices (Hồ sơ thiết bị phần cứng)", [
            ("device_id", "VARCHAR(36)", "PRIMARY KEY", "Mã thiết bị nội bộ UUID"),
            ("serial_number", "VARCHAR(100)", "NOT NULL, UNIQUE, INDEX", "Số Serial Number / IMEI định danh phần cứng"),
            ("model_name", "VARCHAR(100)", "NOT NULL, INDEX", "Tên dòng máy (Dell XPS 15, Asus ROG, HP...)"),
            ("brand", "VARCHAR(50)", "NOT NULL", "Nhãn hiệu nhà sản xuất thiết bị"),
            ("purchase_date", "DATE", "NULL", "Ngày khách hàng mua thiết bị")
        ]),
        ("4. Bảng warranty_tickets (Phiếu tiếp nhận bảo hành trung tâm)", [
            ("ticket_id", "VARCHAR(30)", "PRIMARY KEY", "Mã phiếu định dạng chuẩn TKT_YYYYMMDD_x (BR01)"),
            ("customer_id", "VARCHAR(36)", "NOT NULL, FK(customers)", "Liên kết khách hàng tiếp nhận"),
            ("device_id", "VARCHAR(36)", "NOT NULL, FK(devices)", "Liên kết thiết bị tiếp nhận"),
            ("intake_type", "VARCHAR(20)", "NOT NULL", "Hình thức: 'SAME_DAY' hoặc 'HOLD_FOR_REPAIR'"),
            ("promised_return_date", "DATE", "NOT NULL, INDEX", "Ngày hẹn trả khách hàng cụ thể (BR02, BR08)"),
            ("reported_issue", "TEXT", "NOT NULL", "Mô tả sự cố khách hàng khai báo"),
            ("initial_condition", "TEXT", "NOT NULL", "Hiện trạng ngoại quan máy khi tiếp nhận"),
            ("accessories_included", "VARCHAR(255)", "NOT NULL", "Danh mục phụ kiện kèm theo (sạc, túi...)"),
            ("status", "VARCHAR(30)", "NOT NULL, INDEX", "Trạng thái vòng đời FSM hiện hành (1 trong 9 trạng thái)"),
            ("tracking_code_hash", "VARCHAR(64)", "NOT NULL", "Mã SHA-256 của mã tra cứu bí mật cho khách (BR10)"),
            ("current_technician_id", "VARCHAR(36)", "NULL, FK(users), INDEX", "KTV phụ trách duy nhất hiện thời (BR04)"),
            ("signed_parts_json", "JSONB", "NOT NULL DEFAULT '[]'", "Danh mục linh kiện khách ký đối chiếu khi giữ máy"),
            ("customer_signature_confirmed", "BOOLEAN", "NOT NULL DEFAULT FALSE", "Xác nhận chữ ký giao nhận thiết bị giữ máy"),
            ("final_return_confirmed", "BOOLEAN", "NOT NULL DEFAULT FALSE", "Xác nhận đối chiếu chữ ký, test đạt khi giao trả"),
            ("cancellation_reason", "TEXT", "NULL", "Lý do hủy phiếu nếu hủy trước sửa (BR09)"),
            ("created_at", "TIMESTAMP WITH TIME ZONE", "NOT NULL, INDEX", "Thời điểm tạo lập phiếu tiếp nhận")
        ]),
        ("5. Bảng warranty_assessments (Kết quả thẩm định chính sách bảo hành)", [
            ("assessment_id", "VARCHAR(36)", "PRIMARY KEY", "Mã bản thẩm định WAR_xxxxxxxx"),
            ("ticket_id", "VARCHAR(30)", "NOT NULL, UNIQUE, FK(warranty_tickets)", "Liên kết 1-1 với phiếu bảo hành"),
            ("purchase_date", "DATE", "NOT NULL", "Ngày mua thiết bị theo chứng từ"),
            ("incident_date", "DATE", "NOT NULL", "Thời điểm phát sinh lỗi kỹ thuật"),
            ("is_warranty_valid", "BOOLEAN", "NOT NULL", "Xác định máy còn hạn bảo hành hay không"),
            ("defect_origin", "VARCHAR(20)", "NOT NULL", "Nguồn gốc lỗi: MANUFACTURER / USER_DAMAGE / UNCLEAR"),
            ("eligibility", "VARCHAR(30)", "NOT NULL", "Kết luận: ELIGIBLE / INELIGIBLE / INSUFFICIENT_INFO"),
            ("resolution", "VARCHAR(30)", "NOT NULL", "Phương án: ONE_TO_ONE_EXCHANGE / FREE_REPAIR / PAID_REPAIR"),
            ("customer_agreed", "BOOLEAN", "NOT NULL DEFAULT FALSE", "Khách hàng đồng ý phương án (bắt buộc với có phí)"),
            ("replacement_device_serial", "VARCHAR(100)", "NULL", "Serial máy đổi thay thế nếu là đổi 1-1 (BR01)"),
            ("created_at", "TIMESTAMP WITH TIME ZONE", "NOT NULL", "Thời điểm hoàn thành thẩm định")
        ]),
        ("6. Bảng ticket_status_history (Nhật ký lịch sử thay đổi trạng thái - Audit Trail)", [
            ("log_id", "VARCHAR(36)", "PRIMARY KEY", "Định danh bản ghi log UUID"),
            ("ticket_id", "VARCHAR(30)", "NOT NULL, FK(warranty_tickets), INDEX", "Phiếu bảo hành được ghi vết"),
            ("from_status", "VARCHAR(30)", "NULL", "Trạng thái trước khi chuyển đổi"),
            ("to_status", "VARCHAR(30)", "NOT NULL", "Trạng thái mới sau khi chuyển đổi"),
            ("changed_by_user_id", "VARCHAR(36)", "NOT NULL, FK(users)", "Tài khoản nhân sự thực hiện thao tác"),
            ("changed_at", "TIMESTAMP WITH TIME ZONE", "NOT NULL, INDEX", "Thời điểm chính xác xảy ra thay đổi"),
            ("reason", "TEXT", "NOT NULL", "Lý do giải trình chuyển trạng thái")
        ]),
        ("7. Bảng repair_work_logs (Nhật ký sửa chữa chi tiết của kỹ thuật viên)", [
            ("work_log_id", "VARCHAR(36)", "PRIMARY KEY", "Định danh bản ghi nhật ký kỹ thuật"),
            ("ticket_id", "VARCHAR(30)", "NOT NULL, FK(warranty_tickets), INDEX", "Phiếu bảo hành đang xử lý"),
            ("technician_id", "VARCHAR(36)", "NOT NULL, FK(users)", "Kỹ thuật viên thực tế thao tác ghi nhật ký (BR04)"),
            ("created_at", "TIMESTAMP WITH TIME ZONE", "NOT NULL", "Thời điểm ghi nhận thao tác"),
            ("diagnosis_findings", "TEXT", "NOT NULL", "Kết quả chẩn đoán kỹ thuật"),
            ("actions_performed", "TEXT", "NOT NULL", "Các thao tác kỹ thuật đã can thiệp"),
            ("pending_tasks", "TEXT", "NOT NULL", "Các hạng mục công việc còn tồn đọng cần bàn giao")
        ]),
        ("8. Bảng handover_sessions (Phiên bàn giao điều chuyển kỹ thuật viên)", [
            ("session_id", "VARCHAR(36)", "PRIMARY KEY", "Mã phiên bàn giao định dạng HO_xxxxxxxx (BR07)"),
            ("ticket_id", "VARCHAR(30)", "NOT NULL, FK(warranty_tickets), INDEX", "Phiếu bảo hành được bàn giao"),
            ("initiated_by_admin_id", "VARCHAR(36)", "NOT NULL, FK(users)", "Admin khởi tạo phiên bàn giao"),
            ("previous_technician_id", "VARCHAR(36)", "NOT NULL, FK(users)", "Kỹ thuật viên đang phụ trách cũ"),
            ("target_technician_id", "VARCHAR(36)", "NOT NULL, FK(users)", "Kỹ thuật viên được chỉ định tiếp nhận mới"),
            ("status", "VARCHAR(20)", "NOT NULL", "Trạng thái phiên: PENDING / ACCEPTED / REJECTED / CANCELLED"),
            ("is_previous_technician_absent", "BOOLEAN", "NOT NULL DEFAULT FALSE", "Cờ báo KTV cũ vắng mặt (BR07)"),
            ("missing_info_notes", "TEXT", "NULL", "Ghi chú các thông tin còn thiếu khi KTV vắng mặt"),
            ("rejection_reason", "TEXT", "NULL", "Lý do KTV mới từ chối tiếp nhận nếu có"),
            ("created_at", "TIMESTAMP WITH TIME ZONE", "NOT NULL", "Thời điểm khởi tạo phiên bàn giao"),
            ("decided_at", "TIMESTAMP WITH TIME ZONE", "NULL", "Thời điểm KTV mới chấp thuận hoặc từ chối")
        ]),
        ("9. Bảng spare_parts (Danh mục linh kiện trong kho)", [
            ("part_id", "VARCHAR(36)", "PRIMARY KEY", "Mã linh kiện nội bộ UUID"),
            ("part_code", "VARCHAR(50)", "NOT NULL, UNIQUE, INDEX", "Mã quản lý linh kiện định dạng PRT_xxx (FR_INV_01)"),
            ("part_name", "VARCHAR(150)", "NOT NULL", "Tên quy chuẩn của linh kiện (Màn hình, Pin, RAM...)"),
            ("unit", "VARCHAR(20)", "NOT NULL", "Đơn vị tính (Chiếc, Bộ, Thanh...)"),
            ("stock_quantity", "INTEGER", "NOT NULL DEFAULT 0", "Số lượng tồn kho thực tế hiện hành"),
            ("minimum_threshold", "INTEGER", "NOT NULL DEFAULT 0", "Ngưỡng tồn kho tối thiểu cảnh báo an toàn (FR_INV_05)")
        ]),
        ("10. Bảng part_allocations (Linh kiện cấp phát cho phiếu bảo hành)", [
            ("allocation_id", "VARCHAR(36)", "PRIMARY KEY", "Mã cấp phát định dạng ALC_xxxxxxxx"),
            ("ticket_id", "VARCHAR(30)", "NOT NULL, FK(warranty_tickets), INDEX", "Phiếu bảo hành được xuất cấp linh kiện"),
            ("part_id", "VARCHAR(36)", "NOT NULL, FK(spare_parts)", "Linh kiện được cấp phát"),
            ("allocated_quantity", "INTEGER", "NOT NULL", "Số lượng linh kiện Admin đã xuất kho cấp phát"),
            ("used_quantity", "INTEGER", "NOT NULL DEFAULT 0", "Số lượng KTV thực tế đã lắp ráp sử dụng (BR06)"),
            ("allocated_at", "TIMESTAMP WITH TIME ZONE", "NOT NULL", "Thời điểm xuất kho cấp phát")
        ])
    ]

    for table_title, cols in db_tables_spec:
        add_body_p(doc, f"Cấu trúc bảng {table_title}:")
        t_elem = doc.add_table(rows=len(cols)+1, cols=4)
        t_elem.alignment = WD_TABLE_ALIGNMENT.CENTER
        t_headers = ["Tên trường (Column)", "Kiểu dữ liệu (Data Type)", "Ràng buộc (Constraints)", "Mô tả ý nghĩa nghiệp vụ"]
        for i, h in enumerate(t_headers):
            cell = t_elem.cell(0, i)
            cell.paragraphs[0].text = h
            cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
            cell.paragraphs[0].runs[0].font.size = Pt(11)
            cell.paragraphs[0].runs[0].font.bold = True
            cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        format_row(t_elem.rows[0], is_header=True)

        for r_idx, col_tuple in enumerate(cols, start=1):
            for c_idx, text_val in enumerate(col_tuple):
                cell = t_elem.cell(r_idx, c_idx)
                cell.paragraphs[0].text = text_val
                cell.paragraphs[0].runs[0].font.name = 'Times New Roman'
                cell.paragraphs[0].runs[0].font.size = Pt(10)
                cell.paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.LEFT if c_idx == 3 else WD_ALIGN_PARAGRAPH.CENTER
            format_row(t_elem.rows[r_idx], is_header=False)
        doc.add_paragraph().paragraph_format.space_after = Pt(4)

    # 4.7. Quy tắc đặt tên (Naming Conventions)
    add_heading_1(doc, "4.7. Quy tắc đặt tên kỹ thuật toàn diện trong dự án (Naming Conventions)")
    add_body_p(
        doc,
        "Để đảm bảo tính nhất quán cao độ giữa tài liệu phân tích, tài liệu thiết kế, mã nguồn phần mềm và cơ sở dữ liệu, "
        "dự án thiết lập bộ quy chuẩn đặt tên chi tiết bắt buộc mọi thành viên phải tuân thủ nghiêm ngặt:"
    )

    add_body_p(
        doc,
        "Cấu trúc quy chuẩn: PSE.G102_[Increment]_[DocumentType]_[Description]_[Version].[ext]\n"
        "Ví dụ: PSE.G102_SAD_KienTrucHeThong_v1.0.docx; PSE.G102_INC1_TestReport_v1.0.pdf. "
        "Tất cả tài liệu chung không gắn với phân đợt cụ thể thì lược bỏ thành phần Increment.",
        bold_prefix="1. Quy tắc đặt tên tài liệu kỹ thuật: "
    )

    add_body_p(
        doc,
        "Mã định danh nghiệp vụ được chuẩn hóa nhằm tránh trùng lặp và phản ánh trực quan bản chất đối tượng:\n"
        "• Mã phiếu bảo hành (BR01): TKT_YYYYMMDD_x (Ví dụ: TKT_20261124_1).\n"
        "• Mã bản thẩm định bảo hành: WAR_XXXXXXXX (Ví dụ: WAR_A8B9C0D1).\n"
        "• Mã linh kiện kho: PRT_XXXXXX (Ví dụ: PRT_RAM16G, PRT_PINXPS).\n"
        "• Mã phiên bàn giao KTV (BR07): HO_XXXXXXXX (Ví dụ: HO_F1E2D3C4).\n"
        "• Mã cấp phát linh kiện: ALC_XXXXXXXX (Ví dụ: ALC_99887766).\n"
        "• Mã tài khoản người dùng: USR_VAI_TRÒ_xx (Ví dụ: USR_ADMIN_01, USR_TECH_01).",
        bold_prefix="2. Quy tắc đặt tên mã nghiệp vụ hệ thống: "
    )

    add_body_p(
        doc,
        "Tuân thủ nghiêm ngặt các quy tắc lập trình sạch (Clean Code Standards):\n"
        "• Tên lớp (Classes / Models / Interfaces): Sử dụng PascalCase (Ví dụ: WarrantyTicket, TicketService, InMemoryRepository).\n"
        "• Tên hàm / phương thức (Functions / Methods): Sử dụng snake_case trong Python (Ví dụ: create_ticket, evaluate_and_record_policy) "
        "hoặc camelCase trong JavaScript/TypeScript (Ví dụ: createTicket).\n"
        "• Tên biến và thuộc tính (Variables / Fields): Sử dụng snake_case (Ví dụ: promised_return_date, current_technician_id).\n"
        "• Hằng số (Constants / Enums): Sử dụng UPPER_SNAKE_CASE (Ví dụ: MAX_REPAIR_DAYS, WAITING_FOR_PARTS).\n"
        "• Tên tệp tin và gói mã nguồn (Files / Packages): Sử dụng toàn bộ chữ thường snake_case (Ví dụ: ticket_service.py, domain_models.py).",
        bold_prefix="3. Quy tắc đặt tên mã nguồn (Source Code): "
    )

    add_body_p(
        doc,
        "Quy ước chuẩn mực cho hệ quản trị PostgreSQL:\n"
        "• Tên bảng: Sử dụng danh từ số nhiều, chữ thường dạng snake_case (Ví dụ: users, warranty_tickets, spare_parts).\n"
        "• Tên khóa chính: Sử dụng cú pháp <tên_bảng_số_ít>_id (Ví dụ: ticket_id, customer_id, part_id).\n"
        "• Tên khóa ngoại: Giữ nguyên tên của khóa chính bảng đích được liên kết để dễ truy vết.\n"
        "• Tên chỉ mục (Index): idx_<table>_<column> (Ví dụ: idx_tickets_status, idx_devices_serial).\n"
        "• Tên ràng buộc duy nhất (Unique Constraint): uq_<table>_<column> (Ví dụ: uq_devices_serial_number).",
        bold_prefix="4. Quy tắc đặt tên cơ sở dữ liệu (Database Schema): "
    )

    add_body_p(
        doc,
        "Tuân thủ chuẩn RESTful API:\n"
        "• Tài nguyên: Sử dụng danh từ số nhiều ở dạng chữ thường (Ví dụ: /api/v1/tickets, /api/v1/spare-parts).\n"
        "• Phương thức HTTP: GET (Tra cứu, đọc), POST (Tạo mới), PUT (Cập nhật toàn phần), PATCH (Cập nhật từng phần), DELETE (Hủy/Xóa).\n"
        "• Truy vấn con: /api/v1/tickets/{ticket_id}/work-logs; /api/v1/tickets/{ticket_id}/handovers.",
        bold_prefix="5. Quy tắc đặt tên API Endpoints: "
    )

    add_body_p(
        doc,
        "Áp dụng chuẩn Conventional Commits cho hệ thống kiểm soát phiên bản Git:\n"
        "• Nhánh tính năng: feat/<tên-tính-năng>, fix/<mã-lỗi>, refactor/<mô-tả>.\n"
        "• Định dạng commit message: <loại>(<phân-hệ>): <mô-tả ngắn gọn> (Ví dụ: feat(tkt): implement hold for repair signed parts validation per BR02).\n"
        "• Nhãn phiên bản phát hành (Release Tags): INC1-v1.0, INC2-v1.0, INC3-v1.0.",
        bold_prefix="6. Quy tắc quản lý phiên bản Git và Commit: "
    )

    # 4.8. Một số thiết kế chi tiết theo kiến trúc được chọn
    add_heading_1(doc, "4.8. Một số thiết kế chi tiết theo kiến trúc được chọn")
    add_body_p(
        doc,
        "Để minh chứng tính khả thi và cung cấp đặc tả kỹ thuật chi tiết cho các lập trình viên ở Chương 5, nhóm tiến hành mô hình hóa "
        "chi tiết các biểu đồ tuần tự (Sequence Diagrams) cho 4 kịch bản nghiệp vụ phức tạp nhất:"
    )

    add_heading_2(doc, "4.8.1. Kịch bản 1: Tiếp nhận thiết bị giữ máy và kiểm tra ký linh kiện (UC03 - BR02)")
    add_diagram_box(doc, [
        "Admin                  TicketController             TicketService              Repository",
        "  |                           |                           |                         |",
        "  |-- 1. Nhập hồ sơ, LK ký -->|                           |                         |",
        "  |   (HOLD_FOR_REPAIR)       |-- 2. create_ticket() ---->|                         |",
        "  |                           |                           |-- 3. Kiểm tra LK ký --->| (BR02 Guard)",
        "  |                           |                           |      [Nếu rỗng: Báo lỗi]|",
        "  |                           |                           |-- 4. Sinh mã phiếu ---->| get_next_daily_seq()",
        "  |                           |                           |      TKT_YYYYMMDD_x     |",
        "  |                           |                           |-- 5. Băm SHA-256 code ->|",
        "  |                           |                           |-- 6. Lưu Ticket -------->| tickets[id] = ticket",
        "  |                           |                           |-- 7. Lưu Log Status --->| history.append(log)",
        "  |                           |<-- 8. Return Ticket ------|                         |",
        "  |<-- 9. In phiếu tiếp nhận -| (Trạng thái: RECEIVED)    |                         |"
    ])
    add_figure_caption(doc, "Hình 4.5: Biểu đồ tuần tự luồng tiếp nhận thiết bị giữ máy và ký linh kiện")

    add_heading_2(doc, "4.8.2. Kịch bản 2: Điều chuyển và bàn giao kỹ thuật viên khi KTV cũ vắng mặt (UC06 - BR07)")
    add_diagram_box(doc, [
        "Admin                 RepairService                Repository             KTV Mới (Target)",
        "  |                          |                          |                        |",
        "  |-- 1. initiate_handover ->|                          |                        |",
        "  |   (is_absent=True)       |-- 2. Kiểm tra phiên chờ->| get_pending_handover() |",
        "  |                          |      (Tối đa 1 phiên)    |                        |",
        "  |                          |-- 3. Tạo HandoverSession>| handovers[id] = session|",
        "  |                          |      (Status: PENDING)   |                        |",
        "  |                          |                          |-- 4. Thông báo phiên ->|",
        "  |                          |                          |                        |-- 5. Xem hồ sơ & nhật ký",
        "  |                          |<-- 6. respond_handover(accept=True)---------------|",
        "  |                          |-- 7. Đổi KTV phụ trách ->| ticket.current_tech = new",
        "  |                          |-- 8. Ghi Audit Log ----->| ticket.history.append()|",
        "  |                          |-- 9. Đổi Session ACCEPTED| session.status = ACCEPTED",
        "  |<-- 10. Báo thành công ---|"
    ])
    add_figure_caption(doc, "Hình 4.6: Biểu đồ tuần tự quy trình bàn giao điều chuyển KTV vắng mặt")

    add_heading_2(doc, "4.8.3. Kịch bản 3: Cập nhật sửa chữa và sử dụng linh kiện từ kho (UC07, UC08 - BR05, BR06)")
    add_diagram_box(doc, [
        "KTV Phụ trách          RepairService              InventoryService          Repository",
        "  |                          |                           |                       |",
        "  |-- 1. update_status ----->|                           |                       |",
        "  |   (UNDER_REPAIR->RESULT) |-- 2. Kiểm tra FSM Guard ->|                       | (Valid State Transition)",
        "  |                          |-- 3. Ghi RepairWorkLog -->|                       | work_logs.append()",
        "  |                          |                           |                       |",
        "  |-- 4. record_part_usage ->|                           |-- 5. Check allocated->| allocations[ticket_id]",
        "  |   (part_id, used_qty)    |                           |      used <= allocated|",
        "  |                          |                           |-- 6. Tăng used_qty -->| (KHÔNG giảm kho lần 2)",
        "  |<-- 7. Xác nhận cập nhật -|                           |<-- 8. Return alloc ---|"
    ])
    add_figure_caption(doc, "Hình 4.7: Biểu đồ tuần tự cập nhật tiến độ và ghi nhận sử dụng linh kiện kho")

    add_heading_2(doc, "4.8.4. Kịch bản 4: Tự động tổng hợp và gửi email điểm tin SLA 08:00 (SLA - BR08)")
    add_diagram_box(doc, [
        "Scheduler (08:00)         SlaService                 SimulatedClock         EmailService Mock",
        "  |                           |                             |                       |",
        "  |-- 1. Trigger Cronjob ---->|                             |                       |",
        "  |                           |-- 2. Lấy ngày hôm nay ----->| clock.today()         |",
        "  |                           |   (Hỗ trợ giả lập TB.02)    |                       |",
        "  |                           |-- 3. Quét Tickets chưa xong |                       |",
        "  |                           |      Phân loại Nhóm 1 (Đỏ)  |                       |",
        "  |                           |      Phân loại Nhóm 2 (Lưu ý)                       |",
        "  |                           |      (Không trùng lặp phiếu)|                       |",
        "  |                           |-- 4. Định dạng thân email ->|                       |",
        "  |                           |-- 5. dispatch_email() ----------------------------->| send_email()",
        "  |                           |                             |                       | (Lưu buffer kiểm thử TB.05)",
        "  |<-- 6. Hoàn tất báo cáo ---|"
    ])
    add_figure_caption(doc, "Hình 4.8: Biểu đồ tuần tự bộ máy tự động gửi điểm tin SLA lúc 08:00")

    # Conclusion of Chapter 4
    add_heading_1(doc, "4.9. Kết luận Chương 4")
    add_body_p(
        doc,
        "Chương 4 đã giải quyết trọn vẹn và toàn diện nhiệm vụ được phân công cho thành viên Nguyễn Hoàng Thiện Anh (Mã SV: B23DCKD003, Role D&T): "
        "'Thiết kế kiến trúc tổng thể, quy tắc đặt tên, thiết kế chi tiết luồng dữ liệu bảo hành'. "
        "Những đóng góp chính bao gồm:\n"
        "1. Thiết lập mô hình Kiến trúc phân tầng dạng Clean Layered Architecture kết hợp Tiêm phụ thuộc (Dependency Injection), "
        "đáp ứng đầy đủ các thuộc tính chất lượng ISO/IEC 25010 và đặc tính Kiểm thử được (Testability TB.01 đến TB.12).\n"
        "2. Chuẩn hóa bộ quy tắc đặt tên toàn diện (Naming Conventions) từ tài liệu, mã nghiệp vụ, mã nguồn, cơ sở dữ liệu đến giao diện lập trình REST API.\n"
        "3. Xây dựng chi tiết luồng dữ liệu bảo hành qua hệ thống biểu đồ DFD Cấp 0, Cấp 1, Cấp 2 và cỗ máy chuyển trạng thái State Machine chặt chẽ.\n"
        "4. Thiết kế cơ sở dữ liệu vật lý chuẩn hóa 3NF gồm 10 bảng thực thể, đầy đủ ràng buộc toàn vẹn và chiến lược lập chỉ mục tối ưu hiệu năng.\n"
        "5. Hiện thực hóa mã nguồn mẫu Clean Code trong module warranty_core và vượt qua 100% 19 ca kiểm thử tự động với Pytest (0 warnings, 0 errors).\n"
        "Toàn bộ tài liệu được soạn thảo tuân thủ nghiêm ngặt thể thức văn bản hành chính theo Thông tư 30 / Nghị định 30 (Times New Roman, cỡ 13pt, "
        "căn lề chuẩn A4, giãn dòng 1.35, không dùng highlight màu mè), tạo tiền đề vững chắc cho việc lập trình và kiểm thử chi tiết ở Chương 5."
    )

    output_path = r'E:\Warranty Management System\docs\PSE.G102_Chuong4_KienTrucPhanMem.docx'
    doc.save(output_path)
    # Also save a copy directly in the root directory for immediate user access
    root_path = r'E:\Warranty Management System\PSE.G102_Chuong4_KienTrucPhanMem.docx'
    doc.save(root_path)
    print(f"Document successfully created at {output_path} and {root_path}!")

if __name__ == '__main__':
    build_chuong4_document()
