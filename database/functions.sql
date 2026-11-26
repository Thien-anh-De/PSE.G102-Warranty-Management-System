-- 01. Generate daily warranty ticket ID

CREATE OR REPLACE FUNCTION fn_generate_ticket_id(
    p_ticket_date DATE
)
RETURNS VARCHAR(30)
LANGUAGE plpgsql
AS $$
DECLARE
    v_last_number INTEGER;

BEGIN

    IF p_ticket_date IS NULL THEN
        RAISE EXCEPTION
            'Ticket date cannot be null';
    END IF;

    INSERT INTO ticket_counters (
        counter_date,
        last_number
    )
    VALUES (
        p_ticket_date,
        1
    )

    ON CONFLICT (counter_date)
    DO UPDATE SET
        last_number =
            ticket_counters.last_number + 1

    RETURNING last_number
    INTO v_last_number;

    RETURN
        'TKT_' ||
        TO_CHAR(p_ticket_date, 'YYYYMMDD') ||
        '_' ||
        v_last_number::TEXT;

END;
$$;

