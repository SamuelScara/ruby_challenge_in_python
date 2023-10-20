import json
from datetime import datetime, timedelta

def is_valid_date_format(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

try:
    # Read data from file 'data.json'
    with open("data.json", "r") as file:
        data = json.load(file)
except FileNotFoundError:
    print("File 'data.json' not found")
    exit(1)

# Function to check if a date is in the specified project
def date_in_period(date, since_date, until_date):
    if date.year > until_date.year or date.year < since_date.year:
        return 0
    years_counter = (until_date.year - since_date.year) + 1
    k = 0
    for n in range(years_counter):
        check_date = datetime(since_date.year + n, date.month, date.day)
        check_since_date = datetime(since_date.year, since_date.month, since_date.day)
        check_until_date = datetime(until_date.year, until_date.month, until_date.day)
        if check_since_date <= check_date <= check_until_date:
            k += 1
    return k
    

# Function for incrementing the holidays counter if the date is a working day
def increment_holidays_if_date_is_working_day(date, since_date, until_date, holidays):
    n = date_in_period(date, since_date, until_date)
    for i in range(n):
        check_date = datetime(since_date.year + i, date.month, date.day)
        if 1 <= check_date.weekday() <= 5:
            holidays += 1
    return holidays 

availabilities = []


# Calculating availabilities for each project
for project in data["projects"]:

    # Checking if the project dates are valid
    since_date_str = project.get("since")
    until_date_str = project.get("until")

    if not is_valid_date_format(since_date_str) or not is_valid_date_format(until_date_str):
        raise ValueError(f"Invalid date format in project {project['id']}")

    # Parsing starting date and ending date from project
    since_date = datetime.strptime(project["since"], "%Y-%m-%d")
    until_date = datetime.strptime(project["until"], "%Y-%m-%d")

    if until_date < since_date:
            raise ValueError(f"End date is before start date in project {project['id']}")

    # Total days in project
    days = (until_date - since_date).days + 1
    
    wdays_with_holidays = sum(1 for date in (since_date + timedelta(n) for n in range(days))
                                        if 1 <= date.weekday() <= 5)

    # Holidays for project
    if project["id"] == 1:
        holidays = 10
    elif project["id"] == 2:
        holidays = 3
    else:
        holidays = 0

    # Calculating working days
    working_days = wdays_with_holidays - holidays

    # Total working days for project
    total_working_days_for_project = 0

    # Calculating total working days for project
    for developer in data["developers"]:
        dev_holidays = holidays

    
        # Checking if the birthday date is valid
        birthday_str = developer.get("birthday")
        if not is_valid_date_format(birthday_str):
            raise ValueError(f"Invalid date format in developer {developer['id']}")
        
        # Incrementing the holidays counter if the birthday date is a working day
        birthday = datetime.strptime(developer["birthday"], "%Y-%m-%d").date()
        birthday = birthday.replace(year=since_date.year)
        if date_in_period(birthday, since_date, until_date) >= 1:
            dev_holidays = increment_holidays_if_date_is_working_day(birthday, since_date, until_date, dev_holidays)
        
        # Incrementing the holidays counter if the local holidays date is a working day
        for local_holiday in data["local_holidays"]:
            # Checking if the local holiday date is valid
            local_holiday_date_str = local_holiday.get("day")
            if not is_valid_date_format(local_holiday_date_str):
                raise ValueError(f"Invalid date format in local holiday {local_holiday['day']}")
            local_holiday_date = datetime.strptime(local_holiday["day"], "%Y-%m-%d").date()
            if date_in_period(local_holiday_date, since_date, until_date) >= 1:
                dev_holidays = increment_holidays_if_date_is_working_day(local_holiday_date, since_date, until_date, dev_holidays)
        
        # Calculating total working days for developer
        working_days_for_dev = wdays_with_holidays - dev_holidays + holidays
        total_working_days_for_project += working_days_for_dev

        
    weekend_days = days - wdays_with_holidays

    # Calculating feasibility
    effort_days = project["effort_days"]

    if effort_days > working_days:
        raise ValueError(f"Effort days are greater than working days in project {project['id']}")
    
    feasibility = total_working_days_for_project >= effort_days

    # Adding availabilities to list
    availabilities.append({
            'project_id': project["id"],
            'total_days': days,
            'workdays': working_days,
            'weekend_days': weekend_days,
            'holidays': holidays,
            'feasibility': feasibility 
        })

# Creating hash with availabilities 
output = {'availabilities': availabilities}

# Writing output to file 'output.json'
with open("output.json", "w") as output_file:
    json.dump(output, output_file, indent=2)

print("Done! Check output.json file")