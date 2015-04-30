import os
import cv2
import csv
from pylab import *
import scipy
import scipy.misc
from scipy import stats
from PIL import Image
import collections

def return_rows(filename, file_encoding = 'rU'):
  with open(filename, file_encoding) as f: 
    reader = csv.reader(f)
    rowsInData = [row for row in reader]
  return rowsInData  


def create_hourly_colors(lines, out_file):
    #lines = return_rows(in_file)

    hours = set([line[1] for line in lines[0:]])
    hours_colors = {}
    width = 500
    for hour in hours:
        #hsv_colors = array([list(map(lambda x: float(x) - 1.0, line[2:])) for line in lines[0:] if line[1] == hour])
        hsv_colors = array([list(map(lambda x: float(x), line[2:])) for line in lines[0:] if line[1] == hour])
        hsv_colors[:,1] = 255 # keep saturation fixed
        #hsv_colors[:,2] = 255 # keep value fixed
        #hsv_colors = hsv_colors[hsv_colors[:,0].argsort()]
        ind = lexsort((hsv_colors[:,0], hsv_colors[:,1], hsv_colors[:,2]))
        hsv_colors = hsv_colors[ind]
        height = hsv_colors.shape[0]
        hsv = reshape(hsv_colors, (height, 1, 3))
        hours_colors[int(hour)] = array(tile(hsv, (1, width, 1)), dtype = uint8)


    od = collections.OrderedDict(sorted(hours_colors.items()))

    all_hours = cv2.cvtColor(od[0], cv2.COLOR_HSV2BGR)
    for hour in od.keys()[1:]:
        all_hours = hstack((all_hours, cv2.cvtColor(od[hour], cv2.COLOR_HSV2BGR)))

    cv2.imwrite(out_file, all_hours)

if __name__ == "__main__":
    in_file = "/Users/myazdaniUCSD/Dropbox/Broadway_processed_data/processedData/dom_HSV_sample.csv"
    out_path = "/Users/myazdaniUCSD/Desktop/hourly_colors/all_hours.png"

    create_hourly_colors(return_rows(in_file), out_path)
