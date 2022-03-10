from lib2to3.pytree import Base
import pandas as pd

from casp.base.etl import BaseETL


class CASP_To_CSV(BaseETL):
    """CASP Pipeline"""

    def extract(self, url: str, **kwargs):
        """Extract CASP table data from """
        df = pd.read_html(url)
        df = df.concat(df)

        return df

    def transform(self, data, **kwargs):
        """Transform data"""
        
        breakpoint()

    def load(self, data, **kwargs):
        """Load data into target"""
        pass