import subprocess

class Commander:
    def run_command(self, command, shell):
        print("Running command: ", command)
        subprocess.run(command, shell=shell)
