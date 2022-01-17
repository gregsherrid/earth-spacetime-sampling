from text_to_float import text_to_float
from sample_from_time import sample_year
from sample_from_globe import sample_lat_long
import re

def get_brutus_lines():
    with open('./data/brutus.txt', 'r') as f:
        return f.read().split("\n")
    return

def get_fixed_length_substrings(text, l):
    return [text[i * l:(i + 1) * l] for i in range(0, 1 + len(text) // l)]

def get_tolstoy(by="sentence"):
    with open('./data/tolstoy.txt', 'r') as f:
        text = f.read()

    if by == "sentence":
        # Not a precise way to split by sentence, but good enough for an example
        spans = text.split(".")

    elif by == "word":
        spans = re.split("\s+", text)

    elif by == "span-10":
        spans = get_fixed_length_substrings(text, 10)

    elif by == "span-100":
        spans = get_fixed_length_substrings(text, 100)

    elif by == "span-1000":
        spans = get_fixed_length_substrings(text, 1000)

    else:
        raise "Unknown span by %s" % by

    spans = [x.strip() for x in spans]
    return [x for x in spans if len(x) > 0]

def print_example_lat_long_pairs():
    print("Latitude", "Longitude")
    for span in get_tolstoy()[0:100]:
        value = text_to_float(span)
        lat, lon = sample_lat_long(value)
        print(lat, lon)

print_example_lat_long_pairs()