# ASA normalization constants were taken from:
# M. Z. Tien, A. G. Meyer, D. K. Sydykova, S. J. Spielman, C. O. Wilke (2013).
RES_MAX_ACC = {
    'A': 129.0, 'R': 274.0, 'N': 195.0, 'D': 193.0,
    'C': 167.0, 'Q': 225.0, 'E': 223.0, 'G': 104.0,
    'H': 224.0, 'I': 197.0, 'L': 201.0, 'K': 236.0,
    'M': 224.0, 'F': 240.0, 'P': 159.0, 'S': 155.0,
    'T': 172.0, 'W': 285.0, 'Y': 263.0, 'V': 174.0
}

# Secondary structure Q8 constants from DSSP documentation
Q8 = ["H", "B", "E", "G", "I", "T", "S"]


def asa_to_rsa(amino_acid: str, asa: int) -> float:
    """Convert ASA to RSA """
    if amino_acid.islower():
        amino_acid = "C"

    if amino_acid in RES_MAX_ACC:
        max_acc = RES_MAX_ACC[amino_acid]
        return float(asa) / max_acc

    return 0.0


def parse_dssp_q8(q8: str) -> str:
    """Parse a Q8 string and returns a valid secondary structure"""
    q8 = q8.strip()
    if len(q8) <= 1:
        return "C"
    
    if q8[0] in Q8:
        return q8[0]
    return "C"


def parse_dssp_line(dssp_line: str) -> tuple:
    """Parse a DSSP line and returns tuple of amino acid, 
    chain, secondary structure (Q8), accessible surface area, 
    relative surface areaphi, phi and psi.
    """
    aa = dssp_line[13]
    chain = dssp_line[11]
    q8 = parse_dssp_q8(dssp_line[14:28])
    asa = float(dssp_line[34:38].strip())
    rsa = asa_to_rsa(aa, asa)
    phi = float(dssp_line[104:109])
    psi = float(dssp_line[110:115])

    return aa, chain, q8, asa, rsa, phi, psi
