# Want to sample from 5000 BC to 2000 AD.
MIN_YEAR = -1999 # Actually 2000 BC because of how we handle the fact that there's no year 0
MAX_YEAR = 2000

def sample_year(value, start_year=MIN_YEAR, end_year=MAX_YEAR):
    part_1 = value ** 0.3
    part_2 = 1 - (1 - value) ** 3

    scaled = (part_1 + part_2) / 2
    raw_year = scaled * (MAX_YEAR - MIN_YEAR) + MIN_YEAR

    # Annoying behavior to deal with there being no year 0
    if raw_year < 0.5:
        year = round(abs(raw_year - 1))
        return "%s BC" % year
    else:
        year = round(raw_year)
        return "%s AD" % year