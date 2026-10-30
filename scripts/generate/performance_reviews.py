import os
import sys
import datetime
import random
from collections import defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import get_org_profile, read_csv, write_csv
from organisations import generate_organisations
from employees import generate_employees


def generate_performance_reviews(seed=47):
    rng = random.Random(seed)
    orgs = read_csv("organisations.csv")
    if not orgs:
        orgs = generate_organisations()
    org_profiles = {o["org_id"]: get_org_profile(o) for o in orgs}

    emp_rows = read_csv("employees.csv")
    if not emp_rows:
        emp_rows = generate_employees()

    current_emps = [r for r in emp_rows if r["is_current"] == "True"]

    reviewers_by_org = defaultdict(list)
    for r in current_emps:
        if r["job_level"] in ("Lead/Manager", "Director", "Executive"):
            reviewers_by_org[r["org_id"]].append(r["employee_id"])

    all_emps_by_org = defaultdict(list)
    for r in current_emps:
        all_emps_by_org[r["org_id"]].append(r["employee_id"])

    review_years = [2020, 2021, 2022, 2023, 2024, 2025, 2026]
    ratings = [1, 2, 3, 4, 5]

    rows = []
    review_counter = 1

    for emp in current_emps:
        emp_id = emp["employee_id"]
        org_id = emp["org_id"]
        rating_weights_by_year = org_profiles[org_id]["rating_weights_by_year"]

        hire_date = datetime.date.fromisoformat(emp["hire_date"])
        term_date = (
            datetime.date.fromisoformat(emp["termination_date"])
            if emp["termination_date"]
            else None
        )

        org_reviewers = [rv for rv in reviewers_by_org[org_id] if rv != emp_id]
        if not org_reviewers:
            org_reviewers = [rv for rv in all_emps_by_org[org_id] if rv != emp_id] or [emp_id]

        for yr in review_years:
            # Must be hired before the review eligibility cutoff and active during the review cycle
            hire_cutoff = datetime.date(yr, 7, 31) if yr == 2026 else datetime.date(yr, 9, 30)
            term_cutoff = datetime.date(yr, 10, 15) if yr == 2026 else datetime.date(yr, 11, 15)
            if hire_date > hire_cutoff:
                continue
            if term_date and term_date < term_cutoff:
                continue

            rating = rng.choices(ratings, weights=rating_weights_by_year[yr], k=1)[0]
            reviewer_id = rng.choice(org_reviewers)

            rows.append({
                "review_id": f"REV-{review_counter:07d}",
                "employee_id": emp_id,
                "org_id": org_id,
                "review_year": yr,
                "rating": rating,
                "reviewer_id": reviewer_id,
            })
            review_counter += 1

    fieldnames = [
        "review_id",
        "employee_id",
        "org_id",
        "review_year",
        "rating",
        "reviewer_id",
    ]
    write_csv("performance_reviews.csv", fieldnames, rows)
    return rows


if __name__ == "__main__":
    generate_performance_reviews()
