import pandas as pd

from pathlib import Path
from casp.base.etl import BaseETL


class Summary_To_CSV(BaseETL):
    """CASP Domains Summary Pipeline"""

    def extract(self, url: str, **kwargs) -> pd.DataFrame:
        """Extract CASP table data from url"""
        df = pd.read_html(url)
        df = pd.concat(df)

        return df

    def transform(self, df: pd.DataFrame, class_filter: list, **kwargs) -> pd.DataFrame:
        """Cleanup and transform CASP table data and filter out unwanted classifications"""
        df.columns = df.columns.str.lower()

        # filter unwanted classes
        df["classification"] = df["classification"].str.lower()
        df = df.drop(df[~df["classification"].isin(class_filter)].index)

        # remove pdb column non numeric values
        df["pdb"] = df["pdb"].str.extract(r"([a-zA-Z0-9]+)")
        df = df.drop(df[~pd.notnull(df["pdb"])].index)

        # keep necessary columns and remove duplicates
        df = df.drop_duplicates(subset=['target'])
        df = df.iloc[:, 1:8]

        return df

    def load(self, df: pd.DataFrame, output: str, **kwargs):
        """Load data into a csv file"""
        Path(output).parent.mkdir(parents=True, exist_ok=True)
        
        df.to_csv(output, index=False)

