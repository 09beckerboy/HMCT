import os
from pydub import AudioSegment

script_dir = os.path.dirname(os.path.abspath(__file__))

#From boredom's script
def convert_to_aiff(audio_input_file, audio_output_file):
    audio = AudioSegment.from_file(audio_input_file)
    audio.export(audio_output_file, format="aiff")
    os.remove(audio_input_file)

for file in os.listdir(script_dir):
    folder = os.path.join(script_dir, file)
    if os.path.isdir(folder):
        with open(folder + ".audioscript", "w") as output_file:
            print("\n{}.audioscript:".format(folder))
            output_file.write("package:\n{} [volume=1.00 priority=255]\n\nfiles:\n".format(file))
            print("package:\n{} [volume=1.00 priority=255]\n\nfiles:".format(file))
            filename_list = []
            for filename in os.listdir(folder):
                if filename.endswith(".wav") or filename.endswith(".mp3"):
                    audio_input_file = os.path.join(folder, filename)
                    audio_output_file = os.path.splitext(audio_input_file)[0] + ".aiff"
                    convert_to_aiff(audio_input_file, audio_output_file)
                    output_file.write("{0}A    hot LipSync   {1}/{2}.aiff\n".format(filename.split(".")[0].lower(), file, filename.split(".")[0]))
                    print("{0}A    hot LipSync   {1}/{2}.aiff".format(filename.split(".")[0].lower(), file, filename.split(".")[0]))
                    filename_list.append(filename.split(".")[0])
                if filename.endswith(".aiff"):
                    output_file.write("{0}A    hot LipSync   {1}/{2}.aiff\n".format(filename.split(".")[0].lower(), file, filename.split(".")[0]))
                    print("{0}A    hot LipSync   {1}/{2}.aiff".format(filename.split(".")[0].lower(), file, filename.split(".")[0]))
                    filename_list.append(filename.split(".")[0])
            output_file.write("\n\n\ndescriptors:\n")
            print("\n\n\ndescriptors:\n")
            for filename in filename_list:
                output_file.write("{} rlist\n".format(filename) + "{" + "\n    {}A\n".format(filename.lower()) + "}" + "\n\n")
                print("{} rlist\n".format(filename) + "{" + "\n    {}A\n".format(filename.lower()) + "}" + "\n")
