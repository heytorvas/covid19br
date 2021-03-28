import subprocess

subprocess.run("python3 scraping.py & python3 api/app.py", shell=True)