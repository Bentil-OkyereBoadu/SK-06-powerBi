import csv
import os
import random

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")

FIRST_NAMES = [
    "James", "Mary", "Robert", "Patricia", "John", "Jennifer", "Michael", "Linda",
    "David", "Elizabeth", "William", "Barbara", "Richard", "Susan", "Joseph", "Jessica",
    "Thomas", "Sarah", "Charles", "Karen", "Christopher", "Lisa", "Daniel", "Nancy",
    "Matthew", "Betty", "Anthony", "Margaret", "Mark", "Sandra", "Donald", "Ashley",
    "Steven", "Kimberly", "Paul", "Emily", "Andrew", "Donna", "Joshua", "Michelle",
    "Kenneth", "Carol", "Kevin", "Amanda", "Brian", "Dorothy", "George", "Melissa",
    "Timothy", "Deborah", "Ronald", "Stephanie", "Edward", "Rebecca", "Jason", "Sharon",
    "Jeffrey", "Laura", "Ryan", "Cynthia", "Jacob", "Kathleen", "Gary", "Amy",
    "Nicholas", "Angela", "Eric", "Shirley", "Jonathan", "Anna", "Stephen", "Brenda",
    "Larry", "Pamela", "Justin", "Emma", "Scott", "Nicole", "Brandon", "Helen",
    "Benjamin", "Samantha", "Samuel", "Katherine", "Gregory", "Christine", "Alexander", "Debra",
    "Frank", "Rachel", "Patrick", "Carolyn", "Raymond", "Janet", "Jack", "Catherine",
    "Dennis", "Maria", "Jerry", "Heather", "Tyler", "Diane", "Aaron", "Ruth",
    "Jose", "Julie", "Adam", "Olivia", "Nathan", "Joyce", "Henry", "Virginia",
    "Douglas", "Victoria", "Zachary", "Kelly", "Peter", "Lauren", "Kyle", "Christina",
    "Ethan", "Joan", "Walter", "Evelyn", "Noah", "Judith", "Jeremy", "Megan",
    "Christian", "Andrea", "Keith", "Cheryl", "Roger", "Hannah", "Terry", "Jacqueline",
    "Gerald", "Martha", "Harold", "Gloria", "Sean", "Teresa", "Austin", "Ann",
    "Carl", "Sara", "Arthur", "Madison", "Lawrence", "Frances", "Dylan", "Kathryn",
    "Jesse", "Janice", "Jordan", "Jean", "Bryan", "Abigail", "Billy", "Alice",
    "Joe", "Judy", "Bruce", "Sophia", "Gabriel", "Grace", "Logan", "Denise",
    "Albert", "Amber", "Willie", "Doris", "Alan", "Marilyn", "Juan", "Danielle",
    "Wayne", "Beverly", "Elijah", "Isabella", "Randy", "Theresa", "Roy", "Diana",
    "Vincent", "Natalie", "Ralph", "Brittany", "Eugene", "Charlotte", "Russell", "Marie",
    "Bobby", "Kayla", "Mason", "Alexis", "Philip", "Lori", "Louis", "Priya",
    "Arjun", "Mei", "Wei", "Sven", "Astrid", "Mateo", "Valentina", "Liam",
    "fatima", "Omar", "Yuki", "Kenji", "Amina", "Kofi", "Kwame", "Ama"
]
FIRST_NAMES = [n.capitalize() for n in FIRST_NAMES]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson", "Thomas",
    "Taylor", "Moore", "Jackson", "Martin", "Lee", "Perez", "Thompson", "White",
    "Harris", "Sanchez", "Clark", "Ramirez", "Lewis", "Robinson", "Walker", "Young",
    "Allen", "King", "Wright", "Scott", "Torres", "Nguyen", "Hill", "Flores",
    "Green", "Adams", "Nelson", "Baker", "Hall", "Rivera", "Campbell", "Mitchell",
    "Carter", "Roberts", "Gomez", "Phillips", "Evans", "Turner", "Diaz", "Parker",
    "Cruz", "Edwards", "Collins", "Reyes", "Stewart", "Morris", "Morales", "Murphy",
    "Cook", "Rogers", "Gutierrez", "Ortiz", "Morgan", "Cooper", "Peterson", "Bailey",
    "Reed", "Kelly", "Howard", "Ramos", "Kim", "Cox", "Ward", "Richardson",
    "Watson", "Brooks", "Chavez", "Wood", "James", "Bennett", "Gray", "Mendoza",
    "Ruiz", "Hughes", "Price", "Alvarez", "Castillo", "Sanders", "Patel", "Myers",
    "Long", "Ross", "Foster", "Jimenez", "Powell", "Jenkins", "Perry", "Russell",
    "Sullivan", "Bell", "Coleman", "Butler", "Henderson", "Barnes", "Gonzales", "Fisher",
    "Vasquez", "Simmons", "Romero", "Jordan", "Patterson", "Alexander", "Hamilton", "Graham",
    "Reynolds", "Griffin", "Wallace", "Moreno", "West", "Cole", "Hayes", "Bryant",
    "Herrera", "Gibson", "Ellis", "Tran", "Medina", "Aguilar", "Stevens", "Murray",
    "Ford", "Castro", "Marshall", "Owens", "Harrison", "Fernandez", "McDonald", "Woods",
    "Washington", "Kennedy", "Wells", "Vargas", "Henry", "Chen", "Freeman", "Webb",
    "Tucker", "Guzman", "Burns", "Crawford", "Olson", "Simpson", "Porter", "Hunter",
    "Gordon", "Mendez", "Silva", "Shaw", "Snyder", "Mason", "Dixon", "Munoz",
    "Hunt", "Hicks", "Holmes", "Palmer", "Wagner", "Black", "Robertson", "Boyd",
    "Rose", "Stone", "Salazar", "Fox", "Warren", "Mills", "Meyer", "Rice",
    "Schmidt", "Garza", "Daniels", "Ferguson", "Nichols", "Stephens", "Soto", "Weaver",
    "Ryan", "Gardner", "Payne", "Grant", "Dunn", "Kelley", "Spencer", "Hawkins",
    "Okyere", "Mensah", "Boadu", "Osei", "Lindqvist", "Kowalski", "Tanaka", "Sato"
]

