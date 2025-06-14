from datetime import date


def calculate_age(birth_day, birth_month, birth_year):
    today = date.today()

    try:
        birth_date = date(birth_year, birth_month, birth_day)
    except ValueError:
        return None, "Invalid date. Please enter a valid calendar date."

    if birth_date > today:
        return None, "Invalid date: Birth date is in the future."

    # Calculate initial differences
    age_years = today.year - birth_date.year
    age_months = today.month - birth_date.month
    age_days = today.day - birth_date.day

    # Adjust for negative days
    if age_days < 0:
        age_months -= 1
        previous_month = today.month - 1 if today.month > 1 else 12
        previous_year = today.year if today.month > 1 else today.year - 1
        days_in_prev_month = (date(previous_year, previous_month + 1, 1) - date(previous_year, previous_month, 1)).days
        age_days += days_in_prev_month

    # Adjust for negative months
    if age_months < 0:
        age_years -= 1
        age_months += 12

    return (age_years, age_months, age_days), None


# ---------- Main Program Flow ----------
def main():
    print("Today's date is:", date.today().strftime('%d-%m-%Y'))
    birth_date_input = input("Enter your birth date in DD-MM-YYYY format: ")

    try:
        day, month, year = map(int, birth_date_input.strip().split('-'))
    except ValueError:
        print("Invalid format. Please enter the date as DD-MM-YYYY.")
        return

    age, error = calculate_age(day, month, year)

    if error:
        print(error)
    else:
        years, months, days = age
        print(f"\nYou are {years} years, {months} months, and {days} days old.")
        print(f"(As of today: {date.today().strftime('%d-%m-%Y')})")


# Run the program
main()
