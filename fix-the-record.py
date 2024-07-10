import random
import subprocess
from datetime import datetime, timedelta

DAYS_OFF_PER_YEAR = 25
WEEKENDS_PER_MONTH = 2


def is_weekend(date):
    return date.weekday() == 5 or date.weekday() == 6


def determine_days_per_weekend():
    return random.randint(0, 2)


def get_current_year(current_date):
    return current_date.year


def get_current_month(current_date):
    return current_date.month


def get_current_day(current_date):
    return current_date.day


def get_current_week(current_date):
    iso_calendar = current_date.isocalendar()
    return iso_calendar[1]


def get_days_off_per_year():
    return DAYS_OFF_PER_YEAR


def reset_monthly_report():
    return {
        "weekend_days_worked": 0,
        "days_worked": 0,
        "weekend_days_off": 0,
        "checkins": 0,
        "vacation_days": 0,
    }


def next_day(current_date):
    return (current_date + timedelta(days=1)).replace(hour=8)
    # print("NEW DAY: ", current_date.isoformat())


def print_monthly_report():
    avg_checkins = monthly_report["checkins"] // monthly_report["days_worked"]
    print(
        f"days_worked: {monthly_report['days_worked']}, vacation_days: {monthly_report['vacation_days']}, weekend_days_worked: {monthly_report['weekend_days_worked']},  weekend_days_off: {monthly_report['weekend_days_off']}, avg_daily_chkins: {avg_checkins}"
    )


def worked_the_weekend():
    monthly_report["weekend_days_worked"] += 1


def worked_today():
    monthly_report["days_worked"] += 1


def weekend_day_off():
    # print("WEEKEND DAY OFF")
    monthly_report["weekend_days_off"] += 1


def checkin():
    monthly_report["checkins"] += 1


def vacation_day():
    monthly_report["vacation_days"] += 1


date_start = datetime.fromisoformat(f"2021-01-01")
date_end = datetime.fromisoformat("2021-05-01")
current_date = date_start

weekends_per_month = WEEKENDS_PER_MONTH
current_year = get_current_year(current_date)
current_month = get_current_month(current_date)
current_week = get_current_week(current_date)
current_day = get_current_day(current_date)
days_per_weekend = determine_days_per_weekend()
days_off_remaining_this_year = get_days_off_per_year()
days_since_day_off = 0
time_off = 0
daily_checkins = 0
monthly_report = reset_monthly_report()


while current_date < date_end:
    time_in_day_remaining = 12 * 60
    if time_off <= 0 and days_since_day_off > 21:
        if days_off_remaining_this_year > 0:
            # Assuming its been 14 days of work on average since we've take a vacation day or a holiday
            # and assuming we have any days left in the year to take time off...
            # let's calculate the remaining range of days and then set time_off
            min_days = min(days_off_remaining_this_year, 5)
            if min_days < 3:
                min_days = 3
            time_off = random.randint(1, min_days)

            if current_month < 6:
                time_off = time_off // 2

            # prevent taking too many days off
            if time_off > days_off_remaining_this_year:
                time_off = days_off_remaining_this_year

            # CHRISTMAS VACATION!!!
            if current_month == 12 and current_week > 50:
                time_off = days_off_remaining_this_year

            # NEW YEARS!!!!
            if current_month == 12 and current_day == 31:
                time_off = 2

    if current_year < get_current_year(current_date):
        print("HAPPY NEW YEAR!!")
        current_year = get_current_year(current_date)
        days_off_remaining_this_year = get_days_off_per_year()

    # determine what the current MONTH and WEEK are
    if current_month != get_current_month(current_date):
        current_month = get_current_month(current_date)
        weekends_per_month = WEEKENDS_PER_MONTH
        print_monthly_report()
        monthly_report = reset_monthly_report()

    if current_week != get_current_week(current_date):
        current_week = get_current_week(current_date)
        days_per_weekend = determine_days_per_weekend()
        # print(f"Current Week: {current_week}")
        # print(f"This week you will work ({days_per_weekend}) weekend days.  FUN!")

    if current_day != get_current_day(current_date):
        current_day = get_current_day(current_date)
        print(f"Daily Checkins: {daily_checkins}")
        daily_checkins = 0
        # IF THIS HAPPENS TO BE A WEEKEND...
        # ....and we have some allocated days to work them..
        if is_weekend(current_date) and (
            days_per_weekend <= 0 or weekends_per_month <= 0
        ):
            weekend_day_off()
            time_in_day_remaining = 0
            current_date = next_day(current_date)
            continue

        if time_off > 0:
            vacation_day()
            # VACATION DAY
            time_off -= 1
            time_in_day_remaining = 0
            days_off_remaining_this_year -= 1
            days_since_day_off = 0
            current_date = next_day(current_date)
            continue

        if is_weekend(current_date):
            days_per_weekend -= 1  # this
            weekends_per_month -= 1
            worked_the_weekend()
        else:
            days_since_day_off += 1

        worked_today()

    # IF WE HAVE NO TIME OFF
    # AND... We did't get the weekend off...
    if time_off <= 0 and time_in_day_remaining > 0:

        # WE NEED TO WORK
        while time_in_day_remaining > 0:
            # DURING THE DAY

            # Calculate an INTERVAL between commits
            rand_min = random.randint(20, 380)
            rand_min_two = random.randint(20, 280)
            ran_min = rand_min + rand_min_two // 2
            rand_second = random.randint(0, 60)

            # Decrement the time remaining after we "worked"
            time_in_day_remaining -= rand_min
            # what time is it now?
            current_date = current_date + timedelta(
                minutes=rand_min, seconds=rand_second
            )
            checkin()
            daily_checkins += 1
            if daily_checkins > 8:
                # more than 8 checkin's per day is pushing it
                # time_in_day_remaining = 0
                pass
        # DAY OVER

    current_date = next_day(current_date)


# for date in dates:
# command = f"USERNAME=lsmolic ACCESS_TOKEN=abcd YEAR={year} MONTH={month} DAY={day} ./make-history.sh"
# result = subprocess.run(['bash',command], check=True, text=True, capture_output=True)
