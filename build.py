import os
import subprocess

def find_dockerfiles(root_dir):
    dockerfiles = []
    for root, dirs, files in os.walk(root_dir):
        if "Dockerfile" in files:
            dockerfiles.append(os.path.join(root, "Dockerfile"))
    return dockerfiles

def clean(value):
    value = "".join(char.lower() for char in value if char.isalnum() or char in ["-", "_"])
    return value

to_build = {}
to_delete = []
for dockerfile in find_dockerfiles(os.path.join(".", "Hack@AC_2024")):
    repository, category, name, folder = (clean(value) for value in dockerfile.split(os.sep)[1:5])
    tag = f"dohackme.azurecr.io/{repository}/{category}/{name}:latest"
    if folder == "src":
        if tag in to_build.keys():
            to_delete.append(tag) # Repeat tags probably mean the challenge requires a stack, and should be skipped
        else:
            to_build.update({tag: dockerfile})

for tag in to_delete:
    to_build.pop(tag)
    print(f"{tag} removed")

for tag, location in to_build.items():
    print(f"Building {tag}")
    result = subprocess.run(["docker", "build", "-t", tag, "-f", location, os.path.dirname(location)],
                            capture_output=True, text=True)
    if result.returncode == 0:
        print(f"{tag} built successfully")
    else:
        print(f"{tag} failed")