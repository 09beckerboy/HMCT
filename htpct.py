import os
import shutil
from zipfile import ZipFile
import sys
import importlib
import json

script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("{0}/extensions".format(script_dir))
for file in os.listdir("{0}/extensions".format(script_dir)):
    if file.endswith(".py"):
        extension = importlib.import_module(file.split(".")[0])
        if "__all__" in extension.__dict__:
            names = extension.__dict__["__all__"]
        else:
            names = [x for x in extension.__dict__ if not x.startswith("_")]
        globals().update({k: getattr(extension, k) for k in names})
        if os.path.exists("{0}/extensions/{1}.runtime".format(script_dir, file.split(".")[0])):
            exec(open("{0}/extensions/{1}".format(script_dir, file)).read())

with open("shortcuts.json", "r") as read_file:
    shortcuts = json.load(read_file)

def mainMenu():
    os.system("title Main Menu")
    os.system('cls||clear')
    print("         _________ _______  _______ _________\n|\     /|\__   __/(  ____ )(  ____ \\__   __/\n| )   ( |   ) (   | (    )|| (    \/   ) (   \n| (___) |   | |   | (____)|| |         | |   \n|  ___  |   | |   |  _____)| |         | |   \n| (   ) |   | |   | (      | |         | |   \n| )   ( |   | |   | )      | (____/\   | |   \n|/     \|   )_(   |/       (_______/   )_(   ")
    print("\n         v1.4 by 09beckerboy")
    print("_____________________________________________")
    print("Message me on Discord with any suggestions @09beckerboy")
    print("GUI version coming eventually!")
    print("_____________________________________________")
    print("1: New Pack")
    print("2: Load Pack")
    print("3: Import Pack")
    print("4: Export Pack")
    print("5: Delete Pack")
    print("6: Exit")
    command = int(input("Enter option\n: "))
    if command == 1: newPack()
    if command == 2:
        try:
            os.system("title Load Pack")
            os.system('cls||clear')
            print("Packs:")
            for name in os.listdir("{0}/texture packs/".format(script_dir)):
                    pack = os.path.join("{0}/texture packs/".format(script_dir), name)
                    if os.path.isdir(pack):
                        print("   "+name)
            pack_load_name = input("Select pack to load, or 'cancel' to return to main menu\n: ")
            if pack_load_name == "cancel": mainMenu()
            else: loadPack(pack_load_name)
        except Exception as e: mainMenu()
    if command == 3:
        try:
            os.system("title Import Pack")
            os.system('cls||clear')
            pack_import_path = input("Provide the path to the pack you wish to import\nMake sure to use '/' instead of '\' and end with .zip (path/to/pack/pack.zip)\nMake sure you don't already have a pack with the same name!\nType 'cancel' to return to the main menu\n: ")
            if pack_import_path == "cancel": mainMenu()
            else: importPack(pack_import_path)
        except Exception as e: mainMenu()
    if command == 4:
        try:
            os.system("title Export Pack")
            os.system('cls||clear')
            print("Packs:")
            for name in os.listdir("{0}/texture packs/".format(script_dir)):
                    pack = os.path.join("{0}/texture packs/".format(script_dir), name)
                    if os.path.isdir(pack):
                        print("   "+name)
            pack_export_name = input("Select pack to export, or 'cancel' to go back to the main menu\n: ")
            if pack_export_name == "cancel":
                mainMenu()
            else:
                exportPack(pack_export_name)
        except Exception as e: mainMenu()
    if command == 5:
        try:
            os.system("title Delete Pack")
            os.system('cls||clear')
            print("Packs:")
            for name in os.listdir("{0}/texture packs/".format(script_dir)):
                    pack = os.path.join("{0}/texture packs/".format(script_dir), name)
                    if os.path.isdir(pack):
                        print("   "+name)
            pack_delete_name = input("Select pack to delete, or 'cancel' to go back to the main menu\n: ")
            if pack_delete_name == "cancel":
                mainMenu()
            else:
                confirm = str(input("Are you sure want to delete the pack '{0}'?\nY or N\n: ".format(pack_delete_name))).upper()
                if confirm == "Y": 
                    shutil.rmtree("{0}\\texture packs\\{1}".format(script_dir, pack_delete_name))
                    print("Pack successfully deleted")
                    input("Press Enter to return to main menu...")
                    mainMenu()
                else: mainMenu()
        except Exception as e: mainMenu()
    if command == 6: exit()

