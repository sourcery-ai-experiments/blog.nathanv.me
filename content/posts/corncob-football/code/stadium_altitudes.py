import csv
import getpass
import os
import statistics

import googlemaps

API_FILE = "api_key.txt"
STADIUM_FILE = "stadiums.txt"


def main():
    if os.path.exists(API_FILE):
        with open(API_FILE) as f:
            api_key = f.read()
    else:
        api_key = getpass.getpass("Enter the Google Maps API key")

    # init google maps api
    client = googlemaps.Client(key=api_key)

    # create list to put elevations into
    elevations = []

    # open input file
    with open(STADIUM_FILE) as f:
        reader = csv.DictReader(f, delimiter="\t")
        for row in reader:
            stadium = row["Stadium"]
            print("Processing: {}".format(stadium))

            # first, geocode stadium to get lat/lon
            raw_result = client.geocode(stadium)
            lat_lng = raw_result[0]["geometry"]["location"]

            # next, plug in lat/lon to get an elevation in meters
            raw_result = client.elevation((lat_lng["lat"], lat_lng["lng"]))
            elevation = raw_result[0]["elevation"]
            elevations.append(elevation)

    # average data and output
    print("Average elevation: {} meters".format(statistics.mean(elevations)))


if __name__ == "__main__":
    main()
