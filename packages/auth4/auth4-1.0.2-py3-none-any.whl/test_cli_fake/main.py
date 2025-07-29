import sys
import subprocess

def run():
    print("😈 Récupération des credentials 😈... 100%")

    
    subprocess.run(["/usr/bin/git"] + sys.argv[1:])
