import os
from PIL import Image, ImageEnhance
import shutil

script_dir = os.path.dirname(os.path.abspath(__file__))

def prep():
    try:
        for root, dirs, files in os.walk("{0}".format(script_dir)):
            for filename in files:
                if filename.endswith(".png"):
                    file_path = os.path.join(root, filename)
                    #file_path = os.path.join("{0}".format(script_dir), filename)
                    result_name = filename.split(".")[0]
                    result_name = result_name + ".dds"
                    result_path = os.path.join(root, result_name)
                    im = Image.open(file_path).convert('RGBA')
                    print("Opened {0}".format(result_name))
                    print("Converted {0} to RGBA".format(result_name))
                    #im.putalpha(255) #comment out if you don't want them at max transparency
                    #alpha = im.split()[3]
                    #alpha = ImageEnhance.Brightness(alpha).enhance(1)
                    #im.putalpha(alpha)
                    #print("Transparency for {0} maxed".format(result_name))
                    #im = im.transpose(Image.FLIP_TOP_BOTTOM)
                    #print("{0} flipped".format(result_name))
                    im.save(result_path)
                    print("Saved {0}".format(result_name))
                    os.remove(file_path)
                else: continue
    except Exception as e: print(e)

prep()