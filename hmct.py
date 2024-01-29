import os
import shutil
import zipfile
import sys
import importlib
import json
import random
import filecmp

#Setup script environment
script_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append("{0}/plugins".format(script_dir))
splashes = []
#Import splashes
with open("splashes.txt", "r") as f:
    for line in f.readlines():
        splashes.append(line[:-1])
#Import plugins
for file in os.listdir("{0}/plugins".format(script_dir)):
    if file.endswith(".py"):
        plugin = importlib.import_module(file.split(".")[0])
        if "__all__" in plugin.__dict__:
            names = plugin.__dict__["__all__"]
        else:
            names = [x for x in plugin.__dict__ if not x.startswith("_")]
        globals().update({k: getattr(plugin, k) for k in names})
        if os.path.exists("{0}/plugins/{1}.runtime".format(script_dir, file.split(".")[0])):
            exec(open("{0}/plugins/{1}".format(script_dir, file)).read())
#Import shortcuts
with open("shortcuts.json", "r") as read_file:
    shortcuts = json.load(read_file)
#Import settings
with open("settings.json", "r") as read_file:
    settings = json.load(read_file)

def mainMenu(*none):
    #Set up main menu
    os.system("title Main Menu")
    os.system('cls||clear')
    splash_text = random.choice(splashes)
    print("          _______  _______ _________\n|\     /|(       )(  ____ \\__   __/\n| )   ( || () () || (    \/   ) (   \n| (___) || || || || |         | |   \n|  ___  || |(_)| || |         | |   \n| (   ) || |   | || |         | |   \n| )   ( || )   ( || (____/\   | |   \n|/     \||/     \|(_______/   )_(   ")
    print("\n       v2.0 by 09beckerboy")
    print("         Formerly HTPCT")
    print("_____________________________________")
    print("Special thanks to @modera!")
    print("\n" + splash_text)
    print("_____________________________________")
    print("1: New Project")
    print("2: Load Project")
    print("3: Import Mod")
    print("4: Export Mod")
    print("5: Delete Project")
    print("6: Exit")
    option = int(input("Enter option\n: "))
    if option == 1: newProject()
    if option == 2:
        try:
            os.system("title Load Project")
            os.system('cls||clear')
            print("Projects:")
            for name in os.listdir("{0}/projects/".format(script_dir)):
                    project = os.path.join("{0}/projects/".format(script_dir), name)
                    if os.path.isdir(project):
                        print("   "+name)
            project_load_name = input("Select project to load, or 'cancel' to return to main menu\n: ")
            if project_load_name == "cancel": mainMenu()
            else: loadProject(project_load_name)
        except Exception as e: mainMenu()
    if option == 3:
        try:
            os.system("title Import Mod")
            os.system('cls||clear')
            mod_import_path = input("Provide the path to the mod you wish to import\nMake sure to use '/' instead of '\' and end with .zip (path/to/mod/mod.zip)\nMake sure you don't already have a project with the same name!\nType 'cancel' to return to the main menu\n: ")
            if mod_import_path == "cancel": mainMenu()
            elif not os.path.exists("{0}\\projects\\{1}".format(script_dir, mod_import_path.split("/")[-1])): importMod(mod_import_path)
        except Exception as e: mainMenu()
    if option == 4:
        try:
            os.system("title Export Mod")
            os.system('cls||clear')
            print("Projects:")
            for name in os.listdir("{0}/projects/".format(script_dir)):
                    project = os.path.join("{0}/projects/".format(script_dir), name)
                    if os.path.isdir(project):
                        print("   "+name)
            mod_export_name = input("Select project to export, or 'cancel' to go back to the main menu\n: ")
            if mod_export_name == "cancel":
                mainMenu()
            else:
                exportMod(mod_export_name)
        except Exception as e: mainMenu()
    if option == 5:
        try:
            os.system("title Delete Project")
            os.system('cls||clear')
            print("Projects:")
            for name in os.listdir("{0}/projects/".format(script_dir)):
                    project = os.path.join("{0}/projects/".format(script_dir), name)
                    if os.path.isdir(project):
                        print("   "+name)
            project_delete_name = input("Select project to delete, or 'cancel' to go back to the main menu\n: ")
            if project_delete_name == "cancel":
                mainMenu()
            else:
                confirm = str(input("Are you sure want to delete the project '{0}'?\nY or N\n: ".format(project_delete_name))).upper()
                if confirm == "Y": 
                    shutil.rmtree("{0}\\projects\\{1}".format(script_dir, project_delete_name))
                    print("Project successfully deleted")
                    input("Press Enter to return to main menu...")
                    mainMenu()
                else: mainMenu()
        except Exception as e: mainMenu()
    if option == 6: exit()

