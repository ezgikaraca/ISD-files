#!/bin/tcsh -f

# source the location of haddock configuration file
# required to set the env for $HADDOCKTOOLS
source ./haddock_configure.csh

# fitting will be done via Profit, it's corresponding variables should be set:
# reference - the most anisotropic monomer
# atoms - should be CA or P depending on the molecule type, i.e. protein or nucleic acids
# profit_path - location of profit

set refe = ../reference.pdb
set atoms = 'CA'
set profit_path = /struct/carlomag/karaca/software/profit/ProFitV3.1/src

# zone definition should be changed according to the segment/chain id of the refe molecule
# profit recognizes only chain ids, here chain ids are mapped to segid's before fitting
foreach i (*pdb)
  $HADDOCKTOOLS/pdb_segid-to-chain $i >$i:r.tmp
  $profit_path/profit <<_Eod_ |grep RMS > /dev/null
      refe $refe
      mobi $i:r.tmp
      atom $atoms
      zone A*
	  fit
	  write $i:r.fit
      quit
_Eod_
end
rm -rf *tmp

# remove segid's
foreach i(*fit)
  $HADDOCKTOOLS/pdb_blank_chain $i > a
  /bin/mv -f a $i
  echo END >> $i
end
