import sys
import os
from montage_manager import Montages
import pandas as pd

class Menu:
	'''Display menu and respond to choices when run.'''
	def __init__(self):
		self.montage = Montages()
		self.choices = {
		"1": self.montage_dir,
		"2": self.montage_from_csv,
		"3": self.img_scatter,
		"4": self.image_hist_from_csv,
		"5": self.quit
		}

	def display_menu(self):
		print("""
PyMontage Menu
1. Create montages from recursively from given directory and sub-directories
2. Create montages from provided CSV files (split by categories or bins)
3. Create vetical montge from provided CSV file
4. Create image histogram from provided CSV file
5. Quit 
""")

	def run(self):
		'''Display the menu and responsd to choices'''
		while True:
			self.display_menu()
			choice = input("Enter an option: ")
			action = self.choices.get(str(choice))
			if action:
				action()
			else:
				print("{0} is not a valid choice".format(choice))

	def enter_dir(self, message = "Provide valid directory"):
		while True:
			provided_dir = raw_input(message)
			if os.path.isdir(provided_dir): break
			else: print("Not a valid directory")

		return provided_dir

	def montage_dir(self):
		input_dir = self.enter_dir("Provide full path to directory to create montages: ")
		output_dir = self.enter_dir("Provide full path to valid direcotry to save montages: ")
		self.montage.input_data(src_path = input_dir, dest_path = output_dir)
		print("Creating montages...")
		created_montages = self.montage.montages_from_directory()
		for i, created_montage in enumerate(created_montages):
			created_montage.save(output_dir + "/montage-" + str(i) + ".jpg")
		print("Saving montages complete.")

	def enter_csv(self, message = "provide path to valid csv"):
		while True:
			provided_csv = raw_input(message)
			if os.path.isfile(provided_csv): break
			else: print("Not a valid file")

		return provided_csv

	def montage_from_csv(self):
		input_csv = self.enter_csv("Provide full path to csv file for creating montages: ")
		output_dir = self.enter_dir("Provide full path to valid direcotry to save montages: ")
		print("Creating montages...")
		df = pd.read_csv(input_csv)
		created_montages = self.montage.binned_montage(df)
		for i, created_montage in enumerate(created_montages):
			created_montage.save(output_dir + "/montage-" + str(i) + ".png")
		print("Saving montages complete.")


	def img_scatter(self):
		input_csv = self.enter_csv("Provide full path to csv file for creating image scatter plot: ")
		output_dir = self.enter_dir("Provide full path and name to valid direcotry to save image scatter plot: ")
		print("Creating image scatter plot...")
		df = pd.read_csv(input_csv)
		created_img_scatter = self.montage.scatter(df)
		created_img_scatter.save(output_dir)

	def image_hist_from_csv(self):
		input_CSV = self.enter_csv("Provide full path to csv file for creating image histogram: ")
		output_dir = self.enter_dir("Provide full path and fielname to  save image histogram: ")
		self.montage.input_data(src_path = input_CSV, dest_path = output_dir)
		print("Creating image histogram...")
		self.montage.create_image_hist()


	def quit(self):
		print("Good bye!")
		sys.exit(0)

if __name__ == "__main__":
	Menu().run()