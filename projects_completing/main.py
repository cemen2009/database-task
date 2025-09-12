import os
import time
import logging
import psycopg2
from psycopg2.extras import execute_values

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s [%(levelname)s] %(message)s")

DB_HOST = os.getenv("DB_HOST", "db")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "admin")
DB_PASSWORD = os.getenv("DB_PASSWORD", "secret")
DB_NAME = os.getenv("DB_NAME", "mydb")


def wait_for_db():
    while True:
        try:
            conn = psycopg2.connect(
                host=DB_HOST, port=DB_PORT, user=DB_USER,
                password=DB_PASSWORD, dbname=DB_NAME
            )
            conn.close()
            break
        except Exception as e:
            logging.info("DB isn't ready, retrying...")
            time.sleep(1.5)


def init_db():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, user=DB_USER,
        password=DB_PASSWORD, dbname=DB_NAME
    )

    # creating tables
    cursor = conn.cursor()

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS clients
                (
                    id
                    SERIAL
                    PRIMARY
                    KEY,
                    name
                    VARCHAR
                (
                    255
                ) NOT NULL
                    );
                """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS projects
                (
                    id
                    SERIAL
                    PRIMARY
                    KEY,
                    name
                    VARCHAR
                (
                    255
                ) NOT NULL,
                    client_id INT REFERENCES clients
                (
                    id
                ),
                    manager VARCHAR
                (
                    255
                ),
                    start_date DATE,
                    planned_duration INT,
                    complexity_category VARCHAR
                (
                    50
                )
                    );
                """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS employees
                (
                    id
                    SERIAL
                    PRIMARY
                    KEY,
                    name
                    VARCHAR
                (
                    255
                ),
                    position VARCHAR
                (
                    100
                ),
                    qualification VARCHAR
                (
                    100
                ),
                    hourly_rate NUMERIC
                    );
                """)

    cursor.execute("""
                CREATE TABLE IF NOT EXISTS work_reports
                (
                    id
                    SERIAL
                    PRIMARY
                    KEY,
                    employee_id
                    INT
                    REFERENCES
                    employees
                (
                    id
                ),
                    project_id INT REFERENCES projects
                (
                    id
                ),
                    work_date DATE,
                    hours_worked NUMERIC,
                    description TEXT
                    );
                """)

    conn.commit()

    cursor.execute("TRUNCATE work_reports, employees, projects, clients RESTART IDENTITY CASCADE;")

    clients = [("OpenAI",), ("ACME Corp",), ("Globex",)]
    execute_values(cursor, "INSERT INTO clients (name) VALUES %s", clients)

    projects = [
        ("AI Platform", 1, "Alice", "2025-01-10", 120, "High"),
        ("ERP System", 2, "Bob", "2025-02-01", 200, "Medium"),
        ("Mobile App", 3, "Charlie", "2025-03-15", 90, "Low")
    ]
    execute_values(cursor, """
        INSERT INTO projects (name, client_id, manager, start_date, planned_duration, complexity_category)
        VALUES %s
    """, projects)

    employees = [
        ("John", "Developer", "Senior", 40),
        ("Mary", "Developer", "Middle", 30),
        ("Steve", "Tester", "Junior", 20),
        ("Anna", "Project Manager", "Senior", 50)
    ]
    execute_values(cursor, """
        INSERT INTO employees (name, position, qualification, hourly_rate)
        VALUES %s
    """, employees)

    reports = []
    for day in range(1, 11):  # 10 днів
        reports.append((1, 1, f"2025-09-{day:02d}", 6, "Feature development"))
        reports.append((2, 1, f"2025-09-{day:02d}", 5, "Bug fixes"))
        reports.append((3, 2, f"2025-09-{day:02d}", 4, "Testing"))
        reports.append((1, 2, f"2025-09-{day:02d}", 3, "Integration"))
        reports.append((4, 3, f"2025-09-{day:02d}", 7, "Project coordination"))

    execute_values(cursor, """
        INSERT INTO work_reports (employee_id, project_id, work_date, hours_worked, description)
        VALUES %s
    """, reports)

    conn.commit()
    cursor.close()
    conn.close()
    logging.info("DB initialized with extended test data")


def get_reports():
    conn = psycopg2.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME,
        user=DB_USER, password=DB_PASSWORD
    )
    cur = conn.cursor()

    logging.info("=== REPORT: Total hours per project ===")
    cur.execute("""
                SELECT p.name, SUM(w.hours_worked)
                FROM projects p
                         JOIN work_reports w ON p.id = w.project_id
                GROUP BY p.name;
                """)
    for row in cur.fetchall():
        logging.info(row)

    logging.info("=== REPORT: Salary per employee ===")
    cur.execute("""
                SELECT e.name, SUM(w.hours_worked * e.hourly_rate)
                FROM employees e
                         JOIN work_reports w ON e.id = w.employee_id
                GROUP BY e.name;
                """)
    for row in cur.fetchall():
        logging.info(row)

    cur.close()
    conn.close()


if __name__ == "__main__":
    wait_for_db()
    init_db()
    get_reports()
