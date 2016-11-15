#!/usr/bin/env python
# -*- coding: utf-8 -*

__ver_major__ = 0
__ver_minor__ = 2
__ver_patch__ = 0
__ver_sub__ = ""
__version__ = "%d.%d.%d" % (__ver_major__, __ver_minor__, __ver_patch__)
"""
This program rebuild translantion of parts for Kerbal Space Program.

:authors: John Byaka
:copyright: Copyright 2016, BYaka
:license: Apache License 2.0

:license:

   Copyright 2016 BYaka

   Licensed under the Apache License, Version 2.0 (the "License");
   you may not use this file except in compliance with the License.
   You may obtain a copy of the License at http://www.apache.org/licenses/LICENSE-2.0

   Unless required by applicable law or agreed to in writing, software
   distributed under the License is distributed on an "AS IS" BASIS,
   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
   See the License for the specific language governing permissions and
   limitations under the License.
"""

import sys, os, re
sys.path.append('libs/')

from functionsex import *

def updatePart(dataOld, dataNew):
   # find title and description
   tArr1_1=re.findall(r'^\s*title\s?=\s?(.+)$', dataOld, re.MULTILINE)
   tArr1_2=re.findall(r'^\s*title\s?=\s?(.+)$', dataNew, re.MULTILINE)
   tArr2_1=re.findall(r'^\s*description\s?=\s?(.+)$', dataOld, re.MULTILINE)
   tArr2_2=re.findall(r'^\s*description\s?=\s?(.+)$', dataNew, re.MULTILINE)
   if len(tArr1_1)!=1 or len(tArr1_2)!=1 or len(tArr2_1)!=1 or len(tArr2_2)!=1: return None
   # replace in original with translated values
   data=dataNew
   data=re.sub(r'^(\s*title\s?=\s?)(.+)$', r'\1'+tArr1_1[0], data, count=1, flags=re.MULTILINE)
   data=re.sub(r'^(\s*description\s?=\s?)(.+)$', r'\1'+tArr2_1[0], data, count=1, flags=re.MULTILINE)
   return data

def updateParts(pathKSP, pathSource, pathOutput):
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
         data=updatePart(dataOld, dataNew)
         if not data:
            print '! Wrong format for part "%s", original used'%f
            data=dataNew
         # write to output
         fileWrite(pathOutput+p+'/'+f, data)
      # add sub-dirs to stack
      stack+=[p+'/'+s for s in pathList(pathSource+p, fullPath=False, alsoFiles=False, alsoDirs=True)]
   print 'Updating categories complited! Output saved to "%s"'%pathOutput

# def updateCategory(pathKSP, pathSource, pathOutput):
#    pathSource+='Parts/'
#    pathOutput+='Parts/'
#    pathKSP+='GameData/Squad/Parts/'
#    stack=pathList(pathSource, fullPath=False, alsoFiles=False, alsoDirs=True)
#    while stack:
#       p=stack.pop()
#       # check or create dir in pathOutput
#       if not os.path.exists(pathOutput+p):
#          os.makedirs(pathOutput+p)
#       # proc parts
#       for f in pathList(pathSource+p, fullPath=False, alsoFiles=True, alsoDirs=False):
#          if not f.endswith('.cfg'): continue
#          if not os.path.exists(pathKSP+p+'/'+f):
#             print '~ This part not existed in KSP: "%s"'%f
#             continue
#          dataOld=fileGet(pathSource+p+'/'+f)
#          dataNew=fileGet(pathKSP+p+'/'+f)
#          # find category in new and replace in old
#          tArr=re.findall(r'^\s*category\s?=\s?(\w*)$', dataNew, re.MULTILINE)
#          if len(tArr)!=1:
#             print '! Wrong category data for part "%s"'%f
#             data=dataNew
#          else:
#             data=re.sub(r'^(\s*category\s?=\s?)(\w*)$', r'\1'+tArr[0], dataOld, count=1, flags=re.MULTILINE)
#          # write to output
#          fileWrite(pathOutput+p+'/'+f, data)
#       # add sub-dirs to stack
#       stack+=[p+'/'+s for s in pathList(pathSource+p, fullPath=False, alsoFiles=False, alsoDirs=True)]
#    print 'Updating categories complited! Output saved to "%s"'%pathOutput

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
   updateParts(pathKSP, pathSource, pathOutput)
