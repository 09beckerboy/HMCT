from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from ttkwidgets import CheckboxTreeview
import os
from PIL import ImageTk, Image, ImageEnhance
import sys
import random
from functools import partial
import shutil
import json
import zipfile
import filecmp
from tkinter import filedialog
import importlib
import sv_ttk
import threading
import logging

script_dir = os.path.dirname(os.path.abspath(__file__))

# class Command:
#     def __init__(self, name, function):
#         self.name = "Default"
#         self.function = "doNothing"

def doNothing(): messagebox.showwarning(title="Nothing happened...", message="This feature is not currently implemented")

def _previewFile(x):
    console_text.delete(0, END)
    printGUI(project_tree.focus())
    if project_tree.focus().endswith(".dds"):
        preview_image = Image.open(project_tree.focus()).convert("RGBA")
        #preview_image.putalpha(ImageEnhance.Brightness(preview_image.split()[3]).enhance(1)) #Image.open(projectTree.focus()
        preview_image.putalpha(255)
        if preview_image.height >= preview_image.width: preview_image = ImageTk.PhotoImage(preview_image.resize(((preview_image.width*int(891/preview_image.height)), 891), Image.NEAREST))
        else : preview_image = ImageTk.PhotoImage(preview_image.resize((1157, (preview_image.height*int(1157/preview_image.width))), Image.NEAREST))
        #hmct_window.iconphoto(False, preview_image)
        preview_text.pack_forget()
        preview_image_canvas.pack(side=TOP, anchor=W)
        preview_image_canvas.delete('all')
        preview_image_canvas.create_image(0,0, anchor=NW, image=preview_image)
        preview_image_canvas.config(image=preview_image)
        #temp_image =  #.convert("RGBA") #Image.open(projectTree.focus()
        #preview_image = ImageTk.PhotoImage(Image.open(project_tree.focus())) #.resize(((temp_image.size[0]*int(1157/temp_image.size[0])), (temp_image.size[1]*int(891/temp_image.size[1]))), Image.NEAREST)
        #hmct_window.iconphoto(False, preview_image)
        #preview_image = ImageTk.PhotoImage(file = str(project_tree.focus()))
        #preview_image_canvas.config(preview_image, image=temp_image)
        #preview_image_canvas.delete('all')
        #preview_image_canvas.create_image(0, 0, anchor=NW, image=preview_image)
    if str(project_tree.focus()).lower().endswith(".png"):
        pass
    if str(project_tree.focus()).lower().endswith(".txt") or str(project_tree.focus()).lower().endswith(".json") or str(project_tree.focus()).lower().endswith(".bin") or str(project_tree.focus()).lower().endswith(".h"):
        preview_image_canvas.pack_forget()
        preview_text.pack(side=TOP, anchor=W, fill=BOTH)
        with open(project_tree.focus(), "r") as text_file:
            preview_text.configure(state='normal')
            preview_text.delete('1.0', END)
            for line in text_file.readlines():
                preview_text.insert('end', line)
            preview_text.configure(state='disabled')
    # else:
    #     preview_image = Image.open("{}/assets/no_preview.png".format(script_dir)).convert("RGBA") #Image.open(projectTree.focus()
    #     preview_image = ImageTk.PhotoImage(preview_image.resize(((preview_image.size[0]*int(1157/preview_image.size[0])), (preview_image.size[1]*int(891/preview_image.size[1]))), Image.NEAREST))
    #     hmct_window.iconphoto(False, preview_image)
    #     preview_image_canvas.config(image=preview_image)
    #     preview_image_canvas.delete('all')
    #     preview_image_canvas.create_image(0,0, anchor=NW, image=preview_image)

def _makeProjectTree(path, depth, parent, filter):
    depth += 1
    for file in os.listdir(path):
        file_path = str(os.path.join(path, file))
        if os.path.isdir(file_path):
            project_tree.insert(parent, "0", file_path, text = file + "/")
            project_tree.move(file_path, parent, "end")
            t1 = threading.Thread(target=_makeProjectTree, args=(file_path, depth, file_path, filter,))
            t1.start()
        elif depth != 1:
            if filter == "*" or str(filter).lower() in str(file).lower() or str(file).lower().endswith(str(filter).lower()):
                project_tree.insert(parent, "0", file_path, text = file)
                project_tree.move(file_path, parent, "end")
                values = list(filter_dropdown["values"])
                extension = ["." + str(file).split(".")[-1].upper()]
                if extension[0] not in values: filter_dropdown["values"] = values + extension

def refreshProjectTree(filter):
    t1 = threading.Thread(target=_makeProjectTree, args=("{0}/projects/{1}".format(script_dir, current_project), 0, current_project, filter,))
    t1.start()

def _moveTools(project_name):
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

