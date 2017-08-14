#!/usr/bin/python
#uses classes defined in geometry.py

from Bio.PDB import PDBParser
from geometry import *
from sys      import argv

P = PDBParser(PERMISSIVE=2)
s = P.get_structure('a', argv[1])
print calculate_gyration_tensor(s)
