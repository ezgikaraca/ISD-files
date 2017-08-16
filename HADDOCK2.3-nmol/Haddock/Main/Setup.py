"""
Setup.py
"""
__author__   = "$Author: abonvin $"
__revision__ = "$Revision: 2.0 $"
__date__     = "$Date: 2007/05/22 08:30:59 $"

import copy, glob, os, re, shutil, string

from Haddock.Main import Messages, ParsePath
from Haddock.ThirdParty import TextFile

def SetupNewProject(Haddockdir, projectdir, runnumber,\
                    pdbfileandlistdict, cgpdbfileandlistdict, dihedfile,\
                    c1File, c2File, c3File, c4File, c5File,\
                    rdc1File, rdc2File, rdc3File, rdc4File, rdc5File,\
                    dani1File, dani2File, dani3File, dani4File, dani5File,\
                    pcs1File, pcs2File, pcs3File, pcs4File, pcs5File,\
                    pcs6File, pcs7File, pcs8File, pcs9File, pcsAFile,\
                    tensorfile, hbondfile, segiddict, ncomponents, cryoemFile):
    """
    sets up a new directory tree, copy and create files on the fly
    OUTPUT: returns nothing, but a directory tree will be created
    """

    #relatif -> absolut path for cns
    projectdir=os.path.abspath(projectdir)
    Haddockdir=os.path.abspath(Haddockdir)

    runDir = os.path.join(projectdir, 'run' + runnumber)
    if os.path.exists(projectdir) == 1:
        if os.path.exists(runDir) == 1:
            print 'run' + runnumber, 'already exists => HADDOCK stopped'
            Messages.StopHaddock()
        else:
            print 'project', projectdir, 'exists, run', runnumber, 'does not exist'
            print 'create the new run', runnumber
    else:
        print 'setting up a new project in directory', projectdir
        os.mkdir(projectdir)
    
    #create directories:
    os.mkdir(runDir)
    os.mkdir(os.path.join(runDir, 'begin'))
    os.mkdir(os.path.join(runDir, 'begin-aa'))
    os.mkdir(os.path.join(runDir, 'data'))
    os.mkdir(os.path.join(runDir, 'data/ensemble-models'))
    os.mkdir(os.path.join(runDir, 'data/dihedrals'))
    os.mkdir(os.path.join(runDir, 'data/hbonds'))
    os.mkdir(os.path.join(runDir, 'data/jcouplings'))
    os.mkdir(os.path.join(runDir, 'data/rdcs'))
    os.mkdir(os.path.join(runDir, 'data/dani'))
    os.mkdir(os.path.join(runDir, 'data/pcs'))
    os.mkdir(os.path.join(runDir, 'data/tensor'))
    os.mkdir(os.path.join(runDir, 'data/sequence'))
    os.mkdir(os.path.join(runDir, 'data/cryo-em'))
    os.mkdir(os.path.join(runDir, 'protocols'))
    os.mkdir(os.path.join(runDir, 'structures'))
    os.mkdir(os.path.join(runDir, 'tools'))
    os.mkdir(os.path.join(runDir, 'toppar'))
    os.mkdir(os.path.join(runDir, 'packages'))
    os.system('chmod g+w ' + os.path.join(runDir, 'packages'))

    #create iterations 0 to 1
    for it in range(0, 2):
        it = str(it)
        os.mkdir(os.path.join(runDir, 'structures/it' + it))
        iterationfile = open(os.path.join(runDir, 'structures/it' + it + \
                                      '/iteration.cns'), 'w')
        iterationfile.write('module ( iteration )\nevaluate (&iteration=' + \
                            it + ')\n')
        iterationfile.close()
        if it == '0':
            iterationfile = open(os.path.join(runDir, 'begin/iteration.cns'), 'w')
            iterationfile.write('module ( iteration )\nevaluate (&iteration=' + \
                            it + ')\n')
            iterationfile.close()
            iterationfile = open(os.path.join(runDir, 'begin-aa/iteration.cns'), 'w')
            iterationfile.write('module ( iteration )\nevaluate (&iteration=' + \
                            it + ')\n')
            iterationfile.close()

        if it == '1':
            os.mkdir(os.path.join(runDir, 'structures/it' + it + '/analysis'))
            os.mkdir(os.path.join(runDir, 'structures/it' + it + '/water'))
            os.mkdir(os.path.join(runDir, 'structures/it' + it + '/water/analysis'))
            iterationfile = open(os.path.join(runDir, 'structures/it' + it + \
                                              '/water/iteration.cns'), 'w')
            iterationfile.write('module ( iteration )\nevaluate (&iteration=2)\n')
            iterationfile.close()
            iterationfile = open(os.path.join(runDir, 'structures/it' + it + \
                                  '/analysis/iteration.cns'), 'w')
            iterationfile.write('module ( iteration )\nevaluate (&iteration=' + \
                                it + ')\n')
            iterationfile.close()
            iterationfile = open(os.path.join(runDir, 'structures/it' + it + \
                                  '/water/analysis/iteration.cns'), 'w')
            iterationfile.write('module ( iteration )\nevaluate (&iteration=2)\n')
            iterationfile.close()

    #create empty .tbl files:
    emptyFiles =['/data/dihedrals/dihedrals.tbl',\
                 '/data/dihedrals/dihedrals_csi.tbl',\
                 '/data/dihedrals/dihedrals_talos.tbl',\
                 '/data/hbonds/hbonds.tbl',\
                 '/data/hbonds/hbonds_csi.tbl',\
                 '/data/jcouplings/c1.tbl',\
                 '/data/jcouplings/c2.tbl',\
                 '/data/jcouplings/c3.tbl',\
                 '/data/jcouplings/c4.tbl',\
                 '/data/jcouplings/c5.tbl',\
                 '/data/rdcs/rdc1.tbl',\
                 '/data/rdcs/rdc2.tbl',\
                 '/data/rdcs/rdc3.tbl',\
                 '/data/rdcs/rdc4.tbl',\
                 '/data/rdcs/rdc5.tbl',\
                 '/data/pcs/pcs1.tbl',\
                 '/data/pcs/pcs2.tbl',\
                 '/data/pcs/pcs3.tbl',\
                 '/data/pcs/pcs4.tbl',\
                 '/data/pcs/pcs5.tbl',\
                 '/data/pcs/pcs6.tbl',\
                 '/data/pcs/pcs7.tbl',\
                 '/data/pcs/pcs8.tbl',\
                 '/data/pcs/pcs9.tbl',\
                 '/data/pcs/pcsA.tbl',\
                 '/data/tensor/tensor.tbl',\
                 '/data/dani/dani1.tbl',\
                 '/data/dani/dani2.tbl',\
                 '/data/dani/dani3.tbl',\
                 '/data/dani/dani4.tbl',\
                 '/data/dani/dani5.tbl']
    for fileToTouch in emptyFiles:
        openfile = runDir + fileToTouch
        openhandle = open(openfile, 'w')
        openhandle.close()

    #write PDB filenames to the various file_i.list
    filelistdict={}
    filelistdict.update({1:"file_A.list"})
    filelistdict.update({2:"file_B.list"})
    filelistdict.update({3:"file_C.list"})
    filelistdict.update({4:"file_D.list"})
    filelistdict.update({5:"file_E.list"})
    filelistdict.update({6:"file_F.list"})
    filelistdict.update({7:"file_G.list"})
    filelistdict.update({8:"file_H.list"})
    filelistdict.update({9:"file_I.list"})
    filelistdict.update({10:"file_J.list"})
    filelistdict.update({11:"file_K.list"})
    filelistdict.update({12:"file_L.list"})
    filelistdict.update({13:"file_M.list"})
    filelistdict.update({14:"file_N.list"})
    filelistdict.update({15:"file_O.list"})
    filelistdict.update({16:"file_P.list"})
    filelistdict.update({17:"file_Q.list"})
    filelistdict.update({18:"file_R.list"})
    filelistdict.update({19:"file_S.list"})
    filelistdict.update({20:"file_T.list"})

    for ccjj in range(1,1+ncomponents):
        openfile = runDir + '/data/sequence/'+filelistdict[ccjj]
        openhandle = open(openfile, 'w')
        pdbfilei=pdbfileandlistdict[ccjj][0]
        r = runDir
        if r == "." or r.startswith("./"): r = "../" + r[2:]    
        writefile = '"' + r + '/data/sequence/' + ParsePath.GetTail(pdbfilei) + '"\n'
        openhandle.write(writefile)
        openhandle.close()
    
    #write CG PDB filenames to the various file_i.list-cg
    filelistcgdict={}
    filelistcgdict.update({1:"file_A.list-cg"})
    filelistcgdict.update({2:"file_B.list-cg"})
    filelistcgdict.update({3:"file_C.list-cg"})
    filelistcgdict.update({4:"file_D.list-cg"})
    filelistcgdict.update({5:"file_E.list-cg"})
    filelistcgdict.update({6:"file_F.list-cg"})
    filelistcgdict.update({7:"file_G.list-cg"})
    filelistcgdict.update({8:"file_H.list-cg"})
    filelistcgdict.update({9:"file_I.list-cg"})
    filelistcgdict.update({10:"file_J.list-cg"})
    filelistcgdict.update({11:"file_K.list-cg"})
    filelistcgdict.update({12:"file_L.list-cg"})
    filelistcgdict.update({13:"file_M.list-cg"})
    filelistcgdict.update({14:"file_N.list-cg"})
    filelistcgdict.update({15:"file_O.list-cg"})
    filelistcgdict.update({16:"file_P.list-cg"})
    filelistcgdict.update({17:"file_Q.list-cg"})
    filelistcgdict.update({18:"file_R.list-cg"})
    filelistcgdict.update({19:"file_S.list-cg"})
    filelistcgdict.update({20:"file_T.list-cg"})
    for ccjj in range(1,1+ncomponents):
        openfile = runDir + '/data/sequence/'+filelistcgdict[ccjj]
        openhandle = open(openfile, 'w')
        pdbfilei=cgpdbfileandlistdict[ccjj][0]
	if pdbfilei:
            r = runDir
            if r == "." or r.startswith("./"): r = "../" + r[2:]    
            writefile = '"' + r + '/data/sequence/' + ParsePath.GetTail(pdbfilei) + '"\n'
            openhandle.write(writefile)
            openhandle.close()
    
    #copy parameter and topology files to /toppar of new project:
    tocopy = glob.glob(Haddockdir + '/toppar/*')
    for filetocopy in tocopy:
        if not os.path.isdir(filetocopy) and filetocopy[-3:] != 'RCS':
            shutil.copy(filetocopy, runDir + '/toppar')
        elif os.path.isdir(filetocopy):
            shutil.copytree(filetocopy, runDir + '/toppar/' + os.path.basename(filetocopy))

    #copy protocols to /protocols of your new project:
    tocopy = glob.glob(Haddockdir + '/protocols/*')
    for filetocopy in tocopy:
        if filetocopy[-3:] != 'RCS':
            shutil.copy(filetocopy, runDir + '/protocols')
    shutil.copy(Haddockdir+"/Haddock/CNS/KeepAlive.py", runDir + '/protocols')
    shutil.copy(Haddockdir+"/Haddock/CNS/RemoveBadPDB.py", runDir + '/protocols')
    
    #copy tools to /tools of your new project:
    tocopy = glob.glob(Haddockdir + '/tools/*')
    for filetocopy in tocopy:
        if filetocopy[-3:] != 'RCS':
            shutil.copy(filetocopy, runDir + '/tools')
    
    #copy the dihedrals, hbonds, jcouplings, rdcs, cryo-em:
    tocopy =[[dihedfile, '/data/dihedrals/dihedrals.tbl'],\
             [hbondfile, '/data/hbonds/hbonds.tbl'],\
             [c1File, '/data/jcouplings/c1.tbl'],\
             [c2File, '/data/jcouplings/c2.tbl'],\
             [c3File, '/data/jcouplings/c3.tbl'],\
             [c4File, '/data/jcouplings/c4.tbl'],\
             [c5File, '/data/jcouplings/c5.tbl'],\
             [rdc1File, '/data/rdcs/rdc1.tbl'],\
             [rdc2File, '/data/rdcs/rdc2.tbl'],\
             [rdc3File, '/data/rdcs/rdc3.tbl'],\
             [rdc4File, '/data/rdcs/rdc4.tbl'],\
             [rdc5File, '/data/rdcs/rdc5.tbl'],\
             [dani1File, '/data/dani/dani1.tbl'],\
             [dani2File, '/data/dani/dani2.tbl'],\
             [dani3File, '/data/dani/dani3.tbl'],\
             [dani4File, '/data/dani/dani4.tbl'],\
             [dani5File, '/data/dani/dani5.tbl'],\
             [pcs1File, '/data/pcs/pcs1.tbl'],\
             [pcs2File, '/data/pcs/pcs2.tbl'],\
             [pcs3File, '/data/pcs/pcs3.tbl'],\
             [pcs4File, '/data/pcs/pcs4.tbl'],\
             [pcs5File, '/data/pcs/pcs5.tbl'],\
             [pcs6File, '/data/pcs/pcs6.tbl'],\
             [pcs7File, '/data/pcs/pcs7.tbl'],\
             [pcs8File, '/data/pcs/pcs8.tbl'],\
             [pcs9File, '/data/pcs/pcs9.tbl'],\
             [pcsAFile, '/data/pcs/pcsA.tbl'],\
             [tensorfile, '/data/tensor/tensor.tbl'],\
             [cryoemFile, '/data/cryo-em/cryo-em.xplor'],\
             ]

    for filetocopy in tocopy:
        if filetocopy[0] and not os.path.exists(filetocopy[0]):
            print '\n**** /!\ Warning: could not find file /!\ ****', filetocopy[0], '\n'
        if filetocopy[0] and os.path.exists(filetocopy[0]):
            print '  copying', filetocopy[0], '\n    to', runDir + \
                  filetocopy[1]
            shutil.copy(filetocopy[0], runDir + filetocopy[1])

    #check first PDB files
    for ccjj in range(1,1+ncomponents):
        pdbfilei=pdbfileandlistdict[ccjj][0]
        if os.path.exists(pdbfilei) == 1:
            pdbcoor = TextFile.TextFile(pdbfilei,'r')
            okstatus=0
            endmdl = re.compile('ENDMDL')
            endstat = re.compile('END')
            for line in pdbcoor:
                if endmdl.match(line):
                    print 'Your PDB file ',pdbfilei,' contains an ENDMDL statement. Please remove it and'
                    print 'make sure that the file ends with an END statement.'
                    whatToDo = 'rm -rf ' + runDir
                    os.system(whatToDo)
                    print '  HADDOCK aborted and run directory removed'
                    Messages.StopHaddock()
                if endstat.match(line):
                    okstatus=1
            if okstatus == 0:
                print 'Your PDB file ',pdbfilei,' does not contain an END statement. Please add it.'
                whatToDo = 'rm -rf ' + runDir
                os.system(whatToDo)
                print '  HADDOCK aborted and run directory removed'
                Messages.StopHaddock()
            pdbcoor.close()
        else:
            print '  could not find', pdbfilei
            whatToDo = 'rm -rf ' + runDir
            os.system(whatToDo)
            print '  HADDOCK aborted and run directory removed'
            Messages.StopHaddock()
            
    #check first CG PDB files
    for ccjj in range(1,1+ncomponents):
        pdbfilei=cgpdbfileandlistdict[ccjj][0]
	if pdbfilei:
            if os.path.exists(pdbfilei) == 1:
                pdbcoor = TextFile.TextFile(pdbfilei,'r')
                okstatus=0
                endmdl = re.compile('ENDMDL')
                endstat = re.compile('END')
                for line in pdbcoor:
                    if endmdl.match(line):
                        print 'Your PDB file ',pdbfilei,' contains an ENDMDL statement. Please remove it and'
                        print 'make sure that the file ends with an END statement.'
                        whatToDo = 'rm -rf ' + runDir
                        os.system(whatToDo)
                        print '  HADDOCK aborted and run directory removed'
                        Messages.StopHaddock()
                    if endstat.match(line):
                        okstatus=1
                if okstatus == 0:
                    print 'Your PDB file ',pdbfilei,' does not contain an END statement. Please add it.'
                    whatToDo = 'rm -rf ' + runDir
                    os.system(whatToDo)
                    print '  HADDOCK aborted and run directory removed'
                    Messages.StopHaddock()
                pdbcoor.close()
            else:
                print '  could not find', pdbfilei
                whatToDo = 'rm -rf ' + runDir
                os.system(whatToDo)
                print '  HADDOCK aborted and run directory removed'
                Messages.StopHaddock()
            
    #copy PDB files
    for ccjj in range(1,1+ncomponents):
        pdbfilei=pdbfileandlistdict[ccjj][0]
	whatToDo = Haddockdir + '/tools/pdb_blank_chain-segid ' + pdbfilei + '>' + runDir + '/data/sequence/' + ParsePath.GetTail(pdbfilei)
	os.system(whatToDo)
        print '  ', pdbfilei, ' copied to ', runDir + '/data/sequence after removing the chain and segIDs'
           
    #copy CG PDB files
    for ccjj in range(1,1+ncomponents):
        pdbfilei=cgpdbfileandlistdict[ccjj][0]
	if pdbfilei:
            whatToDo = Haddockdir + '/tools/pdb_blank_chain-segid ' + pdbfilei + '>' + runDir + '/data/sequence/' + ParsePath.GetTail(pdbfilei)
	    os.system(whatToDo)
            print '  ', pdbfilei, ' copied to ', runDir + '/data/sequence after removing the chain and segIDs'
           
    #now parsing the information of new.html and writing to run.cns
    print 'editing run.cns: setting the default values'
    runcnsfile = Haddockdir + '/protocols/run.cns'
    runcnshandle = TextFile.TextFile(runcnsfile)
    newruncnshandle = TextFile.TextFile(runDir + '/run.cns', 'w')
    fileRootparsed = ParsePath.GetTail(projectdir)
    pdbtag = re.compile('.pdb')
    templateparsed = fileRootparsed + '_template.pdb'
    structureparsed = fileRootparsed + '.psf'
    arrow = re.compile('{===>}')

    #get the relative path:
    dihedfile = ParsePath.GetTail(dihedfile)
    hbondfile = ParsePath.GetTail(hbondfile)
    c1File = ParsePath.GetTail(c1File)
    c2File = ParsePath.GetTail(c2File)
    c3File = ParsePath.GetTail(c3File)
    c4File = ParsePath.GetTail(c4File)
    c5File = ParsePath.GetTail(c5File)

    if not hbondfile: hbondfile = ''
    if not structureparsed: structureparsed = ''
    if not templateparsed: templateparsed = ''
    multiparsed = 'false'

    toparse = {'haddock_dir': Haddockdir,
               'fileroot': fileRootparsed,
               'hbonds_file': hbondfile,
               'ncomponents': ncomponents,
               'project_dir': projectdir,
               'prot_multi': multiparsed,
               'run_dir': runDir,
               'structure': structureparsed,
               'template': templateparsed,
               'temptrash_dir': runDir}
               
    tmpdict={1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"I",10:"J",11:"K",12:"L",13:"M",14:"N",15:"O",16:"P",17:"Q",18:"R",19:"S",20:"T"}
    for ccjj in range(1,1+ncomponents):
        pdbfilei = pdbfileandlistdict[ccjj][0]
        cgpdbfilei = cgpdbfileandlistdict[ccjj][0]
        pdbpathparsedi = ParsePath.GetTail(pdbfilei)
        cgpdbpathparsedi = ParsePath.GetTail(cgpdbfilei)
        if not pdbpathparsedi: pdbpathparsedi = ''
        if not cgpdbpathparsedi:
            cgpdbpathparsedi= ''
        else:
            protcgi='cg_'+tmpdict[ccjj]+"=false"
	    coarse="true"
            toparse.update({protcgi:coarse})
        pdblisti = pdbfileandlistdict[ccjj][1]
        cgpdblisti = cgpdbfileandlistdict[ccjj][1]
        if pdblisti: multiparsed = 'true'
        pdbtag = re.compile('.pdb')
        rootpathparsedi = pdbtag.sub('',pdbpathparsedi)
        if not pdbpathparsedi: rootpathparsedi = ''
        psfpathparsedi = rootpathparsedi + '.psf'
        if not pdbpathparsedi: psfpathparsedi = ''
        protpsfi='prot_psf_'+tmpdict[ccjj]
        protcoori='prot_coor_'+tmpdict[ccjj]
        protrooti='prot_root_'+tmpdict[ccjj]
        protsegidi='prot_segid_'+tmpdict[ccjj]
        if not segiddict[ccjj]: segiddict[ccjj] = tmpdict[ccjj]
        toparse.update({protpsfi:psfpathparsedi})
        toparse.update({protcoori:pdbpathparsedi})
        toparse.update({protrooti:rootpathparsedi})
        toparse.update({protsegidi:segiddict[ccjj]})

    # parse some paramters from the XPLOR/CNS density file, to substitute in
    # run.cns
    if cryoemFile:
        try:
            cryoem_parameters = parse_xplor(cryoemFile)
        except (IOError, ValueError):
            cryoem_parameters = {}
            msg = 'The cryo-EM density file could not be properly parsed.\n' \
                  'Make sure it is in the XPLOR/CNS format.'
            print msg
        finally:
            toparse.update(cryoem_parameters)

    # fill in the new run.cns file to help out user
    ARROW = '{===>}'
    BOOLEANS = ('false', 'true')
    for line in runcnshandle:
        if line.startswith(ARROW):
            parameter = parse_run_parameter(line)
            if toparse.has_key(parameter):
                value = toparse[parameter]
                # if the value is a string, it should be between ""
                if isinstance(value, str) and value not in BOOLEANS:
                    value = '"' + value + '"'
                line = ('%s %s=%s;\n') % (ARROW, parameter, str(value))
        newruncnshandle.write(line)
    runcnshandle.close()
    newruncnshandle.close()
    
    #copy new.html from the current directory in the html directory:
    if os.path.exists('new.html'):
        newhtml = 'new.html'
        print 'copying new.html to', runDir + '/data/new.html' 
        shutil.copy(newhtml, runDir + '/data/new.html')
    else:
        print 'WARNING: could not find new.html file!'
        Messages.StopHaddock()

    #end:

    print 'created new run' + runnumber, \
          'for the project', projectdir
    
def parse_run_parameter(line):
    """Parse a definition line and return the parameter name"""
    # syntax of CNS definition is:
    #{===>} <parameter>=<keyword>;
    return line.split()[1].split('=')[0]

def parse_xplor(cryoemFile):
    """Parse XPLOR/CNS density file and return size parameters"""

    parameters = {}
    with open(cryoemFile) as f:
        # first line is blank
        f.readline()
        # parse number of REMARK lines and skip them
        nlines_to_skip = int(f.readline()[:8])
        for n in xrange(nlines_to_skip):
            f.readline()
        # parse number of voxels in each dimension
        line = f.readline()
        parameters['nx'] = int(line[:8])
        parameters['ny'] = int(line[24: 32])
        parameters['nz'] = int(line[48:56])
        # parse length of each dimension
        line = f.readline()
        parameters['xlength'] = float(line[: 12])
        parameters['ylength'] = float(line[12: 24])
        parameters['zlength'] = float(line[24: 36])
    return parameters
