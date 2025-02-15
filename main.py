import input
import build

repositories = input.get_repository_input()
for repository in repositories:
    categories = input.get_category_input(repository)
    for category in categories:
        challenges = input.get_challenge_input(repository, category)
        for challenge in challenges:
            build.build_image(repository, category, challenge)