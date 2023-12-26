import os
import platform
import subprocess
import os


current_os = platform.system()

subprocess.run(["pip", "install", "-r", "requirements.txt"])

if current_os == "Windows":
    with open("ccload.bat", "w") as file:
        file.write("python main.py %*")
        ccload_path = "C:\\Program Files\\ccload\\ccload.bat"
        if os.path.exists(ccload_path):
            os.remove(ccload_path)
            
        os.symlink(os.getcwd() + "\\ccload.bat", ccload_path)
else:
    with open("ccload", "w") as file:
        file.write("#!/bin/bash\npython main.py \"$@\"\n")
        ccload_path = "/usr/local/bin/ccload"
        if os.path.exists(ccload_path):
            subprocess.Popen('unlink ' + ccload_path, shell=True)
            
        subprocess.Popen('ln -s $(pwd)/ccload /usr/local/bin/', shell=True)