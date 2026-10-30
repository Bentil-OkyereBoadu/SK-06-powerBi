import os
import sys

GENERATE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "generate")
sys.path.insert(0, GENERATE_DIR)

from organisations import generate_organisations
from departments import generate_departments
from employees import generate_employees
from employee_monthly_snapshots import generate_employee_monthly_snapshots
from leave_records import generate_leave_records
from performance_reviews import generate_performance_reviews
from security_mapping import generate_security_mapping


def run_all():
    print("Starting CloudHR data generation in dependency order...")
    generate_organisations()
    generate_departments()
    generate_employees()
    generate_employee_monthly_snapshots()
    generate_leave_records()
    generate_performance_reviews()
    generate_security_mapping()
    print("All CloudHR CSV datasets have been generated successfully.")


if __name__ == "__main__":
    run_all()
