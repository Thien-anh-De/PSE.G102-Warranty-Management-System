import json
from datetime import datetime, date, timedelta, timezone
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Optional
from urllib.parse import urlparse, parse_qs

from src.warranty_core.repository import InMemoryRepository
from src.warranty_core.services.clock_service import SimulatedClockService
from src.warranty_core.services.dashboard_service import DashboardService, DashboardServiceError
from src.warranty_core.domain_models import User, Customer, Device, WarrantyTicket, WarrantyAssessment
from src.warranty_core.enums import (
    UserRole,
    TicketStatus,
    IntakeType,
    WarrantyEligibility,
    WarrantyResolution,
    DefectOrigin,
)


def init_demo_repository() -> InMemoryRepository:
    """Khởi tạo tập dữ liệu mẫu chuẩn hóa (TB.01) cho Dashboard độc lập."""
    repo = InMemoryRepository()
    repo.users["USR_ADMIN_01"] = User("USR_ADMIN_01", "admin1", "hash", "Quản trị viên Hệ thống", UserRole.ADMIN, True)
    repo.users["USR_TECH_01"] = User("USR_TECH_01", "tech1", "hash", "Nguyễn Văn An (KTV 01)", UserRole.TECHNICIAN, True)
    repo.users["USR_TECH_02"] = User("USR_TECH_02", "tech2", "hash", "Trần Minh Bình (KTV 02)", UserRole.TECHNICIAN, True)
    repo.users["USR_TECH_03"] = User("USR_TECH_03", "tech3", "hash", "Lê Hoàng Cường (KTV 03)", UserRole.TECHNICIAN, True)

    repo.customers["CUST_01"] = Customer("CUST_01", "Khách hàng Tiêu chuẩn", "0912345678")

    models = [
        ("DEV_01", "SN-DELL-9520", "Dell XPS 15 9520", "Dell"),
        ("DEV_02", "SN-ASUS-G15", "Asus ROG Strix G15", "Asus"),
        ("DEV_03", "SN-HP-PAV15", "HP Pavilion 15", "HP"),
        ("DEV_04", "SN-LEN-X1C", "Lenovo ThinkPad X1 Carbon", "Lenovo"),
        ("DEV_05", "SN-MAC-M3P", "MacBook Pro 14 M3", "Apple"),
    ]
    for d_id, sn, m_name, brand in models:
        repo.devices[d_id] = Device(d_id, sn, m_name, brand, date(2026, 9, 15))

    seed_tickets(repo, count=72)
    return repo


def seed_tickets(repo: InMemoryRepository, count: int) -> None:
    repo.tickets.clear()
    repo.assessments.clear()
    base_dt = datetime(2026, 11, 1, 8, 0, tzinfo=timezone.utc)
    statuses = list(TicketStatus)
    techs = ["USR_TECH_01", "USR_TECH_02", "USR_TECH_03"]
    devs = ["DEV_01", "DEV_02", "DEV_03", "DEV_04", "DEV_05"]
    eligibilities = [
        WarrantyEligibility.ELIGIBLE,
        WarrantyEligibility.ELIGIBLE,
        WarrantyEligibility.INELIGIBLE,
        WarrantyEligibility.INSUFFICIENT_INFO,
    ]

    for i in range(1, count + 1):
        day_offset = i % 24
        tid = f"TKT_202611{day_offset + 1:02d}_{i:04d}"
        st = statuses[i % len(statuses)]
        tech = None if st in {TicketStatus.RECEIVED, TicketStatus.PENDING_ASSIGNMENT} else techs[i % 3]
        created = base_dt + timedelta(days=day_offset, hours=(i % 10))
        promised = (created + timedelta(days=(i % 6) + 1)).date()

        repo.tickets[tid] = WarrantyTicket(
            ticket_id=tid,
            customer_id="CUST_01",
            device_id=devs[i % len(devs)],
            intake_type=IntakeType.HOLD_FOR_REPAIR if i % 4 != 0 else IntakeType.SAME_DAY,
            promised_return_date=promised,
            reported_issue="Kiểm tra lỗi phần cứng / nguồn / màn hình",
            initial_condition="Ngoại quan nguyên vẹn",
            accessories_included="Sạc zin theo máy",
            status=st,
            tracking_code_hash="sha256_demo",
            created_at=created,
            current_technician_id=tech,
        )

        el = eligibilities[i % len(eligibilities)]
        repo.assessments[f"ASS_{i:04d}"] = WarrantyAssessment(
            assessment_id=f"ASS_{i:04d}",
            ticket_id=tid,
            purchase_date=date(2026, 9, 15),
            incident_date=created.date(),
            is_warranty_valid=(el == WarrantyEligibility.ELIGIBLE),
            defect_origin=DefectOrigin.MANUFACTURER if el == WarrantyEligibility.ELIGIBLE else DefectOrigin.USER_DAMAGE,
            eligibility=el,
            resolution=WarrantyResolution.FREE_REPAIR if el == WarrantyEligibility.ELIGIBLE else WarrantyResolution.PAID_REPAIR,
            customer_agreed=True,
        )


