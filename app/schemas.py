from pydantic import BaseModel, Field

class IssueCreate(BaseModel):
    title: str = Field(..., description="The title of the GitHub issue")
    body: str | None = Field(default=None, description="The detailed description of the issue")

class PullRequestCreate(BaseModel):
    title: str = Field(..., description="The title of the pull request")
    head: str = Field(..., description="The branch containing your changes (e.g., 'feature-branch')")
    base: str = Field(..., description="The branch you want to merge into (e.g., 'main' or 'master')")
    body: str | None = Field(default=None, description="The detailed description of the pull request")