-- 01. Ticket overview for internal dashboard

CREATE OR REPLACE VIEW vw_ticket_overview AS
SELECT
    t.ticket_id,
    t.customer_id,
    t.contact_name AS customer_name,
    t.contact_phone AS phone_number,

    d.device_id,
    d.serial_number,
    d.model_name,
    d.brand,

    t.intake_type,
    t.reported_issue,
    t.status,

    t.current_technician_id,
    u.full_name AS technician_name,

    t.created_at,
    t.promised_return_date,

    CASE
        WHEN t.status IN (
            'RETURNED',
            'CANCELLED'
        ) THEN FALSE

        WHEN t.promised_return_date <
            (CURRENT_TIMESTAMP AT TIME ZONE
                'Asia/Ho_Chi_Minh')::DATE
        THEN TRUE

        ELSE FALSE
    END AS is_overdue

FROM warranty_tickets t

JOIN devices d
    ON t.device_id = d.device_id

LEFT JOIN users u
    ON t.current_technician_id = u.user_id;



-- 02. Inventory overview

CREATE OR REPLACE VIEW vw_stock_overview AS
SELECT
    part_id,
    part_code,
    part_name,
    unit,
    stock_quantity,
    minimum_threshold,

    CASE
        WHEN stock_quantity = 0
            THEN 'OUT_OF_STOCK'

        WHEN stock_quantity < minimum_threshold
            THEN 'LOW_STOCK'

        ELSE 'NORMAL'
    END AS stock_status

FROM spare_parts;



-- 03. Part allocation overview

CREATE OR REPLACE VIEW vw_part_allocation_overview AS
SELECT
    a.allocation_id,
    a.ticket_id,

    p.part_id,
    p.part_code,
    p.part_name,
    p.unit,

    a.allocated_quantity,
    a.used_quantity,

    a.allocated_quantity - a.used_quantity
        AS remaining_quantity,

    a.allocated_at

FROM part_allocations a

JOIN spare_parts p
    ON a.part_id = p.part_id;


-- 04. Customer ticket progress

CREATE OR REPLACE VIEW vw_public_ticket_progress AS
SELECT
    t.ticket_id,

    d.brand,
    d.model_name,

    t.status,
    t.created_at,
    t.promised_return_date

FROM warranty_tickets t

JOIN devices d
    ON t.device_id = d.device_id;