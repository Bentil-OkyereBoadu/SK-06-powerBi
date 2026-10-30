import os
import sys
import datetime
import random
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import (
    EMPLOYMENT_TYPES,
    FIRST_NAMES,
    INDUSTRY_DEPT_WEIGHTS,
    JOB_LEVELS,
    LAST_NAMES,
    TERMINATION_REASONS,
    get_org_profile,
    read_csv,
    write_csv,
)
from organisations import generate_organisations
from departments import generate_departments


def _sample_hire_date(rng, year_hire_weights, cutoff_date):
    years = [2019, 2020, 2021, 2022, 2023, 2024, 2025, 2026]
    weights = [year_hire_weights[y] for y in years]
    yr = rng.choices(years, weights=weights, k=1)[0]
    y_start = datetime.date(yr, 1, 1)
    y_end = min(datetime.date(yr, 12, 31), cutoff_date)
    span = max(0, (y_end - y_start).days)
    return y_start + datetime.timedelta(days=rng.randint(0, span))


def _sample_term_date(rng, hire_date, min_tenure_days, cutoff_date, year_term_weights):
    earliest = hire_date + datetime.timedelta(days=min_tenure_days)
    if earliest >= cutoff_date:
        return None

    # Candidate years between earliest.year and cutoff_date.year
    cand_years = list(range(max(2020, earliest.year), cutoff_date.year + 1))
    if not cand_years:
        return earliest + datetime.timedelta(days=rng.randint(0, (cutoff_date - earliest).days))

    yr_weights = [year_term_weights.get(y, 1.0) for y in cand_years]
    chosen_yr = rng.choices(cand_years, weights=yr_weights, k=1)[0]
    w_start = max(earliest, datetime.date(chosen_yr, 1, 1))
    w_end = min(cutoff_date, datetime.date(chosen_yr, 12, 31))
    if w_end < w_start:
        return earliest + datetime.timedelta(days=rng.randint(0, (cutoff_date - earliest).days))
    return w_start + datetime.timedelta(days=rng.randint(0, (w_end - w_start).days))


