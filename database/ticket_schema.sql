-- 04. Daily ticket counters

CREATE TABLE ticket_counters (
    counter_date DATE PRIMARY KEY,
    last_number INTEGER NOT NULL DEFAULT 0,

    CONSTRAINT chk_ticket_counters_number
        CHECK (last_number >= 0)
);


-- 05. Warranty tickets

CREATE TABLE warranty_tickets (
    ticket_id VARCHAR(30) PRIMARY KEY,

    customer_id VARCHAR(36) NOT NULL
        REFERENCES customers(customer_id),

    device_id VARCHAR(36) NOT NULL
        REFERENCES devices(device_id),

    created_by_user_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    contact_name VARCHAR(100) NOT NULL,
    contact_phone VARCHAR(20) NOT NULL,

    intake_type VARCHAR(20) NOT NULL,

    promised_return_date DATE NOT NULL,

    reported_issue TEXT NOT NULL,
    initial_condition TEXT NOT NULL,
    accessories_included VARCHAR(255) NOT NULL,

    status VARCHAR(30) NOT NULL
        DEFAULT 'RECEIVED',

    tracking_code_hash VARCHAR(64) NOT NULL,

    current_technician_id VARCHAR(36)
        REFERENCES users(user_id),

    customer_signature_confirmed BOOLEAN
        NOT NULL DEFAULT FALSE,

    final_return_confirmed BOOLEAN
        NOT NULL DEFAULT FALSE,

    return_notes TEXT,
    cancellation_reason TEXT,

    version INTEGER NOT NULL DEFAULT 1,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_tickets_intake_type
        CHECK (intake_type IN (
            'SAME_DAY',
            'HOLD_FOR_REPAIR'
        )),

    CONSTRAINT chk_tickets_status
        CHECK (status IN (
            'RECEIVED',
            'PENDING_ASSIGNMENT',
            'UNDER_INSPECTION',
            'UNDER_REPAIR',
            'WAITING_FOR_PARTS',
            'WAITING_FOR_RESULT_CHECK',
            'WAITING_FOR_RETURN',
            'RETURNED',
            'CANCELLED'
        )),

    CONSTRAINT chk_tickets_signature
        CHECK (
            intake_type <> 'HOLD_FOR_REPAIR'
            OR customer_signature_confirmed = TRUE
        ),

    CONSTRAINT chk_tickets_tracking_hash
        CHECK (
            tracking_code_hash ~ '^[0-9a-f]{64}$'
        ),

    CONSTRAINT chk_tickets_version
        CHECK (version >= 1),

    CONSTRAINT chk_tickets_return
        CHECK (
            status <> 'RETURNED'
            OR final_return_confirmed = TRUE
        )
);

CREATE INDEX idx_warranty_tickets_customer_id
ON warranty_tickets(customer_id);

CREATE INDEX idx_warranty_tickets_device_id
ON warranty_tickets(device_id);

CREATE INDEX idx_warranty_tickets_status
ON warranty_tickets(status);

CREATE INDEX idx_warranty_tickets_promised_return_date
ON warranty_tickets(promised_return_date);

CREATE INDEX idx_warranty_tickets_current_technician_id
ON warranty_tickets(current_technician_id);

CREATE INDEX idx_warranty_tickets_created_at
ON warranty_tickets(created_at);

CREATE INDEX idx_warranty_tickets_contact_phone
ON warranty_tickets(contact_phone);


-- 06. Signed components

CREATE TABLE signed_components (
    component_id BIGINT
        GENERATED ALWAYS AS IDENTITY PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    part_name VARCHAR(150) NOT NULL,
    signature_mark TEXT NOT NULL,
    notes TEXT,

    CONSTRAINT chk_signed_components_part_name
        CHECK (length(trim(part_name)) > 0),

    CONSTRAINT chk_signed_components_signature
        CHECK (length(trim(signature_mark)) > 0)
);

CREATE INDEX idx_signed_components_ticket_id
ON signed_components(ticket_id);

-- 07. Ticket status history

CREATE TABLE ticket_status_history (
    log_id VARCHAR(36) PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    from_status VARCHAR(30),
    to_status VARCHAR(30) NOT NULL,

    changed_by_user_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    changed_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    reason TEXT NOT NULL,

    CONSTRAINT chk_ticket_history_from_status
        CHECK (from_status IN (
            'RECEIVED',
            'PENDING_ASSIGNMENT',
            'UNDER_INSPECTION',
            'UNDER_REPAIR',
            'WAITING_FOR_PARTS',
            'WAITING_FOR_RESULT_CHECK',
            'WAITING_FOR_RETURN',
            'RETURNED',
            'CANCELLED'
        )),

    CONSTRAINT chk_ticket_history_to_status
        CHECK (to_status IN (
            'RECEIVED',
            'PENDING_ASSIGNMENT',
            'UNDER_INSPECTION',
            'UNDER_REPAIR',
            'WAITING_FOR_PARTS',
            'WAITING_FOR_RESULT_CHECK',
            'WAITING_FOR_RETURN',
            'RETURNED',
            'CANCELLED'
        )),

    CONSTRAINT chk_ticket_history_status_change
        CHECK (
            from_status IS NULL
            OR from_status <> to_status
        )
);

CREATE INDEX idx_ticket_status_history_ticket_id
ON ticket_status_history(ticket_id);

CREATE INDEX idx_ticket_status_history_changed_at
ON ticket_status_history(changed_at);