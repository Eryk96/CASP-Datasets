from abc import ABC, abstractmethod

class BaseETL(ABC):
    """Base class for ETL pipeline"""

    @abstractmethod
    def extract(self, **kwargs):
        """Extract data from source"""

    @abstractmethod
    def transform(self, data, **kwargs):
        """Transform data"""

    @abstractmethod
    def load(self, data, **kwargs):
        """Load data into target"""