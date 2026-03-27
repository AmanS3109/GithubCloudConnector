from fastapi import APIRouter, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.services.github_api import github_service
from app.schemas import IssueCreate, PullRequestCreate

router = APIRouter(
    prefix="/github",
    tags=["GitHub Connector"]
)

security = HTTPBearer()

@router.get("/repos/{username}")
async def fetch_repositories(username: str, creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    repos = await github_service.get_user_repos(username, token)
    return {
        "user": username,
        "repository_count": len(repos),
        "repositories": [{"name": repo["name"], "url": repo["html_url"]} for repo in repos]
    }

@router.post("/repos/{username}/{repo_name}/issues", status_code=201)
async def create_new_issue(username: str, repo_name: str, issue_data: IssueCreate, creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    issue = await github_service.create_issue(
        username=username, repo=repo_name, title=issue_data.title, token=token, body=issue_data.body
    )
    return {"message": "Issue created!", "issue_url": issue["html_url"]}

@router.get("/repos/{username}/{repo_name}/issues")
async def list_issues(username: str, repo_name: str, creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    issues = await github_service.get_repo_issues(username, repo_name, token)
    formatted_issues = [{"number": i["number"], "title": i["title"], "state": i["state"], "user": i["user"]["login"], "url": i["html_url"]} for i in issues]
    return {"repository": f"{username}/{repo_name}", "total_issues": len(formatted_issues), "issues": formatted_issues}

@router.post("/repos/{username}/{repo_name}/pulls", status_code=201)
async def create_new_pull_request(username: str, repo_name: str, pr_data: PullRequestCreate, creds: HTTPAuthorizationCredentials = Depends(security)):
    token = creds.credentials
    pr = await github_service.create_pull_request(
        username=username, repo=repo_name, title=pr_data.title, head=pr_data.head, base=pr_data.base, token=token, body=pr_data.body
    )
    return {"message": "Pull request created!", "pr_url": pr["html_url"]}