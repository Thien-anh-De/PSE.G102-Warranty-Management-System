-- 01. Import spare parts into inventory

CREATE OR REPLACE FUNCTION fn_import_stock(
    p_transaction_id VARCHAR,
    p_admin_id VARCHAR,
    p_part_id VARCHAR,
    p_quantity INTEGER,
    p_reference_note TEXT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = p_admin_id
            AND role = 'ADMIN'
            AND is_active = TRUE
    ) THEN

        RAISE EXCEPTION
            'Only active Admin can import stock';

    END IF;

    IF p_quantity IS NULL OR p_quantity <= 0 THEN

        RAISE EXCEPTION
            'Import quantity must be positive';

    END IF;

    UPDATE spare_parts
    SET stock_quantity =
        stock_quantity + p_quantity
    WHERE part_id = p_part_id;

    IF NOT FOUND THEN

        RAISE EXCEPTION
            'Spare part does not exist';

    END IF;

    INSERT INTO part_transactions (
        transaction_id,
        part_id,
        ticket_id,
        transaction_type,
        quantity,
        performed_by_user_id,
        reference_note
    )
    VALUES (
        p_transaction_id,
        p_part_id,
        NULL,
        'IMPORT',
        p_quantity,
        p_admin_id,
        COALESCE(p_reference_note, 'Stock import')
    );

END;
$$;



-- 02. Allocate spare parts to a warranty ticket

CREATE OR REPLACE FUNCTION fn_allocate_part(
    p_transaction_id VARCHAR,
    p_allocation_id VARCHAR,
    p_admin_id VARCHAR,
    p_ticket_id VARCHAR,
    p_part_id VARCHAR,
    p_quantity INTEGER,
    p_reference_note TEXT
)
RETURNS VARCHAR
LANGUAGE plpgsql
AS $$
DECLARE

    v_ticket_status VARCHAR(30);
    v_allocation_id VARCHAR(36);

BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = p_admin_id
            AND role = 'ADMIN'
            AND is_active = TRUE
    ) THEN

        RAISE EXCEPTION
            'Only active Admin can allocate parts';

    END IF;

    IF p_quantity IS NULL OR p_quantity <= 0 THEN

        RAISE EXCEPTION
            'Allocation quantity must be positive';

    END IF;

    SELECT status
    INTO v_ticket_status
    FROM warranty_tickets
    WHERE ticket_id = p_ticket_id
    FOR UPDATE;

    IF NOT FOUND THEN

        RAISE EXCEPTION
            'Warranty ticket does not exist';

    END IF;

    IF v_ticket_status IN (
        'RETURNED',
        'CANCELLED'
    ) THEN

        RAISE EXCEPTION
            'Cannot allocate parts to a closed ticket';

    END IF;

    UPDATE spare_parts
    SET stock_quantity =
        stock_quantity - p_quantity
    WHERE part_id = p_part_id
        AND stock_quantity >= p_quantity;

    IF NOT FOUND THEN

        RAISE EXCEPTION USING
            ERRCODE = '23514',
            MESSAGE = 'Insufficient stock or invalid part';

    END IF;

    INSERT INTO part_allocations (
        allocation_id,
        ticket_id,
        part_id,
        allocated_quantity,
        used_quantity
    )
    VALUES (
        p_allocation_id,
        p_ticket_id,
        p_part_id,
        p_quantity,
        0
    )

    ON CONFLICT (ticket_id, part_id)
    DO UPDATE SET
        allocated_quantity =
            part_allocations.allocated_quantity
            + EXCLUDED.allocated_quantity

    RETURNING allocation_id
    INTO v_allocation_id;

    INSERT INTO part_transactions (
        transaction_id,
        part_id,
        ticket_id,
        transaction_type,
        quantity,
        performed_by_user_id,
        reference_note
    )
    VALUES (
        p_transaction_id,
        p_part_id,
        p_ticket_id,
        'ALLOCATE',
        p_quantity,
        p_admin_id,
        COALESCE(p_reference_note, 'Part allocation')
    );

    RETURN v_allocation_id;

END;
$$;



-- 03. Record spare part usage

CREATE OR REPLACE FUNCTION fn_record_part_usage(
    p_technician_id VARCHAR,
    p_ticket_id VARCHAR,
    p_part_id VARCHAR,
    p_quantity INTEGER,
    p_notes TEXT
)
RETURNS VOID
LANGUAGE plpgsql
AS $$
DECLARE

    v_current_technician_id VARCHAR(36);
    v_ticket_status VARCHAR(30);
    v_allocation_id VARCHAR(36);

BEGIN

    IF NOT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = p_technician_id
            AND role = 'TECHNICIAN'
            AND is_active = TRUE
    ) THEN

        RAISE EXCEPTION
            'Invalid or inactive technician';

    END IF;

    IF p_quantity IS NULL OR p_quantity <= 0 THEN

        RAISE EXCEPTION
            'Used quantity must be positive';

    END IF;

    SELECT
        current_technician_id,
        status
    INTO
        v_current_technician_id,
        v_ticket_status
    FROM warranty_tickets
    WHERE ticket_id = p_ticket_id
    FOR UPDATE;

    IF NOT FOUND THEN

        RAISE EXCEPTION
            'Warranty ticket does not exist';

    END IF;

    IF v_current_technician_id
        IS DISTINCT FROM p_technician_id THEN

        RAISE EXCEPTION
            'Technician is not assigned to this ticket';

    END IF;

    IF v_ticket_status IN (
        'RETURNED',
        'CANCELLED'
    ) THEN

        RAISE EXCEPTION
            'Cannot record usage for a closed ticket';

    END IF;

    UPDATE part_allocations
    SET used_quantity =
        used_quantity + p_quantity
    WHERE ticket_id = p_ticket_id
        AND part_id = p_part_id
        AND p_quantity <=
            allocated_quantity - used_quantity

    RETURNING allocation_id
    INTO v_allocation_id;

    IF NOT FOUND THEN

        RAISE EXCEPTION USING
            ERRCODE = '23514',
            MESSAGE = 'Usage exceeds remaining allocation';

    END IF;

    INSERT INTO part_usage_logs (
        allocation_id,
        technician_id,
        used_quantity,
        notes
    )
    VALUES (
        v_allocation_id,
        p_technician_id,
        p_quantity,
        p_notes
    );

END;
$$;