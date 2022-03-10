from lib2to3.pytree import Base
from casp.base.etl import BaseETL

class CASP_Pipeline(BaseETL):
    """CASP Pipeline"""

    def extract(self, url: str, **kwargs):
        """Extract data from source"""
        breakpoint()
        pass

    def transform(self, data, **kwargs):
        """Transform data"""
        pass

    def load(self, data, **kwargs):
        """Load data into target"""
        pass