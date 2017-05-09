import csv
import operator
from my_montage_maker import *
import math
import numpy as np
from PIL import Image, ImageDraw
from operator import itemgetter
import os
import sys
import heapq
import pandas as pd

class Montages:
	'''Create and manage montages'''
	def __init__(self, src_path ="", dest_path = "", image_src_path = ""):
		self.photow = 75
		self.photoh = 75
		#self.photow = 12000
		#self.photoh = 1000
		self.src_path = src_path
		self.dest_path = dest_path
		self.image_src_path  = image_src_path
		self.image_type = (".jpg", ".JPG", ".PNG", ".png", ".tiff", ".TIFF", ".jpeg", ".JPEG")

	def _return_rows(self, filename, file_encoding = 'rU'):
		with open(filename, file_encoding) as f: 
			reader = csv.reader(f)
			rowsInData = [row for row in reader]
		return rowsInData  

	def _get_paths_from_dir(self, dir_path):
		path_parents = []
		for root, dirs, files in os.walk(dir_path):
			path_parents.append([os.path.join(root, f) for f in files if f.endswith(self.image_type)])
		return path_parents

	def input_data(self, src_path, dest_path, image_src_path = ""):
		self.src_path = src_path
		self.dest_path = dest_path
		self.image_src_path  = image_src_path


	def create_montage(self, image_paths, montage_filename = "", ncols = None, nrows = None):
		filedim = math.sqrt(len(image_paths))
		if ncols == None:
			if (filedim%int(filedim) == 0): ncols, nrows = int(filedim),int(filedim)
			else: ncols, nrows = int(filedim), int(filedim)+1
		if ncols == 0: 
			ncols = 1
			nrows = len(image_paths)

		if nrows == 0:
			nrows = 1
			ncols = len(image_paths)
		photo = (self.photow,self.photoh)
		margins = [0,0,0,0]
		padding = 0
		inew = make_contact_sheet(image_paths,(ncols,nrows),photo,margins,padding)
		#inew.save(self.dest_path + montage_filename + ".jpg")
		return inew, montage_filename


	def montages_from_directory(self, thumb_w = 75, thumb_h = 75):
		'''create montages from given directory recursively'''
		self.photow = thumb_w
		self.photoh = thumb_h
		path_parents = self._get_paths_from_dir(self.src_path)
		montages_created = []
		for path_parent in path_parents:
			if len(path_parent) == 0: continue
			path_split = path_parent[0].split(self.src_path)[1].split("/")[0]
			montage_filename = path_split + "_montage"
			montages_created.append(self.create_montage(path_parent, montage_filename))

		return montages_created

	def read_data(self):
		# df = pd.read_csv(self.src_path, header = True)
		df = self._return_rows(self.src_path)
		return df
	'''
	def montage_from_csv_binned(self, data, ncols = None, nrows = None):
		#rows = self._return_rows(self.src_path)
		rows = data
		header = rows.pop(0)
		bins = list(set([row[1] for row in rows]))
		path_parents = {}
		for bin in bins:
			if len(header) > 2:
				unsorted_list = [[self.image_src_path + row[0], float(row[-1])] for row in rows if row[1] == bin]
				sorted_list = sorted(unsorted_list, key=itemgetter(1))
				path_parents[bin] = [item[0] for item in sorted_list]
			else:
				path_parents[bin] = [self.image_src_path + row[0] for row in rows if row[1] == bin]
		for bin in path_parents.keys():
			montage_filename = "bin_" + bin
			self.create_montage(path_parents[bin], montage_filename, ncols, nrows)
	'''

	def binned_montage(self, df, img_paths_col = None, bins_col = None, vals_col = None):
		#rows = self._return_rows(self.src_path)
		if img_paths_col in df.columns and bins_col in df.columns and vals_col in df.columns:
			df_rel = df[[img_paths_col, bins_col, vals_col]]
		else:
			df_rel = df.iloc[:,range(3)]
		data = df_rel.values.tolist()
		rows = data
		header = rows.pop(0)
		bins = list(set([row[1] for row in rows]))
		path_parents = {}
		for bin in bins:
			if len(header) > 2:
				unsorted_list = [[self.image_src_path + row[0], float(row[-1])] for row in rows if row[1] == bin]
				sorted_list = sorted(unsorted_list, key=itemgetter(1))
				path_parents[bin] = [item[0] for item in sorted_list]
			else:
				path_parents[bin] = [self.image_src_path + row[0] for row in rows if row[1] == bin]
		montages_created = []
		for bin in path_parents.keys():
			montage_filename = "bin_" + bin
			print "number of images:", len(path_parents[bin])           
			montages_created.append(self.create_montage(path_parents[bin], montage_filename, ncols = None, nrows = None))
		return montages_created

	def scatter(self, df, img_w = 20000, img_h = 20000, thumb_w = 175, thumb_h = 175, img_paths_col = None, x_col = None, y_col = None):
		if img_paths_col in df.columns and x_col in df.columns and y_col in df.columns:
			df_rel = df[[img_paths_col, x_col, y_col]]
		else:
			df_rel = df.iloc[:,range(3)]

		rows = df_rel.values.tolist()

		image_paths = [row[0] for row in rows]
		projected_features = np.array([(float(row[1]), float(row[2])) for row in rows])

		h,w = img_h,img_w
		img = Image.new('RGB',(w,h),(0,0,0))
		draw = ImageDraw.Draw(img)

		scale = abs(projected_features).max(0)
		scaled = np.floor(np.array([ (p / scale) * (w/2-20,h/2-20) + (w/2,h/2) for p in projected_features]))
		print "number of images", len(image_paths)
		for i in range(len(image_paths)):
		  nodeim = Image.open(image_paths[i]) 
		  nodeim = nodeim.resize((thumb_w,thumb_h))
		  ns = nodeim.size 
		  img.paste(nodeim,(int(scaled[i][0]-ns[0]//2),int(scaled[i][1]-ns[1]//2),int(scaled[i][0]+ns[0]//2+1),int(scaled[i][1]+ns[1]//2+1))) 

		return img

	def create_image_hist(self, src_path = None):
		#first opening the csv file to be read
		f = open(self.src_path, 'rb')
		data = csv.reader(f)

		#initializing the heapq to be read into
		heap = []
		#initializing the dict to be read into
		bins = {}
		#for loop to read through the csv file
		for row in data:
			#first read the bin into a string
			try:
				bin = int(row[1])
			except:
				continue
		    #check if this key already exists in the dict
			if bin not in bins.keys():
		    	#if not create a new list at that bin index
				bins[bin] = []
		    #either way append the tuple to the list at the right bin
			bins[int(bin)].append((int(row[2]), row[0]))
			#pushing the value and path combination onto the heap
			#heappush(heap, (int(row[2]), row[0]))    bins
		#have now finished reading in all the data, now must make all the lists, min heaps with heapq
		#for loop to do this
		height = 0
		index = 0
		for key in bins:
			#changing every list into a heapq
			heapq.heapify(bins[key])
			length  = len(bins[key])
			#getting the tallest height
			if height<length:
				height=length
		#getting the total number of bins
		NumBins = len(bins)
		#size of each image
		size = 75
		size1 = size + 5
		graphH = size1 * height
		graphW = size1 * NumBins
		#creating the background window
		img = Image.new('RGB',(graphW,graphH),(0,0,0))
		SIZES = size, size
		#for loop to loop through each bin and paste

		for key in bins:
			theQ = bins[key]
			#initializing the yCoord as the very bottom of the graph
			yCoord = graphH
			xCoord = key * size1
			#while loop to loop through the heapq and paste the images one by one from bottom up
			while len(theQ) != 0:
				#getting the image path
				popped = heapq.heappop(theQ)
				path = popped[1]
				im = Image.open(path)
				im.thumbnail(SIZES, Image.ANTIALIAS)
				img.paste(im,(xCoord,yCoord))
				yCoord = yCoord - size1

		#end of the for loop
		#saving the img into a png image
		#img.save(self.dest_path + "hist.png" )
		return img
        



if __name__ == "__main__":
	in_file = "/Users/myazdaniUCSD/Dropbox/Broadway_processed_data/processedData/dom_HSV_small_sample.csv"
	image_dir = "/Users/myazdaniUCSD/Dropbox/Broadway_processed_data/broadway_images_sample/"
	out_file = "/Users/myazdaniUCSD/Desktop/"
	a_montage = Montages()
	a_montage.intput_data(src_path = in_file, dest_path = out_file, image_src_path = image_dir)

