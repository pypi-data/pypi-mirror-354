#!/usr/bin/env python

from pickle import FALSE
import sys
import os
import argparse
from mako.template import Template
from mrtutils.mrtTemplateHelper import *
import git
import re
from mrtutils.updates import *
import subprocess
import yaml
import json

args = None
parser = None

#def filter_commits:

th = TemplateHelper()

reIncrement = re.compile(r'\+([0-9]*)')



def incrementAlphaVersion(version, n):
    def incrementChar(c, n):
        # Increment a single character by n, with rollover
        alphabet_size = 26
        new_char_code = ord(c) + n
        if new_char_code > ord('Z'):
            rollover = (new_char_code - ord('A')) % alphabet_size
            return chr(ord('A') + rollover), (new_char_code - ord('A')) // alphabet_size
        return chr(new_char_code), 0
    
    # Convert the version string into a list of characters for easier manipulation
    version_list = list(version)
    carry = n
    i = len(version) - 1
    
    # Process each character, starting from the end, to handle rollovers
    while i >= 0 and carry > 0:
        incremented_char, carry = incrementChar(version_list[i], carry)
        version_list[i] = incremented_char
        i -= 1
    
    # If there's still a carry after processing all characters, prepend a new character
    if carry > 0:
        version_list.insert(0, chr(ord('A') + carry - 1))
    
    # Convert the list of characters back into a string
    return ''.join(version_list)
    



