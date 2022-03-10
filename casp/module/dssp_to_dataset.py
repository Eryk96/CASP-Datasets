from re import A
import pandas as pd
import glob

from casp.base.etl import BaseETL

# ASA normalization constants were taken from:
# M. Z. Tien, A. G. Meyer, D. K. Sydykova, S. J. Spielman, C. O. Wilke (2013).
# Maximum allowed solvent accessibilities of residues in proteins. PLOS ONE
# 8:e80635.
RES_MAX_ACC = {'A': 129.0, 'R': 274.0, 'N': 195.0, 'D': 193.0,
               'C': 167.0, 'Q': 225.0, 'E': 223.0, 'G': 104.0,
               'H': 224.0, 'I': 197.0, 'L': 201.0, 'K': 236.0,
               'M': 224.0, 'F': 240.0, 'P': 159.0, 'S': 155.0,
               'T': 172.0, 'W': 285.0, 'Y': 263.0, 'V': 174.0}


def load_dssp(dssp_files: list, **kwargs):
    """Generator for loading DSSP output"""
    for dssp_file in dssp_files:
        with open(dssp_file, "r") as f:
            yield f.readlines()[28:]


def asa_to_rsa(amino_acid: str, asa: int) -> float:
    """Convert ASA to RSA"""
    if amino_acid.islower():
        amino_acid = "C"
    if amino_acid in RES_MAX_ACC:
        max_acc = RES_MAX_ACC[amino_acid]
        return float(asa) / max_acc
    return 0


class DSSP_To_Dataset(BaseETL):
    """To add"""

    def extract(self, input: str, **kwargs) -> object:
        files = glob.glob(f"{input}/*")
        data = load_dssp(files)

        return data

    def transform(self, data: object, **kwargs) -> pd.DataFrame:
        for dssp in data:
            aa = list(map(lambda line: line[13], dssp))
            q8 = list(map(lambda line: line[13:28].strip(), dssp))
            asa = list(map(lambda line: int(line[35:40].strip()), dssp))
            rsa = list(map(lambda value: asa_to_rsa(
                value[0], value[1]), zip(aa, asa)))
            phi = []
            psi = []
            
            df = pd.DataFrame(list(zip(aa, q8, asa, rsa)), columns=["aa", "q8", "asa", "rsa"])

            breakpoint()

        breakpoint()
        return data

    def load(self, df: pd.DataFrame, output: str, **kwargs):
        """Load data into a csv file"""

        pass
