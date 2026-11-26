import React from "react";
import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  act,
  cleanup,
  fireEvent,
  render,
  screen,
} from "@testing-library/react";
import userEvent from "@testing-library/user-event";
import WarrantyLookup from "../app/warranty_lookup";

const ticketId = "TKT_20261126_1";
const secretCode = "HT-DEMO-001";
const publicData = {
  ticket_id: ticketId,
  device_model: "Dell XPS 15 9520",
  device_serial_masked: "SN****00",
  status: "UNDER_REPAIR",
  promised_return_date: "2026-11-28",
};

function response(data = publicData, status = 200, headers = {}) {
  return {
    ok: status >= 200 && status < 300,
    status,
    headers: { get: (name) => headers[name] ?? null },
    json: async () => data,
  };
}

function fillForm(code = ticketId, secret = secretCode) {
  fireEvent.change(screen.getByLabelText(/Mã phiếu bảo hành/), {
    target: { value: code },
  });
  fireEvent.change(screen.getByLabelText(/Mã tra cứu bí mật/), {
    target: { value: secret },
  });
}

function submit() {
  fireEvent.click(screen.getByRole("button", { name: "Tra cứu bảo hành" }));
}

beforeEach(() => {
  vi.stubGlobal("fetch", vi.fn().mockResolvedValue(response()));
});

afterEach(() => {
  cleanup();
  vi.useRealTimers();
  vi.unstubAllGlobals();
  vi.restoreAllMocks();
});

