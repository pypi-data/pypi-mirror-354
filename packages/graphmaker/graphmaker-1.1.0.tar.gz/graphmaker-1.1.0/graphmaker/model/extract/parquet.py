from typing import Generator
import pandas as pd
import pyarrow.parquet as pq
import pyarrow.compute as pc

from graphmaker.model.extract._dataprovider import DataProvider
from graphmaker.model.extract.pandas import Pandas

class Parquet(DataProvider):
    """
    DataProvider for Parquet files.
    This class provides methods to read data from Parquet files, including
    connecting to the file, retrieving data in batches, and performing
    operations like unique value extraction and value counts.
    """
    def __init__(self, file, batch_size=1000):
        self.file = file
        self.batch_size = batch_size
        self.p_file = None

    def df(self, rows=None, columns=None) -> pd.DataFrame:
        disconnect = False
        if not self.is_connected():
            self.connect()
            disconnect = True

        if rows is not None:
            ret = None
            for batch in self.p_file.iter_batches(batch_size=rows):
                ret = batch.to_pandas()
                break
            return ret
        ret = self.p_file.read(columns=columns, use_threads=True).to_pandas()
        if disconnect:
            self.close()
        return ret

    def to_pandas(self, rows=None, columns=None) -> Pandas:
        if self.is_connected():
            return Pandas(self.df(rows=rows, columns=columns), batch_size=self.batch_size)
        self.connect()
        ret = Pandas(self.df(rows=rows, columns=columns), batch_size=self.batch_size).connect()
        self.close()
        return ret

    def is_connected(self):
        return self.p_file is not None

    def connect(self):
        self.p_file = pq.ParquetFile(self.file)
        return self

    def close(self):
        if self.p_file is None:
            return
        self.p_file.close()
        self.p_file = None

    def total_rows(self):
        if not self.is_connected():
            raise ValueError("Parquet file is not connected. Call .connect() first.")
        return self.p_file.metadata.num_rows

    def columns(self):
        df = self.df(rows=1)
        return df.columns.tolist()

    def unique(self, column):
        col = self.p_file.read(columns=[column], use_threads=True).column(0)
        return pc.unique(col).to_pylist()

    def unique_multiple(self, columns):
        df = self.df(columns=columns)
        for col in columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(str)
        return df.drop_duplicates(subset=columns).dropna()

    def value_counts_multiple(self, columns):
        df = self.df(columns=columns)
        # Convert columns to strings to handle unhashable types
        for col in columns:
            if df[col].dtype == 'object':
                df[col] = df[col].apply(str)
        return df.groupby(columns).size().reset_index(name="count")

    def next(self) -> Generator[list[str | int | float], None, None]:
        for batch in self.p_file.iter_batches(batch_size=self.batch_size):
            yield batch.to_pylist()

    