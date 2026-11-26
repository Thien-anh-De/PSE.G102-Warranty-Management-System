export const STATUS_DETAILS = {
  RECEIVED: {
    label: "Đã tiếp nhận",
    description: "Trung tâm đã tiếp nhận thiết bị của bạn.",
    tone: "blue",
    phase: 0,
  },
  PENDING_ASSIGNMENT: {
    label: "Chờ phân công",
    description: "Thiết bị đang chờ phân công kỹ thuật viên phụ trách.",
    tone: "blue",
    phase: 0,
  },
  UNDER_INSPECTION: {
    label: "Đang kiểm tra",
    description: "Kỹ thuật viên đang kiểm tra tình trạng thiết bị.",
    tone: "blue",
    phase: 1,
  },
  UNDER_REPAIR: {
    label: "Đang sửa chữa",
    description: "Kỹ thuật viên đang xử lý thiết bị của bạn.",
    tone: "blue",
    phase: 2,
  },
  WAITING_FOR_PARTS: {
    label: "Chờ linh kiện",
    description: "Thiết bị đang chờ linh kiện để tiếp tục xử lý.",
    tone: "amber",
    phase: 2,
  },
  WAITING_FOR_RESULT_CHECK: {
    label: "Chờ kiểm tra kết quả",
    description: "Thiết bị đang chờ kiểm tra kết quả xử lý.",
    tone: "blue",
    phase: 2,
  },
  WAITING_FOR_RETURN: {
    label: "Chờ trả",
    description: "Thiết bị đang chờ bàn giao lại cho bạn.",
    tone: "green",
    phase: 3,
  },
  RETURNED: {
    label: "Đã trả",
    description: "Thiết bị đã được bàn giao lại cho khách hàng.",
    tone: "green",
    phase: 4,
  },
  CANCELLED: {
    label: "Đã hủy",
    description: "Phiếu bảo hành này đã kết thúc theo hình thức hủy.",
    tone: "neutral",
    phase: null,
  },
};

export class PortalLookupError extends Error {
  constructor(kind, retryAfter = 0) {
    super(kind);
    this.name = "PortalLookupError";
    this.kind = kind;
    this.retryAfter = retryAfter;
  }
}

export async function lookupWarranty(ticketId, secretCode, signal) {
  let response;
  try {
    response = await fetch("/api/v1/portal/lookups", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        ticket_id: ticketId,
        plain_secret_code: secretCode,
      }),
      cache: "no-store",
      signal,
    });
  } catch (error) {
    if (error.name === "AbortError") throw error;
    throw new PortalLookupError("network");
  }

  if (!response.ok) {
    if (response.status === 429) {
      const seconds = Number(response.headers.get("Retry-After"));
      throw new PortalLookupError(
        "limited",
        Number.isFinite(seconds) && seconds > 0
          ? Math.min(Math.ceil(seconds), 86400)
          : 60,
      );
    }
    if (response.status === 404) throw new PortalLookupError("invalid");
    if (response.status === 422) throw new PortalLookupError("input");
    throw new PortalLookupError("server");
  }

  let data;
  try {
    data = await response.json();
  } catch {
    throw new PortalLookupError("server");
  }
  const valid =
    data &&
    data.ticket_id === ticketId &&
    typeof data.device_model === "string" &&
    typeof data.device_serial_masked === "string" &&
    Object.hasOwn(STATUS_DETAILS, data.status) &&
    typeof data.promised_return_date === "string" &&
    /^\d{4}-\d{2}-\d{2}$/.test(data.promised_return_date);
  if (!valid) throw new PortalLookupError("server");
  return data;
}