describe("customer lookup journey", () => {
  it("requires both codes and focuses the first incomplete field", () => {
    render(<WarrantyLookup />);
    submit();
    expect(
      screen.getByText("Vui lòng nhập mã phiếu bảo hành."),
    ).toBeInTheDocument();
    expect(
      screen.getByText("Vui lòng nhập mã tra cứu bí mật."),
    ).toBeInTheDocument();
    expect(screen.getByLabelText(/Mã phiếu bảo hành/)).toHaveFocus();
    expect(fetch).not.toHaveBeenCalled();
  });

  it("submits both codes in a POST body and displays the verified public result", async () => {
    render(<WarrantyLookup />);
    fillForm("  tkt_20261126_1  ");
    submit();
    expect(
      await screen.findByRole("heading", { name: "Thông tin bảo hành" }),
    ).toHaveFocus();
    expect(screen.getByText("Dell XPS 15 9520")).toBeInTheDocument();
    expect(screen.getByText("SN****00")).toBeInTheDocument();
    expect(screen.getByText("Đang sửa chữa")).toBeInTheDocument();
    expect(screen.getByText("28/11/2026")).toBeInTheDocument();
    expect(fetch).toHaveBeenCalledWith(
      "/api/v1/portal/lookups",
      expect.objectContaining({
        method: "POST",
        cache: "no-store",
        body: JSON.stringify({
          ticket_id: ticketId,
          plain_secret_code: secretCode,
        }),
      }),
    );
    expect(fetch.mock.calls[0][0]).not.toContain(secretCode);
  });

  it("hides and reveals the secret without submitting the form", async () => {
    const user = userEvent.setup();
    render(<WarrantyLookup />);
    const secret = screen.getByLabelText(/Mã tra cứu bí mật/);
    expect(secret).toHaveAttribute("type", "password");
    await user.click(screen.getByRole("button", { name: "Hiện mã tra cứu" }));
    expect(secret).toHaveAttribute("type", "text");
    await user.click(screen.getByRole("button", { name: "Ẩn mã tra cứu" }));
    expect(secret).toHaveAttribute("type", "password");
    expect(fetch).not.toHaveBeenCalled();
  });

  it("clears the old result on edits and never displays backend error details", async () => {
    fetch
      .mockResolvedValueOnce(response())
      .mockResolvedValueOnce(
        response({ detail: "PRIVATE_CUSTOMER_0987654321" }, 404),
      );
    render(<WarrantyLookup />);
    fillForm();
    submit();
    await screen.findByText("Dell XPS 15 9520");
    fireEvent.change(screen.getByLabelText(/Mã tra cứu bí mật/), {
      target: { value: "WRONG_CODE" },
    });
    expect(screen.queryByTestId("lookup-result")).not.toBeInTheDocument();
    submit();
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Chưa xác minh được thông tin",
    );
    expect(screen.queryByText(/PRIVATE_CUSTOMER/)).not.toBeInTheDocument();
  });

  it("prevents duplicate requests while a lookup is pending", async () => {
    let resolveRequest;
    fetch.mockImplementationOnce(
      () =>
        new Promise((resolve) => {
          resolveRequest = resolve;
        }),
    );
    render(<WarrantyLookup />);
    fillForm();
    submit();
    const busyButton = await screen.findByRole("button", {
      name: "Đang tra cứu…",
    });
    expect(busyButton).toBeDisabled();
    fireEvent.click(busyButton);
    expect(fetch).toHaveBeenCalledTimes(1);
    resolveRequest(response());
    await screen.findByTestId("lookup-result");
  });

  it("shows rate-limit feedback and respects Retry-After", async () => {
    fetch.mockResolvedValue(response(null, 429, { "Retry-After": "60" }));
    render(<WarrantyLookup />);
    fillForm();
    submit();
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Vui lòng chờ trước khi tra cứu lại",
    );
    expect(
      screen.getByRole("button", { name: /Thử lại sau \d+ giây/ }),
    ).toBeDisabled();
  });

  it("handles a lost connection and allows a new attempt", async () => {
    fetch
      .mockRejectedValueOnce(new TypeError("Network failed"))
      .mockResolvedValueOnce(response());
    render(<WarrantyLookup />);
    fillForm();
    submit();
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Chưa kết nối được với trung tâm",
    );
    submit();
    expect(await screen.findByTestId("lookup-result")).toHaveTextContent(
      "Đang sửa chữa",
    );
  });

  it("allows a new lookup when the retry period has expired", async () => {
    vi.useFakeTimers();
    vi.setSystemTime(new Date("2026-11-26T03:00:00Z"));
    fetch
      .mockResolvedValueOnce(response(null, 429, { "Retry-After": "60" }))
      .mockResolvedValueOnce(response());
    render(<WarrantyLookup />);
    fillForm();
    await act(async () => {
      submit();
    });
    expect(
      screen.getByRole("button", { name: /Thử lại sau \d+ giây/ }),
    ).toBeDisabled();
    await act(async () => {
      vi.advanceTimersByTime(60000);
    });
    expect(screen.queryByRole("alert")).not.toBeInTheDocument();
    expect(
      screen.getByRole("button", { name: "Tra cứu bảo hành" }),
    ).toBeEnabled();
    await act(async () => {
      submit();
    });
    expect(screen.getByTestId("lookup-result")).toHaveTextContent(
      "Đang sửa chữa",
    );
  });

  it.each([
    { ...publicData, ticket_id: "TKT_20261126_999" },
    { ...publicData, status: "UNRECOGNIZED_STATUS" },
    { ...publicData, promised_return_date: null },
  ])("rejects an inconsistent API response", async (data) => {
    fetch.mockResolvedValue(response(data));
    render(<WarrantyLookup />);
    fillForm();
    submit();
    expect(await screen.findByRole("alert")).toHaveTextContent(
      "Chưa thể lấy kết quả",
    );
    expect(screen.queryByTestId("lookup-result")).not.toBeInTheDocument();
  });

  it("shows cancellation without implying that the repair journey completed", async () => {
    fetch.mockResolvedValue(response({ ...publicData, status: "CANCELLED" }));
    render(<WarrantyLookup />);
    fillForm();
    submit();
    expect(await screen.findByText("Đã hủy")).toBeInTheDocument();
    expect(
      screen.queryByLabelText("Các giai đoạn xử lý tổng quan"),
    ).not.toBeInTheDocument();
  });

  it("renders device text safely and does not expose extra response fields", async () => {
    const deviceName = '<img src=x onerror="alert(1)">';
    fetch.mockResolvedValue(
      response({
        ...publicData,
        device_model: deviceName,
        work_logs: ["PRIVATE_WORK_LOG"],
        phone_number: "PRIVATE_PHONE",
      }),
    );
    const { container } = render(<WarrantyLookup />);
    fillForm();
    submit();
    expect(await screen.findByText(deviceName)).toBeInTheDocument();
    expect(container.querySelector("img")).toBeNull();
    expect(screen.queryByText("PRIVATE_WORK_LOG")).not.toBeInTheDocument();
    expect(screen.queryByText("PRIVATE_PHONE")).not.toBeInTheDocument();
  });

  it("resets both codes and returns keyboard focus to the ticket field", async () => {
    render(<WarrantyLookup />);
    fillForm();
    submit();
    await screen.findByTestId("lookup-result");
    fireEvent.click(screen.getByRole("button", { name: "Tra cứu phiếu khác" }));
    expect(screen.getByLabelText(/Mã phiếu bảo hành/)).toHaveValue("");
    expect(screen.getByLabelText(/Mã tra cứu bí mật/)).toHaveValue("");
    expect(screen.getByLabelText(/Mã phiếu bảo hành/)).toHaveFocus();
    expect(screen.queryByTestId("lookup-result")).not.toBeInTheDocument();
  });
});
