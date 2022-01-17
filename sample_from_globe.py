import math
import csv

# https://sedac.ciesin.columbia.edu/data/set/gpw-v4-population-count-rev11/data-download
POPULATION_GRID_FILE = "data/gpw_v4_population_count_rev11_2000_15_min.asc"

POPULATION_FLAT_FILE = "data/world-population-2000.csv"

# Will be loaded in the first time `sample_lat_long` is called
SUM_POPULATION = None
SUM_LOG_POPULATION = None
POPULATION_DATA = None

def sample_lat_long(value, with_sqrt_pops=False):

    if POPULATION_DATA is None:
        populate_population_data()

    if with_sqrt_pops:
        pop_key = "SQRT Population"
        cumulative_target = value * SUM_LOG_POPULATION
    else:
        pop_key = "Population"
        cumulative_target = value * SUM_POPULATION

    # This could be improved by a lot with binary search / sensible data structures
    running_count = 0
    for row in POPULATION_DATA:
        running_count += row[pop_key]
        if running_count > cumulative_target:
            return (row["Latitude"], row["Longitude"])


def populate_population_data():
    global POPULATION_DATA, SUM_POPULATION, SUM_LOG_POPULATION

    POPULATION_DATA = []
    SUM_POPULATION = 0
    SUM_LOG_POPULATION = 0

    with open(POPULATION_FLAT_FILE, newline="") as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            row = dict(row)
            row["Population"] = int(row["Population"])
            row["SQRT Population"] = int(row["SQRT Population"])
            SUM_POPULATION += row["Population"]
            SUM_LOG_POPULATION += row["SQRT Population"]
            POPULATION_DATA.append(row)


# Only run to turn the .asc file into the (more verbose; easier to parse) format I want
# I found it fun to do this without libraries
def generate_population_flatfile():
    with open(POPULATION_GRID_FILE) as file:
        # We assume specific headers
        N_COLS = file.readline().strip().split(" ")[-1]
        N_ROWS = file.readline().strip().split(" ")[-1]
        MIN_LON = float(file.readline().strip().split(" ")[-1])
        MIN_LAT = float(file.readline().strip().split(" ")[-1])
        CELLSIZE = float(file.readline().strip().split(" ")[-1])
        NODATA = file.readline().strip().split(" ")[-1]

        line = file.readline().strip()
        lat = 90 # You'd think this woud be MIN_LAT, but no, too easy

        output_rows = [[
            "Latitude",
            "Longitude",
            "Population",
            "SQRT Population"
        ]]

        while line:
            lon = MIN_LON
            for cell in line.strip().split(" "):
                lon = lon + CELLSIZE
                
                if cell == NODATA:
                    # No people here
                    continue

                population = math.floor(float(cell))
                if population == 0:
                    # Still not really any people here
                    continue

                output = [
                    lat + CELLSIZE / 2,
                    lon + CELLSIZE / 2,
                    population,
                    round(math.sqrt(population))
                ]
                output_rows.append(output)

            lat = lat - CELLSIZE # Again, you'd think + CELLSIZE, but we're actually counting down on lat
            line = file.readline().strip()

        with open(POPULATION_FLAT_FILE, "w", newline="") as csvfile:
            writer = csv.writer(csvfile, delimiter=",")
            for line in output_rows:
                writer.writerow(line)

if __name__ == "__main__":
    generate_population_flatfile()