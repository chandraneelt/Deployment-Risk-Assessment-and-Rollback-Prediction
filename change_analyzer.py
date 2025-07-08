from fastapi import APIRouter, Body, HTTPException
from pydantic import BaseModel, Field
from typing import List, Optional
import git
import os

router = APIRouter()

RISKY_KEYWORDS = ["config", "migration", "schema", "dockerfile", "requirements", "env"]

class ChangeAnalysisRequest(BaseModel):
    repo_path: str = Field(..., description="Path to the local git repository")
    base_commit: str = Field(..., description="Base commit hash")
    new_commit: str = Field(..., description="New commit hash")

class ChangeAnalysisResponse(BaseModel):
    files_changed: List[str]
    risky_changes: List[str]
    summary: str
    error: Optional[str] = None

@router.post("/analyze", response_model=ChangeAnalysisResponse, summary="Analyze code/config changes between two commits.")
def analyze_changes(
    req: ChangeAnalysisRequest
) -> ChangeAnalysisResponse:
    try:
        repo = git.Repo(req.repo_path)
        diff_index = repo.commit(req.base_commit).diff(req.new_commit)
        files_changed = [item.a_path for item in diff_index] + [item.b_path for item in diff_index]
        files_changed = list(set([f for f in files_changed if f]))
        risky_changes = [f for f in files_changed if any(kw in f.lower() for kw in RISKY_KEYWORDS)]
        summary = f"{len(files_changed)} files changed, {len(risky_changes)} risky changes"
        return ChangeAnalysisResponse(
            files_changed=files_changed,
            risky_changes=risky_changes,
            summary=summary
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Change analysis failed: {str(e)}") 