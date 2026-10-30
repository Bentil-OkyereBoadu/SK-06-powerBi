import os
import sys
import datetime
import random
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import LEAVE_TYPES, get_org_profile, read_csv, write_csv
from organisations import generate_organisations
from employees import generate_employees


def generate_leave_records(seed=46):
    rng = random.Random(seed)
    orgs = read_csv("organisations.csv")
    if not orgs:
        orgs = generate_organisations()
    org_profiles = {o["org_id"]: get_org_profile(o) for o in orgs}

    emp_rows = read_csv("employees.csv")
    if not emp_rows:
        emp_rows = generate_employees()

    current_emps = [r for r in emp_rows if r["is_current"] == "True"]

    approvers_by_org = defaultdict(list)
    for r in current_emps:
        if r["job_level"] in ("Lead/Manager", "Director", "Executive"):
            approvers_by_org[r["org_id"]].append(r["employee_id"])

    all_emps_by_org = defaultdict(list)
    for r in current_emps:
        all_emps_by_org[r["org_id"]].append(r["employee_id"])

    rows = []
    leave_counter = 1
    window_start = datetime.date(2020, 1, 1)
    window_end = datetime.date(2026, 10, 31)

    base_duration_by_type = {
        "Annual Leave": (2, 10),
        "Sick Leave": (1, 4),
        "Parental Leave": (30, 90),
        "Compassionate Leave": (2, 5),
        "Unpaid Leave": (3, 14),
        "Study Leave": (1, 5),
    }

    for emp in current_emps:
        emp_id = emp["employee_id"]
        org_id = emp["org_id"]
        profile = org_profiles[org_id]
        freq_mult = profile["leave_freq_mult"]
        lv_weights = profile["leave_type_weights"]

        hire_date = datetime.date.fromisoformat(emp["hire_date"])
        term_date = (
            datetime.date.fromisoformat(emp["termination_date"])
            if emp["termination_date"]
            else window_end
        )

        eff_start = max(hire_date, window_start)
        eff_end = min(term_date, window_end)
        if eff_end <= eff_start + datetime.timedelta(days=14):
            continue

        org_approvers = [a for a in approvers_by_org[org_id] if a != emp_id]
        if not org_approvers:
            org_approvers = [a for a in all_emps_by_org[org_id] if a != emp_id] or [emp_id]

        # Generate leaves per active calendar year (2020..2026) for realistic YoY metrics
        for yr in range(eff_start.year, eff_end.year + 1):
            yr_start = max(eff_start, datetime.date(yr, 1, 1))
            yr_end = min(eff_end, datetime.date(yr, 12, 31), window_end)
            active_days = (yr_end - yr_start).days
            if active_days < 20:
                continue

            year_fraction = active_days / 365.0
            expected_leaves = 1.6 * freq_mult * year_fraction
            base_count = int(expected_leaves)
            extra = 1 if rng.random() < (expected_leaves - base_count) else 0
            num_leaves = max(0, base_count + extra + rng.choice([-1, 0, 0, 1]))

            for _ in range(num_leaves):
                leave_type = rng.choices(LEAVE_TYPES, weights=lv_weights, k=1)[0]
                min_d, max_d = base_duration_by_type[leave_type]
                if leave_type == "Annual Leave" and freq_mult > 1.15:
                    max_d = min(15, int(round(max_d * 1.25)))
                days_taken = rng.randint(min_d, max_d)

                span_days = active_days - days_taken
                if span_days <= 0:
                    continue

                start_date = yr_start + datetime.timedelta(days=rng.randint(0, span_days))
                end_date = start_date + datetime.timedelta(days=max(0, days_taken - 1))
                approved_by = rng.choice(org_approvers)

                rows.append({
                    "leave_id": f"LVE-{leave_counter:07d}",
                    "employee_id": emp_id,
                    "org_id": org_id,
                    "leave_type": leave_type,
                    "start_date": start_date.isoformat(),
                    "end_date": end_date.isoformat(),
                    "days_taken": days_taken,
                    "approved_by": approved_by,
                })
                leave_counter += 1

    fieldnames = [
        "leave_id",
        "employee_id",
        "org_id",
        "leave_type",
        "start_date",
        "end_date",
        "days_taken",
        "approved_by",
    ]
    write_csv("leave_records.csv", fieldnames, rows)
    return rows


if __name__ == "__main__":
    generate_leave_records()
