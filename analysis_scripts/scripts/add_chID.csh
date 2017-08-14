#!/bin/csh
# adds chain id to the *fit coordinate files

source ./haddock_configure.csh #located in the main haddock directory
foreach i(*fit)
	$HADDOCKTOOLS/pdb_segid-to-chain $i > a
	/bin/mv a $i
end
