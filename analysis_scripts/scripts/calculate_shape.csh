#!/bin/csh
# calculates the shape parameters for each solution by using shape.py

touch shape.data
foreach i(protein?)
	echo $i `python shape.py $i` >> shape.data
end
