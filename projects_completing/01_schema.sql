CREATE TABLE customer (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

CREATE TABLE job_title (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    bonus_coefficient DECIMAL(10,2) NOT NULL
);

CREATE TABLE worker (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    job_title_id INT NOT NULL REFERENCES job_title(id),
    qualification_name VARCHAR(100) NOT NULL,
    hourly_rate DECIMAL(10,2) NOT NULL
);

CREATE TABLE project (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    customer_id INT NOT NULL REFERENCES customer(id),
    team_lead_id INT NOT NULL REFERENCES worker(id),
    expected_work_hours DECIMAL(10,2),
    category_name VARCHAR(100) NOT NULL,
    category_multiplier DECIMAL(10,2) NOT NULL,
    start_date DATE NOT NULL
);

CREATE TABLE work_report (
    id SERIAL PRIMARY KEY,
    worker_id INT NOT NULL REFERENCES worker(id),
    project_id INT NOT NULL REFERENCES project(id),
    report_date DATE NOT NULL,
    description TEXT,
    hours_spent INT NOT NULL CHECK (hours_spent > 0)
);