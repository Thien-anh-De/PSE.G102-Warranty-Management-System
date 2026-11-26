import csv
import io
from datetime import date
from typing import Dict, List, Optional, Any

from ..domain_models import WarrantyTicket
from ..enums import TicketStatus, UserRole, IntakeType, WarrantyEligibility
from ..repository import InMemoryRepository
from .clock_service import IClockService


class DashboardServiceError(Exception):
    """Ngoại lệ nghiệp vụ dành riêng cho phân hệ Dashboard (INC3 - DASH)."""
    pass


class DashboardService:
    """
    Dịch vụ tổng hợp chỉ số thống kê, lọc đa tiêu chí đồng thời và xuất báo cáo Excel/PDF
    đáp ứng FR_DASH_01..03, NFR_PERF_02, NFR_SEC_01, NFR_COMP_01 và TB.12.
    """

    def __init__(self, repository: InMemoryRepository, clock_service: IClockService):
        self.repository = repository
        self.clock_service = clock_service

    def _verify_admin_access(self, actor_user_id: str) -> None:
        """
        NFR_SEC_01 & T06: Kiểm tra phân quyền RBAC ở tầng xử lý nghiệp vụ.
        Từ chối 100% yêu cầu từ Kỹ thuật viên hoặc tài khoản bị khóa.
        """
        user = self.repository.users.get(actor_user_id)
        if not user or not user.is_active or user.role != UserRole.ADMIN:
            raise DashboardServiceError(
                "403 Forbidden: Truy cập bị từ chối. Chỉ tài khoản Admin mới có quyền xem Dashboard và xuất báo cáo."
            )

    def get_filter_options(self, actor_user_id: str) -> Dict[str, Any]:
        """Cung cấp danh sách giá trị chuẩn cho các bộ lọc trên giao diện Web."""
        self._verify_admin_access(actor_user_id)
        technicians = [
            {"user_id": u.user_id, "full_name": u.full_name}
            for u in self.repository.users.values()
            if u.role == UserRole.TECHNICIAN and u.is_active
        ]
        models = sorted(
            {d.model_name for d in self.repository.devices.values() if d.model_name}
        )
        statuses = [st.value for st in TicketStatus]
        return {
            "technicians": technicians,
            "models": models,
            "statuses": statuses,
        }

    def filter_tickets(
        self,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        technician_id: Optional[str] = None,
        status: Optional[TicketStatus] = None,
        model_name: Optional[str] = None,
    ) -> List[WarrantyTicket]:
        """
        FR_DASH_02: Lọc đồng thời (điều kiện AND) trên trạng thái hiện hành của tập phiếu nguồn.
        """
        if start_date and end_date and start_date > end_date:
            raise DashboardServiceError("Ngày bắt đầu lọc không được lớn hơn ngày kết thúc.")

        filtered: List[WarrantyTicket] = []
        model_query = model_name.strip().lower() if model_name else None

        for ticket in self.repository.tickets.values():
            ticket_date = ticket.created_at.date()
            if start_date and ticket_date < start_date:
                continue
            if end_date and ticket_date > end_date:
                continue
            if technician_id and ticket.current_technician_id != technician_id:
                continue
            if status and ticket.status != status:
                continue
            if model_query:
                device = self.repository.devices.get(ticket.device_id)
                if not device or model_query not in device.model_name.lower():
                    continue

            filtered.append(ticket)

        return filtered

    def get_dashboard_summary(
        self,
        actor_user_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        technician_id: Optional[str] = None,
        status: Optional[TicketStatus] = None,
        model_name: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        FR_DASH_01: Tổng hợp toàn diện chỉ số vận hành từ tập phiếu nguồn sau lọc:
        - KPI tổng quan & tỷ lệ hoàn thành / quá hạn
        - Phân bố 9 trạng thái vòng đời (FSM Hình 3.7)
        - Phân bố hình thức tiếp nhận (Lấy trong ngày / Giữ máy 3-7 ngày)
        - Phân bố kết luận thẩm định bảo hành (Đủ ĐK / Không đủ ĐK / Chưa đủ TT)
        - Phân bố khối lượng công việc theo Kỹ thuật viên hiện hành
        - Xu hướng tiếp nhận theo ngày & danh sách phiếu quá hạn cần xử lý
        """
        self._verify_admin_access(actor_user_id)

        tickets = self.filter_tickets(
            start_date=start_date,
            end_date=end_date,
            technician_id=technician_id,
            status=status,
            model_name=model_name,
        )

        # Ánh xạ nhanh ticket_id -> assessment để tra cứu O(1)
        assessment_by_ticket = {
            a.ticket_id: a for a in self.repository.assessments.values()
        }

        status_counts: Dict[str, int] = {st.value: 0 for st in TicketStatus}
        intake_counts: Dict[str, int] = {
            IntakeType.SAME_DAY.value: 0,
            IntakeType.HOLD_FOR_REPAIR.value: 0,
        }
        eligibility_counts: Dict[str, int] = {
            WarrantyEligibility.ELIGIBLE.value: 0,
            WarrantyEligibility.INELIGIBLE.value: 0,
            WarrantyEligibility.INSUFFICIENT_INFO.value: 0,
        }
        model_counts: Dict[str, int] = {}
        daily_trend: Dict[str, int] = {}
        overdue_list: List[Dict[str, Any]] = []
        tech_workload: Dict[str, Dict[str, Any]] = {}

        today = self.clock_service.today()
        closed_statuses = {TicketStatus.RETURNED, TicketStatus.CANCELLED}
        completed_count = 0
        waiting_parts_count = 0

        for t in tickets:
            st_key = t.status.value if isinstance(t.status, TicketStatus) else str(t.status)
            status_counts[st_key] = status_counts.get(st_key, 0) + 1

            if t.status == TicketStatus.RETURNED:
                completed_count += 1
            if t.status == TicketStatus.WAITING_FOR_PARTS:
                waiting_parts_count += 1

            intake_key = t.intake_type.value if isinstance(t.intake_type, IntakeType) else str(t.intake_type)
            intake_counts[intake_key] = intake_counts.get(intake_key, 0) + 1

            # Thống kê kết luận thẩm định bảo hành
            ass = assessment_by_ticket.get(t.ticket_id)
            if ass:
                el_key = ass.eligibility.value if isinstance(ass.eligibility, WarrantyEligibility) else str(ass.eligibility)
                eligibility_counts[el_key] = eligibility_counts.get(el_key, 0) + 1
            else:
                eligibility_counts[WarrantyEligibility.INSUFFICIENT_INFO.value] += 1

            # Xu hướng theo ngày tiếp nhận
            day_str = t.created_at.date().isoformat()
            daily_trend[day_str] = daily_trend.get(day_str, 0) + 1

            # Thống kê dòng máy
            device = self.repository.devices.get(t.device_id)
            m_name = device.model_name if device else "Thiết bị khác"
            serial_no = device.serial_number if device else "N/A"
            model_counts[m_name] = model_counts.get(m_name, 0) + 1

            # Kiểm tra quá hạn trả (BR08: loại trừ Đã trả / Đã hủy)
            is_overdue = t.status not in closed_statuses and t.promised_return_date < today
            if is_overdue:
                days_late = (today - t.promised_return_date).days
                tech_user = self.repository.users.get(t.current_technician_id) if t.current_technician_id else None
                overdue_list.append({
                    "ticket_id": t.ticket_id,
                    "model_name": m_name,
                    "serial_number": serial_no,
                    "status": st_key,
                    "promised_return_date": t.promised_return_date.isoformat(),
                    "days_overdue": days_late,
                    "technician_id": t.current_technician_id or "CHƯA PHÂN CÔNG",
                    "technician_name": tech_user.full_name if tech_user else "Chưa phân công",
                })

            # Phân bố công việc theo Kỹ thuật viên hiện hành
            if t.current_technician_id:
                tech_id = t.current_technician_id
                if tech_id not in tech_workload:
                    tech_user = self.repository.users.get(tech_id)
                    tech_name = tech_user.full_name if tech_user else tech_id
                    tech_workload[tech_id] = {
                        "technician_id": tech_id,
                        "technician_name": tech_name,
                        "assigned_tickets": 0,
                        "in_progress_tickets": 0,
                        "completed_tickets": 0,
                        "overdue_tickets": 0,
                    }
                tech_workload[tech_id]["assigned_tickets"] += 1
                if t.status == TicketStatus.RETURNED:
                    tech_workload[tech_id]["completed_tickets"] += 1
                elif t.status not in closed_statuses:
                    tech_workload[tech_id]["in_progress_tickets"] += 1
                if is_overdue:
                    tech_workload[tech_id]["overdue_tickets"] += 1

        total = len(tickets)
        in_progress_total = total - completed_count - status_counts[TicketStatus.CANCELLED.value]
        completion_rate = round((completed_count / total * 100), 2) if total > 0 else 0.0
        overdue_rate = round((len(overdue_list) / total * 100), 2) if total > 0 else 0.0

        overdue_list.sort(key=lambda x: x["days_overdue"], reverse=True)
        sorted_trend = dict(sorted(daily_trend.items()))

        return {
            "snapshot_at": self.clock_service.now().isoformat(),
            "filters_applied": {
                "start_date": start_date.isoformat() if start_date else "ALL",
                "end_date": end_date.isoformat() if end_date else "ALL",
                "technician_id": technician_id or "ALL",
                "status": status.value if status else "ALL",
                "model_name": model_name or "ALL",
            },
            "kpi": {
                "total_tickets": total,
                "completed_tickets": completed_count,
                "in_progress_tickets": in_progress_total,
                "waiting_parts_tickets": waiting_parts_count,
                "overdue_tickets": len(overdue_list),
                "completion_rate_percent": completion_rate,
                "overdue_rate_percent": overdue_rate,
            },
            # Tương thích ngược các khóa top-level cho unit test
            "total_tickets": total,
            "overdue_tickets": len(overdue_list),
            "by_status": status_counts,
            "by_intake_type": intake_counts,
            "by_eligibility": eligibility_counts,
            "by_model": model_counts,
            "daily_trend": sorted_trend,
            "technician_distribution": list(tech_workload.values()),
            "overdue_details": overdue_list[:30],
        }

    def export_report_excel(
        self,
        actor_user_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        technician_id: Optional[str] = None,
        status: Optional[TicketStatus] = None,
        model_name: Optional[str] = None,
    ) -> io.BytesIO:
        """
        FR_DASH_03: Xuất báo cáo Excel CSV (UTF-8 BOM) ghi rõ điều kiện lọc,
        thời điểm chốt dữ liệu và toàn bộ bảng số liệu đối chiếu.
        """
        summary = self.get_dashboard_summary(
            actor_user_id=actor_user_id,
            start_date=start_date,
            end_date=end_date,
            technician_id=technician_id,
            status=status,
            model_name=model_name,
        )

        text_buffer = io.StringIO()
        writer = csv.writer(text_buffer)

        writer.writerow(["BAO CAO THONG KE HOAT DONG BAO HANH - CONG TY MAY TINH HUNG THIEN"])
        writer.writerow(["Thoi diem chot du lieu", summary["snapshot_at"]])
        writer.writerow(["Dieu kien loc ap dung", str(summary["filters_applied"])])
        writer.writerow([])

        writer.writerow(["I. TONG QUAN CHI SO KPI", "GIA TRI"])
        writer.writerow(["Tong so phieu theo bo loc", summary["kpi"]["total_tickets"]])
        writer.writerow(["Dang xu ly ky thuat", summary["kpi"]["in_progress_tickets"]])
        writer.writerow(["Dang cho linh kien (WAITING_FOR_PARTS)", summary["kpi"]["waiting_parts_tickets"]])
        writer.writerow(["Da hoan thanh & tra may (RETURNED)", summary["kpi"]["completed_tickets"]])
        writer.writerow(["So phieu qua han tra", summary["kpi"]["overdue_tickets"]])
        writer.writerow(["Ty le hoan thanh (%)", f"{summary['kpi']['completion_rate_percent']}%"])
        writer.writerow([])

        writer.writerow(["II. PHAN BO THEO 9 TRANG THAI VONG DOI", "SO LUONG"])
        for st_name, count in summary["by_status"].items():
            writer.writerow([st_name, count])
        writer.writerow([])

        writer.writerow(["III. PHAN BO KET LUAN THAM DINH BAO HANH", "SO LUONG"])
        for el_name, count in summary["by_eligibility"].items():
            writer.writerow([el_name, count])
        writer.writerow([])

        writer.writerow(["IV. HIEU SUAT KY THUAT VIEN", "Ho ten", "Tong giao", "Dang xu ly", "Hoan thanh", "Qua han"])
        for tech in summary["technician_distribution"]:
            writer.writerow([
                tech["technician_id"],
                tech["technician_name"],
                tech["assigned_tickets"],
                tech["in_progress_tickets"],
                tech["completed_tickets"],
                tech["overdue_tickets"],
            ])

        byte_stream = io.BytesIO(text_buffer.getvalue().encode("utf-8-sig"))
        byte_stream.seek(0)
        return byte_stream

    def export_report_pdf(
        self,
        actor_user_id: str,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        technician_id: Optional[str] = None,
        status: Optional[TicketStatus] = None,
        model_name: Optional[str] = None,
    ) -> io.BytesIO:
        """
        FR_DASH_03 & NFR_COMP_01: Xuất báo cáo PDF 1.4 chuẩn khổ giấy A4 (595x842 pt),
        không bị cắt xén lề, tự động phân trang nhiều trang.
        """
        summary = self.get_dashboard_summary(
            actor_user_id=actor_user_id,
            start_date=start_date,
            end_date=end_date,
            technician_id=technician_id,
            status=status,
            model_name=model_name,
        )

        f_info = summary["filters_applied"]
        kpi = summary["kpi"]
        lines = [
            "BAO CAO THONG KE BAO HANH - TRUNG TAM KY THUAT HUNG THIEN",
            f"Thoi diem chot du lieu: {summary['snapshot_at']}",
            f"Bo loc: Tu={f_info['start_date']} | Den={f_info['end_date']} | KTV={f_info['technician_id']} | TT={f_info['status']} | May={f_info['model_name']}",
            "=====================================================================================",
            f"TONG PHIEU: {kpi['total_tickets']}  |  HOAN THANH: {kpi['completed_tickets']} ({kpi['completion_rate_percent']}%)  |  QUA HAN: {kpi['overdue_tickets']}",
            "=====================================================================================",
            "1. PHAN BO PHIEU THEO 9 TRANG THAI VONG DOI (FSM):",
        ]
        for st_name, count in summary["by_status"].items():
            lines.append(f"   - {st_name:<30}: {count} phieu")

        lines.append("")
        lines.append("2. PHAN BO KET LUAN THAM DINH BAO HANH:")
        for el_name, count in summary["by_eligibility"].items():
            lines.append(f"   - {el_name:<30}: {count} phieu")

        lines.append("")
        lines.append("3. PHAN BO CONG VIEC THEO KY THUAT VIEN:")
        if not summary["technician_distribution"]:
            lines.append("   - Khong co du lieu phan cong.")
        else:
            for tech in summary["technician_distribution"]:
                lines.append(
                    f"   - {tech['technician_name']} ({tech['technician_id']}): "
                    f"Giao={tech['assigned_tickets']}, DangXuLy={tech['in_progress_tickets']}, "
                    f"Xong={tech['completed_tickets']}, QuaHan={tech['overdue_tickets']}"
                )

        lines_per_page = 48
        pages_lines = [
            lines[i : i + lines_per_page] for i in range(0, len(lines), lines_per_page)
        ] or [[]]

        pdf_objects: List[bytes] = []
        page_obj_ids = []
        next_id = 4
        for _ in pages_lines:
            page_obj_ids.append((next_id, next_id + 1))
            next_id += 2

        kids_str = " ".join(f"{p_id} 0 R" for p_id, _ in page_obj_ids)
        pdf_objects.append(b"1 0 obj\n<< /Type /Catalog /Pages 2 0 R >>\nendobj\n")
        pdf_objects.append(
            f"2 0 obj\n<< /Type /Pages /Kids [{kids_str}] /Count {len(page_obj_ids)} >>\nendobj\n".encode("ascii")
        )
        pdf_objects.append(
            b"3 0 obj\n<< /Type /Font /Subtype /Type1 /BaseFont /Courier >>\nendobj\n"
        )

        for idx, (page_id, content_id) in enumerate(page_obj_ids):
            page_lines = pages_lines[idx] + ["", f"Trang {idx + 1}/{len(page_obj_ids)} - Kho giay chuan A4 (595x842 pt)"]
            ops = ["BT", "/F1 9.5 Tf", "40 800 Td", "14 TL"]
            for line in page_lines:
                safe = line.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")
                ops.append(f"({safe}) Tj T*")
            ops.append("ET")
            stream_bytes = "\n".join(ops).encode("latin-1", errors="replace")

            pdf_objects.append(
                f"{page_id} 0 obj\n<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
                f"/Contents {content_id} 0 R /Resources << /Font << /F1 3 0 R >> >> >>\nendobj\n".encode("ascii")
            )
            pdf_objects.append(
                f"{content_id} 0 obj\n<< /Length {len(stream_bytes)} >>\nstream\n".encode("ascii")
                + stream_bytes
                + b"\nendstream\nendobj\n"
            )

        out = io.BytesIO()
        out.write(b"%PDF-1.4\n")
        offsets = [0]
        for obj in pdf_objects:
            offsets.append(out.tell())
            out.write(obj)

        xref_start = out.tell()
        out.write(f"xref\n0 {len(pdf_objects) + 1}\n".encode("ascii"))
        out.write(b"0000000000 65535 f \n")
        for off in offsets[1:]:
            out.write(f"{off:010d} 00000 n \n".encode("ascii"))

        out.write(
            f"trailer\n<< /Size {len(pdf_objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_start}\n%%EOF\n".encode("ascii")
        )
        out.seek(0)
        return out