REPO = init_demo_repository()
CLOCK = SimulatedClockService(datetime(2026, 11, 24, 8, 0, 0, tzinfo=timezone.utc))
DASHBOARD_SERVICE = DashboardService(REPO, CLOCK)


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="vi" class="scroll-smooth">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Warranty Analytics Command Center — Dashboard Thống Kê & Báo Cáo</title>
  <script src="https://cdn.tailwindcss.com"></script>
  <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
  <link href="https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <style>
    body { font-family: 'Plus Jakarta Sans', sans-serif; }
    @media print {
      aside, header, #sec-filter, .no-print { display: none !important; }
      body { background: white !important; }
      main { padding: 0 !important; }
    }
  </style>
</head>
<body class="bg-slate-100/90 text-slate-800 antialiased">
  <div class="min-h-screen flex flex-col lg:flex-row">
    <!-- Sidebar Độc Lập 100% Chức Năng Thực Tế -->
    <aside class="w-full lg:w-72 bg-gradient-to-b from-slate-950 via-slate-900 to-indigo-950 text-slate-300 flex-shrink-0 flex flex-col justify-between lg:sticky lg:top-0 lg:h-screen shadow-xl">
      <div>
        <div class="p-6 border-b border-white/10 flex items-center gap-3.5">
          <div class="w-11 h-11 rounded-2xl bg-gradient-to-tr from-blue-600 via-indigo-500 to-cyan-400 flex items-center justify-center text-white font-extrabold text-lg shadow-lg shadow-blue-500/30">
            BI
          </div>
          <div>
            <p class="text-white font-extrabold text-sm tracking-wide">WARRANTY ANALYTICS</p>
            <p class="text-[11px] text-cyan-300/80 font-medium">Executive Dashboard • INC3</p>
          </div>
        </div>

        <nav class="p-4 space-y-1.5 text-sm">
          <p class="px-3 pt-1 pb-2 text-[10px] font-bold uppercase tracking-widest text-slate-400">Danh mục phân tích</p>
          <a href="#sec-filter" class="px-3.5 py-2.5 rounded-xl bg-white/10 text-white hover:bg-blue-600 font-semibold flex items-center justify-between transition">
            <span>1. Bộ lọc & Xuất báo cáo</span>
            <span class="text-[10px] bg-blue-500/40 text-blue-200 px-2 py-0.5 rounded-md">FR02-03</span>
          </a>
          <a href="#sec-kpi" class="px-3.5 py-2.5 rounded-xl text-slate-300 hover:bg-white/10 hover:text-white font-medium flex items-center justify-between transition">
            <span>2. Chỉ số KPI điều hành</span>
            <span class="text-[10px] bg-white/10 px-2 py-0.5 rounded-md">FR01</span>
          </a>
          <a href="#sec-charts" class="px-3.5 py-2.5 rounded-xl text-slate-300 hover:bg-white/10 hover:text-white font-medium flex items-center justify-between transition">
            <span>3. Biểu đồ đa chiều (5 Charts)</span>
            <span class="text-[10px] bg-white/10 px-2 py-0.5 rounded-md">Visual</span>
          </a>
          <a href="#sec-tech-table" class="px-3.5 py-2.5 rounded-xl text-slate-300 hover:bg-white/10 hover:text-white font-medium flex items-center justify-between transition">
            <span>4. Bảng hiệu suất Kỹ thuật viên</span>
            <span class="text-[10px] bg-emerald-500/20 text-emerald-300 px-2 py-0.5 rounded-md">KPI</span>
          </a>
          <a href="#sec-overdue" class="px-3.5 py-2.5 rounded-xl text-slate-300 hover:bg-white/10 hover:text-white font-medium flex items-center justify-between transition">
            <span>5. Cảnh báo phiếu quá hạn</span>
            <span class="text-[10px] bg-rose-500/30 text-rose-300 px-2 py-0.5 rounded-md">SLA</span>
          </a>
        </nav>
      </div>

      <div class="p-4 border-t border-white/10 text-xs space-y-3">
        <div class="bg-white/5 p-3.5 rounded-xl border border-white/10 backdrop-blur">
          <label for="actor_role_select" class="block text-slate-300 text-[11px] font-bold">Kiểm thử phân quyền RBAC (T06)</label>
          <select id="actor_role_select" onchange="loadDashboard()" class="mt-2 w-full bg-slate-900 text-white border border-slate-700 rounded-lg px-2.5 py-2 text-xs focus:ring-2 focus:ring-cyan-400 outline-none">
            <option value="USR_ADMIN_01">Admin (Toàn quyền Dashboard)</option>
            <option value="USR_TECH_01">Kỹ thuật viên (Test chặn 403)</option>
          </select>
        </div>
        <div class="text-[11px] text-slate-400 flex justify-between px-1">
          <span>Độ đo: T06, T11–T13</span>
          <span class="text-emerald-400 font-semibold">● Online</span>
        </div>
      </div>
    </aside>

    <!-- Nội Dung Chính -->
    <div class="flex-1 flex flex-col min-w-0">
      <!-- Top Header -->
      <header class="bg-white/90 backdrop-blur border-b border-slate-200 px-6 py-4 flex flex-col xl:flex-row justify-between items-start xl:items-center gap-3 sticky top-0 z-20 shadow-sm">
        <div>
          <div class="flex items-center gap-2">
            <span class="px-2 py-0.5 text-[10px] font-extrabold uppercase tracking-wider bg-indigo-100 text-indigo-700 rounded-md">Standalone Analytics Module</span>
            <span id="perf-badge" class="px-2 py-0.5 text-[10px] font-bold bg-emerald-100 text-emerald-700 rounded-md">API: -- ms</span>
          </div>
          <h1 class="text-lg sm:text-xl font-extrabold text-slate-900 mt-1">Dashboard Thống Kê & Báo Cáo Hoạt Động Bảo Hành</h1>
        </div>
        <div class="flex flex-wrap items-center gap-2">
          <span id="snapshot-badge" class="text-xs font-mono bg-slate-100 text-slate-700 border border-slate-200 px-3 py-1.5 rounded-lg">
            Chốt dữ liệu: --
          </span>
          <button data-testid="btn-seed-5000" onclick="seedTicketsCount(5000)" class="bg-gradient-to-r from-amber-500 to-orange-500 hover:from-amber-600 hover:to-orange-600 text-white text-xs font-bold px-3.5 py-2 rounded-lg shadow-sm transition cursor-pointer">
            Nạp 5.000 phiếu (Test T12)
          </button>
          <button onclick="seedTicketsCount(72)" class="bg-slate-200 hover:bg-slate-300 text-slate-700 text-xs font-semibold px-3 py-2 rounded-lg transition cursor-pointer">
            Reset mẫu (72)
          </button>
        </div>
      </header>

      <!-- Banner Cảnh Báo Lỗi / Phân Quyền -->
      <div id="alert-banner" class="hidden mx-6 mt-5 p-4 rounded-xl bg-rose-50 border border-rose-300 text-rose-800 text-sm font-semibold flex items-center justify-between shadow-sm">
        <span id="alert-message"></span>
        <span class="text-xs font-mono bg-rose-200 text-rose-900 px-2.5 py-1 rounded font-bold">HTTP 403 FORBIDDEN</span>
      </div>

      <main id="dashboard-content" class="p-6 space-y-6">
        <!-- 1. Thanh Bộ Lọc Đa Tiêu Chí & Xuất Báo Cáo -->
        <section id="sec-filter" class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 scroll-mt-24">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center pb-3.5 mb-4 border-b border-slate-100 gap-3">
            <div>
              <h2 class="text-sm font-extrabold text-slate-800">Bộ Lọc Dữ Liệu Đồng Thời (Điều kiện AND — FR_DASH_02)</h2>
              <p id="perf-metric" class="text-xs text-emerald-600 font-semibold mt-0.5">Đang đo hiệu năng truy vấn...</p>
            </div>
            <div class="flex flex-wrap gap-2">
              <button data-testid="btn-export-excel" onclick="downloadReport('excel')" class="bg-emerald-600 hover:bg-emerald-700 text-white text-xs sm:text-sm font-bold px-4 py-2 rounded-xl shadow-sm transition cursor-pointer">
                Xuất Excel (.csv)
              </button>
              <button data-testid="btn-export-pdf" onclick="downloadReport('pdf')" class="bg-rose-600 hover:bg-rose-700 text-white text-xs sm:text-sm font-bold px-4 py-2 rounded-xl shadow-sm transition cursor-pointer">
                Xuất PDF (Khổ A4)
              </button>
              <button onclick="window.print()" class="bg-slate-800 hover:bg-slate-900 text-white text-xs sm:text-sm font-semibold px-3.5 py-2 rounded-xl shadow-sm transition cursor-pointer">
                In trực tiếp A4
              </button>
            </div>
          </div>

          <div class="grid grid-cols-1 sm:grid-cols-2 xl:grid-cols-6 gap-3">
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Từ ngày tiếp nhận</label>
              <input data-testid="filter-start-date" id="start_date" type="date" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Đến ngày tiếp nhận</label>
              <input data-testid="filter-end-date" id="end_date" type="date" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none" />
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Kỹ thuật viên hiện hành</label>
              <select data-testid="filter-technician" id="technician_id" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                <option value="">-- Tất cả KTV --</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Trạng thái vòng đời</label>
              <select data-testid="filter-status" id="status" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                <option value="">-- Tất cả 9 trạng thái --</option>
              </select>
            </div>
            <div>
              <label class="block text-xs font-semibold text-slate-600 mb-1">Dòng thiết bị (Model)</label>
              <select data-testid="filter-model" id="model_name" class="w-full border border-slate-300 rounded-xl px-3 py-2 text-sm focus:ring-2 focus:ring-blue-500 outline-none">
                <option value="">-- Tất cả dòng máy --</option>
              </select>
            </div>
            <div class="flex items-end gap-2">
              <button data-testid="btn-apply-filter" onclick="loadDashboard()" class="flex-1 bg-blue-600 hover:bg-blue-700 text-white text-sm font-bold py-2 px-3 rounded-xl shadow-sm transition cursor-pointer">
                Áp dụng
              </button>
              <button data-testid="btn-reset-filter" onclick="resetFilters()" class="bg-slate-100 hover:bg-slate-200 text-slate-700 text-sm font-semibold py-2 px-3 rounded-xl transition cursor-pointer">
                Xóa lọc
              </button>
            </div>
          </div>
        </section>

        <!-- 2. 6 Thẻ KPI Điều Hành Có Thanh Tiến Độ -->
        <section id="sec-kpi" class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 xl:grid-cols-6 gap-4 scroll-mt-24">
          <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
            <p class="text-[11px] font-bold uppercase tracking-wider text-slate-400">Tổng phiếu lọc</p>
            <p data-testid="kpi-total" id="kpi-total" class="text-2xl font-extrabold text-slate-900 mt-2">0</p>
            <div class="w-full bg-slate-100 h-1.5 rounded-full mt-3"><div class="bg-slate-700 h-1.5 rounded-full w-full"></div></div>
            <p class="text-[11px] text-slate-500 mt-1.5">100% tập dữ liệu khớp lọc</p>
          </div>

          <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
            <p class="text-[11px] font-bold uppercase tracking-wider text-blue-500">Đang xử lý</p>
            <p data-testid="kpi-in-progress" id="kpi-in-progress" class="text-2xl font-extrabold text-blue-600 mt-2">0</p>
            <div class="w-full bg-blue-100 h-1.5 rounded-full mt-3"><div id="bar-in-progress" class="bg-blue-600 h-1.5 rounded-full" style="width:0%"></div></div>
            <p id="kpi-in-progress-rate" class="text-[11px] text-slate-500 mt-1.5">Chiếm 0% tổng phiếu</p>
          </div>

          <div class="bg-white p-5 rounded-2xl shadow-sm border border-amber-200 bg-amber-50/20">
            <p class="text-[11px] font-bold uppercase tracking-wider text-amber-600">Chờ linh kiện</p>
            <p id="kpi-waiting-parts" class="text-2xl font-extrabold text-amber-600 mt-2">0</p>
            <div class="w-full bg-amber-100 h-1.5 rounded-full mt-3"><div id="bar-waiting-parts" class="bg-amber-500 h-1.5 rounded-full" style="width:0%"></div></div>
            <p id="kpi-waiting-rate" class="text-[11px] text-amber-700 mt-1.5">Chiếm 0% tổng phiếu</p>
          </div>

          <div class="bg-white p-5 rounded-2xl shadow-sm border border-emerald-200 bg-emerald-50/20">
            <p class="text-[11px] font-bold uppercase tracking-wider text-emerald-600">Đã trả máy</p>
            <p data-testid="kpi-completed" id="kpi-completed" class="text-2xl font-extrabold text-emerald-600 mt-2">0</p>
            <div class="w-full bg-emerald-100 h-1.5 rounded-full mt-3"><div id="bar-completed" class="bg-emerald-500 h-1.5 rounded-full" style="width:0%"></div></div>
            <p id="kpi-completed-rate" class="text-[11px] text-emerald-700 font-semibold mt-1.5">Hoàn thành: 0%</p>
          </div>

          <div class="bg-white p-5 rounded-2xl shadow-sm border border-rose-200 bg-rose-50/30">
            <p class="text-[11px] font-bold uppercase tracking-wider text-rose-600">Quá hạn trả</p>
            <p data-testid="kpi-overdue" id="kpi-overdue" class="text-2xl font-extrabold text-rose-600 mt-2">0</p>
            <div class="w-full bg-rose-100 h-1.5 rounded-full mt-3"><div id="bar-overdue" class="bg-rose-600 h-1.5 rounded-full" style="width:0%"></div></div>
            <p id="kpi-overdue-rate" class="text-[11px] text-rose-700 font-semibold mt-1.5">Tỷ lệ trễ: 0%</p>
          </div>

          <div class="bg-white p-5 rounded-2xl shadow-sm border border-indigo-200 bg-indigo-50/20">
            <p class="text-[11px] font-bold uppercase tracking-wider text-indigo-600">Đúng hạn SLA</p>
            <p id="kpi-sla-rate" class="text-2xl font-extrabold text-indigo-600 mt-2">0%</p>
            <div class="w-full bg-indigo-100 h-1.5 rounded-full mt-3"><div id="bar-sla" class="bg-indigo-600 h-1.5 rounded-full" style="width:0%"></div></div>
            <p class="text-[11px] text-indigo-700 mt-1.5">Phiếu trong hạn cam kết</p>
          </div>
        </section>

        <!-- 3. Hệ Thống 5 Biểu Đồ Phân Tích Đa Chiều -->
        <div id="sec-charts" class="space-y-6 scroll-mt-24">
          <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="lg:col-span-2 bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
              <div class="flex justify-between items-center mb-3">
                <h3 class="text-sm font-extrabold text-slate-800">Phân Bố Phiếu Theo 9 Trạng Thái Vòng Đời (FSM)</h3>
                <span class="text-[11px] font-medium text-slate-400">Trạng thái hiện hành</span>
              </div>
              <div class="h-72">
                <canvas id="statusChart"></canvas>
              </div>
            </div>

            <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
              <div class="flex justify-between items-center mb-3">
                <h3 class="text-sm font-extrabold text-slate-800">Kết Luận Thẩm Định Bảo Hành</h3>
                <span class="text-[11px] font-medium text-slate-400">BR03</span>
              </div>
              <div class="h-72">
                <canvas id="eligibilityChart"></canvas>
              </div>
            </div>
          </section>

          <section class="grid grid-cols-1 lg:grid-cols-3 gap-6">
            <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
              <h3 class="text-sm font-extrabold text-slate-800 mb-3">Khối Lượng Công Việc Theo KTV</h3>
              <div class="h-72">
                <canvas id="techChart"></canvas>
              </div>
            </div>

            <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
              <h3 class="text-sm font-extrabold text-slate-800 mb-3">Phân Bố Theo Dòng Thiết Bị</h3>
              <div class="h-72">
                <canvas id="modelChart"></canvas>
              </div>
            </div>

            <div class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200">
              <h3 class="text-sm font-extrabold text-slate-800 mb-3">Lưu Lượng Tiếp Nhận Theo Ngày</h3>
              <div class="h-72">
                <canvas id="trendChart"></canvas>
              </div>
            </div>
          </section>
        </div>

        <!-- 4. Bảng Hiệu Suất Từng Kỹ Thuật Viên -->
        <section id="sec-tech-table" class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 scroll-mt-24">
          <div class="mb-4">
            <h3 class="text-sm font-extrabold text-slate-800">Bảng Tổng Hợp Hiệu Suất Kỹ Thuật Viên (Theo Phân Công Hiện Hành)</h3>
            <p class="text-xs text-slate-500">Đối chiếu số phiếu đang phụ trách, đã hoàn tất và phiếu đang bị trễ hạn của từng KTV</p>
          </div>
          <div class="overflow-x-auto">
            <table class="min-w-full text-sm text-left border-collapse">
              <thead>
                <tr class="bg-slate-50 text-slate-600 border-y border-slate-200 text-xs uppercase">
                  <th class="py-3 px-4 font-bold">Mã KTV</th>
                  <th class="py-3 px-4 font-bold">Họ và tên Kỹ thuật viên</th>
                  <th class="py-3 px-4 font-bold text-center">Tổng phiếu giao</th>
                  <th class="py-3 px-4 font-bold text-center text-blue-600">Đang xử lý</th>
                  <th class="py-3 px-4 font-bold text-center text-emerald-600">Đã hoàn thành</th>
                  <th class="py-3 px-4 font-bold text-center text-rose-600">Đang quá hạn</th>
                  <th class="py-3 px-4 font-bold">Tỷ lệ hoàn tất</th>
                </tr>
              </thead>
              <tbody id="tech-table-body" class="divide-y divide-slate-100"></tbody>
            </table>
          </div>
        </section>

        <!-- 5. Bảng Cảnh Báo Phiếu Quá Hạn -->
        <section id="sec-overdue" class="bg-white p-5 rounded-2xl shadow-sm border border-slate-200 scroll-mt-24">
          <div class="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-3 mb-4">
            <div>
              <h3 class="text-sm font-extrabold text-slate-800">Danh Sách Phiếu Quá Hạn Trả Cần Ưu Tiên Xử Lý</h3>
              <p class="text-xs text-slate-500">Sắp xếp giảm dần theo số ngày trễ hạn (loại trừ Đã trả / Đã hủy)</p>
            </div>
            <input
              id="overdue-search"
              oninput="filterOverdueTable()"
              type="text"
              placeholder="Tìm nhanh mã phiếu, serial, KTV..."
              class="w-full sm:w-72 border border-slate-300 rounded-xl px-3.5 py-2 text-xs focus:ring-2 focus:ring-blue-500 outline-none"
            />
          </div>

          <div class="overflow-x-auto">
            <table class="min-w-full text-sm text-left border-collapse">
              <thead>
                <tr class="bg-slate-50 text-slate-600 border-y border-slate-200 text-xs uppercase">
                  <th class="py-3 px-4 font-bold">Mã phiếu</th>
                  <th class="py-3 px-4 font-bold">Dòng máy & Serial</th>
                  <th class="py-3 px-4 font-bold">Trạng thái hiện tại</th>
                  <th class="py-3 px-4 font-bold">KTV phụ trách</th>
                  <th class="py-3 px-4 font-bold">Ngày hẹn trả</th>
                  <th class="py-3 px-4 font-bold text-rose-600">Mức độ trễ</th>
                </tr>
              </thead>
              <tbody id="overdue-table-body" class="divide-y divide-slate-100"></tbody>
            </table>
          </div>
        </section>
      </main>
    </div>
  </div>

  <script>
    let statusChartInst = null;
    let eligibilityChartInst = null;
    let techChartInst = null;
    let modelChartInst = null;
    let trendChartInst = null;
    let cachedOverdueRows = [];

    function getActorHeader() {
      return { 'X-User-Id': document.getElementById('actor_role_select').value };
    }

    function buildQueryParams() {
      const params = new URLSearchParams();
      ['start_date', 'end_date', 'technician_id', 'status', 'model_name'].forEach(id => {
        const val = document.getElementById(id).value;
        if (val) params.append(id, val);
      });
      return params.toString();
    }

    function showErrorBanner(msg) {
      const banner = document.getElementById('alert-banner');
      document.getElementById('alert-message').innerText = msg;
      banner.classList.remove('hidden');
    }

    function hideErrorBanner() {
      document.getElementById('alert-banner').classList.add('hidden');
    }

    async function initFilterOptions() {
      const res = await fetch('/api/v1/dashboard/filters', { headers: getActorHeader() });
      if (!res.ok) return;
      const data = await res.json();
      const techSel = document.getElementById('technician_id');
      data.technicians.forEach(t => {
        techSel.innerHTML += `<option value="${t.user_id}">${t.full_name}</option>`;
      });
      const stSel = document.getElementById('status');
      data.statuses.forEach(s => {
        stSel.innerHTML += `<option value="${s}">${s}</option>`;
      });
      const modSel = document.getElementById('model_name');
      data.models.forEach(m => {
        modSel.innerHTML += `<option value="${m}">${m}</option>`;
      });
    }

    async function loadDashboard() {
      hideErrorBanner();
      const t0 = performance.now();
      const query = buildQueryParams();
      const res = await fetch('/api/v1/dashboard/summary?' + query, { headers: getActorHeader() });
      const data = await res.json();

      if (!res.ok) {
        showErrorBanner(data.error || 'Lỗi truy cập dữ liệu Dashboard.');
        document.getElementById('dashboard-content').classList.add('opacity-40', 'pointer-events-none');
        return;
      }

      document.getElementById('dashboard-content').classList.remove('opacity-40', 'pointer-events-none');
      const elapsed = (performance.now() - t0).toFixed(1);

      document.getElementById('perf-badge').innerText = `API: ${elapsed} ms`;
      document.getElementById('perf-metric').innerText = `Thời gian phản hồi API & Render: ${elapsed} ms (Đạt chuẩn T12 <= 2000 ms)`;
      document.getElementById('snapshot-badge').innerText = `Chốt dữ liệu: ${data.snapshot_at}`;

      const total = data.kpi.total_tickets || 0;
      const inProgPct = total ? ((data.kpi.in_progress_tickets / total) * 100).toFixed(1) : 0;
      const waitPct = total ? ((data.kpi.waiting_parts_tickets / total) * 100).toFixed(1) : 0;
      const compPct = data.kpi.completion_rate_percent;
      const overPct = data.kpi.overdue_rate_percent;
      const slaPct = total ? (100 - overPct).toFixed(1) : 100;

      document.getElementById('kpi-total').innerText = total.toLocaleString();
      document.getElementById('kpi-in-progress').innerText = data.kpi.in_progress_tickets.toLocaleString();
      document.getElementById('bar-in-progress').style.width = `${inProgPct}%`;
      document.getElementById('kpi-in-progress-rate').innerText = `Chiếm ${inProgPct}% tổng phiếu`;

      document.getElementById('kpi-waiting-parts').innerText = data.kpi.waiting_parts_tickets.toLocaleString();
      document.getElementById('bar-waiting-parts').style.width = `${waitPct}%`;
      document.getElementById('kpi-waiting-rate').innerText = `Chiếm ${waitPct}% tổng phiếu`;

      document.getElementById('kpi-completed').innerText = data.kpi.completed_tickets.toLocaleString();
      document.getElementById('bar-completed').style.width = `${compPct}%`;
      document.getElementById('kpi-completed-rate').innerText = `Hoàn thành: ${compPct}%`;

      document.getElementById('kpi-overdue').innerText = data.kpi.overdue_tickets.toLocaleString();
      document.getElementById('bar-overdue').style.width = `${overPct}%`;
      document.getElementById('kpi-overdue-rate').innerText = `Tỷ lệ trễ: ${overPct}%`;

      document.getElementById('kpi-sla-rate').innerText = `${slaPct}%`;
      document.getElementById('bar-sla').style.width = `${slaPct}%`;

      renderCharts(data);
      renderTechTable(data.technician_distribution);
      cachedOverdueRows = data.overdue_details;
      filterOverdueTable();
    }

    function renderCharts(data) {
      const stLabels = Object.keys(data.by_status);
      const stValues = Object.values(data.by_status);
      const stColors = [
        '#64748b', '#0ea5e9', '#6366f1', '#2563eb',
        '#f59e0b', '#8b5cf6', '#14b8a6', '#10b981', '#ef4444'
      ];

      if (statusChartInst) statusChartInst.destroy();
      statusChartInst = new Chart(document.getElementById('statusChart'), {
        type: 'bar',
        data: {
          labels: stLabels,
          datasets: [{
            label: 'Số phiếu',
            data: stValues,
            backgroundColor: stColors,
            borderRadius: 6
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          plugins: { legend: { display: false } }
        }
      });

      const elMap = {
        'ELIGIBLE': 'Đủ điều kiện BH',
        'INELIGIBLE': 'Ngoài bảo hành',
        'INSUFFICIENT_INFO': 'Chưa đủ thông tin'
      };
      const elLabels = Object.keys(data.by_eligibility).map(k => elMap[k] || k);
      const elValues = Object.values(data.by_eligibility);

      if (eligibilityChartInst) eligibilityChartInst.destroy();
      eligibilityChartInst = new Chart(document.getElementById('eligibilityChart'), {
        type: 'doughnut',
        data: {
          labels: elLabels,
          datasets: [{
            data: elValues,
            backgroundColor: ['#10b981', '#f43f5e', '#f59e0b'],
            borderWidth: 2
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          cutout: '64%'
        }
      });

      const techLabels = data.technician_distribution.map(t => t.technician_name);
      if (techChartInst) techChartInst.destroy();
      techChartInst = new Chart(document.getElementById('techChart'), {
        type: 'bar',
        data: {
          labels: techLabels,
          datasets: [
            { label: 'Đang xử lý', data: data.technician_distribution.map(t => t.in_progress_tickets), backgroundColor: '#3b82f6', borderRadius: 4 },
            { label: 'Đã hoàn thành', data: data.technician_distribution.map(t => t.completed_tickets), backgroundColor: '#10b981', borderRadius: 4 },
            { label: 'Quá hạn', data: data.technician_distribution.map(t => t.overdue_tickets), backgroundColor: '#ef4444', borderRadius: 4 }
          ]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: { x: { stacked: true }, y: { stacked: true } }
        }
      });

      const modLabels = Object.keys(data.by_model);
      const modValues = Object.values(data.by_model);
      if (modelChartInst) modelChartInst.destroy();
      modelChartInst = new Chart(document.getElementById('modelChart'), {
        type: 'polarArea',
        data: {
          labels: modLabels,
          datasets: [{
            data: modValues,
            backgroundColor: [
              'rgba(59, 130, 246, 0.75)',
              'rgba(16, 185, 129, 0.75)',
              'rgba(245, 158, 11, 0.75)',
              'rgba(139, 92, 246, 0.75)',
              'rgba(244, 63, 94, 0.75)'
            ]
          }]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });

      const trendLabels = Object.keys(data.daily_trend);
      const trendValues = Object.values(data.daily_trend);
      if (trendChartInst) trendChartInst.destroy();
      trendChartInst = new Chart(document.getElementById('trendChart'), {
        type: 'line',
        data: {
          labels: trendLabels,
          datasets: [{
            label: 'Phiếu tiếp nhận mới',
            data: trendValues,
            borderColor: '#4f46e5',
            backgroundColor: 'rgba(79, 70, 229, 0.14)',
            fill: true,
            tension: 0.35,
            pointRadius: 3
          }]
        },
        options: { responsive: true, maintainAspectRatio: false }
      });
    }

    function renderTechTable(techList) {
      const tbody = document.getElementById('tech-table-body');
      if (!techList || !techList.length) {
        tbody.innerHTML = '<tr><td colspan="7" class="py-5 text-center text-slate-400">Không có dữ liệu phân công Kỹ thuật viên.</td></tr>';
        return;
      }
      tbody.innerHTML = techList.map(t => {
        const rate = t.assigned_tickets ? ((t.completed_tickets / t.assigned_tickets) * 100).toFixed(1) : 0;
        return `
          <tr class="hover:bg-slate-50 transition">
            <td class="py-3 px-4 font-mono text-xs font-bold text-slate-600">${t.technician_id}</td>
            <td class="py-3 px-4 font-semibold text-slate-800">${t.technician_name}</td>
            <td class="py-3 px-4 text-center font-bold">${t.assigned_tickets.toLocaleString()}</td>
            <td class="py-3 px-4 text-center font-semibold text-blue-600">${t.in_progress_tickets.toLocaleString()}</td>
            <td class="py-3 px-4 text-center font-semibold text-emerald-600">${t.completed_tickets.toLocaleString()}</td>
            <td class="py-3 px-4 text-center font-bold text-rose-600">${t.overdue_tickets.toLocaleString()}</td>
            <td class="py-3 px-4">
              <div class="flex items-center gap-2">
                <div class="w-24 bg-slate-200 h-2 rounded-full"><div class="bg-emerald-500 h-2 rounded-full" style="width:${rate}%"></div></div>
                <span class="text-xs font-bold text-slate-700">${rate}%</span>
              </div>
            </td>
          </tr>
        `;
      }).join('');
    }

    function filterOverdueTable() {
      const q = document.getElementById('overdue-search').value.trim().toLowerCase();
      const rows = cachedOverdueRows.filter(r =>
        !q ||
        r.ticket_id.toLowerCase().includes(q) ||
        r.model_name.toLowerCase().includes(q) ||
        r.serial_number.toLowerCase().includes(q) ||
        r.technician_name.toLowerCase().includes(q)
      );

      const tbody = document.getElementById('overdue-table-body');
      if (!rows.length) {
        tbody.innerHTML = '<tr><td colspan="6" class="py-6 text-center text-slate-400">Không có phiếu quá hạn nào khớp điều kiện.</td></tr>';
        return;
      }

      tbody.innerHTML = rows.map(r => `
        <tr class="hover:bg-slate-50 transition">
          <td class="py-2.5 px-4 font-mono font-bold text-blue-700">${r.ticket_id}</td>
          <td class="py-2.5 px-4">
            <div class="font-semibold text-slate-800">${r.model_name}</div>
            <div class="text-[11px] font-mono text-slate-400">${r.serial_number}</div>
          </td>
          <td class="py-2.5 px-4"><span class="px-2.5 py-1 text-xs font-semibold rounded-full bg-amber-100 text-amber-800">${r.status}</span></td>
          <td class="py-2.5 px-4 text-slate-700">${r.technician_name}</td>
          <td class="py-2.5 px-4 font-mono text-xs text-slate-600">${r.promised_return_date}</td>
          <td class="py-2.5 px-4"><span class="px-2.5 py-1 text-xs font-bold rounded-full bg-rose-100 text-rose-700">+${r.days_overdue} ngày</span></td>
        </tr>
      `).join('');
    }

    async function downloadReport(fmt) {
      hideErrorBanner();
      const query = buildQueryParams();
      const res = await fetch(`/api/v1/dashboard/export?format=${fmt}&${query}`, {
        headers: getActorHeader()
      });

      if (!res.ok) {
        const err = await res.json();
        showErrorBanner(err.error || 'Không thể xuất báo cáo.');
        return;
      }

      const blob = await res.blob();
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = fmt === 'pdf' ? 'BaoCao_ThongKe_BaoHanh_A4.pdf' : 'BaoCao_ThongKe_BaoHanh.csv';
      document.body.appendChild(a);
      a.click();
      a.remove();
      window.URL.revokeObjectURL(url);
    }

    function resetFilters() {
      ['start_date', 'end_date', 'technician_id', 'status', 'model_name'].forEach(id => {
        document.getElementById(id).value = '';
      });
      loadDashboard();
    }

    async function seedTicketsCount(count) {
      await fetch(`/api/v1/dashboard/seed?count=${count}`, { method: 'POST' });
      loadDashboard();
    }

    initFilterOptions().then(loadDashboard);
  </script>
</body>
</html>
"""


class DashboardRequestHandler(BaseHTTPRequestHandler):
    def _parse_date(self, val: Optional[str]) -> Optional[date]:
        return date.fromisoformat(val) if val else None

    def _parse_status(self, val: Optional[str]) -> Optional[TicketStatus]:
        return TicketStatus(val) if val else None

    def _send_json(self, payload: dict, status_code: int = 200) -> None:
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_POST(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        if parsed.path in {"/api/v1/dashboard/seed", "/api/v1/dashboard/seed-5000"}:
            count = int(qs.get("count", [5000])[0])
            seed_tickets(REPO, count=count)
            self._send_json({"message": f"Đã nạp {count} phiếu bảo hành giả lập thành công."})
        else:
            self._send_json({"error": "Not Found"}, 404)

    def do_GET(self):
        parsed = urlparse(self.path)
        qs = parse_qs(parsed.query)
        actor_id = self.headers.get("X-User-Id", "USR_ADMIN_01")

        try:
            if parsed.path in {"/", "/dashboard"}:
                html_bytes = HTML_TEMPLATE.encode("utf-8")
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(html_bytes)))
                self.end_headers()
                self.wfile.write(html_bytes)

            elif parsed.path == "/api/v1/dashboard/filters":
                data = DASHBOARD_SERVICE.get_filter_options(actor_id)
                self._send_json(data)

            elif parsed.path == "/api/v1/dashboard/summary":
                summary = DASHBOARD_SERVICE.get_dashboard_summary(
                    actor_user_id=actor_id,
                    start_date=self._parse_date(qs.get("start_date", [None])[0]),
                    end_date=self._parse_date(qs.get("end_date", [None])[0]),
                    technician_id=qs.get("technician_id", [None])[0],
                    status=self._parse_status(qs.get("status", [None])[0]),
                    model_name=qs.get("model_name", [None])[0],
                )
                self._send_json(summary)

            elif parsed.path == "/api/v1/dashboard/export":
                fmt = qs.get("format", ["excel"])[0]
                kwargs = dict(
                    actor_user_id=actor_id,
                    start_date=self._parse_date(qs.get("start_date", [None])[0]),
                    end_date=self._parse_date(qs.get("end_date", [None])[0]),
                    technician_id=qs.get("technician_id", [None])[0],
                    status=self._parse_status(qs.get("status", [None])[0]),
                    model_name=qs.get("model_name", [None])[0],
                )
                if fmt == "pdf":
                    stream = DASHBOARD_SERVICE.export_report_pdf(**kwargs)
                    ctype = "application/pdf"
                    fname = "BaoCao_ThongKe_BaoHanh_A4.pdf"
                else:
                    stream = DASHBOARD_SERVICE.export_report_excel(**kwargs)
                    ctype = "text/csv; charset=utf-8"
                    fname = "BaoCao_ThongKe_BaoHanh.csv"

                content = stream.read()
                self.send_response(200)
                self.send_header("Content-Type", ctype)
                self.send_header("Content-Disposition", f'attachment; filename="{fname}"')
                self.send_header("Content-Length", str(len(content)))
                self.end_headers()
                self.wfile.write(content)
            else:
                self._send_json({"error": "Endpoint không tồn tại"}, 404)

        except DashboardServiceError as exc:
            self._send_json({"error": str(exc)}, 403)
        except Exception as exc:
            self._send_json({"error": str(exc)}, 400)


if __name__ == "__main__":
    server = HTTPServer(("127.0.0.1", 8080), DashboardRequestHandler)
    print("Warranty Analytics Command Center đang chạy tại: http://127.0.0.1:8080/dashboard")
    server.serve_forever()