
import sys
sys.path.append(".")
# from source.CodeGeneration.Functionality.Functionality import Functionality


#NOTE - DEPRECATED

class Variables:
    def __init__(self) -> None:
        pass

    def get_value(self, id, id_dict):
        if id.value in id_dict.keys():
            return id_dict[id.value]
        else:
            raise Exception("Variable not found")




class Sequences:
    pass
