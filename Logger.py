import enum

class Logger(enum.Enum):
    ALL = 0
    WARNING = 1
    ERROR = 2

# Takes input and a type then adds the Logger type to the beginning
def Log(text, type=Logger.ALL): # Default logs to ALL
    if(type == Logger.ALL):
        print("[ALL] " + str(text))
    elif(type == Logger.WARNING):
        print("[WARNING] " + str(text))
    elif(type == Logger.ERROR):
        print("[ERROR] " + str(text))

#TODO: Determine if the log type is to be printed to the console based on
#      input given at runtime
