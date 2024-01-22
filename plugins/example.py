#This is an example extension for HMCT
#Commands in extensions are use just like regular commands
#Make sure your new commands do not have the same name as an existing function

#Your commands will be functions, and should be named simple so they are easier to use.
#Users can also configure shortcut commands for them
#This example command takes any amount of names and says hello to them
#If your command uses arguements, make sure to use args, otherwise leave it blank
#Arguements are referenced with args[index]
def hello(args):
    j = 0
    for i in args:
        print("Hello "+ str(args[j]))
        j += 1

#You should add a .help file so people know how to use your commands
#The file should be formatted like this example:
#hello (name) : says hello to someone with the given name(s)

#Each explanation should take one line and follow the given format:
#Command (arguments) : description

#You should not have any extra stuff in the .help file

#If you want to access functions from hmct.py, add the following code to import it
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import hmct

#This is a command that calls the newPack() function in hmct.py
def newpack():
    hmct.newPack()
#Notice how it doesn't have the EXACT same name as the function in hmct.py