def generate_employees(seed=44):
    rng = random.Random(seed)
    orgs = read_csv("organisations.csv")
    if not orgs:
        orgs = generate_organisations()

    depts = read_csv("departments.csv")
    if not depts:
        depts = generate_departments()

    depts_by_org = defaultdict(list)
    for d in depts:
        depts_by_org[d["org_id"]].append(d)

    cutoff_date = datetime.date(2026, 10, 31)

    rows = []
    emp_counter = 1
    scd_row_id = 1
    enterprise_5k_seen = 0

    for org in orgs:
        org_id = org["org_id"]
        band = org["employee_count_band"]
        industry = org["industry"]
        profile = get_org_profile(org)
        org_dept_rows = depts_by_org[org_id]
        org_depts = [d["department_id"] for d in org_dept_rows]

        # Build industry + org specific department headcount weights
        ind_map = INDUSTRY_DEPT_WEIGHTS.get(industry, {})
        dept_weights = []
        for d in org_dept_rows:
            base_w = ind_map.get(d["department_name"], 6)
            dept_weights.append(max(1.0, base_w * rng.uniform(0.75, 1.30)))

        # Realistic org sizing from 50-person startups to 10,000-employee enterprises,
        # weighted toward the lower end of wide bands so 82-month snapshots stay ~3.8M-4.4M rows
        if band in ("1-50",):
            num_employees = 50
        elif band in ("50-200", "51-200"):
            if rng.random() < 0.35:
                num_employees = rng.randint(50, 65)  # True ~50-person startups
            else:
                num_employees = int(50 + 150 * (rng.random() ** 1.7))
        elif band == "201-500":
            num_employees = int(201 + 299 * (rng.random() ** 1.8))
        elif band == "501-1000":
            num_employees = int(501 + 499 * (rng.random() ** 2.0))
        elif band == "1001-5000":
            num_employees = int(1001 + 2800 * (rng.random() ** 2.8))
        elif band in ("5001-10000", "1000+"):
            enterprise_5k_seen += 1
            if enterprise_5k_seen == 1:
                num_employees = 10000  # Flagship 10,000-employee enterprise
            else:
                num_employees = int(5001 + 1800 * (rng.random() ** 2.8))
        else:
            num_employees = rng.randint(50, 500)

        year_hire_weights = profile["year_hire_weights"]
        turnover_prob = profile["turnover_prob"]
        year_term_weights = profile["year_term_weights"]
        promotion_prob = profile["promotion_prob"]
        jl_weights = profile["job_level_weights"]
        emp_t_weights = profile["employment_type_weights"]
        term_r_weights = profile["term_reason_weights"]

        for e_idx in range(num_employees):
            emp_id = f"{emp_counter:07d}"
            emp_counter += 1

            first_name = rng.choice(FIRST_NAMES)
            last_name = rng.choice(LAST_NAMES)
            dept_id = rng.choices(org_depts, weights=dept_weights, k=1)[0]

            # Ensure every org has foundational leadership hired early for approvals & reviews
            if e_idx == 0:
                job_level = "Executive"
                emp_type = "Full-Time"
                hire_date = datetime.date(2019, 1, 1) + datetime.timedelta(days=rng.randint(0, 180))
            elif e_idx < 4:
                job_level = rng.choice(["Lead/Manager", "Director"])
                emp_type = "Full-Time"
                hire_date = datetime.date(2019, 1, 1) + datetime.timedelta(days=rng.randint(0, 365))
            else:
                job_level = rng.choices(JOB_LEVELS, weights=jl_weights, k=1)[0]
                emp_type = rng.choices(EMPLOYMENT_TYPES, weights=emp_t_weights, k=1)[0]
                hire_date = _sample_hire_date(rng, year_hire_weights, cutoff_date)

            # Determine if employee has an SCD Type 2 promotion/transfer history
            days_employed = (cutoff_date - hire_date).days
            has_promotion = (
                days_employed > 420
                and job_level in JOB_LEVELS[:-1]
                and rng.random() < promotion_prob
            )

            # Determine if employee eventually terminated (varies by org turnover rate)
            # Earlier cohorts have had longer exposure to turnover than recent hires
            tenure_exposure = min(1.35, max(0.30, days_employed / 1400.0))
            eff_turnover_prob = min(0.65, turnover_prob * tenure_exposure)
            is_terminated = rng.random() < eff_turnover_prob and e_idx >= 3
            term_date = None
            term_reason = ""
            if is_terminated:
                min_tenure = 390 if has_promotion else 45
                if days_employed > min_tenure + 15:
                    term_date = _sample_term_date(
                        rng, hire_date, min_tenure, cutoff_date, year_term_weights
                    )
                    if term_date:
                        term_reason = rng.choices(TERMINATION_REASONS, weights=term_r_weights, k=1)[0]
                    else:
                        is_terminated = False
                else:
                    is_terminated = False

            if has_promotion:
                max_change_offset = (term_date - hire_date).days - 45 if term_date else days_employed - 45
                if max_change_offset <= 210:
                    has_promotion = False

            if has_promotion:
                change_offset = rng.randint(200, max_change_offset)
                change_date = hire_date + datetime.timedelta(days=change_offset)
                prev_end_date = change_date - datetime.timedelta(days=1)

                next_level_idx = min(JOB_LEVELS.index(job_level) + 1, len(JOB_LEVELS) - 1)
                promoted_level = JOB_LEVELS[next_level_idx]
                new_dept_id = (
                    dept_id
                    if rng.random() < 0.82
                    else rng.choices(org_depts, weights=dept_weights, k=1)[0]
                )

                # Historical SCD2 record
                rows.append({
                    "employee_record_id": f"EREC-{scd_row_id:07d}",
                    "employee_id": emp_id,
                    "org_id": org_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "department_id": dept_id,
                    "job_level": job_level,
                    "employment_type": emp_type,
                    "hire_date": hire_date.isoformat(),
                    "termination_date": "",
                    "termination_reason": "",
                    "effective_from": hire_date.isoformat(),
                    "effective_to": prev_end_date.isoformat(),
                    "is_current": "False",
                })
                scd_row_id += 1

                # Current SCD2 record
                rows.append({
                    "employee_record_id": f"EREC-{scd_row_id:07d}",
                    "employee_id": emp_id,
                    "org_id": org_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "department_id": new_dept_id,
                    "job_level": promoted_level,
                    "employment_type": emp_type,
                    "hire_date": hire_date.isoformat(),
                    "termination_date": term_date.isoformat() if term_date else "",
                    "termination_reason": term_reason,
                    "effective_from": change_date.isoformat(),
                    "effective_to": term_date.isoformat() if term_date else "9999-12-31",
                    "is_current": "True",
                })
                scd_row_id += 1
            else:
                rows.append({
                    "employee_record_id": f"EREC-{scd_row_id:07d}",
                    "employee_id": emp_id,
                    "org_id": org_id,
                    "first_name": first_name,
                    "last_name": last_name,
                    "department_id": dept_id,
                    "job_level": job_level,
                    "employment_type": emp_type,
                    "hire_date": hire_date.isoformat(),
                    "termination_date": term_date.isoformat() if term_date else "",
                    "termination_reason": term_reason,
                    "effective_from": hire_date.isoformat(),
                    "effective_to": term_date.isoformat() if term_date else "9999-12-31",
                    "is_current": "True",
                })
                scd_row_id += 1

    fieldnames = [
        "employee_record_id",
        "employee_id",
        "org_id",
        "first_name",
        "last_name",
        "department_id",
        "job_level",
        "employment_type",
        "hire_date",
        "termination_date",
        "termination_reason",
        "effective_from",
        "effective_to",
        "is_current",
    ]
    write_csv("employees.csv", fieldnames, rows)
    return rows


if __name__ == "__main__":
    generate_employees()
