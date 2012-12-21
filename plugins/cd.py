import os
__definition__ = {
    #Command to execute in the shell
    "command": "cd",
    #Name of registered function
    "do": "cd",
    #Data passed to the command in the shell
    "data": [
        {
            "name": "path",
            #Type of argument (it is used in the autocomplete)
            "type": "path",
            "show": "path"
        }
    ]
}
def run(data, extra, args, struct, config, self):
    os.chdir(data['path'])

