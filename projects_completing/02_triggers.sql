CREATE OR REPLACE FUNCTION prevent_project_if_unpaid()
RETURNS TRIGGER AS $$
BEGIN
    IF EXISTS (
        SELECT 1
        FROM project p
        WHERE p.customer_id = NEW.customer_id
          AND NOT EXISTS (
              SELECT 1
              FROM work_report wr
              WHERE wr.project_id = p.id
                AND wr.report_date >= (CURRENT_DATE - INTERVAL '3 months')
          )
    ) THEN
        RAISE EXCEPTION 'Customer % has unpaid/abandoned projects older than 3 months', NEW.customer_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_project_if_unpaid
BEFORE INSERT ON project
FOR EACH ROW
EXECUTE FUNCTION prevent_project_if_unpaid();


-- prevent >10 hours total per worker per day
CREATE OR REPLACE FUNCTION prevent_overwork()
RETURNS TRIGGER AS $$
DECLARE
    total_hours INT;
BEGIN
    SELECT COALESCE(SUM(hours_spent),0)
    INTO total_hours
    FROM work_report
    WHERE worker_id = NEW.worker_id
      AND report_date = NEW.report_date;

    IF total_hours + NEW.hours_spent > 10 THEN
        RAISE EXCEPTION 'Worker % exceeds 10 hours on %', NEW.worker_id, NEW.report_date;
    END IF;

    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_prevent_overwork
BEFORE INSERT OR UPDATE ON work_report
FOR EACH ROW
EXECUTE FUNCTION prevent_overwork();