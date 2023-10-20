import json
from datetime import datetime, timedelta

# Read data from file 'data.json'
with open("data.json", "r") as file:
    data = json.load(file)

availabilities = []

# Calculating availabilities for each period
for period in data["periods"]:

    # Parsing starting date and ending date from period
    since_date = datetime.strptime(period["since"], "%Y-%m-%d")
    until_date = datetime.strptime(period["until"], "%Y-%m-%d")

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