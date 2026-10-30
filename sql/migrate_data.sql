-- =============================================================================
-- CloudHR Database Schema & CSV Data Migration Script
-- Target Database: cloudhr (PostgreSQL 16)
-- =============================================================================

BEGIN;

SET LOCAL synchronous_commit = off;
SET LOCAL work_mem = '64MB';
SET LOCAL maintenance_work_mem = '512MB';

-- -----------------------------------------------------------------------------
-- 1. Drop existing tables in reverse dependency order (for idempotent re-runs)
-- -----------------------------------------------------------------------------
DROP TABLE IF EXISTS security_mapping CASCADE;
DROP TABLE IF EXISTS performance_reviews CASCADE;
DROP TABLE IF EXISTS leave_records CASCADE;
DROP TABLE IF EXISTS employee_monthly_snapshots CASCADE;
DROP TABLE IF EXISTS employees CASCADE;
DROP TABLE IF EXISTS departments CASCADE;
DROP TABLE IF EXISTS organisations CASCADE;

-- -----------------------------------------------------------------------------
-- 2. Create tables in dependency order
--    (Primary keys and foreign keys are added after bulk COPY for fast loading)
-- -----------------------------------------------------------------------------

-- 2.1 Organisations (200 client companies)
CREATE TABLE organisations (
    org_id              VARCHAR(20)  PRIMARY KEY,
    org_name            VARCHAR(255) NOT NULL,
    industry            VARCHAR(100) NOT NULL,
    employee_count_band VARCHAR(50)  NOT NULL,
    country             VARCHAR(100) NOT NULL,
    subscription_tier   VARCHAR(50)  NOT NULL
);

-- 2.2 Departments (Department hierarchy per organisation)
CREATE TABLE departments (
    department_id    VARCHAR(20)  PRIMARY KEY,
    org_id           VARCHAR(20)  NOT NULL REFERENCES organisations(org_id),
    department_name  VARCHAR(150) NOT NULL,
    department_group VARCHAR(100) NOT NULL,
    cost_centre      VARCHAR(50)  NOT NULL
);

-- 2.3 Employees (Current and historical employees - SCD Type 2)
CREATE TABLE employees (
    employee_record_id VARCHAR(20)  PRIMARY KEY,
    employee_id        VARCHAR(20)  NOT NULL,
    org_id             VARCHAR(20)  NOT NULL REFERENCES organisations(org_id),
    first_name         VARCHAR(100) NOT NULL,
    last_name          VARCHAR(100) NOT NULL,
    department_id      VARCHAR(20)  NOT NULL REFERENCES departments(department_id),
    job_level          VARCHAR(50)  NOT NULL,
    employment_type    VARCHAR(50)  NOT NULL,
    hire_date          DATE         NOT NULL,
    termination_date   DATE,
    termination_reason VARCHAR(100),
    effective_from     DATE         NOT NULL,
    effective_to       DATE         NOT NULL,
    is_current         BOOLEAN      NOT NULL
);

-- 2.4 Employee Monthly Snapshots (One row per employee per month-end)
CREATE TABLE employee_monthly_snapshots (
    snapshot_month  DATE           NOT NULL,
    employee_id     VARCHAR(20)    NOT NULL,
    org_id          VARCHAR(20)    NOT NULL,
    is_active       BOOLEAN        NOT NULL,
    base_salary_usd NUMERIC(12, 2) NOT NULL,
    job_level       VARCHAR(50)    NOT NULL,
    department_id   VARCHAR(20)    NOT NULL
);

-- 2.5 Leave Records (Individual leave instances)
CREATE TABLE leave_records (
    leave_id    VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    org_id      VARCHAR(20) NOT NULL,
    leave_type  VARCHAR(50) NOT NULL,
    start_date  DATE        NOT NULL,
    end_date    DATE        NOT NULL,
    days_taken  INTEGER     NOT NULL,
    approved_by VARCHAR(20) NOT NULL
);

-- 2.6 Performance Reviews (Annual performance ratings)
CREATE TABLE performance_reviews (
    review_id   VARCHAR(20) NOT NULL,
    employee_id VARCHAR(20) NOT NULL,
    org_id      VARCHAR(20) NOT NULL,
    review_year INTEGER     NOT NULL,
    rating      SMALLINT    NOT NULL CHECK (rating BETWEEN 1 AND 5),
    reviewer_id VARCHAR(20) NOT NULL
);

