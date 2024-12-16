import os
import httpx
import base64
import json

# Fetch all repositories
async def fetch_github_repos():
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME")
    headers = {"Authorization": f"token {token}"}

    async with httpx.AsyncClient() as client:
        response = await client.get(f"https://api.github.com/users/{username}/repos", headers=headers)
        response.raise_for_status()
        repos = response.json()

    print(f"Fetched {len(repos)} repositories from GitHub.")

    # Fetch README for each repository
    repos_with_readme = []
    for repo in repos:
        readme_content = await fetch_repo_readme(repo["name"])
        repos_with_readme.append({
            "name": repo["name"],
            "url": repo["html_url"],
            "description": repo.get("description", "No description provided."),
            "readme": readme_content
        })

    print(f"Processed {len(repos_with_readme)} repositories with README.")
    return repos_with_readme


# Fetch the README of a specific repository
async def fetch_repo_readme(repo_name):
    token = os.getenv("GITHUB_TOKEN")
    username = os.getenv("GITHUB_USERNAME")
    headers = {"Authorization": f"token {token}"}

    url = f"https://api.github.com/repos/{username}/{repo_name}/readme"
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        if response.status_code == 200:
            try:
                readme_data = response.json()
                content = base64.b64decode(readme_data["content"]).decode("utf-8")
                return content
            except Exception:
                return "Error decoding README content."
        elif response.status_code == 404:
            return "No README available."
        return "Error fetching README."


# Save repository data to a local JSON file
async def save_repos_to_file(file_path="github_repos.json"):
    repos = await fetch_github_repos()
    with open(file_path, "w") as file:
        json.dump(repos, file, indent=4)
    print(f"Saved {len(repos)} repositories to {file_path}.")


# Load repository data from a local JSON file
def load_repos_from_file(file_path="github_repos.json"):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"{file_path} does not exist.")
    with open(file_path, "r") as file:
        repos = json.load(file)
    print(f"Loaded {len(repos)} repositories from {file_path}.")
    return repos
