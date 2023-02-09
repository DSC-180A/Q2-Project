
import seaborn as sns
import matplotlib.pyplot as pyplot
import pandas as pd

def save_plot(plot, path, filename, extension):
	plot.figure.savefig(path + "/" + filename + "." + extension)