import glob
import pandas as pd

from pathlib import Path
from casp.utils.dssp import parse_dssp_line
from casp.base.etl import BaseETL


class DSSP_To_Dataset(BaseETL):
    """Converts DSSP output files into a dataset"""

    def extract(self, input: str, **kwargs) -> object:
        """Extract data from dssp files"""
        files = glob.glob(f"{input}/*")

        for file in files:
            with open(file, "r") as f:
                yield f.readlines()

    def transform(self, data: object, **kwargs) -> pd.DataFrame:
        """Transform DSSP extracted data into single values"""
        for dssp in data:
            dssp_name = dssp[2].split()[-2]
            dssp_body = dssp[28:]
            for line in dssp_body:
                yield dssp_name, parse_dssp_line(line)

    def load(self, data: object, output: str, **kwargs):
        """Load the parsed dssp data into a csv file"""
        Path(output).parent.mkdir(parents=True, exist_ok=True)

        columns = ["pdb", "aa", "chain", "q8", "asa", "rsa", "phi", "psi"]
        rows = []

        for header, line in data:
            rows.append([header, *line])

        df = pd.DataFrame(rows, columns=columns)
        df.to_csv(output, index=False)
