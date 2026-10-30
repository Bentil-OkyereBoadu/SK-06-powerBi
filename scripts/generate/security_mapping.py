import os
import sys
import random
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import FIRST_NAMES, LAST_NAMES, read_csv, write_csv
from organisations import generate_organisations


def slugify_org_domain(org_name):
    cleaned = re.sub(r"[^a-zA-Z0-9\s]", "", org_name.lower())
    parts = cleaned.split()
    if len(parts) >= 2:
        domain = f"{parts[0]}{parts[1]}.com"
    else:
        domain = f"{parts[0]}.com"
    return domain


def generate_security_mapping(seed=48):
    rng = random.Random(seed)
    orgs = read_csv("organisations.csv")
    if not orgs:
        orgs = generate_organisations()

    rows = []
    used_emails = set()

    for org in orgs:
        org_id = org["org_id"]
        domain = slugify_org_domain(org["org_name"])

        num_users = rng.randint(2, 5)
        for idx in range(num_users):
            while True:
                first = rng.choice(FIRST_NAMES).lower()
                last = rng.choice(LAST_NAMES).lower()
                email = f"{first}.{last}@{domain}"
                if email not in used_emails:
                    used_emails.add(email)
                    break

            access_level = "HR_ADMIN" if idx == 0 or rng.random() < 0.35 else "HR_VIEWER"

            rows.append({
                "user_email": email,
                "org_id": org_id,
                "access_level": access_level,
            })

    fieldnames = [
        "user_email",
        "org_id",
        "access_level",
    ]
    write_csv("security_mapping.csv", fieldnames, rows)
    return rows


if __name__ == "__main__":
    generate_security_mapping()