def newPack():
    os.system("title Pack Creation")
    os.system('cls||clear')
    print("Existing Packs:")
    for name in os.listdir("{0}/texture packs/".format(script_dir)):
        pack = os.path.join("{0}/texture packs/".format(script_dir), name)
        if os.path.isdir(pack):
            print("   "+name)
    print("\n")
    name = input("Enter pack name (Can't be the same as an existing pack)\nEnter 'cancel' to return to main menu\n: ")
    if name == "cancel": mainMenu()
    os.mkdir("{0}/texture packs/{1}".format(script_dir, name))
    moveTools(name)
    levels = []
    levelSelect = ""
    os.system("title Level Select")
    try:
        while levelSelect != "done":
            os.system('cls||clear')
            print("Levels:\nboot\ncommon\nCh00_Dre\nCh01_Hob\nCh02_Roa\nCh02a_Tr\nCh4_Over\nCh05_Swo\nMirkwood\nCh07_Bar\nCH08_Lak\nCh09_Sma\nCh10_Lon\nCh11_Clo")
            print("Currently selected levels:\n"+str(levels))
            levelSelect = input("Select level, type name exactly as shown\nType 'all' to select all levels\nType a level name again to remove\nType 'done' if done selecting or 'cancel' to return to main menu\n: ")
            if levelSelect != "done":
                if levelSelect == "cancel":
                    shutil.rmtree("{0}/texture packs/{1}".format(script_dir, name))
                    mainMenu()
                if levelSelect == "all":
                    for levelName in os.listdir("{0}/The Hobbit(TM)/".format(script_dir)):
                        level = os.path.join("{0}/The Hobbit(TM)/".format(script_dir), levelName)
                        if os.path.isdir(level):
                            levels.append(levelSelect)
                            shutil.copytree("{0}\\The Hobbit(TM)\\{1}".format(script_dir, levelName), "{0}\\texture packs\\{1}\\{2}".format(script_dir, name, levelName))
                else:
                    if levelSelect in levels:
                        levels.remove(levelSelect)
                        print("Removing {0}...".format(levelSelect))
                        shutil.rmtree("{0}\\texture packs\\{1}\\{2}".format(script_dir, name, levelSelect))
                    else:
                        levels.append(levelSelect)
                        print("Adding {0}...".format(levelSelect))
                        shutil.copytree("{0}\\The Hobbit(TM)\\{1}".format(script_dir, levelSelect), "{0}\\texture packs\\{1}\\{2}".format(script_dir, name, levelSelect))
            else:
                pass
    except Exception as e: print(e)
    os.chdir("{0}/texture packs/{1}".format(script_dir, name))
    os.system("convert_xbmp_to_dds.bat")
    os.chdir(script_dir)
    print("Pack successfully created")
    input("Press Enter to continue to editing...")
    loadPack(name)

