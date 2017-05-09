import csv
import operator
from my_montage_maker import *
import math
from PIL import Image

in_file = "/Users/myazdaniUCSD/Documents/kiev-instagram/results/kmeans_hog/Kmeans_RGB_HOG_lat_long_65.csv"
image_path = "/Users/myazdaniUCSD/Documents/kiev-instagram/good_data/all_images/"
output_path = "/Users/myazdaniUCSD/Documents/kiev-instagram/results/kmeans_hog/cluster_montages_HOG_gps_65/"


sample = open(in_file, "r")
csv1 = csv.reader(sample, delimiter = ',')
sorted_csv = sorted(csv1, key = operator.itemgetter(0,2))

#first col = cluster number
#second col = filename
#third col = distance from cluster center

for i in range(1,66):
    print "cluster", i
    cluster_filenames = [image_path + eachLine[1] for eachLine in sorted_csv if eachLine[0] == str(i)]
    if len(cluster_filenames) == 0: continue
    filedim = math.sqrt(len(cluster_filenames))
    if (filedim%int(filedim) == 0): ncols, nrows = int(filedim),int(filedim)
    else: ncols, nrows = int(filedim), int(filedim)+1
    if ncols == 0: continue
    photow,photoh = 150,150
    photo = (photow,photoh)
    margins = [0,0,0,0]
    padding = 0
    inew = make_contact_sheet(cluster_filenames,(ncols,nrows),photo,margins,padding)
    inew.save(output_path+"cluster_"+ str(i)+ ".jpg")
	
	