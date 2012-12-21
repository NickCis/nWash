import os

__definition__ = {
    "command": "pwd",
    "do": "pwd"
}

def run(data, extra, args, struct, config, self):
    print(os.getcwd())
