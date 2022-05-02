from text_to_float import text_to_float
from sample_from_time import sample_year
from sample_from_globe import sample_lat_long
import re
from IPython import embed

def get_brutus_lines():
    with open('./data/brutus.txt', 'r') as f:
        return f.read().split("\n")
    return

def get_fixed_length_substrings(text, l):
    return [text[i * l:(i + 1) * l] for i in range(0, 1 + len(text) // l)]

def get_text_from_file(filepath, by="sentence"):
    with open(filepath, 'r') as f:
        text = f.read()

    if by == "sentence":
        # Not a precise way to split by sentence, but good enough for an example
        spans = text.split(".")

    elif by == "line":
        # Not a precise way to split by sentence, but good enough for an example
        spans = text.split("\n")

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

def print_location_time_pairs(spans):
    index = 0
    while index < len(spans) - 2:
        when_span = spans[index]
        when_value = text_to_float(when_span)
        year = sample_year(when_value)

        where_span = spans[index + 1]
        where_value = text_to_float(where_span)
        lat, lon = sample_lat_long(where_value)

        print(when_span)
        print("When:\t%s" % year)
        print(where_span)
        print("Where:\t%s\t%s" % (lat, lon))
        print("\n-----------\n")

        index += 2

def print_example_lat_long_pairs():
    print("Latitude", "Longitude")
    for span in get_tolstoy()[0:100]:
        value = text_to_float(span)
        lat, lon = sample_lat_long(value)
        print(lat, lon)

if __name__ == "__main__":
    spans = get_text_from_file("./data/byzantium.txt", by="line")
    print_location_time_pairs(spans)