def loadPack(pack_name):
    os.system("title Editing Pack")
    os.system('cls||clear')
    texture_level_pairs = []
    try:
        for level in os.listdir("{0}/texture packs/{1}".format(script_dir, pack_name)):
            for root, dirs, files in os.walk("{0}/texture packs/{1}/{2}".format(script_dir, pack_name, level)):
                for texture in files:
                    if texture.endswith(".dds") or texture.endswith(".XBMP"):
                        texture_level_pair = (texture, level)
                        texture_level_pairs.append(texture_level_pair)
    except Exception as e: print(e)
    command = ""
    global selected
    selected = []
    global current_pack
    current_pack = pack_name
    while True:
        command = input("Enter command, type 'help' for help\n: ")
        try:
            base_command = command.split(" ")[0]
            i = 0
            command_args = []
            for arg in command.split(" ")[1:]:
                command_args.append(arg)
                i += 1
        except Exception as e: pass
        try:
            if base_command in shortcuts:
                temp = getattr(sys.modules[__name__], shortcuts[base_command])
            else: temp = getattr(sys.modules[__name__], base_command)
            if command_args == []: temp()
            else: temp(command_args)
        except Exception as e: print(e)

def exit():
    sys.exit()

def back():
    mainMenu()

def clear():
    os.system('cls||clear')

def convert(args):
    if args[0] == "dds":
        os.chdir("{0}/texture packs/{1}".format(script_dir, current_pack))
        os.system("convert_xbmp_to_dds.bat")
        os.chdir(script_dir)
    if args[0] == "xbmp":
        os.chdir("{0}/texture packs/{1}".format(script_dir, current_pack))
        os.system("convert_dds_to_xbmp.bat")
        os.chdir(script_dir)

def help():
    try:
        with open("htpct.help", "r") as f:
            for line in f.readlines():
                print(line, sep="")
        for file in os.listdir("{0}/extensions".format(script_dir, current_pack)):
            if file.endswith(".help"):
                print("--{0}--".format(file.split(".")[0]))
                os.chdir("{0}/extensions".format(script_dir))
                with open(file, "r") as f:
                    for line in f.readlines():
                        print(line, sep="")
                os.chdir(script_dir)
    except Exception as e: print(e)

def list():
    try:
        for name in os.listdir("{0}/texture packs/{1}".format(script_dir, current_pack)):
            level = os.path.join("{0}/texture packs/{1}".format(script_dir, current_pack), name)
            if os.path.isdir(level):
                print("   "+name)
    except Exception as e: print(e)

def select(args):
    try:
        temp_select = args[0].split(",")
        for texture in temp_select:
            selected.append(texture)
    except Exception as e: print(e)

def view(args):
    try:
        if args[0] == "" or args[0] == "all":
            for level in os.listdir("{0}/texture packs/{1}".format(script_dir, current_pack)):
                print(level+"/")
                for folder in os.listdir("{0}/texture packs/{1}/{2}".format(script_dir, current_pack, level)):
                    print("-"+folder+"/")
                    for folder1 in os.listdir("{0}/texture packs/{1}/{2}/{3}".format(script_dir, current_pack, level, folder)):
                        print("--"+folder1+"/")
                        for texture in os.listdir("{0}/texture packs/{1}/{2}/{3}/{4}".format(script_dir, current_pack, level, folder, folder1)):
                            if texture.endswith(".dds") or texture.endswith(".XBMP"):
                                if texture in selected: print(" * "+texture)
                                else: print("   "+texture)
        else: 
            print(args[0]+"/")
            for folder in os.listdir("{0}/texture packs/{1}/{2}".format(script_dir, current_pack, args[0])):
                print("-"+folder+"/")
                for folder1 in os.listdir("{0}/texture packs/{1}/{2}/{3}".format(script_dir, current_pack, args[0], folder)):
                    print("--"+folder1+"/")
                    for texture in os.listdir("{0}/texture packs/{1}/{2}/{3}/{4}".format(script_dir, current_pack, args[0], folder, folder1)):
                        if texture.endswith(".dds") or texture.endswith(".XBMP"):
                            if texture in selected: print(" * "+texture)
                            else: print("   "+texture)
    except Exception as e: print(e)

