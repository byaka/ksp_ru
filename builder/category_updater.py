# -*- coding: utf-8 -*-
import sys, os, re
sys.path.append('libs/')

from functionsex import *

def updateCategory(pathKSP, pathSource, pathOutput):
   pathSource+='Parts/'
   pathOutput+='Parts/'
   pathKSP+='GameData/Squad/Parts/'
   stack=pathList(pathSource, fullPath=False, alsoFiles=False, alsoDirs=True)
   while stack:
      p=stack.pop()
      # check or create dir in pathOutput
      if not os.path.exists(pathOutput+p):
         os.makedirs(pathOutput+p)
      # proc parts
      for f in pathList(pathSource+p, fullPath=False, alsoFiles=True, alsoDirs=False):
         if not f.endswith('.cfg'): continue
         if not os.path.exists(pathKSP+p+'/'+f):
            print '~ This part not existed in KSP: "%s"'%f
            continue
         dataOld=fileGet(pathSource+p+'/'+f)
         dataNew=fileGet(pathKSP+p+'/'+f)
         # find category in new and replace in old
         tArr=re.findall(r'^\s*category\s?=\s?(\w*)$', dataNew, re.MULTILINE)
         if len(tArr)!=1:
            print '! Wrong category data for part "%s"'%f
            data=dataNew
         else:
            data=re.sub(r'^(\s*category\s?=\s?)(\w*)$', r'\1'+tArr[0], dataOld, count=1, flags=re.MULTILINE)
         # write to output
         fileWrite(pathOutput+p+'/'+f, data)
      # add sub-dirs to stack
      stack+=[p+'/'+s for s in pathList(pathSource+p, fullPath=False, alsoFiles=False, alsoDirs=True)]
   print 'Updating categories complited! Output saved to "%s"'%pathOutput

if __name__ == '__main__':
   path='/'.join(getScriptPath().split('/')[:-1])
   if len(sys.argv)<2 or not sys.argv[1]:
      raise ValueError('Please, pass path to KSP')
   elif len(sys.argv)>2:
      raise ValueError('Too many arguments, maybe your path contains spaces?')
   else:
      pathKSP=sys.argv[1]
      if not os.path.exists(pathKSP):
         raise ValueError('Given path not exised: "%s"'%pathKSP)
      if not pathKSP.endswith('/'): pathKSP+='/'
   pathSource=path+'/data_original/'
   pathOutput=path+'/data_builded/'
   updateCategory(pathKSP, pathSource, pathOutput)
