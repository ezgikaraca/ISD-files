# How to run HADDOCK-M3 as described in the publication:

### Note: All the external scripts are located under `scripts/`.

1. HADDOCK-M3 should be run only for the it0 (global search) step, 
where the number of structures for it1 (local search) and water refinement should be set to 0.
  * This can be done via changing the following parameters in run.cns:
  &nbsp; `structures_0   # number of structures to be generated in it0`
  &nbsp;  `structures_1   # number of structures to be generated in it1`
  &nbsp;  `waterrefine    # number of structures to be generated in water refinement`

2. When the it0 step is finished, instructions given in it0_analysis should be carried out. 
This will ensure generation of new energy files. These files will be used to sample 10 it1 (local search) 
structures around selected it0 (global search) solutions.

3. Before re-running HADDOCK-M3 for it1, the number of structures for it1 should be set to the 
number of lines of `file.nam`.

  * This can be done via changing the following parameters in `run.cns`:
  &nbsp; `structures_1   # number of structures to be generated in it1`

4. For shape analysis, clustering and final scoring, instructions given in it1_analysis should be followed.
