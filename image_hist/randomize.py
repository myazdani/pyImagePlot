import csv
import random

input_path = "/Users/myazdaniUCSD/Desktop/oscars_at_dolb_with_paths.csv"
output_path = "/Users/myazdaniUCSD/Desktop/shuffled.csv"

with open(input_path, "rb") as file:
    rows = list(csv.reader(file, delimiter=","))

random.shuffle(rows)

with open(output_path, "wb") as file:
    csv.writer(file, delimiter=",").writerows(rows)

