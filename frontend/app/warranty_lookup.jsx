"use client";

import React, { useEffect, useRef, useState } from "react";
import { lookupWarranty, STATUS_DETAILS } from "../lib/warranty_api";

function Icon({ name, size = 20, className = "" }) {
  const paths = {
    search: (
      <>
        <circle cx="10.5" cy="10.5" r="6.5" />
        <path d="m16 16 4.5 4.5" />
      </>
    ),
    shield: (
      <>
        <path d="M12 3 4.5 6v5.5c0 4 2.7 7.2 7.5 9.5 4.8-2.3 7.5-5.5 7.5-9.5V6Z" />
        <path d="m8.5 11.5 2.5 2.5 4.5-5" />
      </>
    ),
    lock: (
      <>
        <rect x="5" y="10" width="14" height="11" rx="2" />
        <path d="M8 10V7a4 4 0 0 1 8 0v3m-4 5v2" />
      </>
    ),
    eye: (
      <>
        <path d="M2 12s3.5-7 10-7 10 7 10 7-3.5 7-10 7S2 12 2 12Z" />
        <circle cx="12" cy="12" r="3" />
      </>
    ),
    hidden: (
      <>
        <path d="m3 3 18 18M9.5 5.3A12 12 0 0 1 12 5c6.5 0 10 7 10 7a19 19 0 0 1-3.2 4.2M6.2 6.2A20 20 0 0 0 2 12s3.5 7 10 7c1.7 0 3.2-.5 4.5-1.2" />
        <path d="M10 10a3 3 0 0 0 4 4" />
      </>
    ),
    device: (
      <>
        <rect x="5" y="3" width="14" height="13" rx="2" />
        <path d="m5 16-3 5h20l-3-5M9 8h6m-6 3h4" />
      </>
    ),
    calendar: (
      <>
        <rect x="3" y="5" width="18" height="16" rx="2" />
        <path d="M7 3v4m10-4v4M3 10h18m-13 5h3m3 0h2" />
      </>
    ),
    info: (
      <>
        <circle cx="12" cy="12" r="9" />
        <path d="M12 11v6m0-10h.01" />
      </>
    ),
    check: <path d="m5 12 4 4L19 6" />,
  };
  return (
    <svg
      aria-hidden="true"
      width={size}
      height={size}
      viewBox="0 0 24 24"
      fill="none"
      stroke="currentColor"
      strokeWidth="1.7"
      strokeLinecap="round"
      strokeLinejoin="round"
      className={className}
    >
      {paths[name]}
    </svg>
  );
}

function LookupResult({ result, onReset, headingRef }) {
  const status = STATUS_DETAILS[result.status];
  const [year, month, day] = result.promised_return_date.split("-");
  const phases = ["Tiếp nhận", "Kiểm tra", "Xử lý", "Chờ trả", "Đã trả"];
  return (
    <section
      className="result-card surface"
      aria-labelledby="result-title"
      data-testid="lookup-result"
    >
      <div className="result-topline">
        <span className="verified-label">
          <Icon name="shield" size={17} /> Đã xác minh thông tin
        </span>
        <span className="eyebrow">KẾT QUẢ TRA CỨU</span>
      </div>
      <h2 id="result-title" tabIndex={-1} ref={headingRef}>
        Thông tin bảo hành
      </h2>
      <p className="result-ticket">{result.ticket_id}</p>
      <div className={`current-status status-${status.tone}`}>
        <span className="status-caption">Trạng thái hiện tại</span>
        <strong>{status.label}</strong>
        <p>{status.description}</p>
      </div>
      <dl className="device-details">
        <div>
          <dt>Thiết bị</dt>
          <dd>{result.device_model}</dd>
        </div>
        <div>
          <dt>Số serial</dt>
          <dd className="mono">{result.device_serial_masked}</dd>
        </div>
        <div className="return-date">
          <dt>
            <Icon name="calendar" size={17} /> Ngày hẹn trả
          </dt>
          <dd>
            <time dateTime={result.promised_return_date}>
              {day}/{month}/{year}
            </time>
          </dd>
        </div>
      </dl>
      {status.phase !== null && (
        <ol
          className="process-steps"
          aria-label="Các giai đoạn xử lý tổng quan"
        >
          {phases.map((phase, index) => (
            <li
              key={phase}
              className={index === status.phase ? "current" : ""}
              aria-current={index === status.phase ? "step" : undefined}
            >
              <span className="process-node">
                {index === status.phase ? (
                  <Icon name="device" size={15} />
                ) : (
                  <span />
                )}
              </span>
              <span>{phase}</span>
            </li>
          ))}
        </ol>
      )}
      <button type="button" className="secondary-button" onClick={onReset}>
        Tra cứu phiếu khác
      </button>
    </section>
  );
}

