from fastapi import APIRouter, HTTPException
from app.services.services import clone_repository
from app.services.services import scan_repository
from app.services.services import chunk_repository

router = APIRouter(prefix="/api", tags=["routes"])

@router.get("/health")
async def health_check():
    return {"status": "ok"}


@router.get("/clone-repo")
async def clone_repo(name: str, repo_url: str):
    try:
        print(f"Cloning repository from {repo_url} into {name}...")

        # clone_path = clone_repository(repo_url, name)
        clone_path = './repos/stock_market_analysis'
        print(f"Repository cloned successfully into {clone_path}.")
        scan_results = scan_repository(clone_path)
        chunk = chunk_repository(scan_results)
        return {
            "success": True,
            "message": "Repository cloned successfully.",
            "repository_name": name,
            "repository_url": repo_url,
            "clone_path": clone_path,
            # "scan_results": scan_results
        }

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=str(e)
        )