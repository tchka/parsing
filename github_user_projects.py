import requests


def get_projects(repos):
    repos_names = []
    for repo in repos:
        repos_names.append(repo['name'])
    return repos_names


# username = "DJWOMS"
username = input("Enter username: ")

response = requests.get(f'https://api.github.com/users/{username}/repos')
r = response.json()
if not r:
    print('No repos found')
else:

    with open(f"github_user_{username}_repos.json", "w",
              encoding="utf-8") as f:
        f.write(response.text)

    user_repos = response.json()
    repos_names_list = get_projects(user_repos)
    print(repos_names_list)
    print(len(repos_names_list))
