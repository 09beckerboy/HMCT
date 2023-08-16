#This is an example extension for HTPCT
#Commands from extensions are used like this "+ (extension) (command) (*arguement)"
#Make your extensions have simple names, like "example". It should be all lowercase and not many words

#Your commands will be functions, and should have the same rules for the extension name
#This example command is all lowercase and one word, and should take exactly 1 arguement
def hello(name):
    print("Hello "+name)

#If you want more arguements, you can have them be seperated by ",", and split them
def group(names):
    for name in names.split(","):
        print("Hello "+name)

#You should add a "help" command so people know how to use your commands
#If you don't need any arguements, use "*none"
def help(*none):
    print("Help for example extension\nhelp : displays this message\nhello (name) : says hello (name)\ngroup (names) : says hello to each name listed, which should be seperated by ','")

#If you want to access functions from htpct.py, add the following code to import it
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
import htpct

#This is a command that calls the newPack() function in htpct.py
def newpack(*none):
    htpct.newPack()