def _loadProject(project_name):
    global selected
    selected = []
    global current_project
    current_project = project_name
    global working_dir
    working_dir = current_project
    global project_file_extensions
    project_file_extensions = []
    global project_config
    project_config= {}
    project_tree.delete(*project_tree.get_children())
    project_tree.insert("", "0", project_name, text=project_name + "/")
    filter_dropdown["values"] = ("All")
    with open("{0}/projects/{1}/config.json".format(script_dir, project_name), "r") as read_file:
        project_config = json.load(read_file)
    printGUI('Loaded project: "{}"'.format(project_name))
    refreshProjectTree("*")
    hmct_window.title("HMCT v2.0 | {0} | {1} | {2}".format(project_config["texture_state"], project_config["export_state"], project_config["subtitle_state"]))

def _newProject():
    new_project_window = Toplevel(hmct_window)
    new_project_window.lift(hmct_window)
    new_project_window.geometry("350x650")
    new_project_window.title("New Project")
    new_project_window.iconphoto(False, PhotoImage(file="{}/assets/hmct_icon.png".format(script_dir)))
    Label(new_project_window, text="Project Name").pack(side=TOP)
    project_name = Entry(new_project_window)
    project_name.focus_set()
    project_name.pack(side=TOP)
    Label(new_project_window, text="Project Level(s)").pack(side=TOP)
    levels = []
    level_checklist = {}
    for level in os.listdir("{0}\\The Hobbit(TM)\\PC\\".format(script_dir)):
        levels.append(str(level))
        level_checklist.update({level: IntVar(value=0)})
        Checkbutton(new_project_window, variable=level_checklist[level], text=level).pack(side=TOP)
    def selectButton():
        if os.path.exists("{0}\\projects\\{1}".format(script_dir, project_name.get())): messagebox.showerror("You silly goose!", "You can't have a project with the same name as an existing one!")
        else:
            for level in level_checklist.keys():
                if level_checklist[level].get() == 1:
                    shutil.copytree("{0}\\The Hobbit(TM)\\PC\\{1}".format(script_dir, level), "{0}\\projects\\{1}\\{2}".format(script_dir, project_name.get(), level))
            
            new_project_config = {"texture_state": "xbmp", "export_state": "export", "subtitle_state": "bin"}
            json_object = json.dumps(new_project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, project_name.get()), "w") as outfile:
                outfile.write(json_object)
            t1 = threading.Thread(target=_moveTools, args=(project_name.get(),))
            t1.start()
            #_moveTools(project_name.get())
            refreshAllMenus()
            printGUI('Created project: "{}"'.format(project_name.get()))
            _loadProject(project_name.get())
            new_project_window.destroy()
    Button(new_project_window, text="Create Project", command=selectButton).pack(side=TOP)
    Label(new_project_window, text="May take a while, just be patient").pack(side=TOP)

def _deleteProject(project): 
    if messagebox.askquestion("Don't be a Silly Goose!", 'Are you sure you want to delete the project: "{}"?'.format(project)) == "yes":
        shutil.rmtree("{0}\\projects\\{1}".format(script_dir, project))
        refreshAllMenus()
        project_tree.delete(*project_tree.get_children())
        printGUI('Deleted project: "{}"'.format(project))
        hmct_window.title("HMCT v2.0 | {}".format(splash_text))

def _importMod():
    project_path = filedialog.askopenfilename(initialdir = "\\", title = "Select a Mod to Import", filetypes = (("Zipped Mod", "*.zip"), ("HOBM Mod", "*.hobm")))
    printGUI(project_path)
    if project_path.endswith(".zip"):
        project_name = project_path.split("/")[-1].split(".")[0]
        printGUI(project_name)
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
            t1 = threading.Thread(target=_moveTools, args=(project_name,))
            t1.start()
            #_moveTools(project_name)
        except Exception as e: printGUI(e)
        refreshAllMenus()
        printGUI('Imported mod: "{}"'.format(project_name))
        _loadProject(project_name)

