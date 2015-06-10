import csv

in_file =  "/Users/cheriehuang/Documents/broadway_images_sample/dom_HSV_small_sample.csv"
image_path = "/Users/cheriehuang/Documents/broadway_images_sample/"
out_path = "/Users/cheriehuang/Documents/broadway_images_sample/altered.csv"


def return_rows(filename, file_encoding = 'rU'):
  with open(filename, file_encoding) as f:
    reader = csv.reader(f)
    rowsInData = [row for row in reader]
  return rowsInData

data_rows = return_rows(in_file)

## assume first row is a header row
image_paths = [image_path + data_row[0] for data_row in data_rows[1:]]

f = open(out_path, 'wt')

header_row = data_rows[0]

try:
	writer = csv.writer(f)
	writer.writerow( header_row )
	for i, data_row in enumerate(data_rows[1:]):
		row = [image_paths[i]]
		row.extend(data_row[1:])
		writer.writerow(row)
finally:
	f.close()
