-- 16. Due date history

CREATE TABLE due_date_history (
    change_id BIGINT
        GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    old_due_date DATE NOT NULL,

    new_due_date DATE NOT NULL,

    changed_by_user_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    reason TEXT NOT NULL,

    changed_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_due_date_history_dates
        CHECK (old_due_date <> new_due_date),

    CONSTRAINT chk_due_date_history_reason
        CHECK (length(trim(reason)) > 0)
);

CREATE INDEX idx_due_date_history_ticket_id
ON due_date_history(ticket_id);

CREATE INDEX idx_due_date_history_changed_at
ON due_date_history(changed_at);


-- 17. Return checks

CREATE TABLE return_checks (
    check_id BIGINT
        GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    components_signature_verified BOOLEAN
        NOT NULL DEFAULT FALSE,

    seal_verified BOOLEAN
        NOT NULL DEFAULT FALSE,

    test_run_passed BOOLEAN
        NOT NULL DEFAULT FALSE,

    customer_accepted BOOLEAN
        NOT NULL DEFAULT FALSE,

    evidence TEXT NOT NULL,

    discrepancy_notes TEXT,

    checked_by_user_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    checked_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_return_checks_evidence
        CHECK (length(trim(evidence)) > 0)
);

CREATE INDEX idx_return_checks_ticket_id
ON return_checks(ticket_id);

CREATE INDEX idx_return_checks_checked_at
ON return_checks(checked_at);

-- 18. Ticket cancellations

CREATE TABLE ticket_cancellations (
    cancellation_id BIGINT
        GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    device_returned_to_customer BOOLEAN NOT NULL,

    return_evidence TEXT NOT NULL,

    cancelled_by_user_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    cancelled_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_ticket_cancellations_ticket_id
        UNIQUE (ticket_id),

    CONSTRAINT chk_ticket_cancellations_returned
        CHECK (device_returned_to_customer = TRUE),

    CONSTRAINT chk_ticket_cancellations_evidence
        CHECK (length(trim(return_evidence)) > 0)
);

CREATE INDEX idx_ticket_cancellations_cancelled_at
ON ticket_cancellations(cancelled_at);


-- 19. SLA email logs

CREATE TABLE sla_email_logs (
    email_log_id BIGINT
        GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    report_date DATE NOT NULL,

    recipient VARCHAR(255) NOT NULL,

    subject TEXT NOT NULL,

    body_text TEXT NOT NULL,

    total_red_alert INTEGER NOT NULL
        DEFAULT 0,

    total_attention INTEGER NOT NULL
        DEFAULT 0,

    send_status VARCHAR(20) NOT NULL
        DEFAULT 'PENDING',

    attempt_number INTEGER NOT NULL
        DEFAULT 1,

    error_message TEXT,

    generated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    sent_at TIMESTAMPTZ,

    CONSTRAINT uq_sla_email_logs_attempt
        UNIQUE (
            report_date,
            recipient,
            attempt_number
        ),

    CONSTRAINT chk_sla_email_logs_status
        CHECK (send_status IN (
            'PENDING',
            'ACCEPTED',
            'FAILED'
        )),

    CONSTRAINT chk_sla_email_logs_totals
        CHECK (
            total_red_alert >= 0
            AND total_attention >= 0
        ),

    CONSTRAINT chk_sla_email_logs_attempt
        CHECK (attempt_number >= 1)
);

CREATE INDEX idx_sla_email_logs_report_date
ON sla_email_logs(report_date);

CREATE INDEX idx_sla_email_logs_send_status
ON sla_email_logs(send_status);



-- 20. SLA email items

CREATE TABLE sla_email_items (
    email_log_id BIGINT NOT NULL
        REFERENCES sla_email_logs(email_log_id),

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    sla_group VARCHAR(20) NOT NULL,

    device_label TEXT NOT NULL,

    technician_label TEXT,

    promised_return_date DATE NOT NULL,

    ticket_status VARCHAR(30) NOT NULL,

    reason TEXT NOT NULL,

    PRIMARY KEY (email_log_id, ticket_id),

    CONSTRAINT chk_sla_email_items_group
        CHECK (sla_group IN (
            'RED_ALERT',
            'ATTENTION'
        )),

    CONSTRAINT chk_sla_email_items_status
        CHECK (ticket_status IN (
            'RECEIVED',
            'PENDING_ASSIGNMENT',
            'UNDER_INSPECTION',
            'UNDER_REPAIR',
            'WAITING_FOR_PARTS',
            'WAITING_FOR_RESULT_CHECK'
        ))
);

CREATE INDEX idx_sla_email_items_ticket_id
ON sla_email_items(ticket_id);

CREATE INDEX idx_sla_email_items_sla_group
ON sla_email_items(sla_group);



-- 21. Audit logs

CREATE TABLE audit_logs (
    audit_id BIGINT
        GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    user_id VARCHAR(36)
        REFERENCES users(user_id),

    event_type VARCHAR(50) NOT NULL,

    object_type VARCHAR(50) NOT NULL,

    object_id VARCHAR(100),

    event_details JSONB NOT NULL
        DEFAULT '{}'::JSONB,

    event_result VARCHAR(20) NOT NULL,

    event_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_audit_logs_result
        CHECK (event_result IN (
            'SUCCESS',
            'FAILED'
        )),

    CONSTRAINT chk_audit_logs_event_type
        CHECK (length(trim(event_type)) > 0)
);

CREATE INDEX idx_audit_logs_user_id
ON audit_logs(user_id);

CREATE INDEX idx_audit_logs_event_type
ON audit_logs(event_type);

CREATE INDEX idx_audit_logs_event_at
ON audit_logs(event_at);

CREATE INDEX idx_audit_logs_object
ON audit_logs(object_type, object_id);