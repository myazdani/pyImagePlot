import os
from PIL import Image, ImageDraw
from pylab import *
import csv

class ImageScatterPlot:
  def __init__(self):
    self.h, self.w = 20000,20000
    self.resize_h = 275
    self.resize_w = 275

  def create_save_fig(self, image_paths, projected_features, out_file):
    img_scatter = self.create_fig(image_paths, projected_features)
    self.save_fig(img_scatter, out_file)

  def create_fig(self, image_paths, projected_features):
    img = Image.new('RGB',(self.w,self.h),(255,255,255))
    draw = ImageDraw.Draw(img)

    scale = abs(projected_features).max(0)
    scaled = floor(array([ (p / scale) * (self.w/2-20,self.h/2-20) + (self.w/2,self.h/2) for p in projected_features]))
    print "number of images", len(image_paths)
    for i in range(len(image_paths)):
      nodeim = Image.open(image_paths[i]) 
      nodeim = nodeim.resize((self.resize_w,self.resize_h))
      ns = nodeim.size 
      img.paste(nodeim,(int(scaled[i][0]-ns[0]//2),int(scaled[i][1]-ns[1]//2),int(scaled[i][0]+ns[0]//2+1),int(scaled[i][1]+ns[1]//2+1))) 

    return img

  def save_fig(self, img, out_file):
    img.save(out_file)

if __name__ == "__main__":
  in_file = "PNAR-tsne-HOG-color.csv"
  out_file = "res-class.jpg"
  
  rows = []
  with open(in_file, 'rb') as f:
      reader = csv.reader(f)
      for row in reader:
          rows.append(row)

  rows.pop(0)
  image_paths = [row[0] for row in rows]
  features = array([(float(row[1]), float(row[2])) for row in rows])
  ImageScatterPlot().create_save_fig(image_paths = image_paths, projected_features = features, out_file = out_file)