export default function WarrantyLookup() {
  const [ticketId, setTicketId] = useState("");
  const [secretCode, setSecretCode] = useState("");
  const [showSecret, setShowSecret] = useState(false);
  const [fieldErrors, setFieldErrors] = useState({});
  const [error, setError] = useState(null);
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [retryUntil, setRetryUntil] = useState(0);
  const [remainingSeconds, setRemainingSeconds] = useState(0);
  const ticketRef = useRef(null);
  const secretRef = useRef(null);
  const headingRef = useRef(null);
  const controllerRef = useRef(null);

  useEffect(
    () => () => {
      controllerRef.current?.abort();
      controllerRef.current = null;
    },
    [],
  );
  useEffect(() => {
    if (result) headingRef.current?.focus();
  }, [result]);
  useEffect(() => {
    if (!retryUntil) return;
    const seconds = Math.max(0, Math.ceil((retryUntil - Date.now()) / 1000));
    setRemainingSeconds(seconds);
    if (!seconds) {
      setError((current) => current === "limited" ? null : current);
      return;
    }
    const interval = setInterval(() => {
      const nextSeconds = Math.max(
        0,
        Math.ceil((retryUntil - Date.now()) / 1000),
      );
      setRemainingSeconds(nextSeconds);
      if (!nextSeconds) {
        clearInterval(interval);
        setError((current) => current === "limited" ? null : current);
      }
    }, 1000);
    return () => clearInterval(interval);
  }, [retryUntil]);

  function clearFeedback() {
    setResult(null);
    setError(null);
    setFieldErrors({});
  }

  function resetForm() {
    clearFeedback();
    setTicketId("");
    setSecretCode("");
    setShowSecret(false);
    ticketRef.current?.focus();
  }

  async function handleSubmit(event) {
    event.preventDefault();
    if (controllerRef.current || remainingSeconds > 0) return;
    clearFeedback();
    const errors = {};
    if (!ticketId.trim()) errors.ticket = "Vui lòng nhập mã phiếu bảo hành.";
    if (!secretCode.trim()) errors.secret = "Vui lòng nhập mã tra cứu bí mật.";
    if (Object.keys(errors).length) {
      setFieldErrors(errors);
      (errors.ticket ? ticketRef : secretRef).current?.focus();
      return;
    }
    const controller = new AbortController();
    controllerRef.current = controller;
    setLoading(true);
    try {
      const data = await lookupWarranty(
        ticketId.trim().toUpperCase(),
        secretCode,
        controller.signal,
      );
      setResult(data);
    } catch (failure) {
      if (failure.name !== "AbortError") {
        setError(failure.kind || "server");
        if (failure.kind === "limited") {
          setRemainingSeconds(failure.retryAfter);
          setRetryUntil(Date.now() + failure.retryAfter * 1000);
        }
      }
    } finally {
      if (controllerRef.current === controller) {
        controllerRef.current = null;
        setLoading(false);
      }
    }
  }

  const errorMessages = {
    invalid: [
      "Chưa xác minh được thông tin",
      "Mã phiếu hoặc mã tra cứu chưa đúng. Bạn vui lòng kiểm tra lại cả hai mã trên phiếu tiếp nhận.",
    ],
    input: [
      "Thông tin chưa hợp lệ",
      "Bạn vui lòng kiểm tra mã phiếu và mã tra cứu rồi thử lại.",
    ],
    limited: [
      "Vui lòng chờ trước khi tra cứu lại",
      "Bạn đã tra cứu nhiều lần liên tiếp. Hệ thống sẽ cho phép thử lại sau thời gian chờ.",
    ],
    network: [
      "Chưa kết nối được với trung tâm",
      "Bạn hãy kiểm tra kết nối mạng rồi thử tra cứu lại.",
    ],
    server: [
      "Chưa thể lấy kết quả",
      "Hệ thống tạm thời chưa phản hồi được. Bạn vui lòng thử lại sau.",
    ],
  };

  return (
    <>
      <a className="skip-link" href="#lookup-form">
        Đến phần tra cứu
      </a>
      <header className="site-header">
        <div className="header-inner">
          <a
            href="/"
            className="brand"
            aria-label="Hưng Thiện — trang tra cứu bảo hành"
          >
            <span className="brand-mark">
              HT
              <span />
            </span>
            <span className="brand-wordmark">
              HƯNG THIỆN<small>TRUNG TÂM HỖ TRỢ KỸ THUẬT</small>
            </span>
          </a>
          <nav aria-label="Điều hướng chính">
            <a href="#lookup-form" className="nav-active" aria-current="page">
              Tra cứu bảo hành
            </a>
            <a href="#how-to">Hướng dẫn</a>
          </nav>
        </div>
      </header>
      <main className="main-shell">
        <div className="hero">
          <span className="service-label">
            <span className="label-line" /> CỔNG THÔNG TIN KHÁCH HÀNG
          </span>
          <h1>
            Thiết bị của bạn.
            <br />
            <span>Tiến độ trong tầm tay.</span>
          </h1>
          <p>
            Chủ động theo dõi quá trình bảo hành và ngày hẹn trả,
            <br className="desktop-break" /> chỉ với thông tin trên phiếu tiếp
            nhận.
          </p>
        </div>
        <div className="lookup-layout">
          <section className="form-card surface" aria-labelledby="form-title">
            <div className="card-title-row">
              <span className="icon-square">
                <Icon name="search" size={23} />
              </span>
              <div>
                <h2 id="form-title">Tra cứu tiến độ bảo hành</h2>
                <p>Nhập hai mã để xem thông tin thiết bị.</p>
              </div>
            </div>
            <form
              id="lookup-form"
              onSubmit={handleSubmit}
              noValidate
              autoComplete="off"
              aria-busy={loading}
            >
              <div className="form-field">
                <label htmlFor="ticket-code">
                  Mã phiếu bảo hành <span aria-hidden="true">*</span>
                </label>
                <input
                  id="ticket-code"
                  name="ticket_id"
                  ref={ticketRef}
                  value={ticketId}
                  onChange={(event) => {
                    clearFeedback();
                    setTicketId(event.target.value.toUpperCase());
                  }}
                  placeholder="Ví dụ: TKT_20261126_1"
                  autoComplete="off"
                  autoCapitalize="characters"
                  spellCheck={false}
                  maxLength={64}
                  disabled={loading}
                  aria-invalid={Boolean(fieldErrors.ticket)}
                  aria-describedby={
                    fieldErrors.ticket ? "ticket-error" : "ticket-hint"
                  }
                  required
                />
                {fieldErrors.ticket ? (
                  <p className="field-error" id="ticket-error" role="alert">
                    {fieldErrors.ticket}
                  </p>
                ) : (
                  <p className="field-hint" id="ticket-hint">
                    Mã phiếu được ghi trên phiếu tiếp nhận thiết bị.
                  </p>
                )}
              </div>
              <div className="form-field">
                <label htmlFor="secret-code">
                  Mã tra cứu bí mật <span aria-hidden="true">*</span>
                </label>
                <div className="secret-input">
                  <input
                    id="secret-code"
                    name="plain_secret_code"
                    ref={secretRef}
                    value={secretCode}
                    onChange={(event) => {
                      clearFeedback();
                      setSecretCode(event.target.value);
                    }}
                    type={showSecret ? "text" : "password"}
                    placeholder="Nhập mã tra cứu của bạn"
                    autoComplete="off"
                    autoCapitalize="none"
                    spellCheck={false}
                    maxLength={256}
                    disabled={loading}
                    aria-invalid={Boolean(fieldErrors.secret)}
                    aria-describedby={
                      fieldErrors.secret ? "secret-error" : "secret-hint"
                    }
                    required
                  />
                  <button
                    type="button"
                    className="visibility-button"
                    onClick={() => setShowSecret(!showSecret)}
                    aria-label={
                      showSecret ? "Ẩn mã tra cứu" : "Hiện mã tra cứu"
                    }
                    aria-pressed={showSecret}
                    disabled={loading}
                  >
                    <Icon name={showSecret ? "hidden" : "eye"} />
                  </button>
                </div>
                {fieldErrors.secret ? (
                  <p className="field-error" id="secret-error" role="alert">
                    {fieldErrors.secret}
                  </p>
                ) : (
                  <p className="field-hint" id="secret-hint">
                    Mã được cấp khi tiếp nhận; phân biệt chữ hoa và chữ thường.
                  </p>
                )}
              </div>
              <button
                type="submit"
                className="primary-button"
                disabled={loading || remainingSeconds > 0}
              >
                {loading ? (
                  <>
                    <span className="spinner" /> Đang tra cứu…
                  </>
                ) : remainingSeconds > 0 ? (
                  `Thử lại sau ${remainingSeconds} giây`
                ) : (
                  <>
                    <Icon name="search" /> Tra cứu bảo hành
                  </>
                )}
              </button>
              {error && (
                <div
                  className={`lookup-error ${error === "limited" ? "limit-notice" : ""}`}
                  role="alert"
                >
                  <Icon name="info" />
                  <div>
                    <strong>{errorMessages[error][0]}</strong>
                    <p>{errorMessages[error][1]}</p>
                  </div>
                </div>
              )}
            </form>
            <div className="privacy-note">
              <Icon name="lock" size={17} />
              <p>Kết quả chỉ hiển thị sau khi hai mã được xác minh.</p>
            </div>
          </section>
          <div className="result-region" aria-live="polite" aria-busy={loading}>
            {result ? (
              <LookupResult
                result={result}
                onReset={resetForm}
                headingRef={headingRef}
              />
            ) : (
              <section
                className={`welcome-card surface ${loading ? "is-loading" : ""}`}
                aria-labelledby="welcome-title"
              >
                <div className="device-orbit">
                  <div className="device-emblem">
                    <Icon name="device" size={57} />
                  </div>
                  <span className="shield-emblem">
                    <Icon name="shield" size={24} />
                  </span>
                  <span className="orbit-line orbit-one" />
                  <span className="orbit-line orbit-two" />
                </div>
                <span className="eyebrow">ĐỒNG HÀNH CÙNG THIẾT BỊ CỦA BẠN</span>
                <h2 id="welcome-title">
                  {loading
                    ? "Đang kiểm tra thông tin…"
                    : "Nắm rõ tiến độ, an tâm chờ nhận."}
                </h2>
                <p>
                  {loading
                    ? "Kết quả sẽ hiển thị ngay khi thông tin được xác minh."
                    : "Trạng thái xử lý và ngày hẹn trả sẽ hiển thị tại đây sau khi bạn tra cứu thành công."}
                </p>
                <div className="welcome-benefits">
                  <span>
                    <Icon name="check" size={16} /> Trạng thái hiện tại
                  </span>
                  <span>
                    <Icon name="check" size={16} /> Ngày hẹn trả
                  </span>
                </div>
              </section>
            )}
          </div>
        </div>
        <section className="how-to" id="how-to" aria-labelledby="how-to-title">
          <div className="help-intro">
            <span className="eyebrow">TRA CỨU THẬT ĐƠN GIẢN</span>
            <h2 id="how-to-title">Bạn cần chuẩn bị gì?</h2>
            <p>Giữ phiếu tiếp nhận bên cạnh để nhập đúng thông tin.</p>
          </div>
          <ol className="help-steps">
            <li>
              <span className="step-number">1</span>
              <div>
                <h3>Tìm mã phiếu</h3>
                <p>Lấy mã phiếu bảo hành trên phiếu tiếp nhận thiết bị.</p>
              </div>
            </li>
            <li>
              <span className="step-number">2</span>
              <div>
                <h3>Nhập mã tra cứu</h3>
                <p>Sử dụng mã bí mật được cấp cùng phiếu của bạn.</p>
              </div>
            </li>
            <li>
              <span className="step-number">3</span>
              <div>
                <h3>Xem tiến độ</h3>
                <p>Kiểm tra trạng thái xử lý và ngày hẹn trả thiết bị.</p>
              </div>
            </li>
          </ol>
        </section>
        <div className="support-note">
          <Icon name="info" size={19} />
          <p>
            <strong>Bạn chưa tìm thấy mã?</strong> Vui lòng kiểm tra lại phiếu
            tiếp nhận hoặc liên hệ trung tâm để được hỗ trợ.
          </p>
        </div>
      </main>
      <footer className="site-footer">
        <div>
          <span>Hưng Thiện</span>
          <p>Trung tâm hỗ trợ kỹ thuật</p>
        </div>
        <p>Cổng tra cứu tiến độ bảo hành</p>
      </footer>
    </>
  );
}
