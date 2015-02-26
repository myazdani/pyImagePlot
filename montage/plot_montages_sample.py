import os
import operator
from my_montage_maker import *
import math
from PIL import Image
import random

src_path = "/Users/myazdaniUCSD/Documents/kiev-instagram/data/original_data/images/"
montage_path = "../montages/"

def get_immediate_subdirectories(dir):
    return [name for name in os.listdir(dir)
            if os.path.isdir(os.path.join(dir, name))]
            

days = get_immediate_subdirectories(src_path)
#image_paths = [src_path+days + "/thumb" for image_path in image_paths]

nrows = 30
ncols = 50
image_dim = 30
total_images = nrows*ncols
photow,photoh = image_dim,image_dim
photo = (photow,photoh)
margins = [0,0,0,0]
padding = 0
for day in days:
    print day
    image_path = src_path + "/" + day + "/thumb"
    image_list = [os.path.join(image_path,f) for f in os.listdir(image_path) if f.endswith('.jpg')]
    if len(image_list) < total_images: continue
    inds = random.sample(range(len(image_list)), total_images)
    image_list = [image_list[i] for i in inds]
    inew = make_contact_sheet(image_list,(ncols,nrows),photo,margins,padding)
    inew.save(montage_path+"m_"+ day+ ".jpg")
	
	