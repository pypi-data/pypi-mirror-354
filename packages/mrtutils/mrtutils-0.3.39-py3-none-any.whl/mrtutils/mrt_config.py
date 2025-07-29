#!/usr/bin/env python

import sys
import os
from mrtutils.modsync import *
import argparse
import tempfile

from kconfiglib import Kconfig, \
                       Symbol, MENU, COMMENT, \
                       BOOL, TRISTATE, STRING, INT, HEX, UNKNOWN, \
                       expr_value, \
                       TRI_TO_STR

from mrtutils.menuconfig import menuconfig

remoteRepo = None #Repo("git@bitbucket.org/uprev/uprev-mrt.git") 
localRepo = None #Repo(os.getcwd())

metaRemoteDefault =   "https://gitlab.com/mrt-public" #"git@github.com/uprev-mrt/MrT-Meta.git"

args = None
parser = None
mods_to_add = []
mods_to_remove = []

temp_config_file = ""

os.environ["MENUCONFIG_STYLE"] = "default separator=fg:black,bg:blue,bold frame=fg:black,bg:red,bold"


#   "default": """
#     path=fg:black,bg:white,bold
#     separator=fg:black,bg:blue,bold
#     list=fg:black,bg:white
#     selection=fg:white,bg:blue,bold
#     inv-list=fg:red,bg:white
#     inv-selection=fg:red,bg:blue
#     help=path
#     show-help=list
#     frame=fg:black,bg:blue,bold
#     body=fg:white,bg:black
#     edit=fg:white,bg:blue
#     jump-edit=edit
#     text=list
#     """,



class MrtKConfig(Kconfig):
    global remoteRepo
    global localRepo
    global mods_to_add
    global mods_to_remove

    def write_config(self, filename):
        print("TESTING")
        for sym in self.defined_syms:
            if sym.str_value == 'y':
                newMod = remoteRepo.findMod(sym.name.replace("ENABLE_",""))
                if newMod != None:
                    if not newMod.exists:
                        mods_to_add.append(newMod)
            else:
                newMod = remoteRepo.findMod(sym.name.replace("ENABLE_",""))
                if newMod != None:
                    if newMod.exists:
                        mods_to_remove.append(newMod)
        
        return True
    
    def load_config(self, filename=None, replace=True, verbose=None):
        global temp_config_file
        msg = " configuration '{}'".format(temp_config_file)

        try:
            self._load_config(temp_config_file, replace)
        except UnicodeDecodeError as e:
            _decoding_error(e, filename)
        finally:
            self._warn_assign_no_prompt = True

        self.missing_syms = [] 

        return "Loaded Submodules"


def back_out_to_git_root(max_depth=10):

    """
    Back out to the root of the git repository. 

    return the relative path from the git root to get back to the initial directory

    """
    ret_path = ""
    back_path = ""
    for i in range(max_depth):
        if os.path.exists( back_path+ ".git"):
            return back_path, ret_path
        else:
            cur_dir = os.getcwd().split(os.sep)[-1]
            ret_path = cur_dir + "/" + ret_path
            back_path = "../" + back_path


    return None, None
            
   


# Initialize the argument parser
def init_args():
    global parser
    parser = argparse.ArgumentParser("Tool to import submodules from MrT registry")
    parser.add_argument('localRoot', type=str, nargs='?', help='Local Root of MrT modules', default="MrT")
    parser.add_argument('-a', '--all', action='store_true', help='Skips the UI and just pulls all submodules (used for CI/CD Unit testing)', default= False)
    parser.add_argument('-g', '--gather', action='store_true', help='Gathers the mrt.yml files and creates a single structure', default= False)
    parser.add_argument('-r', '--remote', type=str, help='remote repo or group to sync from. Overrides ${MRT_REMOTE}', default="")
    parser.add_argument('-t', '--unit-test', action='store_true', help='Add Unit Test for modules', default= False)

def main():
    global temp_config_file
    global remoteRepo
    global localRepo
    global mods_to_add
    global mods_to_remove

    init_args()
    args= parser.parse_args()

    kconf_file = tempfile.NamedTemporaryFile(mode = "w")
    conf_file = tempfile.NamedTemporaryFile(mode = "w")


    metaRepo_path = metaRemoteDefault 

    if args.remote != "":
        metaRepo_path = args.remote 
        print('Using Meta-repo: ' + metaRepo_path)
    elif 'MRT_META_REPO' in os.environ:
        metaRepo_path = os.environ.get('MRT_REMOTE')
        print('Using Meta Repo specified by environment: ' + metaRepo_path)


    remoteRepo = Repo(metaRepo_path)

    if remoteRepo.isGroup:
        print("Gathering modules from Group at " + metaRepo_path)
    else: 
        print("Gathering modules from Meta-Repo at " + metaRepo_path)

    if 'bitbucket' in args.remote:
        remoteRepo.isBitbucket = True



    local_root, relativePath = back_out_to_git_root()
    relativePath = relativePath + args.localRoot

    if local_root == None:
        print("Error: Not in a git repository (or too deep in the tree)")
        exit(1)

    elif local_root == "":
        local_root = os.getcwd()
    else:
        backCount = len(relativePath.split("/"))
        absPath = os.getcwd().split("/")
        for i in range(backCount - 1):
            absPath.pop()
        
        absPath = "/".join(absPath)

        print(f"CWD is not the root of the git repository.  Backing out to git root found at {absPath}")

    localRepo = Repo(local_root)

    remoteRepo.getSubModules()
    localRepo.getSubModules()

    localRepo.setRelativePath(relativePath)



    if args.gather:
        with open( localRepo.relativePath + 'mrt.yaml', 'w') as file:
            info = localRepo.gatherModuleYamls()
            doc = yaml.dump(info, file)
        
        exit(0)

    
    

    if not args.all:

        remoteRepo.crossCheckMods(localRepo)


        fileText = remoteRepo.dir.dirs["Modules"].getKConfigString(0)
        conf_file_txt = remoteRepo.getConfigString()

        kconf_file.write(fileText)
        conf_file.write(conf_file_txt)
        conf_file.seek(0,0)
        kconf_file.seek(0,0)
        kconf = MrtKConfig(kconf_file.name)
        temp_config_file = conf_file.name

        
        menuconfig(kconf)
        kconf_file.close()
        conf_file.close()

        for mod in mods_to_add:
            localRepo.addSubModule(mod)

        for mod in mods_to_remove:
            localRepo.removeSubModule(mod)
    else: 
        for mod in remoteRepo.mods:
            localRepo.addSubModule(mod)
        

        

if __name__ == "__main__":
    main()