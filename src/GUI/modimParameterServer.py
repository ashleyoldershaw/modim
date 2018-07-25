variables = {}
    
def setparam(name, value):
    try:
        global variables
        variables[name] = value
    except:
        pass
    
def getparam(name):
    try:
        global variables
        return variables[name]
    except:
        return None

