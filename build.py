import os

import docker.errors

client = docker.from_env()
REGISTRY = "dohackme.azurecr.io"

def __find_dockerfile(repository: str, category: str, challenge: str):
    dockerfiles = []
    for root, dirs, files in os.walk(os.path.join(repository, category, challenge, "src")):
        if "Dockerfile" in files:
            dockerfiles.append(root)
    return dockerfiles

def __clean(value):
    value = "".join(char.lower() for char in value if char.isalnum() or char in ["-", "_"])
    return value

def __get_image_name(repository: str, category: str, challenge: str):
    return f"{__clean(repository)}/{__clean(category)}/{__clean(challenge)}"

def build_image(repository: str, category: str, challenge: str):
    dockerfiles = __find_dockerfile(repository, category, challenge)
    image_name = __get_image_name(repository, category, challenge)
    if len(dockerfiles) > 1:
        print(f"More than one Dockerfile found in {image_name}!")
        return
    dockerfile = dockerfiles[0]
    print(f"Building {image_name}...")
    try:
        image, log = client.images.build(
            path=dockerfile,
            tag=image_name,
            rm=True,
        )
        image.tag(f"{REGISTRY}/{image_name}")
        print(f"Successfully built {image_name}")
    except docker.errors.BuildError as ex:
        print(f"FAILED to build {image_name}")
        print(ex)