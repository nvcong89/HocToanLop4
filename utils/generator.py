import random

def gen_addition(level=1):
    """Generate addition problem based on level."""
    if level == 1:
        a = random.randint(1000, 9999)
        b = random.randint(1000, 9999)
    elif level == 2:
        a = random.randint(10000, 99999)
        b = random.randint(10000, 99999)
    else:
        a = random.randint(100000, 999999)
        b = random.randint(100000, 999999)
    return a, b, a + b

def gen_subtraction(level=1):
    if level == 1:
        b = random.randint(1000, 4999)
        a = random.randint(b + 1, 9999)
    elif level == 2:
        b = random.randint(10000, 49999)
        a = random.randint(b + 1, 99999)
    else:
        b = random.randint(100000, 499999)
        a = random.randint(b + 1, 999999)
    return a, b, a - b

def gen_multiplication(level=1):
    if level == 1:
        a = random.randint(10, 99)
        b = random.randint(2, 9)
    elif level == 2:
        a = random.randint(100, 999)
        b = random.randint(10, 99)
    else:
        a = random.randint(1000, 9999)
        b = random.randint(10, 99)
    return a, b, a * b

def gen_division(level=1):
    if level == 1:
        b = random.randint(2, 9)
        result = random.randint(10, 99)
        a = b * result
        remainder = 0
    elif level == 2:
        b = random.randint(2, 9)
        result = random.randint(100, 999)
        remainder = random.randint(0, b - 1)
        a = b * result + remainder
    else:
        b = random.randint(10, 99)
        result = random.randint(10, 99)
        remainder = random.randint(0, b - 1)
        a = b * result + remainder
    return a, b, result, remainder

def gen_fraction_compare():
    """Generate two fractions to compare."""
    denominators = [2, 3, 4, 5, 6, 8, 10]
    d1 = random.choice(denominators)
    d2 = random.choice([d for d in denominators if d != d1])
    n1 = random.randint(1, d1 - 1)
    n2 = random.randint(1, d2 - 1)
    val1 = n1 / d1
    val2 = n2 / d2
    if val1 > val2:
        sign = ">"
    elif val1 < val2:
        sign = "<"
    else:
        sign = "="
    return n1, d1, n2, d2, sign

def gen_fraction_add_sub(operation="add"):
    """Generate fraction addition or subtraction with same denominator."""
    d = random.choice([2, 3, 4, 5, 6, 8, 10])
    if operation == "add":
        n1 = random.randint(1, d - 1)
        n2 = random.randint(1, d - n1)
        result_n = n1 + n2
        # simplify
        from math import gcd
        g = gcd(result_n, d)
        return n1, d, n2, d, result_n // g, d // g, "+"
    else:
        n1 = random.randint(2, d)
        n2 = random.randint(1, n1 - 1)
        result_n = n1 - n2
        from math import gcd
        g = gcd(result_n, d) if result_n > 0 else 1
        return n1, d, n2, d, result_n // g, d // g, "-"

def gen_perimeter_rectangle():
    a = random.randint(3, 30)
    b = random.randint(3, 30)
    perimeter = 2 * (a + b)
    area = a * b
    return a, b, perimeter, area

def gen_perimeter_square():
    a = random.randint(3, 30)
    perimeter = 4 * a
    area = a * a
    return a, perimeter, area

def gen_unit_conversion(unit_type="length"):
    """Generate unit conversion problems."""
    if unit_type == "length":
        units = {
            "km→m": (1, 1000),
            "m→dm": (1, 10),
            "dm→cm": (1, 10),
            "cm→mm": (1, 10),
            "m→cm": (1, 100),
        }
        key = random.choice(list(units.keys()))
        from_unit, to_unit = key.split("→")
        factor = units[key][1]
        value = random.randint(1, 50)
        return value, from_unit, to_unit, value * factor

    elif unit_type == "weight":
        conversions = {
            "kg→g": 1000,
            "tấn→kg": 1000,
            "yến→kg": 10,
            "tạ→kg": 100,
        }
        key = random.choice(list(conversions.keys()))
        from_unit, to_unit = key.split("→")
        factor = conversions[key]
        value = random.randint(1, 20)
        return value, from_unit, to_unit, value * factor

    elif unit_type == "time":
        conversions = {
            "giờ→phút": 60,
            "phút→giây": 60,
            "ngày→giờ": 24,
            "tuần→ngày": 7,
            "năm→tháng": 12,
        }
        key = random.choice(list(conversions.keys()))
        from_unit, to_unit = key.split("→")
        factor = conversions[key]
        value = random.randint(1, 10)
        return value, from_unit, to_unit, value * factor
