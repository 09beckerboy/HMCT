import os
from rembg import remove
from PIL import Image
import numpy as np

script_dir = os.path.dirname(os.path.abspath(__file__))

for root, dirs, files in os.walk(script_dir):
    for file in files:
        if file.endswith(".txt"):
            try:
                input_path = "{0}/{1}.png".format(root, file.split(".")[0])
                print(input_path)
                output_path = "{0}/{1}.ico".format(root, file.split(".")[0])
                print(output_path)
                input = Image.open(input_path)
                output = remove(input)
                print("Removed background")
                output.getbbox()
                im2 = output.crop(output.getbbox())
                print("Cropped")
                sqrWidth = np.ceil(np.sqrt(im2.size[0]*im2.size[1])).astype(int)
                im_resize = im2.resize((sqrWidth, sqrWidth))
                print("Squarified")
                im_resize.save(output_path, format='ICO', sizes=[(256, 256), (128, 128)])
                print("Saved")
            except Exception as e: print(e)