COMPANY_PREFIXES = [
    "Apex", "Vertex", "Nova", "Blue", "Silver", "Golden", "Prime", "Global",
    "NextGen", "Pacific", "Atlantic", "Nordic", "Alpine", "Summit", "Quantum", "Stellar",
    "Vanguard", "Pioneer", "Horizon", "Catalyst", "Synergy", "Pinnacle", "Aegis", "Crest",
    "Orion", "Zenith", "Atlas", "Cobalt", "Emerald", "Iron", "Titan", "Velocity",
    "Elevate", "Radiant", "Lumina", "Stratos", "Beacon", "Vortex", "Pulse", "Nexus",
    "Omni", "Terra", "Solis", "Astra", "Vector", "Core", "Clear", "Bright",
    "True", "Swift", "Bold", "First", "United", "Allied", "Metro", "Urban",
    "Civic", "Coastal", "Inland", "Frontier", "Heritage", "Legacy", "Modern", "Future"
]

COMPANY_CORES = [
    "Tech", "Systems", "Solutions", "Dynamics", "Labs", "Works", "Networks", "Logix",
    "Analytics", "Cloud", "Data", "Health", "Bio", "Med", "Care", "Pharma",
    "Fin", "Capital", "Wealth", "Trust", "Pay", "Bank", "Ventures", "Holdings",
    "Retail", "Commerce", "Market", "Goods", "Foods", "Brands", "Direct", "Supply",
    "Energy", "Power", "Solar", "Grid", "Wind", "Eco", "Green", "Enviro",
    "Build", "Construct", "Infra", "Steel", "Materials", "Motors", "Aero", "Auto",
    "Media", "Digital", "Interactive", "Creative", "Studio", "Press", "Connect", "Wave",
    "Learn", "Edu", "Academy", "Mind", "Skill", "Path", "Bridge", "Link"
]

