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

script_dir = os.path.dirname(os.path.abspath(__file__))

splashes = []
#Import splashes
with open("splashes.txt", "r") as f:
    for line in f.readlines():
        splashes.append(line[:-1])
splash_text = random.choice(splashes)

#Import settings
with open("settings.json", "r") as read_file:
    settings = json.load(read_file)

def doNothing(): messagebox.showwarning(title="Nothing happened...", message="This feature is not currently implemented")

#Load file to preview
def previewFile(x):
    console_text.delete(0, END)
    printGUI(project_tree.focus())
    if project_tree.focus().endswith(".dds"):
        preview_image = Image.open(project_tree.focus()).convert("RGBA") #Image.open(projectTree.focus()
        preview_image = ImageTk.PhotoImage(preview_image.resize(((preview_image.size[0]*int(1157/preview_image.size[0])), (preview_image.size[1]*int(891/preview_image.size[1]))), Image.NEAREST))
        #app.iconphoto(False, preview_image)
        #image_canvas.config(image=preview_image)
        image_canvas.delete('all')
        image_canvas.create_image(0,0, anchor=NW, image=preview_image)
    if project_tree.focus().endswith(".png"):
        temp_image = Image.open(project_tree.focus()).convert("RGBA") #Image.open(projectTree.focus()
        temp_image = ImageTk.PhotoImage(temp_image.resize(((temp_image.size[0]*int(1157/temp_image.size[0])), (temp_image.size[1]*int(891/temp_image.size[1]))), Image.NEAREST))
        #app.iconphoto(False, preview_image)
        image_canvas.config(preview_image, image=temp_image)
        #image_canvas.delete('all')
        #image_canvas.create_image(0,0, anchor=NW, image=preview_image)
    if project_tree.focus().endswith(".txt"):
        pass
    else:
        preview_image = Image.open("{}/assets/no_preview.png".format(script_dir)).convert("RGBA") #Image.open(projectTree.focus()
        preview_image = ImageTk.PhotoImage(preview_image.resize(((preview_image.size[0]*int(1157/preview_image.size[0])), (preview_image.size[1]*int(891/preview_image.size[1]))), Image.NEAREST))
        #app.iconphoto(False, preview_image)
        #image_canvas.config(image=preview_image)
        image_canvas.delete('all')
        image_canvas.create_image(0,0, anchor=NW, image=preview_image)

#Build file tree
def makeProjectTree(path, depth, parent):
    depth += 1
    for file in os.listdir(path):
        file_path = str(os.path.join(path, file))
        if os.path.isdir(file_path):
            project_tree.insert(parent, "0", file_path, text = file)
            project_tree.move(file_path, parent, "end")
            makeProjectTree(file_path, depth, file_path)
        else:
            project_tree.insert(parent, "0", file_path, text = file)
            project_tree.move(file_path, parent, "end")

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

def loadProject(project_name):
    #file_level_pairs = []
    #try:
        #for level in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
            #for root, dirs, files in os.walk("{0}/projects/{1}/{2}".format(script_dir, project_name, level)):
                #for file in files:
                    #file_level_pair = (level, file)
                    #file_level_pairs.append(file_level_pair)
    #except Exception as e: print(e)
    global selected
    selected = []
    global current_project
    current_project = project_name
    global working_dir
    working_dir = current_project
    project_tree.delete(*project_tree.get_children())
    project_tree.insert("", "0", project_name, text=project_name)
    makeProjectTree("{0}/projects/{1}".format(script_dir, project_name), 0, project_name)

def newProject():
    new_project_window = Toplevel(app)
    new_project_window.lift(app)
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
            moveTools(project_name.get())
            refreshDeleteMenu()
            refreshExportMenu()
            refreshLoadMenu()
            loadProject(project_name.get())
            new_project_window.destroy()
    Button(new_project_window, text="Create Project", command=selectButton).pack(side=TOP)

def deleteProject(project): 
    if messagebox.askquestion("Don't be a Silly Goose!", 'Are you sure you want to delete the project: "{}"?'.format(project)) == "yes":
        shutil.rmtree("{0}\\projects\\{1}".format(script_dir, project))
        refreshDeleteMenu()
        refreshExportMenu()
        refreshLoadMenu()

def importMod():
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
            moveTools(project_name)
        except Exception as e: printGUI(e)
        refreshDeleteMenu()
        refreshExportMenu()
        refreshLoadMenu()
        loadProject(project_name)

