"""
InputFileParser.py

procedures for parsing new.html and run.cns
"""
__author__   = "$Author: abonvin $"
__revision__ = "$Revision $"
__date__     = "$Date $"

import re, string, sys, traceback
from Haddock.Main import ParsePath
from Haddock.ThirdParty import TextFile
from Haddock.Analysis.Diagnostic import HaddockError, RunCNSError
def ParseNewHtml(directory = '.'):
    """
    parse new.html, reads all lines between the '<!-- HADDOCK -->\n' and
    defines the specified variables.
    INPUT:  directory where to search for new.html
    OUTPUT: a dictionary with the variable names as keywords
    """
    print 'reading parameters from the file', directory + '/new.html'
    newhtml = TextFile.TextFile(directory + '/new.html', 'r')
    print '  setting some variables:'
    variablesdic = {}
    readornot=0  #if 1: define variables below, otherwise not
    brTag = re.compile('<BR>')
    for line in newhtml.readlines():
        if line[-17:] == '<!-- HADDOCK -->\n':
            readornot = readornot + 1
            continue
        if readornot == 1:
            line = brTag.sub('', line)    #get rid of the <BR> tag
            linelist = string.split(line, '=')
            variablesdic[linelist[0]] = ParsePath.DelTrailSlash(string.strip(linelist[1]))
    for eachword in variablesdic.keys():
        print '  ' + eachword + ' set to: ' + variablesdic[eachword]
    return variablesdic


def ParseRunCns():
    """
    parses out all variables of run.cns (starting with {===>}) and returns an
    associative array (variablename:value)
    in addition, defines some variables and adds them to dictionary
    Version: 17.7.98 Jens Linge, EMBL
      Modified 30.10.06 Sjoerd de Vries: var_10 => run['var']['10']
      Modified 16.11.07 Sjoerd de Vries: ignore 2nd and later equalsigns on a line
    """
    runcns = TextFile.TextFile('run.cns', 'r')
    variablevalue = {}
    arrow = re.compile('{===>}')
    doublequotation = re.compile('"')
    endarrow = re.compile('{<===}')
    equalsign = re.compile('=')
    pro = re.compile('_pro')
    semicolon = re.compile(';')
    #the normal assignment statements are finished within only 1 line
    #the assignment statement for the ss bridges contains several lines
    assigns = 0    #0 for the normal case, 1 for several assignments
    dodictionary = 0 #0 does nothing, 1 for writing to dictionary
    for line in runcns:
        if equalsign.search(line):  #get arrows, assignments, comments, ...
            if arrow.match(line):
                if semicolon.search(line):
                    dodictionary = 1   #normal assignment found
                else:  #no assignment in this line, therefore:
                    assigns = 1   #this means: 'several assignments'
            elif endarrow.match(line):
                assigns = 0   #this means: end of 'several assignments'
            else:
                if semicolon.search(line):
                    dodictionary = 1
        if dodictionary == 1:
            #write to dictionary:
            line = line[6:]                      #get rid of {===>}
            line = semicolon.sub('', line)       #get rid of ;
            line = doublequotation.sub('', line) #get rid of "
            try:
                #kkk, vvv = equalsign.split(line)     #split uses the =
                splitpoint = line.index("=")
                kkk = line[:splitpoint]
                vvv = line[splitpoint+1:]
            except:
                s = 'WARNING: something is wrong with the run.cns format. Got a traceback:\n' + '-'*60 
                print '-'*60
                traceback.print_exc(file=sys.stdout)
                print '-'*60
                print '         while working on the line:'
                print line
            kkk = pro.sub(' ', kkk)              #get rid of '_pro'
            kkk = string.strip(kkk)
            last_underscore = kkk.rfind("_")
            vvv = vvv[:-1]                       #get rid of linebreaks
            vvv = semicolon.sub('', vvv)         #get rid of ;
            vvv = string.strip(vvv)              #get rid of whitespace     
            array_element = False
            if last_underscore > -1:
              trail = kkk[last_underscore+1:]
              if len(trail) > 0:
                try:
                  t = int(trail)
                except(ValueError):
                  array_element = False
                else:             
                  head = kkk[:last_underscore]
                  if head not in variablevalue:
                    variablevalue[head] = {}
                  variablevalue[head][t] = vvv
                  array_element = True
            if array_element == False:
              variablevalue[kkk] = vvv #creates dictionary
        #print ""
        dodictionary = 0    #set to default again

    #check if fileroot and protein root are not the same
    for k in variablevalue.keys():
      if k.find("prot_root_") == 0: #keys starts with prot_root_
        if variablevalue[k] == variablevalue['fileroot']:
          raise RunCNSError("Fileroot and %s have the same value: %s" % (k, variablevalue['fileroot']))
    
    #set some directory names:
    variablevalue['begindir'] = variablevalue['run_dir'] + '/begin'
    variablevalue['begin_aa_dir'] = variablevalue['run_dir'] + '/begin-aa'
    variablevalue['datadir'] = variablevalue['run_dir'] + '/data'
    variablevalue['protocolsdir'] = variablevalue['run_dir'] + '/protocols'
    variablevalue['sequencedir'] = variablevalue['datadir'] + '/sequence'
    variablevalue['structuresdir'] = variablevalue['run_dir'] + '/structures'
    variablevalue['toolsdir'] = variablevalue['run_dir'] + '/tools'
    variablevalue['toppardir'] = variablevalue['run_dir'] + '/toppar'

    #for the full path of the template and psf files:
    variablevalue['templatefile'] = variablevalue['begindir'] + '/' + \
                                    variablevalue['fileroot'] + '_1.pdb'
    variablevalue['psffile'] = variablevalue['begindir'] + '/' + \
                               variablevalue['fileroot'] + '.psf'
    variablevalue['templatefile_aa'] = variablevalue['begin_aa_dir'] + '/' + \
                                    variablevalue['fileroot'] + '_1.pdb'
    variablevalue['psffile_aa'] = variablevalue['begin_aa_dir'] + '/' + \
                               variablevalue['fileroot'] + '.psf'

    ncomp = int(variablevalue['ncomponents'])
    tmpdict={1:"A",2:"B",3:"C",4:"D",5:"E",6:"F",7:"G",8:"H",9:"I",10:"J",11:"K",12:"L",13:"M",14:"N",15:"O",16:"P",17:"Q",18:"R",19:"S",20:"T"}
    for ccii in range(1,1+ncomp):
        tmp_psf =  'prot_psf_' + tmpdict[ccii]
        tmp_coor = 'prot_coor_' + tmpdict[ccii]
        variablevalue[tmp_psf] = variablevalue['begindir'] + '/' + \
                                        variablevalue[tmp_psf]
        variablevalue[tmp_coor] = variablevalue['begindir'] + '/' + \
                                        variablevalue[tmp_coor]
                                        
    
    #regular end:
    runcns.close()
    variablevalue['waterrefine'] = min([variablevalue['waterrefine'],variablevalue['structures'][1]])
    if variablevalue['clust_meth'] == "FCC" and float(variablevalue['clust_cutoff']) > 1.0 :
        variablevalue['clust_cutoff'] = "0.75"
    return variablevalue