def newProject(*none):
    os.system("title Project Creation")
    os.system('cls||clear')
    print("Existing Projects:")
    for name in os.listdir("{0}/projects/".format(script_dir)):
        project = os.path.join("{0}/projects/".format(script_dir), name)
        if os.path.isdir(project):
            print("   "+name)
    print("\n")
    name = input("Enter project name (Can't be the same as an existing project)\nEnter 'cancel' to return to main menu\n: ")
    if os.path.exists("{0}\\projects\\{1}".format(script_dir, name)): newProject()
    if name == "cancel": mainMenu()
    os.mkdir("{0}/projects/{1}".format(script_dir, name))
    moveTools(name)
    levels = []
    levelSelect = ""
    os.system("title Level Select")
    try:
        while levelSelect != "done":
            os.system('cls||clear')
            print("Levels:\nboot\ncommon\nCommon\nCh00_Dre\nCh01_Hob\nCh02_Roa\nCh02a_Tr\nCh4_Over\nCh05_Swo\nMirkwood\nCh07_Bar\nCH08_Lak\nCh09_Sma\nCh10_Lon\nCh11_Clo\nExtras")
            print("Currently selected levels:\n"+str(levels))
            levelSelect = input("Select level, type name exactly as shown\nType 'all' to select all levels\nType a level name again to remove\nType 'done' if done selecting or 'cancel' to return to main menu\n: ")
            if levelSelect != "done":
                if levelSelect == "cancel":
                    shutil.rmtree("{0}/projects/{1}".format(script_dir, name))
                    mainMenu()
                if levelSelect == "all":
                    for level_name in os.listdir("{0}/The Hobbit(TM)/PC/".format(script_dir)):
                        level = os.path.join("{0}/The Hobbit(TM)/PC/".format(script_dir), level_name)
                        if os.path.isdir(level):
                            print("Adding {0}...".format(level_name), end="\r")
                            levels.append(level_name)
                            shutil.copytree("{0}\\The Hobbit(TM)\\PC\\{1}".format(script_dir, level_name), "{0}\\projects\\{1}\\{2}".format(script_dir, name, level_name))
                elif levelSelect == "Common":
                    levels.append("Common0")
                    print("Adding {0}...".format(levelSelect))
                    shutil.copytree("{0}\\The Hobbit(TM)\\PC\\Common0".format(script_dir), "{0}\\projects\\{1}\\Common0".format(script_dir, name))
                else:
                    if levelSelect in levels:
                        levels.remove(levelSelect)
                        print("Removing {0}...".format(levelSelect))
                        shutil.rmtree("{0}\\projects\\{1}\\{2}".format(script_dir, name, levelSelect))
                    else:
                        levels.append(levelSelect)
                        print("Adding {0}...".format(levelSelect))
                        shutil.copytree("{0}\\The Hobbit(TM)\\PC\\{1}".format(script_dir, levelSelect), "{0}\\projects\\{1}\\{2}".format(script_dir, name, levelSelect))
            else:
                pass
    except Exception as e: print(e)
    #os.chdir("{0}/projects/{1}".format(script_dir, name))
    #os.system("xbmp_to_dds.bat")
    #os.chdir(script_dir)
    print("Project successfully created")
    input("Press Enter to continue to editing...")
    loadProject(name)

def loadProject(project_name):
    os.system("title Editing Project")
    os.system('cls||clear')
    file_level_pairs = []
    try:
        for level in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
            for root, dirs, files in os.walk("{0}/projects/{1}/{2}".format(script_dir, project_name, level)):
                for file in files:
                    file_level_pair = (level, file)
                    file_level_pairs.append(file_level_pair)
    except Exception as e: print(e)
    command = ""
    global selected
    selected = []
    global current_project
    current_project = project_name
    global working_dir
    working_dir = current_project
    while True:
        command = input("\nEnter command, type 'help' for help\n: ")
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
        except AttributeError: print("Command '{}' does not exist".format(base_command))
        except Exception as e: print(e)

