import docker
import os

def find_dockerfiles():
    dockerfiles = []
    for root, dirs, files in os.walk('.'):
        if 'Dockerfile' in files:
            dockerfiles.append(os.path.join(root, 'Dockerfile'))
    return dockerfiles

def clean(value):
    value = ''.join(char.lower() for char in value if char.isalnum() or char in ['-', '_'])
    return value

client = docker.from_env()
    

dockerfiles = find_dockerfiles()
for dockerfile in dockerfiles:
    repository, category, name = (clean(value) for value in dockerfile.split(os.sep)[1:4])
    print(dockerfile)
    print(f'registry.dohack.me/{repository}/{category}/{name}:latest')
    print('-----------------------')