COMPANY_SUFFIXES = [
    "Inc", "Corp", "LLC", "Ltd", "Group", "Partners", "International", "Co",
    "Holdings", "Enterprises", "Global", "PLC", "GmbH", "Technologies", "Services"
]

INDUSTRIES = [
    "Technology & SaaS", "Financial Services", "Healthcare & Life Sciences",
    "Manufacturing", "Retail & E-Commerce", "Professional Services",
    "Energy & Utilities", "Media & Telecommunications", "Logistics & Supply Chain",
    "Education & EdTech", "Hospitality & Travel", "Construction & Real Estate"
]

COUNTRIES = [
    "United States", "United Kingdom", "Canada", "Germany", "Australia",
    "France", "Netherlands", "Singapore", "Ireland", "Sweden", "Switzerland", "Japan"
]

COUNTRY_WEIGHTS = [35, 18, 10, 8, 7, 5, 4, 4, 3, 2, 2, 2]

EMPLOYEE_BANDS = ["50-200", "201-500", "501-1000", "1001-5000", "5001-10000"]
BAND_WEIGHTS = [42, 30, 17, 7, 4]

SUBSCRIPTION_TIERS = ["Starter", "Growth", "Professional", "Enterprise"]

# Country-level compensation & statutory annual leave multipliers
COUNTRY_SALARY_MULTIPLIERS = {
    "United States": 1.15,
    "Switzerland": 1.28,
    "Singapore": 1.05,
    "Australia": 1.02,
    "United Kingdom": 0.95,
    "Germany": 0.96,
    "Netherlands": 0.94,
    "Canada": 0.92,
    "Ireland": 0.93,
    "Sweden": 0.90,
    "France": 0.88,
    "Japan": 0.85,
}

COUNTRY_LEAVE_MULTIPLIERS = {
    "France": 1.35,
    "Germany": 1.30,
    "Sweden": 1.30,
    "United Kingdom": 1.20,
    "Netherlands": 1.20,
    "Ireland": 1.12,
    "Australia": 1.10,
    "Switzerland": 1.10,
    "Canada": 0.92,
    "Singapore": 0.90,
    "Japan": 0.82,
    "United States": 0.78,
}

INDUSTRY_SALARY_MULTIPLIERS = {
    "Technology & SaaS": 1.22,
    "Financial Services": 1.25,
    "Healthcare & Life Sciences": 1.08,
    "Professional Services": 1.12,
    "Energy & Utilities": 1.10,
    "Media & Telecommunications": 1.02,
    "Manufacturing": 0.94,
    "Construction & Real Estate": 0.95,
    "Education & EdTech": 0.88,
    "Logistics & Supply Chain": 0.89,
    "Retail & E-Commerce": 0.82,
    "Hospitality & Travel": 0.76,
}

