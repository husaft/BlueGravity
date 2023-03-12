# BMI (Body Mass Index)

def calc_bmi(weight_kg, height_m, age, new_exp):
    bmi = weight_kg / (height_m ** 2) if not new_exp \
        else 1.3 * weight_kg / (height_m ** 2.5)
    if age < 18:
        raise ValueError("Not reliable for individuals under 18 years old!")
    status = 'healthy'
    if bmi > 40:
        status = 'obese III'
    elif bmi >= 35:
        status = 'obese II'
    elif bmi >= 30:
        status = 'obese'
    elif bmi >= 25:
        status = 'overweight'
    elif bmi < 18.5:
        status = 'underweight'
    return {'b': bmi, 'c': status}


def find_bmi_range(height_m, age, new_exp):
    cat = dict()
    for mkg in range(0, 1500, 1):
        kg = mkg / 10.0
        res = calc_bmi(kg, height_m, age, new_exp)
        rc = res['c']
        if rc not in cat:
            cat[rc] = {'min': 4999, 'max': -4999}
        cat[rc]['min'] = min(cat[rc]['min'], kg)
        cat[rc]['max'] = max(cat[rc]['max'], kg)
    return cat
