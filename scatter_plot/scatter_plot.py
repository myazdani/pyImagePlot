import os
from PIL import Image, ImageDraw
from pylab import *
import csv

in_file = "PNAR-tsne-HOG-color.csv"
out_file = "res.jpg"

rows = []
with open(in_file, 'rb') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

rows.pop(0)
image_paths = [row[0] for row in rows]
projected_features = array([(float(row[1]), float(row[2])) for row in rows])

h,w = 20000,20000
img = Image.new('RGB',(w,h),(255,255,255))
draw = ImageDraw.Draw(img)

scale = abs(projected_features).max(0)
scaled = floor(array([ (p / scale) * (w/2-20,h/2-20) + (w/2,h/2) for p in projected_features]))
print "number of images", len(image_paths)
for i in range(len(image_paths)):
  nodeim = Image.open(image_paths[i]) 
  nodeim = nodeim.resize((275,275))
  ns = nodeim.size 
  img.paste(nodeim,(int(scaled[i][0]-ns[0]//2),int(scaled[i][1]-ns[1]//2),int(scaled[i][0]+ns[0]//2+1),int(scaled[i][1]+ns[1]//2+1))) 

img.save(out_file)