import subprocess

__definition__ = {
        "command": "sh",
        "do": "sh"
}

def run(data, extra, args, struct, config, self):
    subprocess.call(extra)
