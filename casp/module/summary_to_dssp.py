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
            links.append(f"{pdb_bank}{pdb}.cif")

        return links

    # TODO: Add logging to follow progress
    def load(self, links: list, dssp: list, output: str, **kwargs):
        """Load the list of links into the dssp subprocess and store output in output directory"""
        Path(output).mkdir(parents=True, exist_ok=True)

        # Request each .cif download PDB files from the links
        for link in links:
            req = requests.get(link)

            if req.status_code != 200:
                raise Exception(f"Error downloading {link}")

            # write .cif file from PDB Bank to temp file
            with tempfile.NamedTemporaryFile(suffix=".cif") as tmp:
                tmp.write(req.content)
                tmp.flush()

                sub = subprocess.run(dssp + ["--input", tmp.name], stdout=subprocess.PIPE)

                # write DSSP output to file
                out_filename = link.split("/")[-1]
                with open(f"{output}{out_filename}.dssp", "w") as f:
                    f.write(sub.stdout.decode("utf-8"))

            # sleep for 1 second to avoid overloading the PDB Bank
            time.sleep(1)

