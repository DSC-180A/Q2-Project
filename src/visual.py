
import seaborn as sns
import matplotlib.pyplot as pyplot
import pandas as pd

def save_plot(plot, path, filename, extension):
	#Saves the plot to a specific path with a specific file name and extension
	plot.figure.savefig(path + "/" + filename + "." + extension)