def _exportMod(project_name):
    os.chdir("{0}/projects/{1}".format(script_dir, project_name))
    os.system("dds_to_xbmp.bat")
    os.system("text_to_export.bat")
    os.system("text_to_subtitle.bat")
    os.chdir(script_dir)
    if os.path.exists("{0}/exported mods/{1}".format(script_dir, project_name)): pass
    else: os.mkdir("{0}/exported mods/{1}".format(script_dir, project_name))
    export_mod_window = Toplevel(hmct_window)
    export_mod_window.lift(hmct_window)
    export_mod_window.geometry("650x350")
    export_mod_window.title("Export Mod")
    export_mod_window.iconphoto(False, PhotoImage(file="{}/assets/hmct_icon.png".format(script_dir)))
    export_type = IntVar()
    Label(export_mod_window, text="Select format to export to:").pack(side=TOP, anchor=W)
    export_options_frame = Frame(export_mod_window, bd=5, height=75, width=650)
    export_options_frame.pack_propagate(False)
    compress = BooleanVar()
    compress_button = Checkbutton(export_options_frame, variable=compress, text="Compress after export")
    game_dir = Entry(export_options_frame)
    def browse(): game_dir.delete(0,END); game_dir.insert(0,filedialog.askdirectory(initialdir = "/", title = "Select the Game Directory")); export_mod_window.lift(hmct_window)
    browse_files = Button(export_options_frame, text = "Browse", command = browse)
    launch_game = BooleanVar()
    launch_game_button = Checkbutton(export_options_frame, variable=launch_game, text="Launch game after export")
    def select():
        if export_type.get() == 1:
            game_dir.pack_forget()
            browse_files.pack_forget()
            launch_game_button.pack_forget()
            compress_button.pack(side=LEFT, anchor=N)
            export_options_frame.update()
        if export_type.get() == 2:
            compress_button.pack_forget()
            game_dir.delete(0,END)
            game_dir.insert(0,settings["game_directory"])
            game_dir.pack(side=TOP, anchor=W, fill=X)
            browse_files.pack(side=TOP, anchor=W)
            launch_game_button.pack(side=TOP, anchor=W)
            export_options_frame.update()
        if export_type.get() == 3:
            compress_button.pack_forget()
            game_dir.pack_forget()
            browse_files.pack_forget()
            launch_game_button.pack_forget()
            export_options_frame.update()
    classic_button = Radiobutton(export_mod_window, text="Classic", variable=export_type, value=1, command=select).pack(anchor=W, side=TOP)
    dev_button = Radiobutton(export_mod_window, text="Development", variable=export_type, value=2, command=select).pack(anchor=W, side=TOP)
    hobm_button = Radiobutton(export_mod_window, text="HOBM (Alpha)", variable=export_type, value=3, command=select).pack(anchor=W, side=TOP)
    export_options_frame.pack(side=TOP, fill=BOTH)
    def export():
        if export_type.get() == 1:
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
                if name != "Common-" or name != "Extras":
                    level = os.path.join("{0}/projects/{1}".format(script_dir, project_name), name)
                    if os.path.isdir(level):
                        os.chdir("{0}/projects/{1}".format(script_dir, project_name))
                        os.system("dfs.exe -pack {0} {0}.DFS".format(name))
                        os.chdir(script_dir)
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
                if name == "Common-": shutil.move("{0}\\projects\\{1}\\{2}".format(script_dir, project_name, name), "{0}\\exported mods\\{1}\\Common".format(script_dir, project_name))
                if name == "Extras":
                    for item in os.listdir("{0}/projects/{1}/Extras"): shutil.move("{0}\\projects\\{1}\\Extras\\{2}".format(script_dir, project_name, item), "{0}\\exported mods\\{1}\\{2}".format(script_dir, project_name, item))
                if name.endswith(".000") or name.endswith(".DFS"):
                    shutil.move("{0}\\projects\\{1}\\{2}".format(script_dir, project_name, name), "{0}\\exported mods\\{1}\\{2}".format(script_dir, project_name, name))
            if compress.get() == 1: shutil.make_archive(project_name, 'zip', "{0}\\exported mods\\{1}".format(script_dir, project_name))
        elif export_type.get() == 2:
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
                if name != "Common-" or name != "Extras":
                    level = os.path.join("{0}/projects/{1}".format(script_dir, project_name), name)
                    if os.path.isdir(level):
                        os.chdir("{0}/projects/{1}".format(script_dir, project_name))
                        os.system("dfs.exe -pack {0} {0}.DFS".format(name))
                        os.chdir(script_dir)
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
                if name == "Common-": shutil.move("{0}\\projects\\{1}\\{2}".format(script_dir, project_name, name), os.path.join(settings["game_directory"], "Common"))
                if name == "Extras":
                    for item in os.listdir("{0}/projects/{1}/Extras"): shutil.move("{0}\\projects\\{1}\\Extras\\{2}".format(script_dir, project_name, item), os.path.join(settings["game_directory"], item))
                if name.endswith(".000") or name.endswith(".DFS"):
                    shutil.move("{0}\\projects\\{1}\\{2}".format(script_dir, project_name, name), os.path.join(settings["game_directory"], name))
            if launch_game.get() == 1: os.chdir(settings["game_directory"]); os.startfile("Meridian.exe"); os.chdir(script_dir)
        elif export_type.get() == 3:
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
    export_button = Button(export_mod_window, text="Export", command=export).pack(anchor=W, side=TOP)

