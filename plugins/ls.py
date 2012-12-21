#! /usr/bin/python3
import os

#Definition may be autoloaded if it is defined in the plugin, or it could de in
#the configuration file.
__definition__ = {
    #Command to execute in the shell
    "command": "ls",
    #Name registered. This is a plugin, the name registered is the name of the
    #file without the .py extension. The function executed is the run function
    "do": "ls"
}

def run(data, extra, args, struct, config, self):
    '''
    Passed Arguments:
        * data -> Data dictionary
        * args -> Extra arguments
        * argscpy -> Parsed commandline
        * struct -> dict with extended asked and obtained information
        * self.config -> nWash configuration
        * self -> nWash instance
    '''
    files = os.listdir(os.getcwd())
    for x in files:
        print(x)

