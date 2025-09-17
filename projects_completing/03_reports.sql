-- projects with performed work grouped by category

SELECT
    p.category_name,
    p.name AS project_name,
    c.name AS customer_name,
    SUM(wr.hours_spent * w.hourly_rate * jt.bonus_coefficient * p.category_multiplier) * 1.4 AS total_cost
FROM project p
JOIN customer c ON p.customer_id = c.id
JOIN work_report wr ON wr.project_id = p.id
JOIN worker w ON wr.worker_id = w.id
JOIN job_title jt ON w.job_title_id = jt.id
GROUP BY p.category_name, p.name, c.name;

-- payroll grouped by job title
SELECT
    jt.name AS job_title,
    w.id AS worker_id,
    w.name AS worker_name,
    DATE_TRUNC('month', wr.report_date) AS period,
    SUM(wr.hours_spent * w.hourly_rate * jt.bonus_coefficient) AS salary_amount
FROM worker w
JOIN job_title jt ON w.job_title_id = jt.id
JOIN work_report wr ON wr.worker_id = w.id
GROUP BY jt.name, w.id, w.name, DATE_TRUNC('month', wr.report_date)
ORDER BY jt.name, worker_name;

-- work done on a project for a given month
SELECT
    p.name AS project_name,
    DATE_TRUNC('month', wr.report_date) AS period,
    w.name AS worker_name,
    wr.description,
    SUM(wr.hours_spent) AS hours
FROM work_report wr
JOIN project p ON wr.project_id = p.id
JOIN worker w ON wr.worker_id = w.id
WHERE p.id = :project_id
  AND DATE_TRUNC('month', wr.report_date) = DATE_TRUNC('month', :some_date::DATE)
GROUP BY p.name, period, w.name, wr.description;

