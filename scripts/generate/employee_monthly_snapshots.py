import os
import sys
import calendar
import datetime
import random
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import BASE_SALARY_RANGES, get_org_profile, read_csv, write_csv
from organisations import generate_organisations
from employees import generate_employees


def get_month_ends(start_year=2020, end_year=2026, end_month=10):
    months = []
    for year in range(start_year, end_year + 1):
        max_m = end_month if year == end_year else 12
        for month in range(1, max_m + 1):
            last_day = calendar.monthrange(year, month)[1]
            months.append(datetime.date(year, month, last_day))
    return months


def generate_employee_monthly_snapshots(seed=45):
    rng = random.Random(seed)
    orgs = read_csv("organisations.csv")
    if not orgs:
        orgs = generate_organisations()

    org_profiles = {o["org_id"]: get_org_profile(o) for o in orgs}

    emp_rows = read_csv("employees.csv")
    if not emp_rows:
        emp_rows = generate_employees()

    records_by_emp = defaultdict(list)
    for r in emp_rows:
        records_by_emp[r["employee_id"]].append(r)

    month_ends = get_month_ends(2020, 2026, 10)
    month_ends_iso = [m.isoformat() for m in month_ends]
    rows = []

    for emp_id, recs in records_by_emp.items():
        recs.sort(key=lambda x: x["effective_from"])
        org_id = recs[0]["org_id"]
        profile = org_profiles[org_id]
        sal_mult = profile["salary_multiplier"]
        merit_by_year = profile["merit_by_year"]

        hire_date = datetime.date.fromisoformat(recs[0]["hire_date"])
        term_str = recs[-1]["termination_date"]
        term_date = datetime.date.fromisoformat(term_str) if term_str else None

        # Pre-parse effective_from dates and assign base salary per SCD record
        parsed_recs = []
        prev_sal = None
        for idx, rec in enumerate(recs):
            eff_from = datetime.date.fromisoformat(rec["effective_from"])
            low, high = BASE_SALARY_RANGES[rec["job_level"]]
            adj_low = low * sal_mult
            adj_high = high * sal_mult
            if prev_sal is None:
                sal = round(rng.uniform(adj_low, adj_high), -2)
            else:
                sal = max(round(prev_sal * rng.uniform(1.09, 1.18), -2), round(adj_low, -2))
            parsed_recs.append((eff_from, rec, int(sal)))
            prev_sal = sal

        # Precompute cumulative merit multiplier by year from hire_date.year + 1 up to 2026
        cum_merit_by_year = {}
        running_mult = 1.0
        for yr in range(2020, 2027):
            if yr > hire_date.year and yr in merit_by_year:
                running_mult *= (1.0 + merit_by_year[yr])
            cum_merit_by_year[yr] = running_mult

        for m_idx, m_end in enumerate(month_ends):
            if m_end < hire_date:
                continue

            # If terminated in a previous month, stop emitting or emit one inactive month on termination month
            if term_date and m_end > term_date:
                if m_end.year == term_date.year and m_end.month == term_date.month:
                    is_active_str = "False"
                else:
                    break
            else:
                is_active_str = "True"

            # Find active SCD record at month end
            active_rec = parsed_recs[0][1]
            base_sal = parsed_recs[0][2]
            for eff_from, rec, sal in parsed_recs:
                if eff_from <= m_end:
                    active_rec = rec
                    base_sal = sal

            # Apply compounding org-specific annual merit increases
            merit_mult = cum_merit_by_year.get(m_end.year, 1.0)
            if merit_mult != 1.0:
                base_sal = int(round(base_sal * merit_mult, -2))

            rows.append({
                "snapshot_month": month_ends_iso[m_idx],
                "employee_id": emp_id,
                "org_id": org_id,
                "is_active": is_active_str,
                "base_salary_usd": base_sal,
                "job_level": active_rec["job_level"],
                "department_id": active_rec["department_id"],
            })

    fieldnames = [
        "snapshot_month",
        "employee_id",
        "org_id",
        "is_active",
        "base_salary_usd",
        "job_level",
        "department_id",
    ]
    write_csv("employee_monthly_snapshots.csv", fieldnames, rows)
    return rows


if __name__ == "__main__":
    generate_employee_monthly_snapshots()
