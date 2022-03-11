import tempfile
import requests
import subprocess
import time

import pandas as pd

from pathlib import Path
from casp.base.etl import BaseETL


class CSV_To_DSSP(BaseETL):
    """CASP DSSP Pipeline"""

    def extract(self, input: str, **kwargs) -> pd.DataFrame:
        """Extract CASP domain summary from csv file"""
        df = pd.read_csv(input)
        
        return df

    def transform(self, df: pd.DataFrame, pdb_bank: str, **kwargs) -> list:
        """Transform the pdb dataframe column into a list of links for PDB Bank downloads"""
        links = []

        for pdb in set(df["pdb"]):
            links.append(f"{pdb_bank}{pdb}.fasta")

        return links

    # TODO: Add logging to follow progress
    def load(self, links: list, dssp: list, output: str, **kwargs):
        """Load the list of fasta links into a folder"""
        Path(output).mkdir(parents=True, exist_ok=True)

        # Request each .fasta download PDB files from the links
        for link in links:
            req = requests.get(link)

            if req.status_code != 200:
                raise Exception(f"Error downloading {link}")

            # write FASTA output to file
            out_filename = link.split("/")[-1]
            with open(f"{output}{out_filename}.fasta", "w") as f:
                f.write(req.content)

            # sleep for 1 second to avoid overloading the PDB Bank
            time.sleep(1)

