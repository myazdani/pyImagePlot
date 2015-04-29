import csv
import operator
from my_montage_maker import *
import math
from PIL import Image
import os
import sys

if len(sys.argv) < 2:
    print "Include input path, output path, and image type"
    sys.exit()
else:
    src_path = sys.argv[1] #input path
    output_path = sys.argv[2] #output path
    image_type = sys.argv[3] #image type (jpg, png, etc)

photow,photoh = 100,100
 
path_parents = []  
for root, dirs, files in os.walk(src_path):
  path_parents.append([os.path.join(root, f) for f in files if f.endswith(image_type)])


for path_parent in path_parents:
    if len(path_parent) == 0: continue
    #image_paths = path_parent[0:49]
    image_paths = path_parent
    path_splits = image_paths[0].split(src_path)[1].split("/")
    montage_filename = ""
    for path_split in path_splits[:-1]: 
        montage_filename = montage_filename + "_" + path_split
    print "working on", montage_filename

    filedim = math.sqrt(len(image_paths))
    if (filedim%int(filedim) == 0): ncols, nrows = int(filedim),int(filedim)
    else: ncols, nrows = int(filedim), int(filedim)+1
    if ncols == 0: continue
    photo = (photow,photoh)
    margins = [0,0,0,0]
    padding = 0
    inew = make_contact_sheet(image_paths,(ncols,nrows),photo,margins,padding)

    inew.save(output_path + "montage" + montage_filename + ".jpg")
	