def exportMod(project_name):
    os.chdir("{0}/projects/{1}".format(script_dir, project_name))
    os.system("dds_to_xbmp.bat")
    os.system("text_to_export.bat")
    os.system("text_to_subtitle.bat")
    os.chdir(script_dir)
    if os.path.exists("{0}/exported mods/{1}".format(script_dir, project_name)): pass
    else: os.mkdir("{0}/exported mods/{1}".format(script_dir, project_name))
    export_mod_window = Toplevel(app)
    export_mod_window.lift(app)
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
    def browse(): game_dir.delete(0,END); game_dir.insert(0,filedialog.askdirectory(initialdir = "/", title = "Select the Game Directory")); export_mod_window.lift(app)
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
                level = os.path.join("{0}/projects/{1}".format(script_dir, project_name), name)
                if os.path.isdir(level):
                    os.chdir("{0}/projects/{1}".format(script_dir, project_name))
                    os.system("dfs.exe -pack {0} {0}.DFS".format(name))
                    os.chdir(script_dir)
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
                if name.endswith(".000") or name.endswith(".DFS"):
                    shutil.move("{0}\\projects\\{1}\\{2}".format(script_dir, project_name, name), "{0}\\exported mods\\{1}\\{2}".format(script_dir, project_name, name))
            if compress.get() == 1: shutil.make_archive(project_name, 'zip', "{0}\\exported mods\\{1}".format(script_dir, project_name))
        elif export_type.get() == 2:
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
                level = os.path.join("{0}/projects/{1}".format(script_dir, project_name), name)
                if os.path.isdir(level):
                    os.chdir("{0}/projects/{1}".format(script_dir, project_name))
                    os.system("dfs.exe -pack {0} {0}.DFS".format(name))
                    os.chdir(script_dir)
            for name in os.listdir("{0}/projects/{1}".format(script_dir, project_name)):
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

def xbmpToDDS(): os.chdir("{0}/projects/{1}".format(script_dir, current_project)); os.system("xbmp_to_dds.bat"); os.chdir(script_dir); project_tree.delete(*project_tree.get_children()); project_tree.insert("", "0", current_project, text=current_project); makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
def ddsToXBMP(): os.chdir("{0}/projects/{1}".format(script_dir, current_project)); os.system("dds_to_xbmp.bat"); os.chdir(script_dir); project_tree.delete(*project_tree.get_children()); project_tree.insert("", "0", current_project, text=current_project); makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
def ddsToPNG(): pass
def pngToDDS(): pass
def exportToTXT(): os.chdir("{0}/projects/{1}".format(script_dir, current_project)); os.system("export_to_text.bat"); os.chdir(script_dir); project_tree.delete(*project_tree.get_children()); project_tree.insert("", "0", current_project, text=current_project); makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
def exportToJSON(): os.chdir("{0}/projects/{1}".format(script_dir, current_project)); os.system("export_to_json.bat"); os.chdir(script_dir); project_tree.delete(*project_tree.get_children()); project_tree.insert("", "0", current_project, text=current_project); makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
def txtToEXPORT(): os.chdir("{0}/projects/{1}".format(script_dir, current_project)); os.system("text_to_export.bat"); os.chdir(script_dir); project_tree.delete(*project_tree.get_children()); project_tree.insert("", "0", current_project, text=current_project); makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
def jsonToEXPORT(): os.chdir("{0}/projects/{1}".format(script_dir, current_project)); os.system("json_to_export.bat"); os.chdir(script_dir); project_tree.delete(*project_tree.get_children()); project_tree.insert("", "0", current_project, text=current_project); makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
def subtitleToTXT(): os.chdir("{0}/projects/{1}".format(script_dir, current_project)); os.system("subtitle_to_text.bat"); os.chdir(script_dir); project_tree.delete(*project_tree.get_children()); project_tree.insert("", "0", current_project, text=current_project); makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
def txtToSUBTITLE(): os.chdir("{0}/projects/{1}".format(script_dir, current_project)); os.system("text_to_subtitle.bat"); os.chdir(script_dir); project_tree.delete(*project_tree.get_children()); project_tree.insert("", "0", current_project, text=current_project); makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
def addLevel():
    add_level_window = Toplevel(app)
    add_level_window.lift(app)
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
        project_tree.insert("", "0", current_project, text=current_project)
        makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
    Button(add_level_window, text="Add selected level(s)", command=selectButton).pack(side=TOP)

def removeLevel():
    delete_level_window = Toplevel(app)
    delete_level_window.lift(app)
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
        project_tree.insert("", "0", current_project, text=current_project)
        makeProjectTree("{0}/projects/{1}".format(script_dir, current_project), 0, current_project)
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

#Set up window
app = Tk()  
app.title("HMCT v2.0  |  {}".format(splash_text))
app.iconphoto(False, PhotoImage(file="{}/assets/hmct_icon.png".format(script_dir)))
app.geometry("1800x1000")

#Set up console thingy
console_frame = Frame(app, height=20, width=1800, relief=SUNKEN)
console_frame.pack(side=BOTTOM, fill=X, padx=(5,5))
console_frame.pack_propagate(False)
console_text = Entry(console_frame)
console_text.pack(fill=BOTH)
def redirector(inputStr):console_text.insert(INSERT, inputStr)
sys.stdout.write = redirector

def printGUI(output): 
    console_text.delete(0, END)
    print(output)

printGUI("Welcome to HMCT!")

