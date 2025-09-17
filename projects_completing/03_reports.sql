-- project summary by category
CREATE OR REPLACE VIEW v_project_summary AS
SELECT
    p.category,
    p.id AS project_id,
    p.name AS project_name,
    SUM(wr.hours * w.hourly_rate * w.job_coef * p.category_coef * 1.4) AS total_cost
FROM project p
JOIN work_report wr ON p.id = wr.project_id
JOIN worker w ON wr.worker_id = w.id
GROUP BY p.category, p.id, p.name;


-- payroll by job title per month
CREATE OR REPLACE VIEW v_payroll AS
SELECT
    w.job_title,
    w.id AS worker_id,
    w.name AS worker_name,
    DATE_TRUNC('month', wr.report_date) AS month,
    SUM(wr.hours * w.hourly_rate * w.job_coef) AS salary
FROM worker w
JOIN work_report wr ON w.id = wr.worker_id
GROUP BY w.job_title, w.id, w.name, DATE_TRUNC('month', wr.report_date);


-- monthly report per project
CREATE OR REPLACE VIEW v_project_monthly_report AS
SELECT
    p.id AS project_id,
    p.name AS project_name,
    DATE_TRUNC('month', wr.report_date) AS month,
    SUM(wr.hours) AS total_hours,
    SUM(wr.hours * w.hourly_rate * w.job_coef * p.category_coef) AS cost
FROM project p
JOIN work_report wr ON p.id = wr.project_id
JOIN worker w ON wr.worker_id = w.id
GROUP BY p.id, p.name, DATE_TRUNC('month', wr.report_date);