def edit(args):
    try:
        if args[0] == "all":
            for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, current_pack)):
                for name in files:
                    if name.endswith(".dds") or name.endswith(".XBMP"):
                        os.startfile(os.path.join(root, name))
        if args[0] == "selected":
            for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, current_pack)):
                for name in files:
                    if name.endswith(".dds") or name.endswith(".XBMP"):
                        if name in selected:
                            os.startfile(os.path.join(root, name))
        if args[0].endswith(".dds") or args[0].endswith(".XBMP"):
            if "args[1]" in locals():
                for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, current_pack)):
                    for name in dirs:
                        if name == args[1]:
                            for root, dirs, files in os.walk("{0}/texture packs/{1}/{2}".format(script_dir, current_pack, name)):
                                for name2 in files:
                                    if name2.endswith(".dds") or name2.endswith(".XBMP"):
                                        if name2 == args[0]:
                                            os.startfile(os.path.join(root, name2))
            else:
                for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, current_pack)):
                    for name in files:
                        if name.endswith(".dds" or name.endswith(".XBMP")):
                            if name == args[0]:
                                os.startfile(os.path.join(root, name))
        else:
            for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, current_pack)):
                for name in dirs:
                    if name == args[0]:
                        for root, dirs, files in os.walk("{0}/texture packs/{1}/{2}".format(script_dir, current_pack, name)):
                            for name2 in files:
                                if name2.endswith(".dds" or name2.endswith(".XBMP")):
                                    os.startfile(os.path.join(root, name2))
    except Exception as e: print(e)

def add(args):
    try:
        shutil.copytree("{0}\\The Hobbit(TM)\\{1}".format(script_dir, args[0]), "{0}\\texture packs\\{1}\\{2}".format(script_dir, current_pack, args[0]))
    except Exception as e: print(e)

def remove(args):
    try:
        shutil.rmtree("{0}\\texture packs\\{1}\\{2}".format(script_dir, current_pack, args[0]))
    except Exception as e: print(e)

def set(args):
    try:
        exec(args[0] + " = " + args[1])
    except Exception as e: print(e)

def exportPack(pack_name):
    os.system("title Export Pack")
    os.chdir("{0}/texture packs/{1}".format(script_dir, pack_name))
    os.system("convert_dds_to_xbmp.bat")
    os.chdir(script_dir)
    if os.path.exists("{0}/exported packs/{1}".format(script_dir, pack_name)): pass
    else: os.mkdir("{0}/exported packs/{1}".format(script_dir, pack_name))
    for name in os.listdir("{0}/texture packs/{1}".format(script_dir, pack_name)):
        level = os.path.join("{0}/texture packs/{1}".format(script_dir, pack_name), name)
        if os.path.isdir(level):
            os.chdir("{0}/texture packs/{1}".format(script_dir, pack_name))
            os.system("pack_dfs_Drag'n'Drop.bat {0}".format(name))
            os.chdir(script_dir)
    for name in os.listdir("{0}/texture packs/{1}".format(script_dir, pack_name)):
        if name.endswith(".000") or name.endswith(".DFS"):
            shutil.move("{0}\\texture packs\\{1}\\{2}".format(script_dir, pack_name, name), "{0}\\exported packs\\{1}".format(script_dir, pack_name))
    confirm = str(input("Pack successfully exported, do you want to compress it too? Y or N\n: ")).upper()
    if confirm == "Y": shutil.make_archive(pack_name, 'zip', "{0}\\exported packs\\{1}".format(script_dir, pack_name))
    else: pass
    input("Press Enter to return to main menu...")
    mainMenu()

