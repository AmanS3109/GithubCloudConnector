import httpx
from fastapi import HTTPException

class GitHubService:
    def __init__(self):
        self.base_url = "https://api.github.com"

    # We dynamically generate the headers based on the token the user provides
    def _get_headers(self, token: str):
        return {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28"
        }

    async def get_user_repos(self, username: str, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/users/{username}/repos",
                headers=self._get_headers(token)
            )
            if response.status_code == 404: raise HTTPException(status_code=404, detail=f"GitHub user '{username}' not found.")
            elif response.status_code == 401: raise HTTPException(status_code=401, detail="Unauthorized: Invalid token.")
            elif response.status_code != 200: raise HTTPException(status_code=response.status_code, detail="Failed to fetch data.")
            return response.json()

    async def create_issue(self, username: str, repo: str, title: str, token: str, body: str | None = None):
        payload = {"title": title}
        if body: payload["body"] = body

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/repos/{username}/{repo}/issues",
                headers=self._get_headers(token),
                json=payload
            )
            if response.status_code == 404: raise HTTPException(status_code=404, detail="Repository not found.")
            elif response.status_code in (401, 403): raise HTTPException(status_code=403, detail="Permission denied.")
            elif response.status_code != 201: raise HTTPException(status_code=response.status_code, detail="Failed to create issue.")
            return response.json()

    async def get_repo_issues(self, username: str, repo: str, token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/repos/{username}/{repo}/issues",
                headers=self._get_headers(token)
            )
            if response.status_code == 404: raise HTTPException(status_code=404, detail="Repository not found.")
            elif response.status_code != 200: raise HTTPException(status_code=response.status_code, detail="Failed to fetch issues.")
            return response.json()

    async def create_pull_request(self, username: str, repo: str, title: str, head: str, base: str, token: str, body: str | None = None):
        payload = {"title": title, "head": head, "base": base}
        if body: payload["body"] = body

        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/repos/{username}/{repo}/pulls",
                headers=self._get_headers(token),
                json=payload
            )
            if response.status_code == 404: raise HTTPException(status_code=404, detail="Repository not found.")
            elif response.status_code == 422: raise HTTPException(status_code=422, detail="Validation failed. Check branches.")
            elif response.status_code not in (201, 200): raise HTTPException(status_code=response.status_code, detail="Failed to create PR.")
            return response.json()

github_service = GitHubService()