def convertXBMPDDS():
    def convert():
        if project_config["texture_state"] == "xbmp":
            printGUI("Converting textures to DDS...")
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("xbmp_to_dds.bat"); os.chdir(script_dir)
            project_tree.delete(*project_tree.get_children())
            project_tree.insert("", "0", current_project, text=current_project + "/")
            filter_dropdown["values"] = ("All")
            refreshProjectTree("*")
            project_config["texture_state"] = "dds"
            json_object = json.dumps(project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, current_project), "w") as outfile:
                outfile.write(json_object)
            printGUI("Converted textures to DDS")
        elif project_config["texture_state"] == "dds":
            printGUI("Converting textures to XBMP...")
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("dds_to_xbmp.bat"); os.chdir(script_dir)
            project_tree.delete(*project_tree.get_children())
            project_tree.insert("", "0", current_project, text=current_project + "/")
            filter_dropdown["values"] = ("All")
            refreshProjectTree("*")
            project_config["texture_state"] = "xbmp"
            json_object = json.dumps(project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, current_project), "w") as outfile:
                outfile.write(json_object)
            printGUI("Converted textures to XBMP")
        hmct_window.title("HMCT v2.0 | {0} | {1} | {2}".format(project_config["texture_state"], project_config["export_state"], project_config["subtitle_state"]))
    t1 = threading.Thread(target=convert)
    t1.start()

def convertXBMPPNG(): doNothing()

def convertEXPORTTXT():
    def convert():
        if project_config["export_state"] == "export":
            printGUI("Converting export files to TXT...")
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("export_to_text.bat"); os.chdir(script_dir)
            project_tree.delete(*project_tree.get_children())
            project_tree.insert("", "0", current_project, text=current_project + "/")
            filter_dropdown["values"] = ("All")
            refreshProjectTree("*")
            project_config["export_state"] = "txt"
            json_object = json.dumps(project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, current_project), "w") as outfile:
                outfile.write(json_object)
            printGUI("Converted export files to TXT")
        elif project_config["export_state"] == "txt":
            printGUI("Converting export files to EXPORT...")
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("text_to_export.bat"); os.chdir(script_dir)
            project_tree.delete(*project_tree.get_children())
            project_tree.insert("", "0", current_project, text=current_project + "/")
            filter_dropdown["values"] = ("All")
            refreshProjectTree("*")
            project_config["export_state"] = "export"
            json_object = json.dumps(project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, current_project), "w") as outfile:
                outfile.write(json_object)
            printGUI("Converted export files to EXPORT")
        hmct_window.title("HMCT v2.0 | {0} | {1} | {2}".format(project_config["texture_state"], project_config["export_state"], project_config["subtitle_state"]))
    t1 = threading.Thread(target=convert)
    t1.start()

def convertEXPORTJSON():
    def convert():
        if project_config["export_state"] == "export":
            printGUI("Converting export files to JSON...")
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("export_to_json.bat"); os.chdir(script_dir)
            project_tree.delete(*project_tree.get_children())
            project_tree.insert("", "0", current_project, text=current_project + "/")
            filter_dropdown["values"] = ("All")
            refreshProjectTree("*")
            project_config["export_state"] = "json"
            json_object = json.dumps(project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, current_project), "w") as outfile:
                outfile.write(json_object)
            printGUI("Converted export files to JSON")
        elif project_config["export_state"] == "json":
            printGUI("Converting export files to EXPORT...")
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("json_to_export.bat"); os.chdir(script_dir)
            project_tree.delete(*project_tree.get_children())
            project_tree.insert("", "0", current_project, text=current_project + "/")
            filter_dropdown["values"] = ("All")
            refreshProjectTree("*")
            project_config["export_state"] = "export"
            json_object = json.dumps(project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, current_project), "w") as outfile:
                outfile.write(json_object)
            printGUI("Converted export files to EXPORT")
        hmct_window.title("HMCT v2.0 | {0} | {1} | {2}".format(project_config["texture_state"], project_config["export_state"], project_config["subtitle_state"]))
    t1 = threading.Thread(target=convert)
    t1.start()