def exit(*none): sys.exit()

def back(*none): mainMenu()

def clear(*none): os.system('cls||clear')

def convert(args):
    if args[0] == "texture":
        if args[1] == "dds":
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("xbmp_to_dds.bat")
            os.chdir(script_dir)
        if args[1] == "xbmp":
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("dds_to_xbmp.bat")
            os.chdir(script_dir)
    if args[0] == "export":
        if args[1] == "text":
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("export_to_text.bat")
            os.chdir(script_dir)
        if args[1] == "json":
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("export_to_json.bat")
            os.chdir(script_dir)
        if args[1] == "export":
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("text_to_export.bat")
            os.system("json_to_export.bat")
            os.chdir(script_dir)
    if args[0] == "subtitle":
        if args[1] == "text":
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("subtitle_to_text.bat")
            os.chdir(script_dir)
        if args[1] == "subtitle":
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("text_to_subtitle.bat")
            os.chdir(script_dir)

def help(*none):
    try:
        with open("hmct.help", "r") as f:
            for line in f.readlines():
                print(line, sep="")
        for file in os.listdir("{0}/plugins".format(script_dir, current_project)):
            if file.endswith(".help"):
                print("--{0}--".format(file.split(".")[0]))
                os.chdir("{0}/plugins".format(script_dir))
                with open(file, "r") as f:
                    for line in f.readlines():
                        print(line, sep="")
                os.chdir(script_dir)
    except Exception as e: print(e)

def level(args):
    global working_dir
    if args[0] == "clear":
        working_dir = current_project
    elif os.path.exists("{0}/projects/{1}/{2}".format(script_dir, current_project, args[0])):
        working_dir = args[0]

def listDir(path, depth, filex):
    depth += 1
    for file in os.listdir(path):
        file_path = os.path.join(path, file)
        if os.path.isdir(file_path):
            for i in range(depth): print("-", end="")
            print(file+"/")
            listDir(file_path, depth, filex)
        elif filex != "all":
            if file.endswith(filex):
                if file in selected:
                    print("*", end="")
                    depth -= 1
                for i in range(depth): print(" ", end="")
                print(file)
        else:
            if file in selected:
                print("*", end="")
                depth -= 1
            for i in range(depth): print(" ", end="")
            print(file)

def list(args):
    try:
        if args[0] == "levels":
                for name in os.listdir("{0}/projects/{1}".format(script_dir, current_project)):
                    level = os.path.join("{0}/projects/{1}".format(script_dir, current_project), name)
                    if os.path.isdir(level):
                        print("   "+name)
        else:
            if working_dir == current_project:
                for name in os.listdir("{0}/projects/{1}".format(script_dir, current_project)):
                    if os.path.isdir("{0}/projects/{1}/{2}".format(script_dir, current_project, name)):
                        listDir("{0}/projects/{1}/{2}".format(script_dir, current_project, name), 0, args[0])
            else:
                listDir("{0}/projects/{1}/{2}".format(script_dir, current_project, working_dir), 0, args[0])
    except Exception as e: print(e)

def select(args):
    try:
        if args[0] == "clear": selected.clear()
        else:
            temp_select = args[0].split(",")
            for file in temp_select:
                selected.append(file)
    except Exception as e: print(e)

def edit(args):
    try:
        if working_dir == current_project:
            for root, dirs, files in os.walk("{0}/projects/{1}".format(script_dir, current_project)):
                for name in files:
                    if args[0] == "all": 
                        if args[1] == all or name.endswith(args[1]): os.startfile(os.path.join(root, name))
                    if args[0] == "selected":
                        if name in selected: os.startfile(os.path.join(root, name))
                    else:
                        if name == args[0]: 
                            if name == "ALLUSEDLAYERS.TXT": os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe {}".format(os.path.join(root, name))); os.chdir(script_dir)
                            if name.endswith(".RGEOM") or name.endswith(".NPCGEOM"): os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe {}".format(os.path.join(root, name))); os.chdir(script_dir)
                            else: os.startfile(os.path.join(root, name))
        else:
            for root, dirs, files in os.walk("{0}/projects/{1}/{2}".format(script_dir, current_project, working_dir)):
                for name in files:
                    if args[0] == "all": 
                        if args[1] == all or name.endswith(args[1]): os.startfile(os.path.join(root, name))
                    if args[0] == "selected":
                        if name in selected: os.startfile(os.path.join(root, name))
                    else:
                        if name == args[0]: 
                            if name == "ALLUSEDLAYERS.TXT": os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe {}".format(os.path.join(root, name))); os.chdir(script_dir)
                            if name.endswith(".RGEOM") or name.endswith(".NPCGEOM"): os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe {}".format(os.path.join(root, name))); os.chdir(script_dir)
                            else: os.startfile(os.path.join(root, name))
    except Exception as e: print(e)