#Set up top bar
top_bar = Frame(app, bd=5, height=75, width=1800)
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
add_level_button = Button(top_bar, text="Add Level", font=("Segoe UI", 11), image=add_level_image, compound=LEFT, command=addLevel, height=75, width=150)
add_level_button.pack(side=LEFT, padx=(5,0))
delete_level_image = ImageTk.PhotoImage(Image.open("{}/assets/delete_level.png".format(script_dir)).convert("RGBA"))
delete_level_button = Button(top_bar, text="Remove Level", font=("Segoe UI", 11), image=delete_level_image, compound=LEFT, command=removeLevel, height=75, width=150)
delete_level_button.pack(side=LEFT, padx=(5,0))

#Set up mod file structure window
file_window = Frame(app, bd=5, width=500, relief=SUNKEN)
file_window.pack(side=LEFT, fill=Y, padx=(5,0), pady=(0,0))
ttk.Label(file_window, text ="Project Files").pack(side=TOP)

#Set up file tree
project_tree = CheckboxTreeview(file_window)
project_tree.pack(side=LEFT, fill=BOTH)  
project_tree.column("#0", minwidth=0, width=400, stretch=NO)
project_tree.bind('<Double-1>', previewFile)

#Set up file preview window
preview_window = Frame(app, bd=5, relief=SUNKEN, height=1000, width=1285)
preview_window.pack(side=TOP, fill=BOTH, padx=(15,5), pady=(0,0))
preview_window.pack_propagate(False)
ttk.Label(preview_window, text ="File Preview").pack(side=TOP, fill=Y)

#Set up menu bar
menu_bar = Menu(app)

project_menu = Menu(menu_bar, tearoff=0)
project_menu.add_command(label="New Project", command=newProject)
load_menu = Menu(project_menu, tearoff=0)
def refreshLoadMenu():
    load_menu.delete(0, "end")
    for name in os.listdir("{0}/projects/".format(script_dir)):
        pack = os.path.join("{0}/projects/".format(script_dir), name)
        if os.path.isdir(pack):
            load_menu.add_command(label=name, command=partial(loadProject, name))
refreshLoadMenu()
project_menu.add_cascade(label="Load Project", menu=load_menu)
delete_menu = Menu(project_menu, tearoff=0)
def refreshDeleteMenu():
    delete_menu.delete(0, "end")
    for name in os.listdir("{0}/projects/".format(script_dir)):
        pack = os.path.join("{0}/projects/".format(script_dir), name)
        if os.path.isdir(pack):
            delete_menu.add_command(label=name, command=partial(deleteProject, name))
refreshDeleteMenu()
project_menu.add_cascade(label="Delete Project", menu=delete_menu)
project_menu.add_separator()
project_menu.add_command(label="Import Mod", command=importMod)
export_menu = Menu(project_menu, tearoff=0)
def refreshExportMenu():
    export_menu.delete(0, "end")
    for name in os.listdir("{0}/projects/".format(script_dir)):
        project = os.path.join("{0}/projects/".format(script_dir), name)
        if os.path.isdir(project):
            export_menu.add_command(label=name, command=partial(exportMod, name))
refreshExportMenu()
project_menu.add_cascade(label="Export Mod", menu=export_menu)
project_menu.add_separator()
def exit(): sys.exit()
project_menu.add_command(label="Exit", command=exit)
menu_bar.add_cascade(label="Project", menu=project_menu)

tools_menu = Menu(menu_bar, tearoff=0)
convert_menu = Menu(tools_menu, tearoff=0)
convert_menu.add_command(label="XBMP to DDS", command=xbmpToDDS)
convert_menu.add_command(label="DDS to XBMP", command=ddsToXBMP)
convert_menu.add_command(label="DDS to PNG", command=doNothing)
convert_menu.add_command(label="PNG to DDS", command=doNothing)
convert_menu.add_separator()
convert_menu.add_command(label="EXPORT to TXT", command=exportToTXT)
convert_menu.add_command(label="EXPORT to JSON", command=exportToJSON)
convert_menu.add_command(label="TXT to EXPORT", command=txtToEXPORT)
convert_menu.add_command(label="JSON to EXPORT", command=jsonToEXPORT)
convert_menu.add_separator()
convert_menu.add_command(label="SUBTITLE to TXT", command=subtitleToTXT)
convert_menu.add_command(label="TXT to SUBTITLE", command=txtToSUBTITLE)
tools_menu.add_cascade(label="Convert", menu=convert_menu)
plugins_menu = Menu(tools_menu, tearoff=0)
tools_menu.add_cascade(label="Plugins", menu=plugins_menu)
menu_bar.add_cascade(label="Tools", menu=tools_menu)

settings_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Settings", menu=settings_menu)

help_menu = Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label="Help", menu=help_menu)

image_canvas = Canvas(preview_window, height=990, width=1285)
image_canvas.pack(side=TOP)
preview_image = Image.open("{}/assets/no_preview.png".format(script_dir)).convert("RGBA")
preview_image = ImageTk.PhotoImage(preview_image.resize(((preview_image.size[0]*int(1157/preview_image.size[0])), (preview_image.size[1]*int(891/preview_image.size[1]))), Image.NEAREST))
preview_image = image_canvas.create_image(0,0, anchor=NW, image=preview_image)

#Load project
app.config(menu=menu_bar)
app.mainloop()
