import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import DEPARTMENT_TEMPLATES, read_csv, write_csv
from organisations import generate_organisations


def generate_departments(seed=43):
    rng = random.Random(seed)
    orgs = read_csv("organisations.csv")
    if not orgs:
        orgs = generate_organisations()

    rows = []
    dept_counter = 1

    band_dept_counts = {
        "1-50": (4, 6),
        "50-200": (6, 9),
        "51-200": (6, 9),
        "201-500": (8, 12),
        "501-1000": (10, 14),
        "1000+": (12, 14),
        "1001-5000": (12, 14),
        "5001-10000": (13, 14),
    }

    core_indices = [0, 1, 4, 8]  # People, Finance, Engineering, Sales

    for org in orgs:
        org_id = org["org_id"]
        band = org["employee_count_band"]
        min_d, max_d = band_dept_counts.get(band, (5, 8))
        num_depts = rng.randint(min_d, max_d)

        remaining_indices = [idx for idx in range(len(DEPARTMENT_TEMPLATES)) if idx not in core_indices]
        chosen_indices = sorted(core_indices + rng.sample(remaining_indices, k=num_depts - len(core_indices)))

        org_num = org_id.split("-")[1]
        for idx in chosen_indices:
            dept_name, dept_group, base_cc = DEPARTMENT_TEMPLATES[idx]
            dept_id = f"DEP-{dept_counter:05d}"
            dept_counter += 1
            cost_centre = f"{base_cc}-{org_num}"

            rows.append({
                "department_id": dept_id,
                "org_id": org_id,
                "department_name": dept_name,
                "department_group": dept_group,
                "cost_centre": cost_centre,
            })

    fieldnames = [
        "department_id",
        "org_id",
        "department_name",
        "department_group",
        "cost_centre",
    ]
    write_csv("departments.csv", fieldnames, rows)
    return rows


if __name__ == "__main__":
    generate_departments()