def add(args):
    try:
        shutil.copytree("{0}\\The Hobbit(TM)\\PC\\{1}".format(script_dir, args[0]), "{0}\\projects\\{1}\\{2}".format(script_dir, current_project, args[0]))
    except Exception as e: print(e)

def remove(args):
    try:
        shutil.rmtree("{0}\\projects\\{1}\\{2}".format(script_dir, current_project, args[0]))
    except Exception as e: print(e)

def exportMod(project_name):
    os.system("title Export Mod")
    os.chdir("{0}/projects/{1}".format(script_dir, project_name))
    os.system("dds_to_xbmp.bat")
    os.system("text_to_export.bat")
    os.system("text_to_subtitle.bat")
    os.chdir(script_dir)
    export_type = str(input("Which format do you wish to export to? Classic(C), Development(D), or HOBM <Alpha> (H)?\n: ")).upper()
    if os.path.exists("{0}/exported mods/{1}".format(script_dir, project_name)): pass
    else: os.mkdir("{0}/exported mods/{1}".format(script_dir, project_name))
    if export_type == "C":
        for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
            level = os.path.join("{0}/projects/{1}".format(script_dir, project_name), name)
            if os.path.isdir(level):
                os.chdir("{0}/projects/{1}".format(script_dir, project_name))
                os.system("dfs.exe -pack {0} {0}.DFS".format(name))
                os.chdir(script_dir)
        for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
            if name.endswith(".000") or name.endswith(".DFS"):
                shutil.move("{0}\\projects\\{1}\\{2}".format(script_dir, project_name, name), "{0}\\exported mods\\{1}\\{2}".format(script_dir, project_name, name))
        confirm = str(input("Mod successfully exported, do you want to compress it too? Y or N\n: ")).upper()
        if confirm == "Y": shutil.make_archive(project_name, 'zip', "{0}\\exported mods\\{1}".format(script_dir, project_name))
        input("Press Enter to return to main menu...")
    elif export_type == "D":
        if input("Is {} the correct path? Y or N".format(settings["game_directory"])).upper() == "Y":
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
                level = os.path.join("{0}/projects/{1}".format(script_dir, project_name), name)
                if os.path.isdir(level):
                    os.chdir("{0}/projects/{1}".format(script_dir, project_name))
                    os.system("dfs.exe -pack {0} {0}.DFS".format(name))
                    os.chdir(script_dir)
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
                if name.endswith(".000") or name.endswith(".DFS"):
                    shutil.move("{0}\\projects\\{1}\\{2}".format(script_dir, project_name, name), os.path.join(settings["game_directory"], name))
            confirm = str(input("Mod successfully exported, would you like to launch the game to test it? Y or N\n: ")).upper()
            if confirm == "Y": os.chdir(settings["game_directory"]); os.startfile("Meridian.exe"); os.chdir(script_dir)
            else: input("Press Enter to return to main menu...")
        else: exportMod(project_name)
    elif export_type == "H":
        for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
            level = os.path.join("{0}/projects/{1}".format(script_dir, project_name), name)
            if os.path.isdir(level):
                shutil.copytree(level, "{0}\\exported mods\\{1}\\{2}".format(script_dir, project_name, name))
        for root, dirs, files in os.walk("{0}/exported mods/{1}".format(script_dir, project_name)):
            if files != []:
                for file in files:
                    full_path = os.path.join(root, file)
                    rel_path = os.path.relpath(full_path, "{0}\\exported mods\\{1}".format(script_dir, project_name))
                    if os.path.exists("{0}\\The Hobbit(TM)\\PC\\{1}".format(script_dir, rel_path)):
                        if os.path.getsize(full_path) == os.path.getsize("{0}\\The Hobbit(TM)\\PC\\{1}".format(script_dir, rel_path)):
                            if filecmp.cmp(full_path, "{0}\\The Hobbit(TM)\\PC\\{1}".format(script_dir, rel_path), shallow=False):
                                os.remove(full_path)
        with zipfile.ZipFile("{0}\\exported mods\\{1}.zip".format(script_dir, project_name), mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipped_file:
            rootlen = len("{0}\\exported mods\\{1}.zip".format(script_dir, project_name)) - 3
            for root, dirs, files in os.walk("{0}/exported mods/{1}/".format(script_dir, project_name)):
                for file in files:
                    path = os.path.join(root, file)
                    zipped_file.write(path, path[rootlen:])
        shutil.rmtree("{0}\\exported mods\\{1}".format(script_dir, project_name))
        os.rename("{0}\\exported mods\\{1}.zip".format(script_dir, project_name), "{0}\\exported mods\\{1}.hobm".format(script_dir, project_name))
        input("Press Enter to return to main menu...")
    mainMenu()

def importMod(project_path):
    os.system("title Import Mod")
    project_name = project_path.split("/")[-1]
    project_name = project_name.split(".")[0]
    with zipfile.ZipFile(project_path, 'r') as project_zip:
        project_zip.extractall("{0}/projects".format(script_dir))
    try:
        for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
            if name.endswith(".DFS") or name.endswith(".dfs"):
                os.mkdir("{0}/projects/{1}/{2}".format(script_dir, project_name, name.split(".")[0]))
                shutil.move("{0}\\projects\\{1}\\{2}".format(script_dir, project_name, name), "{0}\\projects\\{1}\\{2}\\{3}".format(script_dir, project_name, name.split(".")[0], name))
                shutil.move("{0}\\projects\\{1}\\{2}.000".format(script_dir, project_name, name.split(".")[0]), "{0}\\projects\\{1}\\{2}\\{3}.000".format(script_dir, project_name, name.split(".")[0], name.split(".")[0]))
                shutil.copy2("{0}\\tools\\dfs.exe".format(script_dir), "{0}\\projects\\{1}\\{2}\\dfs.exe".format(script_dir, project_name, name.split(".")[0]))
                os.chdir("{0}/projects/{1}/{2}".format(script_dir, project_name, name.split(".")[0]))
                os.system("dfs.exe -unpack {0}".format(name))
                os.remove("dfs.exe")
                os.remove("{0}".format(name))
                os.remove("{0}.000".format(name.split(".")[0]))
                os.chdir(script_dir)
        moveTools(project_name)
    except Exception as e: print(e)
    print("Mod successfully imported")
    input("Press Enter to continue to editing...")
    loadProject(project_name)

def moveTools(project_name):
    shutil.copy2("{0}\\tools\\dds_to_xbmp.bat".format(script_dir), "{0}\\projects\\{1}\\dds_to_xbmp.bat".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\xbmp_to_dds.bat".format(script_dir), "{0}\\projects\\{1}\\xbmp_to_dds.bat".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\xbmpconverter.exe".format(script_dir), "{0}\\projects\\{1}\\xbmpconverter.exe".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\dfs.exe".format(script_dir), "{0}\\projects\\{1}\\dfs.exe".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\exporttool.exe".format(script_dir), "{0}\\projects\\{1}\\exporttool.exe".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\export_to_text.bat".format(script_dir), "{0}\\projects\\{1}\\export_to_text.bat".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\text_to_export.bat".format(script_dir), "{0}\\projects\\{1}\\text_to_export.bat".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\json_to_export.bat".format(script_dir), "{0}\\projects\\{1}\\json_to_export.bat".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\export_to_json.bat".format(script_dir), "{0}\\projects\\{1}\\export_to_json.bat".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\rgeom2obj.exe".format(script_dir), "{0}\\projects\\{1}\\rgeom2obj.exe".format(script_dir, project_name))
    shutil.copy2("{0}\\tools\\subtitletool.exe".format(script_dir), "{0}\\projects\\{1}\\subtitletool.exe".format(script_dir, project_name))

if __name__ == '__main__':
    if os.path.exists("{}/projects".format(script_dir)): pass
    else: os.mkdir("{}/projects".format(script_dir))
    if os.path.exists("{}/exported mods".format(script_dir)): pass
    else: os.mkdir("{}/exported mods".format(script_dir))
    mainMenu()

#File types to support in the future:
#.ANIM / .CHARANIM
#.OCCDAT
#.XSC
#.TREE
#.SYM
#.FXO
#.bik