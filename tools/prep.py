import os
from PIL import Image, ImageEnhance

script_dir = os.path.dirname(os.path.abspath(__file__))

def prep():
    try:
        #os.chdir("{0}/level_files".format(script_dir))
        directory = os.getcwd()
        # for root, dirs, files in os.walk(script_dir):
        #     for file in files:
        #         os.chdir(root)
        #         if file.endswith(".RGEOM"): os.system(f'cmd /c "rgeom2obj.exe {file} {file.split(".")[0]}.obj"')
        #         os.chdir(script_dir)
        # for root, dirs, files in os.walk(directory):
        #     for filename in files:
        #         if filename.endswith(".mtl"):
        #             os.chdir(root)
        #             with open(filename, 'r', encoding="ansi") as file :
        #                 filedata = file.read()
        #                 print("Read "+filename)
        #             filedata = filedata.replace('.xbmp', '.png')
        #             print("Replaced text in "+filename)
        #             with open(filename, 'w', encoding="ansi") as file:
        #                 file.write(filedata)
        #                 print("Wrote "+filename)
        #             os.chdir(script_dir)
        #             continue
        #         else:
        #             continue
        #os.chdir(script_dir)
        #os.system("convert_xbmp_to_dds.bat")
        for root, dirs, files in os.walk(script_dir):
            for filename in files:
                if filename.endswith(".dds"):
                    file_path = os.path.join(root, filename)
                    result_name = filename.split(".")[0]
                    im = Image.open(file_path).convert('RGBA')
                    print("Opened {0}".format(result_name))
                    print("Converted {0} to RGBA".format(result_name))
                    #im.putalpha(255) #comment out if you don't want them at max transparency
                    # im.show()
                    # input("")
                    alpha = im.split()[3]
                    alpha = ImageEnhance.Brightness(alpha).enhance(1)
                    im.putalpha(alpha)
                    print("Transparency for {0} maxed".format(result_name))
                    im = im.transpose(Image.FLIP_TOP_BOTTOM)
                    print("{0} flipped".format(result_name))
                    im.save("{0}/{1}.png".format(root, result_name))
                    print("Saved {0}".format(result_name))
                    os.remove(file_path)
                else:
                    continue
    except Exception as e: print(e)

prep()