import os
import sys
import random

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from _common import (
    COMPANY_CORES,
    COMPANY_PREFIXES,
    COMPANY_SUFFIXES,
    COUNTRIES,
    COUNTRY_WEIGHTS,
    EMPLOYEE_BANDS,
    BAND_WEIGHTS,
    INDUSTRIES,
    write_csv,
)


def generate_organisations(seed=42):
    rng = random.Random(seed)
    used_names = set()
    rows = []

    tier_by_band = {
        "1-50": ["Starter", "Growth"],
        "50-200": ["Starter", "Growth", "Professional"],
        "51-200": ["Growth", "Professional"],
        "201-500": ["Professional", "Enterprise"],
        "501-1000": ["Professional", "Enterprise"],
        "1000+": ["Enterprise"],
        "1001-5000": ["Enterprise"],
        "5001-10000": ["Enterprise"],
    }

    for i in range(1, 201):
        org_id = f"ORG-{i:04d}"

        while True:
            prefix = rng.choice(COMPANY_PREFIXES)
            core = rng.choice(COMPANY_CORES)
            suffix = rng.choice(COMPANY_SUFFIXES)
            name = f"{prefix} {core} {suffix}"
            if name not in used_names:
                used_names.add(name)
                break

        industry = rng.choice(INDUSTRIES)
        band = rng.choices(EMPLOYEE_BANDS, weights=BAND_WEIGHTS, k=1)[0]
        country = rng.choices(COUNTRIES, weights=COUNTRY_WEIGHTS, k=1)[0]
        tier = rng.choice(tier_by_band[band])

        rows.append({
            "org_id": org_id,
            "org_name": name,
            "industry": industry,
            "employee_count_band": band,
            "country": country,
            "subscription_tier": tier,
        })

    fieldnames = [
        "org_id",
        "org_name",
        "industry",
        "employee_count_band",
        "country",
        "subscription_tier",
    ]
    write_csv("organisations.csv", fieldnames, rows)
    return rows


if __name__ == "__main__":
    generate_organisations()
