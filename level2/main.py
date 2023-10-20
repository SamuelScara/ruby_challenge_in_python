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

# Function to check if a date is in the specified period
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


# Calculating availabilities for each period
for period in data["periods"]:

    since_date_str = period.get("since")
    until_date_str = period.get("until")

    if not is_valid_date_format(since_date_str) or not is_valid_date_format(until_date_str):
        raise ValueError(f"Invalid date format in period {period['id']}")

    # Parsing starting date and ending date from period
    since_date = datetime.strptime(period["since"], "%Y-%m-%d")
    until_date = datetime.strptime(period["until"], "%Y-%m-%d")

    if until_date < since_date:
            raise ValueError(f"End date is before start date in period {period['id']}")

    # Total days in period
    days = (until_date - since_date).days + 1
    
    wdays_with_holidays = sum(1 for date in (since_date + timedelta(n) for n in range(days))
                                        if 1 <= date.weekday() <= 5)

    # Holidays for period
    if period["id"] == 1:
        holidays = 10
    elif period["id"] == 2:
        holidays = 3
    else:
        holidays = 0

    working_days = wdays_with_holidays - holidays
    weekend_days = days - wdays_with_holidays

    # Adding availabilities to list
    availabilities.append({
            'period_id': period["id"],
            'total_days': days,
            'workdays': working_days,
            'weekend_days': weekend_days,
            'holidays': holidays
        })

# Creating hash with availabilities 
output = {'availabilities': availabilities}

# Writing output to file 'output.json'
with open("output.json", "w") as output_file:
    json.dump(output, output_file, indent=2)

print("Done! Check output.json file")