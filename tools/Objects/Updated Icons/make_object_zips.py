import os
import zipfile
import re

script_dir = os.path.dirname(os.path.abspath(__file__))
resource_dir = input("Resource folder path: ")

for root, dirs, files in os.walk(script_dir):
    for file in files:
        if file.endswith(".txt"):
            resource_files = []
            with zipfile.ZipFile("{0}\\{1}.zip".format(root, file.split(".")[0]), mode="w", compression=zipfile.ZIP_DEFLATED) as resource_zip:
                print("Made Zip")
                for fname in os.listdir(resource_dir):
                    if "{0}.RGEOM".format(file.split(".")[0].upper()) == fname:
                        print(fname)
                        resource_files.append(resource_dir + "\\" + "{}.RGEOM".format(file.split(".")[0].upper()))
                        with open(resource_dir + "\\" + fname, encoding="ansi") as rgeom_file: #, mode="rb"
                            rgeom_contents = rgeom_file.read()
                            print(rgeom_contents)
                            print("Opened {0}".format(fname))
                            for other_file in os.listdir(resource_dir):
                                print(other_file)
                                print(rgeom_contents.lower().find(other_file.lower()))
                                if other_file.lower() in rgeom_contents.lower(): #.encode("ansi") re.search(str(other_file), str(rgeom_contents), re.IGNORECASE)
                                    print(other_file)
                                    if other_file not in resource_files: resource_files.append(os.path.join(resource_dir, other_file))
                for a in resource_files:
                    print(a)
                    resource_zip.write(a, a[len(resource_dir) + 1:])
                resource_zip.close()