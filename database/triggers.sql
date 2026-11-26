-- 01. Validate repair work log

CREATE OR REPLACE FUNCTION fn_validate_repair_log()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_technician_id VARCHAR(36);
    v_ticket_status VARCHAR(30);

BEGIN

    SELECT
        current_technician_id,
        status

    INTO
        v_technician_id,
        v_ticket_status

    FROM warranty_tickets

    WHERE ticket_id = NEW.ticket_id

    FOR UPDATE;

    IF NOT FOUND THEN

        RAISE EXCEPTION
            'Warranty ticket does not exist';

    END IF;

    IF v_technician_id
        IS DISTINCT FROM NEW.technician_id THEN

        RAISE EXCEPTION
            'Technician is not assigned to this ticket';

    END IF;

    IF v_ticket_status IN (
        'RETURNED',
        'CANCELLED'
    ) THEN

        RAISE EXCEPTION
            'Cannot update a closed ticket';

    END IF;

    IF NOT EXISTS (
        SELECT 1
        FROM users
        WHERE user_id = NEW.technician_id
            AND role = 'TECHNICIAN'
            AND is_active = TRUE
    ) THEN

        RAISE EXCEPTION
            'Technician is inactive or invalid';

    END IF;

    RETURN NEW;

END;
$$;


CREATE TRIGGER trg_validate_repair_log

BEFORE INSERT ON repair_work_logs

FOR EACH ROW

EXECUTE FUNCTION fn_validate_repair_log();



-- 02. Validate replacement device

CREATE OR REPLACE FUNCTION fn_validate_replacement()
RETURNS TRIGGER
LANGUAGE plpgsql
AS $$
DECLARE
    v_original_device_id VARCHAR(36);

BEGIN

    SELECT device_id

    INTO v_original_device_id

    FROM warranty_tickets

    WHERE ticket_id = NEW.ticket_id

    FOR UPDATE;

    IF NOT FOUND THEN

        RAISE EXCEPTION
            'Warranty ticket does not exist';

    END IF;

    IF NEW.replacement_device_id =
        v_original_device_id THEN

        RAISE EXCEPTION
            'Replacement device must differ from original';

    END IF;

    RETURN NEW;

END;
$$;


CREATE TRIGGER trg_validate_replacement

BEFORE INSERT OR UPDATE
ON device_replacements

FOR EACH ROW

EXECUTE FUNCTION fn_validate_replacement();