class VersionStruct:
    def __init__(self):
        self.major = 0
        self.minor = 0
        self.patch = 0
        self.build = 0
        self.branch = "none"
        self.prefix =""
        self.hash = ""
        self.fileName =""
        self.repo = None
        self.fileType = "none"
        self.diffRegexMajor = None
        self.diffRegexMinor = None
        self.diffRegexPatch = None
        self.format="$MAJOR.$MINOR.$PATCH.$BUILD"

        try:
            #get the current branch
            self.default_branch = subprocess.check_output(['git rev-parse --abbrev-ref HEAD'], shell=True).decode('utf-8').strip()
        except:
            self.default_branch = 'main'

    def setPrefix(self, prefix):
        if not prefix == "":
            self.prefix = prefix+"_"

    def loadFile(self,path):
        base_name, extension = os.path.splitext(path)

        #This covers the case of files like '.env'
        if base_name[0] == '.' and extension == '':
            extension = base_name

        self.fileType = extension.replace(".","")

        if os.path.exists(path):

            if self.fileType == "h":
                self.loadCFile(path)

            elif self.fileType == "yml" or self.fileType == "yaml":
                self.loadYamlFile(path)

            elif self.fileType == "json":
                self.loadJsonFile(path)
            elif self.fileType == "env":
                self.loadEnvFile(path)
            else :
                print("Unsupported File type: " + self.fileType)

    def loadEnvFile(self,path):
        self.diffRegexMajor = re.compile(r'\+.*?VERSION_MAJOR=(\S*?)\s*?\n' )
        self.diffRegexMinor = re.compile(r'\+.*?VERSION_MINOR=(\S*?)\s*?\n' )
        self.diffRegexPatch = re.compile(r'\+.*?VERSION_PATCH=(\S*?)\s*?\n' )

        f = open(path)
        txt = f.read()
        self.fileName = path
        
        reMajor = re.compile(r'VERSION_MAJOR=(\S*?)\s*?\n' )
        reMinor = re.compile(r'VERSION_MINOR=(\S*?)\s*?\n' )
        rePatch = re.compile(r'VERSION_PATCH=(\S*?)\s*?\n' )
        reBuild = re.compile(r'VERSION_BUILD=(\S*?)\s*?\n' )
        
        mMajor = reMajor.findall(txt)
        mMinor = reMinor.findall(txt)

        mPatch = rePatch.findall(txt)
        mBuild = reBuild.findall(txt)

        self.major = mMajor[0].strip()
        self.minor = mMinor[0].strip()
        self.patch = mPatch[0].strip()
        self.build = mBuild[0].strip()

        #convert to int for numbers 
        if self.major.isdigit():
            self.major = int(self.major)
        if self.minor.isdigit():
            self.minor = int(self.minor)
        if self.patch.isdigit():
            self.patch = int(self.patch)
        if self.build.isdigit():
            self.build = int(self.build)

        

    def loadYamlFile(self,path):

        self.diffRegexMajor = re.compile(r'\+.*?major\s*?(\S*?)\s*?\n' )
        self.diffRegexMinor = re.compile(r'\+.*?minor\s*?(\S*?)\s*?\n' )
        self.diffRegexPatch = re.compile(r'\+.*?patch\s*?(\S*?)\s*?\n' )

        f = open(path)
        txt = f.read()
        dict = yaml.load(txt, Loader=yaml.FullLoader)
        self.fileName = path

        self.major = dict[self.prefix+'major']
        self.minor = dict[self.prefix+'minor']
        self.patch = dict[self.prefix+'patch']
        self.build = dict[self.prefix+'build']

    def loadJsonFile(self,path):

        self.diffRegexMajor = re.compile(r'\+.*?major.*?:(.*?),' )
        self.diffRegexMinor = re.compile(r'\+.*?minor.*?:(.*?),' )
        self.diffRegexPatch = re.compile(r'\+.*?patch.*?:(.*?),n' )
    
        f = open(path)
        txt = f.read()
        dict = json.loads(txt)
        self.fileName = path

        self.major = dict[self.prefix+'major']
        self.minor = dict[self.prefix+'minor']
        self.patch = dict[self.prefix+'patch']
        self.build = dict[self.prefix+'build']

        pass

    def loadCFile(self, path):

        self.diffRegexMajor = re.compile(r'\+.*?VERSION_MAJOR\s*?(\S*?)\s*?\n' )
        self.diffRegexMinor = re.compile(r'\+.*?VERSION_MINOR\s*?(\S*?)\s*?\n' )
        self.diffRegexPatch = re.compile(r'\+.*?VERSION_PATCH\s*?(\S*?)\s*?\n' )

        f = open(path)
        txt = f.read()
        self.fileName = path
        
        reMajor = re.compile(r'VERSION_MAJOR\s*?(\S*?)\s*?\n' )
        reMinor = re.compile(r'VERSION_MINOR\s*?(\S*?)\s*?\n' )
        rePatch = re.compile(r'VERSION_PATCH\s*?(\S*?)\s*?\n' )
        reBuild = re.compile(r'VERSION_BUILD\s*?(\S*?)\s*?\n' )
        
        mMajor = reMajor.findall(txt)
        mMinor = reMinor.findall(txt)

        mPatch = rePatch.findall(txt)
        mBuild = reBuild.findall(txt)

        self.major = mMajor[0][0].strip()
        self.minor = mMinor[0][0].strip()
        self.patch = mPatch[0][0].strip()
        self.build = mBuild[0][0].strip()

        #convert to int for numbers 
        if self.major.isdigit():
            self.major = int(self.major)
        if self.minor.isdigit():
            self.minor = int(self.minor)
        if self.patch.isdigit():
            self.patch = int(self.patch)
        if self.build.isdigit():
            self.build = int(self.build)
        
    
    def loadRepo(self,repo):

        self.repo = repo 

        try: 
            self.branch = repo.active_branch.name
        except:
            self.branch = 'DETACHED_' + repo.head.object.hexsha
            print("Repo in Detached head state")
            
        self.hash = repo.head.commit.hexsha



    def setMajor(self, str):
        
        if str[0] == '+':
            val = int(str[1:])

            #if major is a number increment 
            if type(self.major) == int:
                self.major+=val
            elif type(self.major) == str:
                self.major = incrementAlphaVersion(self.major, val)
                #if major is a single character, we can increment 
            self.minor = 0
            self.patch = 0
        
        else:
            if str.isdigit():
                self.major = int(str)
            else:
                self.major = str

    def setMinor(self, str):
        
        if str == 'auto':
            self.patch = self.getCommitsSinceLast(self.default_branch, change='major')
            self.patch = 0
        elif str[0] == '+':
            val = int(str[1:])


            if type(self.minor) == int:
                self.minor+=val
            elif type(self.minor) == str:
                self.minor = incrementAlphaVersion(self.minor, val)
            self.patch = 0
        
        else:
            self.minor = int(str)

    def setPatch(self, str):

        if str == 'auto':
            self.patch = self.getCommitsSinceLast(self.default_branch, change='minor')
        elif str[0] == '+':
            
            if type(self.patch) == int:
                val = int(str[1:])
                self.patch += val
            elif type(self.patch) == str:
                self.patch = incrementAlphaVersion(self.patch, val)
        else:
            if str.isdigit():
                self.patch = int(str)
            else:
                self.patch = str

    def setBuild(self, str):

        if str[0] == '+':
            val = int(str[1:])

            if type(self.build) == int:
                self.build += val
            elif type(self.build) == str:
                self.build = incrementAlphaVersion(self.build, val)
        else:
            if str.isdigit():
                self.build = int(str)
            else:
                self.build = str

    def getCommitsSinceLast(self, branch = 'master', change= 'minor' ):
    
        repatterns = {}
        count = 1

        if change == 'minor':
            repatterns = [self.diffRegexMinor, self.diffRegexMajor]
        if change == 'major':
            repatterns = [self.diffRegexMajor]
        elif change == 'patch':
            repatterns = [self.diffRegexPatch, self.diffRegexMinor, self.diffRegexMajor]

        if change == 'minor':
            repatterns = {
                'minor': self.diffRegexMinor,
                'major': self.diffRegexMajor
            }
        elif change == 'major':
            repatterns = {
                'major': self.diffRegexMajor
            }
        elif change == 'patch':
            repatterns = {
                'patch': self.diffRegexPatch,
                'minor': self.diffRegexMinor,
                'major': self.diffRegexMajor
            }
        
        commit = self.repo.commit(branch)
        firstParent = None 

        #iterate through using first-parent method 
        while(len(commit.parents) > 0):
            firstParent = commit.parents[0]

            try:
                diff = self.repo.git.diff(firstParent, commit, self.fileName)
            except git.exc.GitCommandError as e:
                #print(f"Error: {e}")
                return 0
            
            for [key, repattern] in repatterns.items():
                if repattern.search(diff):
                        #print(f"{key} updated at commit {commit.hexsha}")
                        return count
            
            count+= 1
            commit = firstParent

        
        return 0


    def asString(self):

        out = self.format
        out = out.replace("$MAJOR", str(self.major))
        out = out.replace("$MINOR", str(self.minor))
        out = out.replace("$PATCH", str(self.patch))
        out = out.replace("$BUILD", str(self.build))
        out = out.replace("$BRANCH", self.branch)
        out = out.replace("$HASH", self.hash)

        return out




  