-- 2.7 Security Mapping (Maps user emails to their org_id for RLS)
CREATE TABLE security_mapping (
    user_email   VARCHAR(255) PRIMARY KEY,
    org_id       VARCHAR(20)  NOT NULL REFERENCES organisations(org_id),
    access_level VARCHAR(50)  NOT NULL CHECK (access_level IN ('HR_ADMIN', 'HR_VIEWER'))
);

-- -----------------------------------------------------------------------------
-- 3. Bulk load CSV data in dependency order
--    Note: Uses /data/*.csv mounted inside the cloudhr-db container.
--    If running via local psql without Docker volume mounts, replace COPY with
--    \copy and change '/data/...' to 'data/...'.
-- -----------------------------------------------------------------------------

COPY organisations (
    org_id,
    org_name,
    industry,
    employee_count_band,
    country,
    subscription_tier
)
FROM '/data/organisations.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY departments (
    department_id,
    org_id,
    department_name,
    department_group,
    cost_centre
)
FROM '/data/departments.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY employees (
    employee_record_id,
    employee_id,
    org_id,
    first_name,
    last_name,
    department_id,
    job_level,
    employment_type,
    hire_date,
    termination_date,
    termination_reason,
    effective_from,
    effective_to,
    is_current
)
FROM '/data/employees.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY employee_monthly_snapshots (
    snapshot_month,
    employee_id,
    org_id,
    is_active,
    base_salary_usd,
    job_level,
    department_id
)
FROM '/data/employee_monthly_snapshots.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY leave_records (
    leave_id,
    employee_id,
    org_id,
    leave_type,
    start_date,
    end_date,
    days_taken,
    approved_by
)
FROM '/data/leave_records.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY performance_reviews (
    review_id,
    employee_id,
    org_id,
    review_year,
    rating,
    reviewer_id
)
FROM '/data/performance_reviews.csv'
WITH (FORMAT csv, HEADER true, NULL '');

COPY security_mapping (
    user_email,
    org_id,
    access_level
)
FROM '/data/security_mapping.csv'
WITH (FORMAT csv, HEADER true, NULL '');

-- -----------------------------------------------------------------------------
-- 4. Create primary keys, foreign keys, and indexes after bulk load
-- -----------------------------------------------------------------------------
ALTER TABLE employee_monthly_snapshots
    ADD PRIMARY KEY (snapshot_month, employee_id),
    ADD CONSTRAINT fk_snapshots_org FOREIGN KEY (org_id) REFERENCES organisations(org_id),
    ADD CONSTRAINT fk_snapshots_dept FOREIGN KEY (department_id) REFERENCES departments(department_id);

ALTER TABLE leave_records
    ADD PRIMARY KEY (leave_id),
    ADD CONSTRAINT fk_leave_org FOREIGN KEY (org_id) REFERENCES organisations(org_id);

ALTER TABLE performance_reviews
    ADD PRIMARY KEY (review_id),
    ADD CONSTRAINT fk_reviews_org FOREIGN KEY (org_id) REFERENCES organisations(org_id);

CREATE INDEX idx_departments_org_id               ON departments(org_id);
CREATE INDEX idx_employees_employee_id            ON employees(employee_id);
CREATE INDEX idx_employees_org_id                 ON employees(org_id);
CREATE INDEX idx_employees_department_id          ON employees(department_id);
CREATE INDEX idx_employees_is_current             ON employees(is_current);
CREATE INDEX idx_snapshots_org_id                 ON employee_monthly_snapshots(org_id);
CREATE INDEX idx_snapshots_employee_id            ON employee_monthly_snapshots(employee_id);
CREATE INDEX idx_snapshots_department_id          ON employee_monthly_snapshots(department_id);
CREATE INDEX idx_leave_records_org_id             ON leave_records(org_id);
CREATE INDEX idx_leave_records_employee_id        ON leave_records(employee_id);
CREATE INDEX idx_performance_reviews_org_id       ON performance_reviews(org_id);
CREATE INDEX idx_performance_reviews_employee_id  ON performance_reviews(employee_id);
CREATE INDEX idx_security_mapping_org_id          ON security_mapping(org_id);

COMMIT;

-- Update planner statistics after bulk load
ANALYZE organisations;
ANALYZE departments;
ANALYZE employees;
ANALYZE employee_monthly_snapshots;
ANALYZE leave_records;
ANALYZE performance_reviews;
ANALYZE security_mapping;
