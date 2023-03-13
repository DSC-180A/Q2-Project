
import pandas as pd

def get_data(path):
	"""_summary_: Importing the data with pandas
        Args:
            path: string of file path
        Returns:
            pandas dataframe of csv
        """
	df = pd.read_csv(path)
	return df