# Department weight profiles by industry (matching DEPARTMENT_TEMPLATES names)
INDUSTRY_DEPT_WEIGHTS = {
    "Technology & SaaS": {
        "Software Engineering": 32, "Product Management": 12, "Data & Analytics": 10,
        "Quality Assurance": 9, "Enterprise Sales": 12, "Commercial Sales": 10,
        "Marketing & Growth": 8, "Customer Success": 12, "IT & Security": 5,
        "People & Culture": 4, "Finance & Accounting": 4, "Legal & Compliance": 2,
    },
    "Financial Services": {
        "Finance & Accounting": 22, "Enterprise Sales": 16, "Commercial Sales": 14,
        "Legal & Compliance": 12, "IT & Security": 12, "Data & Analytics": 12,
        "Software Engineering": 14, "Customer Success": 10, "People & Culture": 5,
        "Marketing & Growth": 6, "Product Management": 6,
    },
    "Healthcare & Life Sciences": {
        "Quality Assurance": 18, "Supply Chain & Operations": 18, "Customer Success": 14,
        "Data & Analytics": 10, "Legal & Compliance": 10, "Commercial Sales": 12,
        "Enterprise Sales": 10, "People & Culture": 6, "Finance & Accounting": 6,
        "Software Engineering": 8, "Facilities & Workplace": 8,
    },
    "Manufacturing": {
        "Supply Chain & Operations": 35, "Quality Assurance": 18, "Facilities & Workplace": 15,
        "Commercial Sales": 12, "Enterprise Sales": 10, "Finance & Accounting": 6,
        "People & Culture": 5, "IT & Security": 4, "Software Engineering": 5,
    },
    "Retail & E-Commerce": {
        "Commercial Sales": 28, "Supply Chain & Operations": 26, "Customer Success": 18,
        "Marketing & Growth": 14, "Software Engineering": 8, "Data & Analytics": 6,
        "Finance & Accounting": 5, "People & Culture": 5, "Facilities & Workplace": 8,
    },
    "Professional Services": {
        "Customer Success": 24, "Enterprise Sales": 20, "Commercial Sales": 16,
        "Data & Analytics": 14, "Finance & Accounting": 10, "People & Culture": 8,
        "Marketing & Growth": 8, "Legal & Compliance": 6, "Software Engineering": 8,
    },
    "Energy & Utilities": {
        "Supply Chain & Operations": 30, "Facilities & Workplace": 20, "IT & Security": 10,
        "Legal & Compliance": 9, "Finance & Accounting": 8, "Enterprise Sales": 10,
        "Commercial Sales": 8, "Data & Analytics": 7, "Software Engineering": 6,
    },
    "Media & Telecommunications": {
        "Marketing & Growth": 22, "Commercial Sales": 18, "Enterprise Sales": 14,
        "Software Engineering": 16, "Product Management": 12, "Customer Success": 14,
        "Data & Analytics": 8, "People & Culture": 5, "Finance & Accounting": 5,
    },
    "Logistics & Supply Chain": {
        "Supply Chain & Operations": 42, "Facilities & Workplace": 18, "Commercial Sales": 14,
        "Customer Success": 12, "Enterprise Sales": 10, "IT & Security": 5,
        "Finance & Accounting": 5, "People & Culture": 5, "Software Engineering": 5,
    },
    "Education & EdTech": {
        "Customer Success": 24, "Product Management": 14, "Software Engineering": 16,
        "Marketing & Growth": 14, "Commercial Sales": 14, "People & Culture": 7,
        "Data & Analytics": 7, "Finance & Accounting": 5,
    },
    "Hospitality & Travel": {
        "Customer Success": 30, "Facilities & Workplace": 24, "Supply Chain & Operations": 18,
        "Commercial Sales": 16, "Marketing & Growth": 14, "People & Culture": 6,
        "Finance & Accounting": 5, "Software Engineering": 4,
    },
    "Construction & Real Estate": {
        "Facilities & Workplace": 30, "Supply Chain & Operations": 28, "Commercial Sales": 16,
        "Enterprise Sales": 12, "Legal & Compliance": 9, "Finance & Accounting": 8,
        "People & Culture": 5, "Software Engineering": 4,
    },
}

DEPARTMENT_TEMPLATES = [
    ("People & Culture", "G&A", "CC-100"),
    ("Finance & Accounting", "G&A", "CC-110"),
    ("Legal & Compliance", "G&A", "CC-120"),
    ("IT & Security", "G&A", "CC-130"),
    ("Software Engineering", "R&D", "CC-200"),
    ("Product Management", "R&D", "CC-210"),
    ("Data & Analytics", "R&D", "CC-220"),
    ("Quality Assurance", "R&D", "CC-230"),
    ("Enterprise Sales", "Sales & Marketing", "CC-300"),
    ("Commercial Sales", "Sales & Marketing", "CC-310"),
    ("Marketing & Growth", "Sales & Marketing", "CC-320"),
    ("Customer Success", "Operations", "CC-400"),
    ("Supply Chain & Operations", "Operations", "CC-410"),
    ("Facilities & Workplace", "Operations", "CC-420")
]

