import os
import shutil
import subprocess
from zipfile import ZipFile

script_dir = os.path.dirname(os.path.abspath(__file__))

def mainMenu():
    os.system("title Main Menu")
    os.system('cls||clear')
    print("         _________ _______  _______ _________\n|\     /|\__   __/(  ____ )(  ____ \\__   __/\n| )   ( |   ) (   | (    )|| (    \/   ) (   \n| (___) |   | |   | (____)|| |         | |   \n|  ___  |   | |   |  _____)| |         | |   \n| (   ) |   | |   | (      | |         | |   \n| )   ( |   | |   | )      | (____/\   | |   \n|/     \|   )_(   |/       (_______/   )_(   ")
    print("\n         v1.2 by 09beckerboy")
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
    shutil.copy2("{0}\\xbmp_converter\\convert_dds_to_xbmp.bat".format(script_dir), "{0}\\texture packs\\{1}\\convert_dds_to_xbmp.bat".format(script_dir, name))
    shutil.copy2("{0}\\xbmp_converter\\convert_xbmp_to_dds.bat".format(script_dir), "{0}\\texture packs\\{1}\\convert_xbmp_to_dds.bat".format(script_dir, name))
    shutil.copy2("{0}\\xbmp_converter\\xbmpconverter.exe".format(script_dir), "{0}\\texture packs\\{1}\\xbmpconverter.exe".format(script_dir, name))
    shutil.copy2("{0}\\pack_dfs\\dfs.exe".format(script_dir), "{0}\\texture packs\\{1}\\dfs.exe".format(script_dir, name))
    shutil.copy2("{0}\\pack_dfs\\pack_dfs_Drag'n'Drop.bat".format(script_dir), "{0}\\texture packs\\{1}\\pack_dfs_Drag'n'Drop.bat".format(script_dir, name))
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
                        shutil.rmtree("{0}\\texture packs\\{1}\\{2}".format(script_dir, name, levelSelect))
                    else:
                        levels.append(levelSelect)
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
    os.chdir("{0}/texture packs/{1}".format(script_dir, pack_name))
    os.system("convert_xbmp_to_dds.bat")
    os.chdir(script_dir)
    os.system('cls||clear')
    command = ""
    selected = []
    while command != "exit":
        command = input("Enter command, or ? for help\n: ")
        try:
            base_command = command.split(" ")[0]
            command_arg1 = command.split(" ")[1]
            command_arg2 = command.split(" ")[2]
        except Exception as e: pass
        try:
            if base_command == "?": print("Command (arguments) : description\n\nexit : exits the tool\nback : returns back to the main menu\nlist : lists all levels in project\nview (level) : views textures in level, level name must be spelled exactly, leave blank for all levels\nopen (all/texture/level/selected) (level) : opens textures in your default program, level name must be spelled exactly, or you can type 'all' to open textures in all levels, texture name must be spelled exactly, second (level) is optional, to be used with (texture)\nselect (texture) : adds texture to selected, use view command to see changes\nadd (level) : adds a level to the pack, level name must be spelled correctly\nremove (level) : removes a level from the pack, level name must be spelled correctly")
            if base_command == "back": mainMenu()
            if base_command == "list":
                for name in os.listdir("{0}/texture packs/{1}".format(script_dir, pack_name)):
                    level = os.path.join("{0}/texture packs/{1}".format(script_dir, pack_name), name)
                    if os.path.isdir(level):
                        print("   "+name)
            if base_command == "select":
                temp_select = command_arg1.split(",")
                for i in temp_select:
                    selected.append(i)
            if base_command == "view":
                if command_arg1 == "" or command_arg1 == "all":
                    for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, pack_name)):
                        for name in files:
                            if name.endswith(".dds"):
                                if name in selected: print(" * "+name)
                                else: print("   "+name)
                else: 
                    for root, dirs, files in os.walk("{0}/texture packs/{1}/{2}".format(script_dir, pack_name, command_arg1)):
                        for name in files:
                            if name.endswith(".dds"):
                                if name in selected: print(" * "+name)
                                else: print("   "+name)
            if base_command == "add": shutil.copytree("{0}\\The Hobbit(TM)\\{1}".format(script_dir, command_arg1), "{0}\\texture packs\\{1}\\{2}".format(script_dir, pack_name, command_arg1))
            if base_command == "remove": shutil.rmtree("{0}\\texture packs\\{1}\\{2}".format(script_dir, pack_name, command_arg1))
            if base_command == "open":
                if command_arg1 == "all":
                    for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, pack_name)):
                        for name in files:
                            if name.endswith(".dds"):
                                os.startfile(os.path.join(root, name))
                if command_arg1 == "selected":
                    for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, pack_name)):
                        for name in files:
                            if name.endswith(".dds"):
                                if name in selected:
                                    os.startfile(os.path.join(root, name))
                if command_arg1.endswith(".dds"):
                    if "command_arg2" in locals():
                        for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, pack_name)):
                            for name in dirs:
                                if name == command_arg2:
                                    for root, dirs, files in os.walk("{0}/texture packs/{1}/{2}".format(script_dir, pack_name, name)):
                                        for name2 in files:
                                            if name2.endswith(".dds"):
                                                if name2 == command_arg1:
                                                    os.startfile(os.path.join(root, name2))
                    else:
                        for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, pack_name)):
                            for name in files:
                                if name.endswith(".dds"):
                                    if name == command_arg1:
                                        os.startfile(os.path.join(root, name))
                else:
                    for root, dirs, files in os.walk("{0}/texture packs/{1}".format(script_dir, pack_name)):
                        for name in dirs:
                            if name == command_arg1:
                                for root, dirs, files in os.walk("{0}/texture packs/{1}/{2}".format(script_dir, pack_name, name)):
                                    for name2 in files:
                                        if name2.endswith(".dds"):
                                            os.startfile(os.path.join(root, name2))
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
        shutil.copy2("{0}\\xbmp_converter\\convert_dds_to_xbmp.bat".format(script_dir), "{0}\\texture packs\\{1}\\convert_dds_to_xbmp.bat".format(script_dir, pack_name))
        shutil.copy2("{0}\\xbmp_converter\\convert_xbmp_to_dds.bat".format(script_dir), "{0}\\texture packs\\{1}\\convert_xbmp_to_dds.bat".format(script_dir, pack_name))
        shutil.copy2("{0}\\xbmp_converter\\xbmpconverter.exe".format(script_dir), "{0}\\texture packs\\{1}\\xbmpconverter.exe".format(script_dir, pack_name))
        shutil.copy2("{0}\\pack_dfs\\dfs.exe".format(script_dir), "{0}\\texture packs\\{1}\\dfs.exe".format(script_dir, pack_name))
        shutil.copy2("{0}\\pack_dfs\\pack_dfs_Drag'n'Drop.bat".format(script_dir), "{0}\\texture packs\\{1}\\pack_dfs_Drag'n'Drop.bat".format(script_dir, pack_name))
    except Exception as e: print(e)
    print("Pack successfully imported")
    input("Press Enter to continue to editing...")
    loadPack(pack_name)

if __name__ == '__main__':
    if os.path.exists("{}/texture packs".format(script_dir)): pass
    else: os.mkdir("{}/texture packs".format(script_dir))
    if os.path.exists("{}/exported packs".format(script_dir)): pass
    else: os.mkdir("{}/exported packs".format(script_dir))
    mainMenu()