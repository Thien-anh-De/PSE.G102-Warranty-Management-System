-- 12. Spare parts

CREATE TABLE spare_parts (
    part_id VARCHAR(36) PRIMARY KEY,

    part_code VARCHAR(50) NOT NULL,

    part_name VARCHAR(150) NOT NULL,

    unit VARCHAR(20) NOT NULL,

    stock_quantity INTEGER NOT NULL
        DEFAULT 0,

    minimum_threshold INTEGER NOT NULL
        DEFAULT 0,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_spare_parts_part_code
        UNIQUE (part_code),

    CONSTRAINT chk_spare_parts_stock_quantity
        CHECK (stock_quantity >= 0),

    CONSTRAINT chk_spare_parts_minimum_threshold
        CHECK (minimum_threshold >= 0),

    CONSTRAINT chk_spare_parts_name
        CHECK (length(trim(part_name)) > 0)
);

CREATE INDEX idx_spare_parts_part_name
ON spare_parts(part_name);


-- 13. Part allocations

CREATE TABLE part_allocations (
    allocation_id VARCHAR(36) PRIMARY KEY,

    ticket_id VARCHAR(30) NOT NULL
        REFERENCES warranty_tickets(ticket_id),

    part_id VARCHAR(36) NOT NULL
        REFERENCES spare_parts(part_id),

    allocated_quantity INTEGER NOT NULL,

    used_quantity INTEGER NOT NULL
        DEFAULT 0,

    allocated_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT uq_part_allocations_ticket_part
        UNIQUE (ticket_id, part_id),

    CONSTRAINT chk_part_allocations_quantity
        CHECK (allocated_quantity > 0),

    CONSTRAINT chk_part_allocations_used_quantity
        CHECK (
            used_quantity >= 0
            AND used_quantity <= allocated_quantity
        )
);

CREATE INDEX idx_part_allocations_part_id
ON part_allocations(part_id);



-- 14. Part transactions

CREATE TABLE part_transactions (
    transaction_id VARCHAR(36) PRIMARY KEY,

    part_id VARCHAR(36) NOT NULL
        REFERENCES spare_parts(part_id),

    ticket_id VARCHAR(30)
        REFERENCES warranty_tickets(ticket_id),

    transaction_type VARCHAR(20) NOT NULL,

    quantity INTEGER NOT NULL,

    performed_by_user_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    reference_note TEXT NOT NULL,

    timestamp TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_part_transactions_type
        CHECK (transaction_type IN (
            'IMPORT',
            'ALLOCATE',
            'RETURN'
        )),

    CONSTRAINT chk_part_transactions_quantity
        CHECK (quantity > 0),

    CONSTRAINT chk_part_transactions_ticket
        CHECK (
            (
                transaction_type = 'IMPORT'
                AND ticket_id IS NULL
            )
            OR
            (
                transaction_type IN ('ALLOCATE', 'RETURN')
                AND ticket_id IS NOT NULL
            )
        )
);

CREATE INDEX idx_part_transactions_part_id
ON part_transactions(part_id);

CREATE INDEX idx_part_transactions_ticket_id
ON part_transactions(ticket_id);

CREATE INDEX idx_part_transactions_timestamp
ON part_transactions(timestamp);

CREATE INDEX idx_part_transactions_transaction_type
ON part_transactions(transaction_type);


-- 15. Part usage logs

CREATE TABLE part_usage_logs (
    usage_log_id BIGINT
        GENERATED ALWAYS AS IDENTITY
        PRIMARY KEY,

    allocation_id VARCHAR(36) NOT NULL
        REFERENCES part_allocations(allocation_id),

    technician_id VARCHAR(36) NOT NULL
        REFERENCES users(user_id),

    used_quantity INTEGER NOT NULL,

    notes TEXT,

    created_at TIMESTAMPTZ NOT NULL
        DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT chk_part_usage_logs_quantity
        CHECK (used_quantity > 0)
);

CREATE INDEX idx_part_usage_logs_allocation_id
ON part_usage_logs(allocation_id);

CREATE INDEX idx_part_usage_logs_technician_id
ON part_usage_logs(technician_id);

CREATE INDEX idx_part_usage_logs_created_at
ON part_usage_logs(created_at);