JOB_LEVELS = ["Associate", "Intermediate", "Senior", "Lead/Manager", "Director", "Executive"]
JOB_LEVEL_WEIGHTS = [22, 33, 25, 12, 6, 2]

BASE_SALARY_RANGES = {
    "Associate": (48000, 72000),
    "Intermediate": (70000, 102000),
    "Senior": (100000, 145000),
    "Lead/Manager": (135000, 185000),
    "Director": (175000, 240000),
    "Executive": (230000, 360000),
}

EMPLOYMENT_TYPES = ["Full-Time", "Part-Time", "Contract", "Intern"]
EMPLOYMENT_WEIGHTS = [82, 8, 8, 2]

TERMINATION_REASONS = [
    "Voluntary - Career Opportunity",
    "Voluntary - Relocation",
    "Voluntary - Personal Reasons",
    "Voluntary - Compensation",
    "Involuntary - Performance",
    "Involuntary - Restructuring",
    "End of Contract",
    "Retirement"
]

LEAVE_TYPES = [
    "Annual Leave",
    "Sick Leave",
    "Parental Leave",
    "Compassionate Leave",
    "Unpaid Leave",
    "Study Leave"
]
LEAVE_WEIGHTS = [58, 26, 4, 5, 4, 3]


def ensure_data_dir():
    os.makedirs(DATA_DIR, exist_ok=True)


def write_csv(filename, fieldnames, rows):
    ensure_data_dir()
    filepath = os.path.join(DATA_DIR, filename)
    with open(filepath, mode="w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Generated {filepath} ({len(rows)} rows)")