# Initialize the argument parser
def init_args():
    global parser
    parser = argparse.ArgumentParser("Tool to generate version file")
    parser.add_argument('versionFile', type=str, nargs='?', help='version header file', default="version.h")
    parser.add_argument('-n', '--namespace', type=str, help='namespace to set prefix', default="")
    parser.add_argument('-M', '--major', type=str, help='Major version', default="")
    parser.add_argument('-m', '--minor', type=str, help='Minor version', default="")
    parser.add_argument('-p', '--patch', type=str, help='Patch', default="")
    parser.add_argument('-b', '--build', type=str, help='build number', default="")
    parser.add_argument('-f', '--format', type=str, help='Output format', default="$MAJOR.$MINOR.$PATCH")

    

def main():
    global parser
    global args
    init_args()
    args = parser.parse_args() 
    vs = VersionStruct()
    th = TemplateHelper()


    repo = git.Repo(os.getcwd())
    vs.loadRepo(repo)
    vs.format = args.format
    vs.setPrefix(args.namespace)
    
    vs.loadFile(args.versionFile)

    if not args.major == "":
        vs.setMajor(args.major)
    if not args.minor == "":
        vs.setMinor(args.minor)
    if not args.patch == "":
        vs.setPatch(args.patch)
    if not args.build == "":
        vs.setBuild(args.build)

    th.buildTemplate(vs, "templates/version/version." + vs.fileType , args.versionFile)



    print(vs.asString())



if __name__ == "__main__":
    main()