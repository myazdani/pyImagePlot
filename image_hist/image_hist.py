## image_hist.py
##
## Cherie Huang, Spring 2015


import heapq
import csv
import numpy as np
from PIL import Image, ImageDraw


#the outfile
out_file = '/Users/myazdaniUCSD/Desktop/boston-april-18.png'

#first opening the csv file to be read
f = open('/Users/myazdaniUCSD/Desktop/boston-2013-04-18.csv', 'rb')
data = csv.reader(f)

#initializing the heapq to be read into 
heap = []
#initializing the dict to be read into
bins = {}
#for loop to read through the csv file
for row in data:
	#first read the bin into a string
	bin = int(row[1])
	print bin
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
size = 50
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
img.save(out_file)

