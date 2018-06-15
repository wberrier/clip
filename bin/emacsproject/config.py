
import os
import os.path
import json

def removeComments(text):
    ret = ""
    count = 0
    for line in text.split("\n"):
        if not line.lstrip().startswith("//"):
            ret += line + "\n"
            #print str(count) + ":" + line
            count += 1
    return ret

def loadJsonFile(filename):
    # Read config file
    json_text = open(filename).read()
    return json.loads(removeComments(json_text))

def getConfigDir():
    """Get the directory that has the config file"""

    curdir = os.getcwd()
    while curdir != "/":

        test_file = curdir + "/.emacs_project.json"
        if os.path.exists(test_file):
            return curdir

        curdir = os.path.dirname(curdir)

    # Didn't find the config dir...
    return ""
