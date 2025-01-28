import os
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(script_dir):
    for filename in files:
        if not os.path.exists("{}/rgeom2obj.exe".format(root)):
            shutil.copy2("{0}\\rgeom2obj.exe".format(script_dir), "{0}\\rgeom2obj.exe".format(root))
        if filename.endswith(".RGEOM"):
            print("rgeom2obj.exe \""+filename+"\" \""+filename.split(".")[0]+"\".obj")
            os.chdir(root)
            os.system("cmd /c rgeom2obj.exe \""+filename+"\" \""+filename.split(".")[0]+"\".obj")
            os.chdir(script_dir)
        if filename.endswith(".NPCGEOM"):
            print("rgeom2obj.exe \""+filename+"\" \""+filename.split(".")[0]+"\".obj")
            os.chdir(root)
            os.system("cmd /c rgeom2obj.exe \""+filename+"\" \""+filename.split(".")[0]+"\".obj")
            os.chdir(script_dir)