
class DataProvider:
    def next(self):
        raise NotImplementedError

    def connect(self):
        pass

    def close(self):
        pass

    def total_rows(self):
        raise NotImplementedError

    def columns(self):
        raise NotImplementedError

    def unique_multiple(self, columns):
        raise NotImplementedError
    
    def to_parquet_file(self, output_folder, batch_size=500, verbose=False):
        raise NotImplementedError