def read_csv(filename):
    filepath = os.path.join(DATA_DIR, filename)
    if not os.path.exists(filepath):
        return None
    with open(filepath, mode="r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def get_org_profile(org):
    """
    Deterministically generates a rich, realistic organisation profile from an org dict
    so that headcount trajectory, turnover, promotions, compensation, leaves, and
    performance ratings differ significantly across organisations and over 2020-2026.
    """
    org_id = org["org_id"]
    org_num = int(org_id.split("-")[1])
    rng = random.Random(10000 + org_num * 97)

    industry = org["industry"]
    country = org["country"]
    band = org["employee_count_band"]
    tier = org.get("subscription_tier", "Professional")

    # 1. Growth archetype based on size band & industry
    if band in ("1-50", "50-200", "51-200"):
        archetypes = ["hyper_growth", "steady_growth", "boom_restructure", "seasonal_high_churn"]
        arch_weights = [38, 32, 18, 12]
    elif band in ("201-500", "501-1000"):
        archetypes = ["hyper_growth", "steady_growth", "boom_restructure", "mature_stable", "seasonal_high_churn"]
        arch_weights = [22, 35, 20, 13, 10]
    else:
        archetypes = ["steady_growth", "mature_stable", "boom_restructure", "seasonal_high_churn", "hyper_growth"]
        arch_weights = [35, 32, 16, 10, 7]

    archetype = rng.choices(archetypes, weights=arch_weights, k=1)[0]

    # Base hiring trajectories across 2019..2026 (2026 is 10 months Jan-Oct)
    base_trajectories = {
        # Started small in 2019-2020, rapid scaling through 2026
        "hyper_growth": {
            2019: 4, 2020: 6, 2021: 10, 2022: 15, 2023: 19, 2024: 24, 2025: 29, 2026: 26
        },
        # Steady compounder
        "steady_growth": {
            2019: 16, 2020: 11, 2021: 12, 2022: 13, 2023: 14, 2024: 15, 2025: 16, 2026: 14
        },
        # Heavy 2020-2022 boom, 2023-2024 freeze/restructure, 2025-2026 rebound
        "boom_restructure": {
            2019: 14, 2020: 16, 2021: 24, 2022: 26, 2023: 6, 2024: 8, 2025: 14, 2026: 13
        },
        # Large established base in 2019-2020, modest replacement/expansion hiring
        "mature_stable": {
            2019: 34, 2020: 14, 2021: 11, 2022: 11, 2023: 10, 2024: 10, 2025: 10, 2026: 8
        },
        # High velocity ongoing hiring
        "seasonal_high_churn": {
            2019: 15, 2020: 12, 2021: 15, 2022: 17, 2023: 16, 2024: 18, 2025: 19, 2026: 16
        },
    }
    year_hire_weights = {}
    for yr, w in base_trajectories[archetype].items():
        # Add org-specific year jitter so no two orgs share the exact same YoY curve
        year_hire_weights[yr] = max(1.0, w * rng.uniform(0.75, 1.30))

    # 2. Turnover / Attrition rate (cumulative probability & annual distribution)
    industry_base_churn = {
        "Hospitality & Travel": 0.34,
        "Retail & E-Commerce": 0.30,
        "Logistics & Supply Chain": 0.26,
        "Media & Telecommunications": 0.23,
        "Construction & Real Estate": 0.22,
        "Technology & SaaS": 0.21,
        "Professional Services": 0.20,
        "Manufacturing": 0.17,
        "Healthcare & Life Sciences": 0.18,
        "Education & EdTech": 0.16,
        "Financial Services": 0.15,
        "Energy & Utilities": 0.13,
    }.get(industry, 0.20)

    if archetype == "seasonal_high_churn":
        industry_base_churn *= 1.25
    elif archetype == "mature_stable":
        industry_base_churn *= 0.80
    elif archetype == "boom_restructure":
        industry_base_churn *= 1.15

    turnover_prob = min(0.48, max(0.07, industry_base_churn * rng.uniform(0.70, 1.35)))

    # Year weights for when terminations occur (2020..2026)
    year_term_weights = {
        2020: rng.uniform(0.6, 1.0),
        2021: rng.uniform(0.9, 1.4),  # Great Resignation
        2022: rng.uniform(1.0, 1.5),
        2023: rng.uniform(1.4, 2.2) if archetype == "boom_restructure" else rng.uniform(0.8, 1.3),
        2024: rng.uniform(1.1, 1.6) if archetype == "boom_restructure" else rng.uniform(0.8, 1.3),
        2025: rng.uniform(0.8, 1.3),
        2026: rng.uniform(0.7, 1.15),
    }

    # 3. Promotion velocity
    base_promo = 0.24 if archetype in ("hyper_growth", "steady_growth") else 0.14
    promotion_prob = min(0.35, max(0.06, base_promo * rng.uniform(0.65, 1.40)))

    # 4. Job level pyramid weights: [Associate, Intermediate, Senior, Lead/Manager, Director, Executive]
    if band in ("1-50", "50-200", "51-200"):
        # Flatter, slightly more Senior/Lead relative to Associate in tech/prof services
        base_jl = [20, 32, 28, 12, 5, 3]
    elif band in ("1001-5000", "5001-10000", "1000+"):
        # Broader base, narrower executive apex
        base_jl = [28, 35, 22, 10, 4, 1]
    else:
        base_jl = [23, 34, 25, 11, 5, 2]

    if industry in ("Retail & E-Commerce", "Hospitality & Travel", "Logistics & Supply Chain", "Manufacturing"):
        base_jl[0] += 12
        base_jl[2] = max(10, base_jl[2] - 8)
    elif industry in ("Technology & SaaS", "Financial Services", "Professional Services"):
        base_jl[2] += 8
        base_jl[0] = max(10, base_jl[0] - 6)

    job_level_weights = [max(1, int(round(w * rng.uniform(0.75, 1.25)))) for w in base_jl]

    # 5. Employment type weights: [Full-Time, Part-Time, Contract, Intern]
    if industry in ("Hospitality & Travel", "Retail & E-Commerce"):
        base_emp_t = [62, 22, 12, 4]
    elif industry in ("Logistics & Supply Chain", "Construction & Real Estate", "Media & Telecommunications"):
        base_emp_t = [72, 10, 15, 3]
    elif industry in ("Technology & SaaS", "Financial Services"):
        base_emp_t = [88, 3, 6, 3]
    else:
        base_emp_t = [80, 8, 9, 3]
    employment_type_weights = [max(1, int(round(w * rng.uniform(0.7, 1.3)))) for w in base_emp_t]

    # 6. Termination reason weights
    # [Vol-Career, Vol-Reloc, Vol-Personal, Vol-Comp, Invol-Perf, Invol-Restruct, EndContract, Retirement]
    base_term_r = [28, 8, 12, 18, 10, 8, 10, 6]
    if archetype == "boom_restructure":
        base_term_r[5] += 22  # Involuntary - Restructuring
    if employment_type_weights[2] > 12:
        base_term_r[6] += 15  # End of Contract
    if archetype == "mature_stable":
        base_term_r[7] += 10  # Retirement
    term_reason_weights = [max(1, int(round(w * rng.uniform(0.75, 1.25)))) for w in base_term_r]

    # 7. Compensation multiplier & YoY merit rates (2021..2026)
    c_mult = COUNTRY_SALARY_MULTIPLIERS.get(country, 1.0)
    i_mult = INDUSTRY_SALARY_MULTIPLIERS.get(industry, 1.0)
    tier_mult = {"Starter": 0.88, "Growth": 0.95, "Professional": 1.02, "Enterprise": 1.10}.get(tier, 1.0)
    org_pay_factor = rng.uniform(0.88, 1.14)
    salary_multiplier = round(c_mult * i_mult * tier_mult * org_pay_factor, 4)

    base_merit = rng.uniform(0.022, 0.048)
    merit_by_year = {
        2021: round(base_merit * rng.uniform(0.85, 1.10), 4),
        2022: round(base_merit * rng.uniform(1.15, 1.45), 4),  # Wage inflation peak
        2023: round(base_merit * rng.uniform(1.05, 1.30), 4),
        2024: round(base_merit * rng.uniform(0.90, 1.15), 4),
        2025: round(base_merit * rng.uniform(0.85, 1.15), 4),
        2026: round(base_merit * rng.uniform(0.85, 1.15), 4),
    }

    # 8. Leave profile (frequency & type mix)
    leave_freq_mult = COUNTRY_LEAVE_MULTIPLIERS.get(country, 1.0) * rng.uniform(0.80, 1.25)
    # [Annual Leave, Sick Leave, Parental Leave, Compassionate Leave, Unpaid Leave, Study Leave]
    base_lv = [56, 26, 5, 4, 5, 4]
    leave_type_weights = [max(1, int(round(w * rng.uniform(0.70, 1.35)))) for w in base_lv]

    # 9. Performance rating culture across 2020..2026
    perf_culture = rng.choices(
        ["high_performing", "balanced", "strict_calibration", "struggling"],
        weights=[28, 38, 22, 12],
        k=1,
    )[0]
    culture_base_weights = {
        "high_performing": [2, 8, 42, 34, 14],     # Avg ~3.50
        "balanced": [4, 14, 50, 24, 8],            # Avg ~3.18
        "strict_calibration": [7, 20, 52, 16, 5],  # Avg ~2.92
        "struggling": [10, 26, 46, 13, 5],         # Avg ~2.77
    }[perf_culture]

    rating_weights_by_year = {}
    for yr in range(2020, 2027):
        rating_weights_by_year[yr] = [
            max(1, int(round(w * rng.uniform(0.80, 1.25)))) for w in culture_base_weights
        ]

    return {
        "archetype": archetype,
        "year_hire_weights": year_hire_weights,
        "turnover_prob": turnover_prob,
        "year_term_weights": year_term_weights,
        "promotion_prob": promotion_prob,
        "job_level_weights": job_level_weights,
        "employment_type_weights": employment_type_weights,
        "term_reason_weights": term_reason_weights,
        "salary_multiplier": salary_multiplier,
        "merit_by_year": merit_by_year,
        "leave_freq_mult": leave_freq_mult,
        "leave_type_weights": leave_type_weights,
        "rating_weights_by_year": rating_weights_by_year,
    }

