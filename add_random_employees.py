import os
import django
import random

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'PulseTrack.settings')
django.setup()

from PULSE.models import Employee, Department

# Test data
phone_numbers = [
    '0707427850',
    '0748264302',
    '0782203709',
    '0700125381',
]
names = [
    'Alice', 'Bob', 'Carol', 'Dave', 'Eve', 'Frank', 'Grace', 'Heidi', 'Ivan', 'Judy'
]

# Ensure departments exist
DEPARTMENT_NAMES = ['Sales', 'HR', 'Tech', 'Marketing']
departments = []
for dep_name in DEPARTMENT_NAMES:
    dep, _ = Department.objects.get_or_create(name=dep_name)
    departments.append(dep)

for phone in phone_numbers:
    name = random.choice(names)
    department = random.choice(departments)
    emp, created = Employee.objects.get_or_create(
        phone_number=phone,
        defaults={
            'name': name,
            'department': department,
            'is_active': True,
        }
    )
    if created:
        print(f"Added {name} ({phone}) to {department.name}")
    else:
        print(f"Employee with phone {phone} already exists.")
