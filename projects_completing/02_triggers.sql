-- max 10 hours per worker per day
CREATE OR REPLACE FUNCTION check_daily_hours()
RETURNS TRIGGER AS $$
BEGIN
    IF (
        SELECT COALESCE(SUM(hours), 0)
        FROM work_report
        WHERE worker_id = NEW.worker_id
          AND report_date = NEW.report_date
    ) + NEW.hours > 10 THEN
        RAISE EXCEPTION 'Worker % exceeds 10 hours on %', NEW.worker_id, NEW.report_date;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_daily_hours
BEFORE INSERT OR UPDATE ON work_report
FOR EACH ROW
EXECUTE FUNCTION check_daily_hours();


-- block new projects for inactive customers
CREATE OR REPLACE FUNCTION check_customer_active()
RETURNS TRIGGER AS $$
BEGIN
    IF NOT EXISTS (SELECT 1 FROM customer WHERE id = NEW.customer_id AND active = TRUE) THEN
        RAISE EXCEPTION 'Customer % cannot start new project due to unpaid invoices', NEW.customer_id;
    END IF;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trg_check_customer_active
BEFORE INSERT ON project
FOR EACH ROW
EXECUTE FUNCTION check_customer_active();