def convertSUBTITLETXT():
    def convert():
        if project_config["subtitle_state"] == "bin":
            printGUI("Converting subtitle files to TXT...")
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("subtitle_to_text.bat"); os.chdir(script_dir)
            project_tree.delete(*project_tree.get_children())
            project_tree.insert("", "0", current_project, text=current_project + "/")
            filter_dropdown["values"] = ("All")
            refreshProjectTree("*")
            project_config["subtitle_state"] = "txt"
            json_object = json.dumps(project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, current_project), "w") as outfile:
                outfile.write(json_object)
            printGUI("Converted subtitle files to TXT")
        elif project_config["subtitle_state"] == "txt":
            printGUI("Converting subtitle files to BIN...")
            os.chdir("{0}/projects/{1}".format(script_dir, current_project))
            os.system("text_to_subtitle.bat"); os.chdir(script_dir)
            project_tree.delete(*project_tree.get_children())
            project_tree.insert("", "0", current_project, text=current_project + "/")
            filter_dropdown["values"] = ("All")
            refreshProjectTree("*")
            project_config["subtitle_state"] = "bin"
            json_object = json.dumps(project_config, indent=4)
            with open("{0}/projects/{1}/config.json".format(script_dir, current_project), "w") as outfile:
                outfile.write(json_object)
            printGUI("Converted subtitle files to BIN")
        hmct_window.title("HMCT v2.0 | {0} | {1} | {2}".format(project_config["texture_state"], project_config["export_state"], project_config["subtitle_state"]))
    t1 = threading.Thread(target=convert)
    t1.start()

def convertAUDIOPKG():
    doNothing()


def _addLevel():
    add_level_window = Toplevel(hmct_window)
    add_level_window.lift(hmct_window)
    add_level_window.geometry("350x650")
    add_level_window.title("Add Level(s)")
    add_level_window.iconphoto(False, PhotoImage(file="{}/assets/hmct_icon.png".format(script_dir)))
    Label(add_level_window, text="Select Level(s) to Add").pack(side=TOP)
    levels = []
    level_checklist = {}
    for level in os.listdir("{0}\\The Hobbit(TM)\\PC\\".format(script_dir)):
        levels.append(str(level))
        level_checklist.update({level: IntVar(value=0)})
        Checkbutton(add_level_window, variable=level_checklist[level], text=level).pack(side=TOP)
    def selectButton():
        for level in level_checklist.keys():
            if level_checklist[level].get() == 1:
                if not os.path.exists("{0}\\projects\\{1}\\{2}".format(script_dir, current_project, level)):
                    shutil.copytree("{0}\\The Hobbit(TM)\\PC\\{1}".format(script_dir, level), "{0}\\projects\\{1}\\{2}".format(script_dir, current_project, level))
        project_tree.delete(*project_tree.get_children())
        project_tree.insert("", "0", current_project, text=current_project + "/")
        filter_dropdown["values"] = ("All"); 
        refreshProjectTree("*")
    Button(add_level_window, text="Add selected level(s)", command=selectButton).pack(side=TOP)

def _removeLevel():
    delete_level_window = Toplevel(hmct_window)
    delete_level_window.lift(hmct_window)
    delete_level_window.geometry("350x650")
    delete_level_window.title("Remove Level(s)")
    delete_level_window.iconphoto(False, PhotoImage(file="{}/assets/hmct_icon.png".format(script_dir)))
    Label(delete_level_window, text="Select Level(s) to Remove").pack(side=TOP)
    levels = []
    level_checklist = {}
    for level in os.listdir("{0}\\The Hobbit(TM)\\PC\\".format(script_dir)):
        levels.append(str(level))
        level_checklist.update({level: IntVar(value=0)})
        Checkbutton(delete_level_window, variable=level_checklist[level], text=level).pack(side=TOP)
    def selectButton():
        for level in level_checklist.keys():
            if level_checklist[level].get() == 1:
                if os.path.exists("{0}\\projects\\{1}\\{2}".format(script_dir, current_project, level)):
                    shutil.rmtree("{0}\\projects\\{1}\\{2}".format(script_dir, current_project, level))
        project_tree.delete(*project_tree.get_children())
        project_tree.insert("", "0", current_project, text=current_project + "/")
        filter_dropdown["values"] = ("All"); 
        refreshProjectTree("*")
    Button(delete_level_window, text="Remove selected level(s)", command=selectButton).pack(side=TOP)

def openFile():
    file = str(project_tree.focus())
    if file.endswith("ALLUSEDLAYERS.TXT"): os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe {}".format(file)); os.chdir(script_dir)
    if file.endswith(".RGEOM") or file.endswith(".NPCGEOM"): os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe {}".format(file)); os.chdir(script_dir)
    else: os.startfile(file)

def openSelected(): 
    for file in project_tree.get_checked():
        if not os.path.isdir(file):
            if file.endswith("ALLUSEDLAYERS.TXT"): os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe {}".format(file)); os.chdir(script_dir)
            if file.endswith(".RGEOM") or file.endswith(".NPCGEOM"): os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe {}".format(file)); os.chdir(script_dir)
            else: os.startfile(file)

def printGUI(output): 
    console_text.delete(0, END)
    print(output)

def expandTree():
    def expand(parent): 
        project_tree.item(parent, open=True)
        for child in project_tree.get_children(parent):
            expand(child)
    try: expand(current_project)
    except Exception: pass