def importPack(pack_path):
    os.system("title Import Pack")
    pack_name = pack_path.split("/")[-1]
    pack_name = pack_name.split(".")[0]
    with ZipFile(pack_path, 'r') as pack_zip:
        pack_zip.extractall("{0}/texture packs".format(script_dir))
    try:
        for name in os.listdir("{0}/texture packs/{1}".format(script_dir, pack_name)):
            if name.endswith(".DFS"):
                os.mkdir("{0}/texture packs/{1}/{2}".format(script_dir, pack_name, name.split(".")[0]))
                shutil.move("{0}\\texture packs\\{1}\\{2}".format(script_dir, pack_name, name), "{0}\\texture packs\\{1}\\{2}\\{3}".format(script_dir, pack_name, name.split(".")[0], name))
                shutil.move("{0}\\texture packs\\{1}\\{2}.000".format(script_dir, pack_name, name.split(".")[0]), "{0}\\texture packs\\{1}\\{2}\\{3}.000".format(script_dir, pack_name, name.split(".")[0], name.split(".")[0]))
                shutil.copy2("{0}\\undfs\\undfs.c".format(script_dir), "{0}\\texture packs\\{1}\\{2}\\undfs.c".format(script_dir, pack_name, name.split(".")[0]))
                shutil.copy2("{0}\\undfs\\undfs.exe".format(script_dir), "{0}\\texture packs\\{1}\\{2}\\undfs.exe".format(script_dir, pack_name, name.split(".")[0]))
                shutil.copy2("{0}\\undfs\\undfs.tgt".format(script_dir), "{0}\\texture packs\\{1}\\{2}\\undfs.tgt".format(script_dir, pack_name, name.split(".")[0]))
                shutil.copy2("{0}\\undfs\\undfs.wpj".format(script_dir), "{0}\\texture packs\\{1}\\{2}\\undfs.wpj".format(script_dir, pack_name, name.split(".")[0]))
                os.chdir("{0}/texture packs/{1}/{2}".format(script_dir, pack_name, name.split(".")[0]))
                os.system("undfs.exe {0}".format(name))
                os.remove("{0}".format(name))
                os.remove("{0}.000".format(name.split(".")[0]))
                os.chdir(script_dir)
                os.remove("{0}/texture packs/{1}/{2}/undfs.c".format(script_dir, pack_name, name.split(".")[0]))
                os.remove("{0}/texture packs/{1}/{2}/undfs.exe".format(script_dir, pack_name, name.split(".")[0]))
                os.remove("{0}/texture packs/{1}/{2}/undfs.tgt".format(script_dir, pack_name, name.split(".")[0]))
                os.remove("{0}/texture packs/{1}/{2}/undfs.wpj".format(script_dir, pack_name, name.split(".")[0]))
        moveTools(pack_name)
    except Exception as e: print(e)
    print("Pack successfully imported")
    input("Press Enter to continue to editing...")
    loadPack(pack_name)

def moveTools(pack_name):
    shutil.copy2("{0}\\xbmp_converter\\convert_dds_to_xbmp.bat".format(script_dir), "{0}\\texture packs\\{1}\\convert_dds_to_xbmp.bat".format(script_dir, pack_name))
    shutil.copy2("{0}\\xbmp_converter\\convert_xbmp_to_dds.bat".format(script_dir), "{0}\\texture packs\\{1}\\convert_xbmp_to_dds.bat".format(script_dir, pack_name))
    shutil.copy2("{0}\\xbmp_converter\\xbmpconverter.exe".format(script_dir), "{0}\\texture packs\\{1}\\xbmpconverter.exe".format(script_dir, pack_name))
    shutil.copy2("{0}\\pack_dfs\\dfs.exe".format(script_dir), "{0}\\texture packs\\{1}\\dfs.exe".format(script_dir, pack_name))
    shutil.copy2("{0}\\pack_dfs\\pack_dfs_Drag'n'Drop.bat".format(script_dir), "{0}\\texture packs\\{1}\\pack_dfs_Drag'n'Drop.bat".format(script_dir, pack_name))

if __name__ == '__main__':
    if os.path.exists("{}/texture packs".format(script_dir)): pass
    else: os.mkdir("{}/texture packs".format(script_dir))
    if os.path.exists("{}/exported packs".format(script_dir)): pass
    else: os.mkdir("{}/exported packs".format(script_dir))
    mainMenu()