from dateutil.relativedelta import relativedelta
from datetime import datetime


def parse_person_data(person):
    birth_txt = person['birthdate']
    height_cm = person['height_cm']

    height_m = height_cm / 100.0
    now = datetime.now().date()
    birth = datetime.fromisoformat(birth_txt).date()
    rel_delta = relativedelta(now, birth)
    r_delta = {'y': rel_delta.years, 'm': rel_delta.months, 'd': rel_delta.days}

    return {"birthdate": birth, 'height_cm': height_cm, 'height_m': height_m, 'age': r_delta}
