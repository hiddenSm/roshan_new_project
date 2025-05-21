import jdatetime, re
from datetime import datetime, time

def persian_to_latin_digits(text):
    persian_digits = "۰۱۲۳۴۵۶۷۸۹"
    latin_digits = "0123456789"
    translation_table = str.maketrans(persian_digits, latin_digits)
    return text.translate(translation_table)

# Gregorian is AD date
def jalali_to_gregorian(date_text):
    if "-" in date_text: 
        date_part, time_part = date_text.split(' - ')
        time_part = persian_to_latin_digits(time_part)
        jalali_date = change_date(date_part)

    else:  
        jalali_date = change_date(date_text)
        time_part = "23:59"


    combined_datetime = datetime.strptime(f"{jalali_date} {time_part}", "%Y-%m-%d %H:%M")
    formatted_datetime = combined_datetime.isoformat(timespec='microseconds') + "Z"
    gregorian_date = f"{formatted_datetime}"

    return gregorian_date


def change_date(date_part):
    date_only = re.sub(r'^[^\d]*', '', date_part).strip()

    day, month, year = date_only.split(' ')
    day = int(day)

    months = {
                'فروردین': 1, 'اردیبهشت': 2, 'خرداد': 3,
                'تیر': 4, 'مرداد': 5, 'شهریور': 6,
                'مهر': 7, 'آبان': 8, 'آذر': 9,
                'دی': 10, 'بهمن': 11, 'اسفند': 12
            }
    
    month_number = months.get(month, 1)
    year = int(year)


    jalali_date = jdatetime.date(year, month_number, day).togregorian()
    return jalali_date

# datet = "دوشنبه ۲۹ اردیبهشت ۱۴۰۴ - ۱۶:۳۰"
# datet = "سه‌شنبه ۳۰ اردیبهشت ۱۴۰۴"
# print(jalali_to_gregorian(datet))
# print(type(time(hour=23, minute=59, second=00, microsecond=00)))
# print(new_func(datet))
