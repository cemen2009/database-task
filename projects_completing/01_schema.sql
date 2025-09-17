-- customers, projects, workers, reports

CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    active BOOLEAN DEFAULT TRUE
);

CREATE TABLE project (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    customer_id INT REFERENCES customer(id) ON DELETE CASCADE,
    team_lead TEXT,
    expected_work_hours FLOAT,
    category TEXT NOT NULL,
    category_coef FLOAT NOT NULL DEFAULT 1.0 CHECK (category_coef > 0),
    start_date DATE NOT NULL
);

CREATE TABLE worker (
    id SERIAL PRIMARY KEY,
    name TEXT NOT NULL,
    job_title TEXT NOT NULL,
    job_coef FLOAT NOT NULL DEFAULT 1.0 CHECK (job_coef > 0),
    qualification TEXT NOT NULL,
    hourly_rate FLOAT NOT NULL CHECK (hourly_rate > 0)
);

CREATE TABLE work_report (
    id SERIAL PRIMARY KEY,
    worker_id INT REFERENCES worker(id) ON DELETE CASCADE,
    project_id INT REFERENCES project(id) ON DELETE CASCADE,
    report_date DATE NOT NULL,
    description TEXT,
    hours INT NOT NULL CHECK (hours > 0),
    UNIQUE(worker_id, project_id, report_date, description)
);

-- indexes for performance
CREATE INDEX idx_work_report_worker_date ON work_report(worker_id, report_date);
CREATE INDEX idx_work_report_project ON work_report(project_id);
