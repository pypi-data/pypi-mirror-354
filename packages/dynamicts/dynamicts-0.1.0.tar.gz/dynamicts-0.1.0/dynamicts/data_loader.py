"""
data_loader.py
Module to load time series data and provide a shared interface for other modules.
"""
import logging
from typing import Optional, Union
import pandas as pd
import json
import os

class DataLoader:
    """
    DataLoader is a class for loading and managing time series data from a CSV file.
    Attributes:
        filepath (str): Path to the CSV file containing the data.
        index_col (str or int, optional): Column to use as the row labels of the DataFrame.
        parse_dates (bool or list, optional): Whether to parse dates in the index column.
        data (pd.DataFrame or None): Loaded data after calling `load()`.
    Methods:
        load():
            Loads the data from the specified CSV file, saves metadata, and standardizes column names to lowercase.
            Returns the loaded DataFrame.
        is_regular():
            Checks if the time series index is regular (i.e., intervals between timestamps are uniform).
            Returns True if regular, False otherwise.
        save_metadata():
            Saves metadata (columns, dtypes, shape, index name) of the loaded DataFrame to a JSON file
            with the same name as the CSV file, suffixed with '_meta.json'.
        run_pipeline():
            Runs the data loading pipeline: loads data, checks regularity, and renames the first column to 'y' if regular.
            Returns the processed DataFrame if regular, otherwise None.
    """
    """A class to load and manage time series data."""
    
    def __init__(self, filepath, index_col=None, parse_dates=True):
        self.filepath = filepath
        self.index_col = index_col
        self.parse_dates = parse_dates
        self.data = None
        if "logs" not in os.listdir("dynamicts"):
            os.mkdir("dynamicts/logs")
        # Set up logging
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler("dynamicts/logs/data_loader.log"),
                logging.StreamHandler()
            ]
            )

    def load(self) -> pd.DataFrame:
        """Load the data from the specified CSV file."""
        try:
            self.data = pd.read_csv(self.filepath, index_col=self.index_col, parse_dates=self.parse_dates)
            self.data.columns = self.data.columns.str.lower()
            self.data.index.name = 'date'
            self.save_metadata()
            return self.data
        except Exception as e:
            logging.error(f"Error loading data from {self.filepath}: {e}")
            raise ValueError(f"Failed to load data from {self.filepath}. Please check the file format and path.") from e
    
    def is_regular(self) -> bool:
        """Check if the time series data is regular."""
        if self.data.index.isnull().sum() > 0:
            logging.warning("Data contains null values in the index, Cannot proceed with this data further.")
            return False

        # Ensure index is a DatetimeIndex
        if not isinstance(self.data.index, pd.DatetimeIndex):
            logging.warning("Index is not a DatetimeIndex. Cannot check regularity.")
            return False

        # Calculate differences between consecutive timestamps
        diffs = self.data.index.to_series().diff().dropna()
        if diffs.nunique() == 1:
            logging.info("Data is regular. Index differences are uniform: %s", diffs.iloc[0])
            return True
        else:
            logging.warning("Data is not regular. Index differences are not uniform.")
            logging.warning("Unique differences found:", diffs.unique())
            return False


    def save_metadata(self) -> None:
        """Save metadata of the DataFrame to a JSON file."""
        if "sample_data" not in os.listdir("dynamicts"):
            os.mkdir("dynamicts/sample_data")
        metadata = {
            "columns": list(self.data.columns),
            "dtypes": {col: str(dtype) for col, dtype in self.data.dtypes.items()},
            "shape": self.data.shape,
            "index_name": self.data.index.name,
        }
        # meta_path = os.path.splitext(self.filepath)[0] + "_meta.json"
        meta_path = os.path.join("dynamicts/sample_data/", "_meta.json")
        print(meta_path)
        try:
            with open(meta_path, "w") as f:
                json.dump(metadata, f, indent=4)
        except Exception as e:
            logging.error(f"Error saving metadata to {meta_path}: {e}")
            raise ValueError(f"Failed to save metadata to {meta_path}.") from e
        
    def run_pipeline(self) -> Optional[pd.DataFrame]:
        """Run the data loading pipeline."""
        logging.info("loading data...")
        self.load()
        if not self.is_regular():
            logging.warning("Pipeline completed. Data is loaded but may not be regular.")
            return None
        logging.info("Data loaded is regular. Further processing may be needed.")
        self.data.rename(columns={f"{self.data.columns[0]}": "y"}, inplace=True)
        return self.data



# Usage
if __name__ == "__main__":
    loader = DataLoader(filepath="sample_data/date_count.csv", index_col="Date")
    result = loader.run_pipeline()
    if result is not None:
        logging.info("Data loaded successfully.")
  