def collapseTree():
    def collapse(parent):
        project_tree.item(parent, open=False)
        for child in project_tree.get_children(parent):
            collapseTree(child)
    try: collapse(current_project)
    except Exception: pass

def _searchTree():
    try:
        project_tree.delete(*project_tree.get_children())
        project_tree.insert("", "0", current_project, text=current_project + "/")
        filter_dropdown["values"] = ("All"); 
        refreshProjectTree(str(search_box.get()))
    except Exception: pass

def _filterTree(*none):
    try:
        project_tree.delete(*project_tree.get_children())
        project_tree.insert("", "0", current_project, text=current_project + "/")
        if str(filter_dropdown.get()).lower() == "all": filter_dropdown["values"] = ("All"); refreshProjectTree("*")
        else: filter_dropdown["values"] = ("All"); refreshProjectTree(str(filter_dropdown.get()))
    except Exception: pass

def refreshAllMenus():
    load_menu.delete(0, "end")
    for name in os.listdir("{0}/projects/".format(script_dir)):
        pack = os.path.join("{0}/projects/".format(script_dir), name)
        if os.path.isdir(pack):
            load_menu.add_command(label=name, command=partial(_loadProject, name))
    
    delete_menu.delete(0, "end")
    for name in os.listdir("{0}/projects/".format(script_dir)):
        pack = os.path.join("{0}/projects/".format(script_dir), name)
        if os.path.isdir(pack):
            delete_menu.add_command(label=name, command=partial(_deleteProject, name))

    export_menu.delete(0, "end")
    for name in os.listdir("{0}/projects/".format(script_dir)):
        project = os.path.join("{0}/projects/".format(script_dir), name)
        if os.path.isdir(project):
            export_menu.add_command(label=name, command=partial(_exportMod, name))

def _exitTool(): sys.exit()

def openRGeomView(): os.chdir("{}/tools".format(script_dir)); os.system("rgeomview.exe"); os.chdir(script_dir)

def openGlobalsEditor(): os.chdir("{}/tools".format(script_dir)); os.system("globals-editor.exe"); os.chdir(script_dir)

def openSettingsWindow():
    printGUI(bool(settings["debug_mode"]))
    settings_window = Toplevel(hmct_window)
    settings_window.lift(hmct_window)
    settings_window.geometry("500x400")
    settings_window.title("Settings")
    settings_window.iconphoto(False, PhotoImage(file="{}/assets/hmct_icon.png".format(script_dir)))
    settings_frame = Frame(settings_window, bd=5, height=150, width=500)
    settings_frame.pack_propagate(False)
    settings_frame.pack(side=TOP, anchor=W)
    game_dir = Entry(settings_frame)
    game_dir.delete(0,END)
    game_dir.insert(0, settings["game_directory"])
    game_dir.pack(side=TOP, anchor=W, fill=X)
    def browse(): game_dir.delete(0,END); game_dir.insert(0,filedialog.askdirectory(initialdir = "/", title = "Select the Game Directory")); settings_window.lift(hmct_window)
    Button(settings_frame, text="Browse", command=browse).pack(side=TOP, anchor=W)
    # debug_mode_enabled = BooleanVar() #value=eval(str(settings["debug_mode"]))
    # debug_mode = Checkbutton(settings_frame, variable=debug_mode_enabled, text="Debug Mode")
    # debug_mode.pack(side=TOP, anchor=W)
    def saveSettings():
        settings["game_directory"] = game_dir.get()
        json_object = json.dumps(settings, indent=4)
        with open("settings.json", "w") as outfile:
            outfile.write(json_object)
        messagebox.showinfo(title="Settings Saved!", message="Settings saved successfully")
        settings_window.lift(hmct_window)
    Button(settings_window, text="Save", command=saveSettings).pack(side=TOP, anchor=W)

def openHelpWindow():
    help_window = Toplevel(hmct_window)
    help_window.lift(hmct_window)
    help_window.geometry("400x400")
    help_window.title("Help")
    help_window.iconphoto(False, PhotoImage(file="{}/assets/hmct_icon.png".format(script_dir)))
    Label(help_window, text="Made by 09beckerboy\nRGeomView made by Modera\nGlobals Editor made by king174rus and Mr_Kliff").pack(side=LEFT, anchor=N)

