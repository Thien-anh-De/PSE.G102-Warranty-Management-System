-- 08. Warranty assessments

CREATE TABLE warranty_assessments (
    assessment_id VARCHAR(36) PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    purchase_date DATE NOT NULL,
    incident_date DATE NOT NULL,

    is_warranty_valid BOOLEAN NOT NULL,

    defect_origin VARCHAR(20) NOT NULL,

    eligibility VARCHAR(30) NOT NULL,
    resolution VARCHAR(30) NOT NULL,

    customer_agreed BOOLEAN NOT NULL
        DEFAULT FALSE,

    original_device_serial VARCHAR(100),
    replacement_device_serial VARCHAR(100),

    warranty_evidence TEXT,
    policy_evidence TEXT,

    assessed_by_user_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_warranty_assessments_ticket_id
        UNIQUE (ticket_id),

    CONSTRAINT chk_assessments_defect_origin
        CHECK (defect_origin IN (
            'MANUFACTURER',
            'USER_DAMAGE',
            'UNCLEAR'
        )),

    CONSTRAINT chk_assessments_eligibility
        CHECK (eligibility IN (
            'ELIGIBLE',
            'INELIGIBLE',
            'INSUFFICIENT_INFO'
        )),

    CONSTRAINT chk_assessments_resolution
        CHECK (resolution IN (
            'ONE_TO_ONE_EXCHANGE',
            'FREE_REPAIR',
            'PAID_REPAIR',
            'PENDING_DECISION'
        )),

    CONSTRAINT chk_assessments_dates
        CHECK (incident_date >= purchase_date)
);

CREATE INDEX idx_warranty_assessments_eligibility
ON warranty_assessments(eligibility);

CREATE INDEX idx_warranty_assessments_resolution
ON warranty_assessments(resolution);


-- 09. Device replacements

CREATE TABLE device_replacements (
    replacement_id BIGINT
        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    replacement_device_id VARCHAR(36) NOT NULL
        REFERENCES devices(device_id),

    recorded_by_user_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    replacement_reason TEXT NOT NULL,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_device_replacements_ticket_id
        UNIQUE (ticket_id)
);

CREATE INDEX idx_device_replacements_device_id
ON device_replacements(replacement_device_id);


-- 10. Repair work logs

CREATE TABLE repair_work_logs (
    work_log_id VARCHAR(36) PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    technician_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    diagnosis_findings TEXT NOT NULL,

    actions_performed TEXT NOT NULL,

    pending_tasks TEXT NOT NULL,

    used_parts_summary TEXT,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_repair_work_logs_actions
        CHECK (length(trim(actions_performed)) > 0)
);

CREATE INDEX idx_repair_work_logs_ticket_id
ON repair_work_logs(ticket_id);

CREATE INDEX idx_repair_work_logs_technician_id
ON repair_work_logs(technician_id);

CREATE INDEX idx_repair_work_logs_created_at
ON repair_work_logs(created_at);



-- 11. Handover sessions

CREATE TABLE handover_sessions (
    session_id VARCHAR(36) PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    initiated_by_admin_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    previous_technician_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    target_technician_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    previous_session_id VARCHAR(36)
        REFERENCES handover_sessions(session_id),

    status VARCHAR(20) NOT NULL
        DEFAULT 'PENDING',

    reason TEXT NOT NULL,

    is_previous_technician_absent BOOLEAN NOT NULL
        DEFAULT FALSE,

    missing_info_notes TEXT,

    rejection_reason TEXT,

    handover_snapshot JSONB,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    decided_at TIMESTAMPTZ,

    CONSTRAINT chk_handover_sessions_status
        CHECK (status IN (
            'PENDING',
            'ACCEPTED',
            'REJECTED',
            'CANCELLED'
        )),

    CONSTRAINT chk_handover_sessions_technicians
        CHECK (
            previous_technician_id <> target_technician_id
        ),

    CONSTRAINT chk_handover_sessions_rejection
        CHECK (
            status <> 'REJECTED'
            OR length(trim(coalesce(rejection_reason, ''))) > 0
        ),

    CONSTRAINT chk_handover_sessions_decided_at
        CHECK (
            decided_at IS NULL
            OR decided_at >= created_at
        )
);

CREATE INDEX idx_handover_sessions_ticket_id
ON handover_sessions(ticket_id);

CREATE INDEX idx_handover_sessions_target_technician_id
ON handover_sessions(target_technician_id);

CREATE UNIQUE INDEX uq_handover_sessions_pending
ON handover_sessions(ticket_id)
WHERE status = 'PENDING';


ALTER TABLE ticket_status_history
DROP CONSTRAINT chk_ticket_history_status_change;