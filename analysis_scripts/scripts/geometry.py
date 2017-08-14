# Copyright (C) 2011, Joao Rodrigues (j.p.g.l.m.rodrigues@gmail.com)
# This code is part of the Biopython distribution and governed by its
# license.  Please see the LICENSE file that should have been included
# as part of this package.

# Acknowledgments: Ezgi Karaca (ezzgikaraca@gmail.com)

"""
Module with assorted geometrical functions on
macromolecules.
"""

from Bio.PDB import Entity
from math import sqrt
from numpy import *
import sys

def center_of_mass(entity, geometric=False):
    """
    Returns gravitic [default] or geometric center of mass of an Entity.
    Geometric assumes all masses are equal (geometric=True)
    """
    # Structure, Model, Chain, Residue
    if isinstance(entity, Entity.Entity):
        atom_list = entity.get_atoms()
    # List of Atoms
    elif hasattr(entity, '__iter__') and [x for x in entity if x.level == 'A']:
        atom_list = entity
    else: # Some other weirdo object
        raise ValueError("Center of Mass can only be calculated from the following objects:\n"
                            "Structure, Model, Chain, Residue, list of Atoms.")
    class COM:
        def __init__(self,coord):
	    self.coord=coord
       
    positions = [ [], [], [] ] # [ [X1, X2, ..] , [Y1, Y2, ...] , [Z1, Z2, ...] ]
    masses = []
    
    for atom in atom_list:
        masses.append(atom.mass)
        
        for i, coord in enumerate(atom.coord.tolist()):
            positions[i].append(coord)

    # If there is a single atom with undefined mass complain loudly.
    if 'ukn' in set(masses) and not geometric:
        raise ValueError("Some Atoms don't have an element assigned.\n"
                         "Try adding them manually or calculate the geometrical center of mass instead.")
    
    if geometric:
	com = COM([sum(coord_list)/len(masses) for coord_list in positions])
        return com
    else:       
        w_pos = [ [], [], [] ]
        for atom_index, atom_mass in enumerate(masses):
            w_pos[0].append(positions[0][atom_index]*atom_mass)
            w_pos[1].append(positions[1][atom_index]*atom_mass)
            w_pos[2].append(positions[2][atom_index]*atom_mass)
	com = COM([sum(coord_list)/sum(masses) for coord_list in w_pos])
        return com

def calculate_gyration_tensor(structure):
  
  """
  Calculates the gyration tensor from the molecule.
  Returns a numpy matrix.
  """
   
  com = center_of_mass(structure, True)
  cx, cy, cz = com.coord

  n_atoms = 0
  tensor_xx, tensor_xy, tensor_xz = 0, 0, 0
  tensor_yx, tensor_yy, tensor_yz = 0, 0, 0
  tensor_zx, tensor_zy, tensor_zz = 0, 0, 0

  for atom in structure.get_atoms():
    ax, ay, az = atom.coord
    tensor_xx += (ax-cx)*(ax-cx)
    tensor_yx += (ax-cx)*(ay-cy)
    tensor_xz += (ax-cx)*(az-cz)
    tensor_yy += (ay-cy)*(ay-cy)
    tensor_yz += (ay-cy)*(az-cz)
    tensor_zz += (az-cz)*(az-cz)
    n_atoms += 1

  gy_tensor =  mat([[tensor_xx, tensor_yx, tensor_xz], [tensor_yx, tensor_yy, tensor_yz], [tensor_xz, tensor_yz, tensor_zz]])
  gy_tensor = (1.0/n_atoms) * gy_tensor
  
  D,V = linalg.eig(gy_tensor)
  [a, b, c] = sorted(sqrt(5 * D))
  rg = sqrt(sum(D))
  
  l = average([D[0],D[1],D[2]])
  A = (((D[0] - l)**2 + (D[1] - l)**2 + (D[2] - l)**2) / l**2) * 1/6
  S = (((D[0] - l) * (D[1] - l) * (D[2] - l))/ l**3) * 27
  print "%s" % '#Dim(a,b,c) #Rg #Prolate.'
  print "%.2f" % round(a,2), round(b,2), round(c,2) , round(rg,2) , round(S,2)
  sys.exit()

def calculate_moment_of_intertia_tensor(structure):
  """
  Calculates the moment of inertia tensor from the molecule.
  Returns a numpy matrix.
  """
  com = center_of_mass(structure, False)
  cx, cy, cz = com.coord

  n_atoms = 0
  tensor_xx, tensor_xy, tensor_xz = 0, 0, 0
  tensor_yx, tensor_yy, tensor_yz = 0, 0, 0
  tensor_zx, tensor_zy, tensor_zz = 0, 0, 0
  s_mass = sum([a.mass for a in structure.get_atoms()])

  for atom in structure.get_atoms():
    ax, ay, az = atom.coord
    tensor_xx += ((ay-cy)**2 + (az-cz)**2)*atom.mass
    tensor_xy += -1*(ax-cx)*(ay-cy)*atom.mass
    tensor_xz += -1*(ax-cx)*(az-cz)*atom.mass
    tensor_yy += ((ax-cx)**2 + (az-cz)**2)*atom.mass
    tensor_yz += -1*(ay-cy)*(az-cz)*atom.mass
    tensor_zz += ((ax-cx)**2 + (ay-cy)**2)*atom.mass

  in_tensor =  mat([[tensor_xx, tensor_xy, tensor_xz], [tensor_xy, tensor_yy, tensor_yz], [tensor_xz, 
tensor_yz, tensor_zz]])
  D,V = linalg.eig(in_tensor)
  
  a = sqrt((5/(2*s_mass)) * (D[0] - D[1] + D[2]))
  b = sqrt((5/(2*s_mass)) * (D[2] - D[0] + D[1]))
  c = sqrt((5/(2*s_mass)) * (D[1] - D[2] + D[0]))
  return sorted([a, b, c])