# def _importPlugins():
#     for file in os.listdir("{0}/plugins".format(script_dir)):
#         if file.endswith(".py"):
#             plugin = importlib.import_module(file.split(".")[0])
#             if "__all__" in plugin.__dict__:
#                 names = plugin.__dict__["__all__"]
#             else:
#                 names = [x for x in plugin.__dict__ if not x.startswith("_")]
#             globals().update({k: getattr(plugin, k) for k in names})
#             # if os.path.exists("{0}/plugins/{1}.runtime".format(script_dir, file.split(".")[0])):
#             #     exec(open("{0}/plugins/{1}".format(script_dir, file)).read())
#             plugin_menu = Menu(plugins_menu, tearoff=0)
#             plugins_menu.add_cascade(label=file.split(".")[0], menu=plugin_menu)
#             for x in plugin.__dict__:
#                 if not x.startswith("_"):
#                     plugin_menu.add_command(label=x, command=x)

if __name__ == '__main__':
    #sys.path.append("{0}/plugins".format(script_dir))
    
    logging.basicConfig(filename='latest.log', level=logging.DEBUG)

    splashes = []
    with open("splashes.txt", "r") as f:
        for line in f.readlines():
            splashes.append(line[:-1])
    splash_text = random.choice(splashes)

    with open("settings.json", "r") as read_file:
        settings = json.load(read_file)

    #Set up window
    hmct_window = Tk()  
    hmct_window.title("HMCT v2.0 | {}".format(splash_text))
    hmct_window.iconphoto(False, PhotoImage(file="{}/assets/hmct_icon.png".format(script_dir)))
    hmct_window.geometry("1800x1000")

    #Set up console thingy
    console_frame = Frame(hmct_window, height=20, width=1800, relief=SUNKEN)
    console_frame.pack(side=BOTTOM, fill=X, padx=(5,5))
    console_frame.pack_propagate(False)
    console_text = Entry(console_frame)
    console_text.pack(fill=BOTH)
    def redirector(inputStr):console_text.insert(INSERT, inputStr)
    sys.stdout.write = redirector

    printGUI("Welcome to HMCT!")

    #Set up top bar
    top_bar = Frame(hmct_window, bd=5, height=75, width=1800)
    top_bar.pack(side=TOP, fill=X)
    top_bar.pack_propagate(False)
    open_image = ImageTk.PhotoImage(Image.open("{}/assets/open.png".format(script_dir)).convert("RGBA"))
    open_button = Button(top_bar, text="Open", font=("Segoe UI", 11), image=open_image, compound=LEFT, command=openFile, height=75, width=150)
    open_button.pack(side=RIGHT, padx=(0,5))
    #open_with_image = ImageTk.PhotoImage(Image.open("{}/assets/open_with.png".format(script_dir)).convert("RGBA"))
    #open_with_button = Button(top_bar, text="Open With...", font=("Segoe UI", 11), image=open_with_image, compound=LEFT, command=doNothing, height=75, width=150)
    #open_with_button.pack(side=RIGHT, padx=(0,5))
    open_selected_image = ImageTk.PhotoImage(Image.open("{}/assets/open_selected.png".format(script_dir)).convert("RGBA"))
    open_selected_button = Button(top_bar, text="Open Selected", font=("Segoe UI", 11), image=open_selected_image, compound=LEFT, command=openSelected, height=75, width=150)
    open_selected_button.pack(side=RIGHT, padx=(0,5))
    #open_selected_with_image = ImageTk.PhotoImage(Image.open("{}/assets/open_selected_with.png".format(script_dir)).convert("RGBA"))
    #open_selected_with_button = Button(top_bar, text="Open Selected With...", font=("Segoe UI", 11), image=open_selected_with_image, compound=LEFT, command=doNothing, height=75, width=170)
    #open_selected_with_button.pack(side=RIGHT, padx=(0,5))
    add_level_image = ImageTk.PhotoImage(Image.open("{}/assets/add_level.png".format(script_dir)).convert("RGBA"))
    add_level_button = Button(top_bar, text="Add Level", font=("Segoe UI", 11), image=add_level_image, compound=LEFT, command=_addLevel, height=75, width=150)
    add_level_button.pack(side=LEFT, padx=(5,0))
    delete_level_image = ImageTk.PhotoImage(Image.open("{}/assets/delete_level.png".format(script_dir)).convert("RGBA"))
    delete_level_button = Button(top_bar, text="Remove Level", font=("Segoe UI", 11), image=delete_level_image, compound=LEFT, command=_removeLevel, height=75, width=150)
    delete_level_button.pack(side=LEFT, padx=(5,0))

    #Set up mod file structure window
    file_window = Frame(hmct_window, bd=5, width=500, relief=SUNKEN)
    file_window.pack(side=LEFT, fill=Y, padx=(5,0), pady=(0,0))
    ttk.Label(file_window, text ="Project Files").pack(side=TOP)
    file_window_top = Frame(file_window)
    file_window_top.pack(side=TOP)

    expand_tree_button = Button(file_window_top, text="↓", command=partial(expandTree)).pack(side=LEFT)
    collapse_tree_button = Button(file_window_top, text="↑", command=partial(collapseTree)).pack(side=LEFT)
    search_box = Entry(file_window_top)
    search_box.pack(side=LEFT)

    project_tree = CheckboxTreeview(file_window)
    search_button = Button(file_window_top, text="Search", command=_searchTree).pack(side=LEFT, padx=(0, 50))
    filter_option = StringVar()
    filter_option = "All"
    filter_dropdown = ttk.Combobox(file_window_top, textvariable=filter_option)
    filter_dropdown.bind("<<ComboboxSelected>>", _filterTree)
    filter_dropdown.pack(side=RIGHT)
    filter_dropdown["values"] = ("All")

    #Set up file tree
    project_tree.pack(side=LEFT, fill=BOTH)  
    project_tree.column("#0", minwidth=0, width=400, stretch=NO)
    project_tree.bind('<Double-1>', _previewFile)

    #Set up file preview window
    preview_frame = Frame(hmct_window, bd=5, relief=SUNKEN, height=1000, width=1285)
    #preview_frame.pack_propagate(False)
    preview_frame.pack(side=TOP, fill=BOTH, padx=(15,5), pady=(0,0))
    ttk.Label(preview_frame, text ="File Preview").pack(side=TOP, fill=Y)

    preview_image_canvas = Canvas(preview_frame, height=990, width=1285)
    #preview_image_canvas.pack(side=TOP, anchor=W)
    # preview_image = Image.open("{}/assets/no_preview.png".format(script_dir)).convert("RGBA")
    # preview_image = ImageTk.PhotoImage(preview_image.resize(((preview_image.size[0]*int(1157/preview_image.size[0])), (preview_image.size[1]*int(891/preview_image.size[1]))), Image.NEAREST))
    # preview_image = preview_image_canvas.create_image(0,0, anchor=NW, image=preview_image)

    preview_text = Text(preview_frame, state='disabled', width=1285, height=1000)

    menu_bar = Menu(hmct_window)

    project_menu = Menu(menu_bar, tearoff=0)
    project_menu.add_command(label="New Project", command=_newProject)
    load_menu = Menu(project_menu, tearoff=0)
    delete_menu = Menu(project_menu, tearoff=0)
    export_menu = Menu(project_menu, tearoff=0)

    refreshAllMenus()
    
    project_menu.add_cascade(label="Load Project", menu=load_menu)
    project_menu.add_cascade(label="Delete Project", menu=delete_menu)
    project_menu.add_separator()
    project_menu.add_command(label="Import Mod", command=_importMod)
    project_menu.add_cascade(label="Export Mod", menu=export_menu)
    project_menu.add_separator()
    project_menu.add_command(label="Exit", command=_exitTool)
    menu_bar.add_cascade(label="Project", menu=project_menu)

    tools_menu = Menu(menu_bar, tearoff=0)
    convert_menu = Menu(tools_menu, tearoff=0)
    convert_menu.add_command(label="XBMP <-> DDS", command=convertXBMPDDS)
    #convert_menu.add_command(label="XBMP <-> PNG", command=convertXBMPPNG)
    convert_menu.add_separator()
    convert_menu.add_command(label="EXPORT <-> TXT", command=convertEXPORTTXT)
    convert_menu.add_command(label="EXPORT <-> JSON", command=convertEXPORTJSON)
    convert_menu.add_separator()
    convert_menu.add_command(label="SUBTITLE <-> TXT", command=convertSUBTITLETXT)
    convert_menu.add_separator()
    convert_menu.add_command(label="AUDIOPKG <-> AUDIO", command=convertAUDIOPKG)
    tools_menu.add_cascade(label="Convert", menu=convert_menu)
    tools_menu.add_separator()
    tools_menu.add_command(label="RGeomView", command=openRGeomView)
    tools_menu.add_command(label="Globals Editor", command=openGlobalsEditor)
    menu_bar.add_cascade(label="Tools", menu=tools_menu)

    plugins_menu = Menu(menu_bar, tearoff=0)
    menu_bar.add_cascade(label="Plugins", menu=plugins_menu)

    menu_bar.add_command(label="Settings", command=openSettingsWindow)

    menu_bar.add_command(label="Help", command=openHelpWindow)

    #_importPlugins()

    #Load project
    #sv_ttk.set_theme("dark")
    hmct_window.config(menu=menu_bar)
    hmct_window.state("zoomed")
    hmct_window.mainloop()

#TODO IMPORTANT
#Audio Conversion
#Image preview + PNG conversion
#Keep tree state/filters in settings

#TODO CLEANUP
#Get rid of bad comments
#Make good comments
#Add logging statements

#TODO FEATURE CREEP
#Plugins
#Parser
#Open game in blender
#Sync all copies of files
#File management (create, delete)